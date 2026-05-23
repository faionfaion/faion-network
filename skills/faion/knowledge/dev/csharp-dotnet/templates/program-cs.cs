// Program.cs — ASP.NET Core minimal hosting with DI, EF Core, AutoMapper, FluentValidation.
// Add "public partial class Program;" at the bottom for WebApplicationFactory in xUnit tests.

var builder = WebApplication.CreateBuilder(args);

// Database
builder.Services.AddDbContext<AppDbContext>(o =>
    o.UseNpgsql(builder.Configuration.GetConnectionString("Default"))
     .UseSnakeCaseNamingConvention());

// Repositories (Scoped — share DbContext lifetime)
builder.Services.AddScoped<IUserRepository, UserRepository>();

// Services (Scoped)
builder.Services.AddScoped<IUserService, UserService>();

// Mapping
builder.Services.AddAutoMapper(typeof(Program));

// Validation
builder.Services.AddFluentValidationAutoValidation();
builder.Services.AddValidatorsFromAssemblyContaining<Program>();

// API
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddOpenApi();

// Auth (add JWT or Cookie per project requirement)
builder.Services.AddAuthentication();
builder.Services.AddAuthorization();

var app = builder.Build();

if (app.Environment.IsDevelopment())
    app.MapOpenApi();

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();

// Required for WebApplicationFactory<Program> in xUnit integration tests.
public partial class Program;
