# ASP.NET Core Real-World Examples

Production-ready examples for common ASP.NET Core scenarios.

## Example 1: E-Commerce Product API

Complete REST API for product management with categories, inventory, and search.

### Project Structure

```
ECommerce.Api/
├── Controllers/
│   ├── ProductsController.cs
│   └── CategoriesController.cs
├── Services/
│   ├── ProductService.cs
│   └── SearchService.cs
├── Repositories/
│   ├── ProductRepository.cs
│   └── CategoryRepository.cs
├── Entities/
│   ├── Product.cs
│   ├── Category.cs
│   └── Inventory.cs
└── DTOs/
    ├── ProductDto.cs
    └── SearchRequest.cs
```

### Product Entity with Relationships

```csharp
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string Sku { get; set; } = string.Empty;
    public int CategoryId { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }

    // Navigation properties
    public Category Category { get; set; } = null!;
    public Inventory Inventory { get; set; } = null!;
    public ICollection<ProductImage> Images { get; set; } = new List<ProductImage>();
    public ICollection<ProductReview> Reviews { get; set; } = new List<ProductReview>();
}

public class Category
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public int? ParentId { get; set; }

    public Category? Parent { get; set; }
    public ICollection<Category> Children { get; set; } = new List<Category>();
    public ICollection<Product> Products { get; set; } = new List<Product>();
}

public class Inventory
{
    public int Id { get; set; }
    public int ProductId { get; set; }
    public int QuantityInStock { get; set; }
    public int ReservedQuantity { get; set; }
    public int ReorderLevel { get; set; }
    public DateTime LastRestocked { get; set; }

    public Product Product { get; set; } = null!;
}
```

### EF Core Configuration

```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("products");

        builder.HasKey(p => p.Id);

        builder.Property(p => p.Name)
            .IsRequired()
            .HasMaxLength(200);

        builder.Property(p => p.Description)
            .HasMaxLength(2000);

        builder.Property(p => p.Price)
            .HasPrecision(18, 2);

        builder.Property(p => p.Sku)
            .IsRequired()
            .HasMaxLength(50);

        builder.HasIndex(p => p.Sku)
            .IsUnique();

        builder.HasIndex(p => p.CategoryId);
        builder.HasIndex(p => p.IsActive);

        // Relationships
        builder.HasOne(p => p.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(p => p.CategoryId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasOne(p => p.Inventory)
            .WithOne(i => i.Product)
            .HasForeignKey<Inventory>(i => i.ProductId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasMany(p => p.Images)
            .WithOne(i => i.Product)
            .HasForeignKey(i => i.ProductId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasMany(p => p.Reviews)
            .WithOne(r => r.Product)
            .HasForeignKey(r => r.ProductId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
```

### Product Service with Search

```csharp
public class ProductService : IProductService
{
    private readonly IProductRepository _repository;
    private readonly IMapper _mapper;
    private readonly IMemoryCache _cache;
    private readonly ILogger<ProductService> _logger;

    public ProductService(
        IProductRepository repository,
        IMapper mapper,
        IMemoryCache cache,
        ILogger<ProductService> logger)
    {
        _repository = repository;
        _mapper = mapper;
        _cache = cache;
        _logger = logger;
    }

    public async Task<PagedResult<ProductDto>> SearchAsync(SearchRequest request)
    {
        var products = await _repository.SearchAsync(
            query: request.Query,
            categoryId: request.CategoryId,
            minPrice: request.MinPrice,
            maxPrice: request.MaxPrice,
            page: request.Page,
            pageSize: request.PageSize
        );

        return _mapper.Map<PagedResult<ProductDto>>(products);
    }

    public async Task<ProductDto?> GetBySkuAsync(string sku)
    {
        var cacheKey = $"product_sku_{sku}";

        if (_cache.TryGetValue(cacheKey, out ProductDto? cachedProduct))
        {
            _logger.LogInformation("Product {Sku} retrieved from cache", sku);
            return cachedProduct;
        }

        var product = await _repository.GetBySkuAsync(sku);
        if (product == null)
            return null;

        var productDto = _mapper.Map<ProductDto>(product);

        _cache.Set(cacheKey, productDto, TimeSpan.FromMinutes(10));
        _logger.LogInformation("Product {Sku} cached", sku);

        return productDto;
    }

    public async Task<bool> UpdateInventoryAsync(int productId, int quantity)
    {
        var product = await _repository.GetByIdAsync(productId);
        if (product == null)
            return false;

        product.Inventory.QuantityInStock += quantity;
        product.Inventory.LastRestocked = DateTime.UtcNow;

        await _repository.SaveChangesAsync();

        _logger.LogInformation(
            "Inventory updated for product {ProductId}: {Quantity} units added",
            productId,
            quantity);

        return true;
    }
}
```

### Products Controller with Advanced Filtering

```csharp
[ApiController]
[Route("api/v1/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _service;

    public ProductsController(IProductService service) => _service = service;

    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<ProductDto>), 200)]
    public async Task<ActionResult<PagedResult<ProductDto>>> Search([FromQuery] SearchRequest request)
    {
        var result = await _service.SearchAsync(request);
        return Ok(result);
    }

    [HttpGet("sku/{sku}")]
    [ResponseCache(Duration = 60, VaryByQueryKeys = new[] { "sku" })]
    [ProducesResponseType(typeof(ProductDto), 200)]
    [ProducesResponseType(404)]
    public async Task<ActionResult<ProductDto>> GetBySku(string sku)
    {
        var product = await _service.GetBySkuAsync(sku);
        return product == null ? NotFound() : Ok(product);
    }

    [HttpPost("{id}/inventory")]
    [Authorize(Roles = "Admin,Warehouse")]
    [ProducesResponseType(200)]
    [ProducesResponseType(404)]
    public async Task<IActionResult> UpdateInventory(int id, [FromBody] UpdateInventoryDto dto)
    {
        var success = await _service.UpdateInventoryAsync(id, dto.Quantity);
        return success ? Ok() : NotFound();
    }

    [HttpGet("categories/{categoryId}")]
    [ProducesResponseType(typeof(List<ProductDto>), 200)]
    public async Task<ActionResult<List<ProductDto>>> GetByCategory(
        int categoryId,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        var request = new SearchRequest { CategoryId = categoryId, Page = page, PageSize = pageSize };
        var result = await _service.SearchAsync(request);
        return Ok(result);
    }
}
```

## Example 2: SaaS Multi-Tenant Application

Multi-tenant architecture with tenant isolation and JWT authentication.

### Tenant Entity

```csharp
public class Tenant
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Subdomain { get; set; } = string.Empty;
    public string ConnectionString { get; set; } = string.Empty;
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; }
    public PlanType Plan { get; set; }

    public ICollection<User> Users { get; set; } = new List<User>();
}

public enum PlanType
{
    Free,
    Starter,
    Professional,
    Enterprise
}
```

### Tenant Resolution Middleware

```csharp
public class TenantResolutionMiddleware
{
    private readonly RequestDelegate _next;

    public TenantResolutionMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context, ITenantService tenantService)
    {
        var host = context.Request.Host.Host;
        var subdomain = host.Split('.')[0];

        var tenant = await tenantService.GetBySubdomainAsync(subdomain);
        if (tenant == null)
        {
            context.Response.StatusCode = 404;
            await context.Response.WriteAsync("Tenant not found");
            return;
        }

        context.Items["TenantId"] = tenant.Id;
        context.Items["Tenant"] = tenant;

        await _next(context);
    }
}
```

### Tenant-Scoped DbContext

```csharp
public class TenantDbContext : DbContext
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public TenantDbContext(
        DbContextOptions<TenantDbContext> options,
        IHttpContextAccessor httpContextAccessor)
        : base(options)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public int TenantId => (int)_httpContextAccessor.HttpContext?.Items["TenantId"]!;

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Global query filter for tenant isolation
        modelBuilder.Entity<User>()
            .HasQueryFilter(u => u.TenantId == TenantId);

        modelBuilder.Entity<Order>()
            .HasQueryFilter(o => o.TenantId == TenantId);
    }

    public override int SaveChanges()
    {
        ApplyTenantId();
        return base.SaveChanges();
    }

    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        ApplyTenantId();
        return base.SaveChangesAsync(cancellationToken);
    }

    private void ApplyTenantId()
    {
        var entries = ChangeTracker.Entries()
            .Where(e => e.State == EntityState.Added && e.Entity is ITenantEntity);

        foreach (var entry in entries)
        {
            ((ITenantEntity)entry.Entity).TenantId = TenantId;
        }
    }
}
```

### JWT Authentication Service

```csharp
public class AuthService : IAuthService
{
    private readonly IUserRepository _userRepository;
    private readonly IConfiguration _configuration;
    private readonly IPasswordHasher<User> _passwordHasher;

    public async Task<AuthResult> LoginAsync(LoginDto dto)
    {
        var user = await _userRepository.GetByEmailAsync(dto.Email);
        if (user == null)
            return AuthResult.Failed("Invalid credentials");

        var result = _passwordHasher.VerifyHashedPassword(user, user.PasswordHash, dto.Password);
        if (result == PasswordVerificationResult.Failed)
            return AuthResult.Failed("Invalid credentials");

        var token = GenerateJwtToken(user);
        var refreshToken = GenerateRefreshToken();

        user.RefreshToken = refreshToken;
        user.RefreshTokenExpiry = DateTime.UtcNow.AddDays(7);
        await _userRepository.SaveChangesAsync();

        return AuthResult.Success(token, refreshToken);
    }

    private string GenerateJwtToken(User user)
    {
        var securityKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_configuration["Jwt:Secret"]!));

        var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Email, user.Email),
            new Claim("tenant_id", user.TenantId.ToString()),
            new Claim(ClaimTypes.Role, user.Role)
        };

        var token = new JwtSecurityToken(
            issuer: _configuration["Jwt:Issuer"],
            audience: _configuration["Jwt:Audience"],
            claims: claims,
            expires: DateTime.UtcNow.AddHours(1),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    private string GenerateRefreshToken()
    {
        var randomBytes = new byte[64];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomBytes);
        return Convert.ToBase64String(randomBytes);
    }
}
```

## Example 3: Background Job Processing

Background service for processing orders with retry logic and dead-letter queue.

### Background Service

```csharp
public class OrderProcessingService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<OrderProcessingService> _logger;
    private readonly Channel<OrderMessage> _channel;

    public OrderProcessingService(
        IServiceProvider serviceProvider,
        ILogger<OrderProcessingService> logger,
        Channel<OrderMessage> channel)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
        _channel = channel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Order processing service started");

        await foreach (var message in _channel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                await ProcessOrderAsync(message, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing order {OrderId}", message.OrderId);
                await HandleFailedOrderAsync(message);
            }
        }
    }

    private async Task ProcessOrderAsync(OrderMessage message, CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();
        var emailService = scope.ServiceProvider.GetRequiredService<IEmailService>();

        _logger.LogInformation("Processing order {OrderId}", message.OrderId);

        var order = await orderService.GetByIdAsync(message.OrderId);
        if (order == null)
        {
            _logger.LogWarning("Order {OrderId} not found", message.OrderId);
            return;
        }

        // Process payment
        await orderService.ProcessPaymentAsync(order.Id, ct);

        // Update inventory
        await orderService.UpdateInventoryAsync(order.Id, ct);

        // Send confirmation email
        await emailService.SendOrderConfirmationAsync(order, ct);

        _logger.LogInformation("Order {OrderId} processed successfully", message.OrderId);
    }

    private async Task HandleFailedOrderAsync(OrderMessage message)
    {
        message.RetryCount++;

        if (message.RetryCount < 3)
        {
            // Retry with exponential backoff
            await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, message.RetryCount)));
            await _channel.Writer.WriteAsync(message);
        }
        else
        {
            // Move to dead-letter queue
            _logger.LogError("Order {OrderId} moved to dead-letter queue after {RetryCount} attempts",
                message.OrderId, message.RetryCount);

            // TODO: Write to dead-letter queue
        }
    }
}

public record OrderMessage(int OrderId, int RetryCount = 0);
```

### Queue Service

```csharp
public interface IOrderQueue
{
    ValueTask EnqueueAsync(int orderId);
}

public class OrderQueue : IOrderQueue
{
    private readonly Channel<OrderMessage> _channel;

    public OrderQueue(Channel<OrderMessage> channel) => _channel = channel;

    public async ValueTask EnqueueAsync(int orderId)
    {
        await _channel.Writer.WriteAsync(new OrderMessage(orderId));
    }
}

// In Program.cs
builder.Services.AddSingleton(Channel.CreateUnbounded<OrderMessage>());
builder.Services.AddSingleton<IOrderQueue, OrderQueue>();
builder.Services.AddHostedService<OrderProcessingService>();
```

## Example 4: Real-Time Notifications with SignalR

WebSocket-based real-time notifications for order updates.

### SignalR Hub

```csharp
[Authorize]
public class NotificationHub : Hub
{
    private readonly INotificationService _notificationService;

    public NotificationHub(INotificationService notificationService)
    {
        _notificationService = notificationService;
    }

    public override async Task OnConnectedAsync()
    {
        var userId = Context.User?.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        if (userId != null)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, $"user_{userId}");
            await Clients.Caller.SendAsync("Connected", "Successfully connected to notifications");
        }
        await base.OnConnectedAsync();
    }

    public async Task SubscribeToOrder(int orderId)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, $"order_{orderId}");
        await Clients.Caller.SendAsync("Subscribed", $"Subscribed to order {orderId}");
    }

    public async Task UnsubscribeFromOrder(int orderId)
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, $"order_{orderId}");
    }
}
```

### Notification Service

```csharp
public class NotificationService : INotificationService
{
    private readonly IHubContext<NotificationHub> _hubContext;

    public NotificationService(IHubContext<NotificationHub> hubContext)
    {
        _hubContext = hubContext;
    }

    public async Task NotifyOrderStatusChangedAsync(int orderId, string status, int userId)
    {
        var notification = new
        {
            OrderId = orderId,
            Status = status,
            Timestamp = DateTime.UtcNow
        };

        // Notify order subscribers
        await _hubContext.Clients
            .Group($"order_{orderId}")
            .SendAsync("OrderStatusChanged", notification);

        // Notify user
        await _hubContext.Clients
            .Group($"user_{userId}")
            .SendAsync("Notification", notification);
    }
}

// In Program.cs
builder.Services.AddSignalR();
app.MapHub<NotificationHub>("/hubs/notifications");
```

## Example 5: File Upload with Validation

Secure file upload with validation, virus scanning, and cloud storage.

### File Upload Service

```csharp
public class FileUploadService : IFileUploadService
{
    private readonly IConfiguration _configuration;
    private readonly ILogger<FileUploadService> _logger;
    private const long MaxFileSize = 10 * 1024 * 1024; // 10MB
    private static readonly string[] AllowedExtensions = { ".jpg", ".jpeg", ".png", ".pdf" };

    public async Task<UploadResult> UploadAsync(IFormFile file, string folder)
    {
        // Validate file
        var validationResult = ValidateFile(file);
        if (!validationResult.IsValid)
            return UploadResult.Failed(validationResult.Error!);

        // Generate unique filename
        var fileExtension = Path.GetExtension(file.FileName);
        var fileName = $"{Guid.NewGuid()}{fileExtension}";
        var filePath = Path.Combine(folder, fileName);

        // Save to disk
        using (var stream = new FileStream(filePath, FileMode.Create))
        {
            await file.CopyToAsync(stream);
        }

        // Scan for viruses (integrate with ClamAV or similar)
        var isSafe = await ScanFileAsync(filePath);
        if (!isSafe)
        {
            File.Delete(filePath);
            return UploadResult.Failed("File failed security scan");
        }

        _logger.LogInformation("File uploaded successfully: {FileName}", fileName);

        return UploadResult.Success(fileName, filePath, file.Length);
    }

    private (bool IsValid, string? Error) ValidateFile(IFormFile file)
    {
        if (file == null || file.Length == 0)
            return (false, "File is required");

        if (file.Length > MaxFileSize)
            return (false, $"File size exceeds maximum allowed size of {MaxFileSize / 1024 / 1024}MB");

        var extension = Path.GetExtension(file.FileName).ToLowerInvariant();
        if (!AllowedExtensions.Contains(extension))
            return (false, $"File type {extension} is not allowed");

        return (true, null);
    }

    private async Task<bool> ScanFileAsync(string filePath)
    {
        // Integrate with virus scanning service
        // For demo purposes, always return true
        await Task.CompletedTask;
        return true;
    }
}
```

### Upload Controller

```csharp
[ApiController]
[Route("api/v1/[controller]")]
public class FilesController : ControllerBase
{
    private readonly IFileUploadService _uploadService;

    public FilesController(IFileUploadService uploadService)
    {
        _uploadService = uploadService;
    }

    [HttpPost("upload")]
    [RequestSizeLimit(10 * 1024 * 1024)] // 10MB
    [ProducesResponseType(typeof(UploadResult), 200)]
    [ProducesResponseType(400)]
    public async Task<ActionResult<UploadResult>> Upload(IFormFile file)
    {
        var result = await _uploadService.UploadAsync(file, "uploads");

        if (!result.IsSuccess)
            return BadRequest(new { error = result.Error });

        return Ok(result);
    }

    [HttpPost("upload-multiple")]
    [RequestSizeLimit(50 * 1024 * 1024)] // 50MB total
    public async Task<ActionResult<List<UploadResult>>> UploadMultiple(List<IFormFile> files)
    {
        if (files.Count > 10)
            return BadRequest("Maximum 10 files allowed");

        var results = new List<UploadResult>();

        foreach (var file in files)
        {
            var result = await _uploadService.UploadAsync(file, "uploads");
            results.Add(result);
        }

        return Ok(results);
    }
}
```

## Example 6: API Rate Limiting

Implement rate limiting with different tiers.

### Rate Limiting Middleware

```csharp
public class RateLimitingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly IMemoryCache _cache;

    public RateLimitingMiddleware(RequestDelegate next, IMemoryCache cache)
    {
        _next = next;
        _cache = cache;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var endpoint = context.GetEndpoint();
        var rateLimitAttribute = endpoint?.Metadata.GetMetadata<RateLimitAttribute>();

        if (rateLimitAttribute != null)
        {
            var clientId = GetClientId(context);
            var key = $"rate_limit_{clientId}_{endpoint?.DisplayName}";

            var requestCount = _cache.GetOrCreate(key, entry =>
            {
                entry.AbsoluteExpirationRelativeToNow = rateLimitAttribute.Window;
                return 0;
            });

            if (requestCount >= rateLimitAttribute.Limit)
            {
                context.Response.StatusCode = 429; // Too Many Requests
                context.Response.Headers["Retry-After"] = rateLimitAttribute.Window.TotalSeconds.ToString();
                await context.Response.WriteAsync("Rate limit exceeded");
                return;
            }

            _cache.Set(key, requestCount + 1, rateLimitAttribute.Window);
        }

        await _next(context);
    }

    private string GetClientId(HttpContext context)
    {
        // Use API key, user ID, or IP address
        var apiKey = context.Request.Headers["X-API-Key"].FirstOrDefault();
        if (!string.IsNullOrEmpty(apiKey))
            return apiKey;

        var userId = context.User?.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        if (!string.IsNullOrEmpty(userId))
            return userId;

        return context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
    }
}

[AttributeUsage(AttributeTargets.Method)]
public class RateLimitAttribute : Attribute
{
    public int Limit { get; }
    public TimeSpan Window { get; }

    public RateLimitAttribute(int limit, int windowSeconds = 60)
    {
        Limit = limit;
        Window = TimeSpan.FromSeconds(windowSeconds);
    }
}

// Usage in controller
[HttpGet]
[RateLimit(100, 60)] // 100 requests per minute
public async Task<ActionResult<List<ProductDto>>> GetProducts()
{
    // ...
}
```

## Sources

- [ASP.NET Core Documentation](https://docs.microsoft.com/en-us/aspnet/core/)
- [Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/)
- [SignalR Documentation](https://docs.microsoft.com/en-us/aspnet/core/signalr/)
