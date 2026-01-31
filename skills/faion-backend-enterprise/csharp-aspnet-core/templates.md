# ASP.NET Core Code Templates

Copy-paste templates for common ASP.NET Core patterns.

## Project Structure

```
MyApp/
├── MyApp.Api/
│   ├── Controllers/
│   ├── Middleware/
│   ├── Filters/
│   ├── Program.cs
│   └── appsettings.json
├── MyApp.Application/
│   ├── DTOs/
│   ├── Services/
│   ├── Interfaces/
│   ├── Mappings/
│   └── Validators/
├── MyApp.Domain/
│   ├── Entities/
│   ├── Interfaces/
│   └── ValueObjects/
├── MyApp.Infrastructure/
│   ├── Data/
│   │   ├── Configurations/
│   │   └── AppDbContext.cs
│   ├── Repositories/
│   └── Services/
└── MyApp.Tests/
    ├── Unit/
    ├── Integration/
    └── Fixtures/
```

## Controller Templates

### REST API Controller

```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using MyApp.Application.Services;
using MyApp.Application.DTOs;

namespace MyApp.Api.Controllers;

[ApiController]
[Route("api/v1/[controller]")]
[Authorize]
[Produces("application/json")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IUserService userService, ILogger<UsersController> logger)
    {
        _userService = userService;
        _logger = logger;
    }

    /// <summary>
    /// Get all users with pagination
    /// </summary>
    /// <param name="page">Page number (default: 1)</param>
    /// <param name="pageSize">Page size (default: 20)</param>
    /// <returns>Paged list of users</returns>
    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<UserDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<PagedResult<UserDto>>> GetUsers(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        var result = await _userService.GetAllAsync(page, pageSize);
        return Ok(result);
    }

    /// <summary>
    /// Get user by ID
    /// </summary>
    /// <param name="id">User ID</param>
    /// <returns>User details</returns>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<UserDto>> GetUser(int id)
    {
        var user = await _userService.GetByIdAsync(id);
        if (user == null)
            return NotFound();
        return Ok(user);
    }

    /// <summary>
    /// Create new user
    /// </summary>
    /// <param name="dto">User creation data</param>
    /// <returns>Created user</returns>
    [HttpPost]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<UserDto>> CreateUser([FromBody] CreateUserDto dto)
    {
        var user = await _userService.CreateAsync(dto);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }

    /// <summary>
    /// Update existing user
    /// </summary>
    /// <param name="id">User ID</param>
    /// <param name="dto">Updated user data</param>
    /// <returns>Updated user</returns>
    [HttpPut("{id:int}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<UserDto>> UpdateUser(int id, [FromBody] UpdateUserDto dto)
    {
        var user = await _userService.UpdateAsync(id, dto);
        if (user == null)
            return NotFound();
        return Ok(user);
    }

    /// <summary>
    /// Delete user
    /// </summary>
    /// <param name="id">User ID</param>
    /// <returns>No content</returns>
    [HttpDelete("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var success = await _userService.DeleteAsync(id);
        if (!success)
            return NotFound();
        return NoContent();
    }
}
```

### Minimal Controller (Simple CRUD)

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _service;

    public ProductsController(IProductService service) => _service = service;

    [HttpGet]
    public async Task<ActionResult<List<ProductDto>>> GetAll()
        => Ok(await _service.GetAllAsync());

    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> Get(int id)
    {
        var product = await _service.GetByIdAsync(id);
        return product == null ? NotFound() : Ok(product);
    }

    [HttpPost]
    public async Task<ActionResult<ProductDto>> Create(CreateProductDto dto)
    {
        var product = await _service.CreateAsync(dto);
        return CreatedAtAction(nameof(Get), new { id = product.Id }, product);
    }

    [HttpPut("{id}")]
    public async Task<ActionResult<ProductDto>> Update(int id, UpdateProductDto dto)
    {
        var product = await _service.UpdateAsync(id, dto);
        return product == null ? NotFound() : Ok(product);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
        => await _service.DeleteAsync(id) ? NoContent() : NotFound();
}
```

## Service Layer Templates

### Service Interface

```csharp
namespace MyApp.Application.Services;

public interface IUserService
{
    Task<PagedResult<UserDto>> GetAllAsync(int page, int pageSize);
    Task<UserDto?> GetByIdAsync(int id);
    Task<UserDto> CreateAsync(CreateUserDto dto);
    Task<UserDto?> UpdateAsync(int id, UpdateUserDto dto);
    Task<bool> DeleteAsync(int id);
    Task<UserDto?> GetByEmailAsync(string email);
}
```

### Service Implementation

```csharp
using AutoMapper;
using MyApp.Domain.Entities;
using MyApp.Domain.Interfaces;
using MyApp.Application.DTOs;
using Microsoft.AspNetCore.Identity;

namespace MyApp.Application.Services;

public class UserService : IUserService
{
    private readonly IUserRepository _repository;
    private readonly IMapper _mapper;
    private readonly IPasswordHasher<User> _passwordHasher;
    private readonly ILogger<UserService> _logger;

    public UserService(
        IUserRepository repository,
        IMapper mapper,
        IPasswordHasher<User> passwordHasher,
        ILogger<UserService> logger)
    {
        _repository = repository;
        _mapper = mapper;
        _passwordHasher = passwordHasher;
        _logger = logger;
    }

    public async Task<PagedResult<UserDto>> GetAllAsync(int page, int pageSize)
    {
        var users = await _repository.GetPagedAsync(page, pageSize);
        return _mapper.Map<PagedResult<UserDto>>(users);
    }

    public async Task<UserDto?> GetByIdAsync(int id)
    {
        var user = await _repository.GetByIdAsync(id);
        return user == null ? null : _mapper.Map<UserDto>(user);
    }

    public async Task<UserDto> CreateAsync(CreateUserDto dto)
    {
        var user = _mapper.Map<User>(dto);
        user.PasswordHash = _passwordHasher.HashPassword(user, dto.Password);

        await _repository.AddAsync(user);
        await _repository.SaveChangesAsync();

        _logger.LogInformation("User {UserId} created", user.Id);

        return _mapper.Map<UserDto>(user);
    }

    public async Task<UserDto?> UpdateAsync(int id, UpdateUserDto dto)
    {
        var user = await _repository.GetByIdAsync(id);
        if (user == null)
            return null;

        _mapper.Map(dto, user);
        await _repository.SaveChangesAsync();

        _logger.LogInformation("User {UserId} updated", user.Id);

        return _mapper.Map<UserDto>(user);
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var user = await _repository.GetByIdAsync(id);
        if (user == null)
            return false;

        _repository.Remove(user);
        await _repository.SaveChangesAsync();

        _logger.LogInformation("User {UserId} deleted", user.Id);

        return true;
    }

    public async Task<UserDto?> GetByEmailAsync(string email)
    {
        var user = await _repository.GetByEmailAsync(email);
        return user == null ? null : _mapper.Map<UserDto>(user);
    }
}
```

## Repository Templates

### Repository Interface

```csharp
namespace MyApp.Domain.Interfaces;

public interface IUserRepository
{
    Task<User?> GetByIdAsync(int id);
    Task<User?> GetByEmailAsync(string email);
    Task<PagedResult<User>> GetPagedAsync(int page, int pageSize);
    Task<List<User>> GetAllAsync();
    Task AddAsync(User user);
    void Remove(User user);
    void Update(User user);
    Task<bool> ExistsAsync(int id);
    Task SaveChangesAsync();
}
```

### Repository Implementation

```csharp
using Microsoft.EntityFrameworkCore;
using MyApp.Domain.Entities;
using MyApp.Domain.Interfaces;
using MyApp.Infrastructure.Data;

namespace MyApp.Infrastructure.Repositories;

public class UserRepository : IUserRepository
{
    private readonly AppDbContext _context;

    public UserRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetByIdAsync(int id)
    {
        return await _context.Users
            .Include(u => u.Roles)
            .FirstOrDefaultAsync(u => u.Id == id);
    }

    public async Task<User?> GetByEmailAsync(string email)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.Email == email.ToLower());
    }

    public async Task<PagedResult<User>> GetPagedAsync(int page, int pageSize)
    {
        var query = _context.Users
            .AsNoTracking()
            .OrderByDescending(u => u.CreatedAt);

        var totalCount = await query.CountAsync();
        var items = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return new PagedResult<User>(items, totalCount, page, pageSize);
    }

    public async Task<List<User>> GetAllAsync()
    {
        return await _context.Users
            .AsNoTracking()
            .ToListAsync();
    }

    public async Task AddAsync(User user)
    {
        await _context.Users.AddAsync(user);
    }

    public void Remove(User user)
    {
        _context.Users.Remove(user);
    }

    public void Update(User user)
    {
        _context.Users.Update(user);
    }

    public async Task<bool> ExistsAsync(int id)
    {
        return await _context.Users.AnyAsync(u => u.Id == id);
    }

    public async Task SaveChangesAsync()
    {
        await _context.SaveChangesAsync();
    }
}
```

### Generic Repository (Optional)

```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<List<T>> GetAllAsync();
    Task<IQueryable<T>> Query();
    Task AddAsync(T entity);
    void Update(T entity);
    void Remove(T entity);
    Task SaveChangesAsync();
}

public class Repository<T> : IRepository<T> where T : class
{
    protected readonly AppDbContext Context;
    protected readonly DbSet<T> DbSet;

    public Repository(AppDbContext context)
    {
        Context = context;
        DbSet = context.Set<T>();
    }

    public virtual async Task<T?> GetByIdAsync(int id)
        => await DbSet.FindAsync(id);

    public virtual async Task<List<T>> GetAllAsync()
        => await DbSet.ToListAsync();

    public virtual async Task<IQueryable<T>> Query()
        => await Task.FromResult(DbSet.AsQueryable());

    public virtual async Task AddAsync(T entity)
        => await DbSet.AddAsync(entity);

    public virtual void Update(T entity)
        => DbSet.Update(entity);

    public virtual void Remove(T entity)
        => DbSet.Remove(entity);

    public virtual async Task SaveChangesAsync()
        => await Context.SaveChangesAsync();
}
```

## Entity & Configuration Templates

### Entity

```csharp
using System.ComponentModel.DataAnnotations;

namespace MyApp.Domain.Entities;

public class User
{
    public int Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [MaxLength(255)]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;

    [Required]
    public string PasswordHash { get; set; } = string.Empty;

    public bool IsActive { get; set; } = true;

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }

    // Navigation properties
    public ICollection<Role> Roles { get; set; } = new List<Role>();
    public ICollection<Order> Orders { get; set; } = new List<Order>();
}
```

### Entity Type Configuration

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using MyApp.Domain.Entities;

namespace MyApp.Infrastructure.Data.Configurations;

public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(255);

        builder.HasIndex(u => u.Email)
            .IsUnique();

        builder.Property(u => u.PasswordHash)
            .IsRequired();

        builder.Property(u => u.CreatedAt)
            .HasDefaultValueSql("CURRENT_TIMESTAMP");

        // Relationships
        builder.HasMany(u => u.Roles)
            .WithMany(r => r.Users)
            .UsingEntity<Dictionary<string, object>>(
                "user_roles",
                j => j.HasOne<Role>().WithMany().HasForeignKey("RoleId"),
                j => j.HasOne<User>().WithMany().HasForeignKey("UserId"),
                j =>
                {
                    j.HasKey("UserId", "RoleId");
                    j.ToTable("user_roles");
                }
            );

        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.SetNull);
    }
}
```

## DTO Templates

### Request DTOs

```csharp
using System.ComponentModel.DataAnnotations;

namespace MyApp.Application.DTOs;

public record CreateUserDto(
    [Required][MaxLength(100)] string Name,
    [Required][EmailAddress] string Email,
    [Required][MinLength(8)] string Password
);

public record UpdateUserDto(
    [MaxLength(100)] string? Name,
    [EmailAddress] string? Email
);
```

### Response DTOs

```csharp
namespace MyApp.Application.DTOs;

public record UserDto(
    int Id,
    string Name,
    string Email,
    bool IsActive,
    DateTime CreatedAt,
    List<RoleDto> Roles
);

public record RoleDto(
    int Id,
    string Name
);
```

### Paged Result DTO

```csharp
namespace MyApp.Application.DTOs;

public class PagedResult<T>
{
    public List<T> Items { get; set; } = new();
    public int TotalCount { get; set; }
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalPages => (int)Math.Ceiling((double)TotalCount / PageSize);
    public bool HasPreviousPage => Page > 1;
    public bool HasNextPage => Page < TotalPages;

    public PagedResult() { }

    public PagedResult(List<T> items, int totalCount, int page, int pageSize)
    {
        Items = items;
        TotalCount = totalCount;
        Page = page;
        PageSize = pageSize;
    }
}
```

## AutoMapper Profile

```csharp
using AutoMapper;
using MyApp.Domain.Entities;
using MyApp.Application.DTOs;

namespace MyApp.Application.Mappings;

public class MappingProfile : Profile
{
    public MappingProfile()
    {
        // User mappings
        CreateMap<User, UserDto>()
            .ForMember(dest => dest.Roles, opt => opt.MapFrom(src => src.Roles));

        CreateMap<CreateUserDto, User>()
            .ForMember(dest => dest.PasswordHash, opt => opt.Ignore())
            .ForMember(dest => dest.Id, opt => opt.Ignore());

        CreateMap<UpdateUserDto, User>()
            .ForAllMembers(opts => opts.Condition((src, dest, srcMember) => srcMember != null));

        // Role mappings
        CreateMap<Role, RoleDto>();

        // Paged result mappings
        CreateMap(typeof(PagedResult<>), typeof(PagedResult<>));
    }
}
```

## FluentValidation Validators

```csharp
using FluentValidation;
using MyApp.Application.DTOs;

namespace MyApp.Application.Validators;

public class CreateUserDtoValidator : AbstractValidator<CreateUserDto>
{
    public CreateUserDtoValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(100).WithMessage("Name must not exceed 100 characters");

        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required")
            .EmailAddress().WithMessage("Invalid email format")
            .MaximumLength(255);

        RuleFor(x => x.Password)
            .NotEmpty().WithMessage("Password is required")
            .MinimumLength(8).WithMessage("Password must be at least 8 characters")
            .Matches(@"[A-Z]").WithMessage("Password must contain uppercase letter")
            .Matches(@"[a-z]").WithMessage("Password must contain lowercase letter")
            .Matches(@"[0-9]").WithMessage("Password must contain digit");
    }
}
```

## DbContext Template

```csharp
using Microsoft.EntityFrameworkCore;
using MyApp.Domain.Entities;
using MyApp.Infrastructure.Data.Configurations;

namespace MyApp.Infrastructure.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<User> Users => Set<User>();
    public DbSet<Role> Roles => Set<Role>();
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Apply configurations
        modelBuilder.ApplyConfiguration(new UserConfiguration());
        modelBuilder.ApplyConfiguration(new RoleConfiguration());
        modelBuilder.ApplyConfiguration(new OrderConfiguration());

        // Or apply all configurations from assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }

    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Auto-update timestamps
        var entries = ChangeTracker.Entries()
            .Where(e => e.Entity is User && (e.State == EntityState.Added || e.State == EntityState.Modified));

        foreach (var entry in entries)
        {
            if (entry.State == EntityState.Modified)
            {
                ((User)entry.Entity).UpdatedAt = DateTime.UtcNow;
            }
        }

        return base.SaveChangesAsync(cancellationToken);
    }
}
```

## Program.cs Configuration

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using Serilog;
using MyApp.Infrastructure.Data;
using MyApp.Application.Services;
using MyApp.Application.Mappings;
using MyApp.Infrastructure.Repositories;
using MyApp.Domain.Interfaces;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .CreateLogger();

builder.Host.UseSerilog();

// Add services to the container
builder.Services.AddControllers();

// Database
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// AutoMapper
builder.Services.AddAutoMapper(typeof(MappingProfile));

// Repositories
builder.Services.AddScoped<IUserRepository, UserRepository>();

// Services
builder.Services.AddScoped<IUserService, UserService>();

// Authentication & Authorization (if needed)
// builder.Services.AddAuthentication()...
// builder.Services.AddAuthorization()...

// Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "MyApp API", Version = "v1" });
});

// CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
        policy.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());
});

// Health Checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>();

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors("AllowAll");
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.MapHealthChecks("/health");

app.Run();
```

## Middleware Templates

### Exception Handling Middleware

```csharp
using System.Net;
using System.Text.Json;

namespace MyApp.Api.Middleware;

public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "An unhandled exception occurred");
            await HandleExceptionAsync(context, ex);
        }
    }

    private static async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.ContentType = "application/json";
        context.Response.StatusCode = exception switch
        {
            ArgumentNullException => (int)HttpStatusCode.BadRequest,
            UnauthorizedAccessException => (int)HttpStatusCode.Unauthorized,
            _ => (int)HttpStatusCode.InternalServerError
        };

        var response = new
        {
            error = exception.Message,
            statusCode = context.Response.StatusCode
        };

        await context.Response.WriteAsync(JsonSerializer.Serialize(response));
    }
}
```

## Testing Templates

### Unit Test Template

```csharp
using Moq;
using Xunit;
using FluentAssertions;
using AutoMapper;
using MyApp.Application.Services;
using MyApp.Domain.Entities;
using MyApp.Domain.Interfaces;
using MyApp.Application.DTOs;

namespace MyApp.Tests.Unit.Services;

public class UserServiceTests
{
    private readonly Mock<IUserRepository> _mockRepository;
    private readonly Mock<IMapper> _mockMapper;
    private readonly UserService _service;

    public UserServiceTests()
    {
        _mockRepository = new Mock<IUserRepository>();
        _mockMapper = new Mock<IMapper>();
        _service = new UserService(_mockRepository.Object, _mockMapper.Object, null!, null!);
    }

    [Fact]
    public async Task GetByIdAsync_WhenUserExists_ReturnsUserDto()
    {
        // Arrange
        var user = new User { Id = 1, Name = "John", Email = "john@example.com" };
        var userDto = new UserDto(1, "John", "john@example.com", true, DateTime.UtcNow, new());

        _mockRepository.Setup(r => r.GetByIdAsync(1)).ReturnsAsync(user);
        _mockMapper.Setup(m => m.Map<UserDto>(user)).Returns(userDto);

        // Act
        var result = await _service.GetByIdAsync(1);

        // Assert
        result.Should().NotBeNull();
        result!.Id.Should().Be(1);
        result.Name.Should().Be("John");
    }

    [Fact]
    public async Task GetByIdAsync_WhenUserNotExists_ReturnsNull()
    {
        // Arrange
        _mockRepository.Setup(r => r.GetByIdAsync(999)).ReturnsAsync((User?)null);

        // Act
        var result = await _service.GetByIdAsync(999);

        // Assert
        result.Should().BeNull();
    }
}
```

### Integration Test Template

```csharp
using Microsoft.AspNetCore.Mvc.Testing;
using System.Net.Http.Json;
using Xunit;
using FluentAssertions;
using MyApp.Application.DTOs;

namespace MyApp.Tests.Integration;

public class UsersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public UsersApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetUsers_ReturnsSuccessAndCorrectContentType()
    {
        // Act
        var response = await _client.GetAsync("/api/v1/users");

        // Assert
        response.Should().BeSuccessful();
        response.Content.Headers.ContentType?.MediaType.Should().Be("application/json");
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreated()
    {
        // Arrange
        var createDto = new CreateUserDto("Test User", "test@example.com", "Password123!");

        // Act
        var response = await _client.PostAsJsonAsync("/api/v1/users", createDto);

        // Assert
        response.StatusCode.Should().Be(System.Net.HttpStatusCode.Created);
        var user = await response.Content.ReadFromJsonAsync<UserDto>();
        user.Should().NotBeNull();
        user!.Name.Should().Be("Test User");
    }
}
```

## appsettings.json Template

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=myapp;Username=postgres;Password=postgres"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  },
  "Serilog": {
    "Using": ["Serilog.Sinks.Console", "Serilog.Sinks.File"],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    },
    "WriteTo": [
      { "Name": "Console" },
      {
        "Name": "File",
        "Args": {
          "path": "logs/log-.txt",
          "rollingInterval": "Day"
        }
      }
    ]
  },
  "AllowedHosts": "*"
}
```

## Dockerfile Template

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ["MyApp.Api/MyApp.Api.csproj", "MyApp.Api/"]
COPY ["MyApp.Application/MyApp.Application.csproj", "MyApp.Application/"]
COPY ["MyApp.Domain/MyApp.Domain.csproj", "MyApp.Domain/"]
COPY ["MyApp.Infrastructure/MyApp.Infrastructure.csproj", "MyApp.Infrastructure/"]
RUN dotnet restore "MyApp.Api/MyApp.Api.csproj"

COPY . .
WORKDIR "/src/MyApp.Api"
RUN dotnet build "MyApp.Api.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "MyApp.Api.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyApp.Api.dll"]
```
