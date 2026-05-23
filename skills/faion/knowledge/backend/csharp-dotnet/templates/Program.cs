// purpose: minimal-hosting Program.cs with DI graph + ProblemDetails + hosted services
// consumes: feature list, DI dependency list, EF DbContext type
// produces: ASP.NET Core service entry point conforming to 02-output-contract.xml
// depends-on: content/01-core-rules.xml rules di-lifetimes, problemdetails-errors
// token-budget-impact: ~600 tokens when loaded as context
using Microsoft.EntityFrameworkCore;
using System.Threading.Channels;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IUserService, UserService>();

builder.Services.AddAutoMapper(typeof(Program).Assembly);

builder.Services.AddSingleton(_ => Channel.CreateBounded<int>(
    new BoundedChannelOptions(1024) { FullMode = BoundedChannelFullMode.Wait }));
builder.Services.AddSingleton<IOrderQueue, OrderQueue>();
builder.Services.AddHostedService<BackgroundOrderProcessor>();

builder.Services.AddProblemDetails();
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

var app = builder.Build();

app.UseExceptionHandler();
app.UseStatusCodePages();
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();

public partial class Program { }
