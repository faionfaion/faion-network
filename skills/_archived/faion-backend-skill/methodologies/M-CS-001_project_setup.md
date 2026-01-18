# M-CS-001: C# Project Setup with .NET

## Metadata
- **Category:** Development/Backend/C#
- **Difficulty:** Beginner
- **Tags:** #dev, #csharp, #dotnet, #backend, #methodology
- **Agent:** faion-code-agent

---

## Problem

.NET projects require proper solution structure, NuGet management, and configuration. Without standards, codebases become inconsistent. You need a professional foundation.

## Promise

After this methodology, you will have a professional .NET project with proper solution structure, dependency management, and configuration following C# best practices.

## Overview

Modern .NET (8+) uses minimal APIs, records, and nullable reference types. This methodology covers setup for ASP.NET Core Web APIs.

---

## Framework

### Step 1: .NET SDK Installation

```bash
# Install .NET SDK (Ubuntu)
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update && sudo apt install -y dotnet-sdk-8.0

# macOS
brew install --cask dotnet-sdk

# Verify
dotnet --version
```

### Step 2: Create Project

```bash
# Create solution
dotnet new sln -n MyApp

# Create Web API project
dotnet new webapi -n MyApp.Api -o src/MyApp.Api

# Create class library for domain
dotnet new classlib -n MyApp.Domain -o src/MyApp.Domain

# Create class library for infrastructure
dotnet new classlib -n MyApp.Infrastructure -o src/MyApp.Infrastructure

# Create test project
dotnet new xunit -n MyApp.Tests -o tests/MyApp.Tests

# Add projects to solution
dotnet sln add src/MyApp.Api
dotnet sln add src/MyApp.Domain
dotnet sln add src/MyApp.Infrastructure
dotnet sln add tests/MyApp.Tests

# Add references
dotnet add src/MyApp.Api reference src/MyApp.Domain
dotnet add src/MyApp.Api reference src/MyApp.Infrastructure
dotnet add src/MyApp.Infrastructure reference src/MyApp.Domain
dotnet add tests/MyApp.Tests reference src/MyApp.Api
```

### Step 3: Solution Structure

```
MyApp/
├── MyApp.sln
├── .editorconfig
├── .gitignore
├── Directory.Build.props
├── Directory.Packages.props
├── README.md
├── src/
│   ├── MyApp.Api/
│   │   ├── MyApp.Api.csproj
│   │   ├── Program.cs
│   │   ├── appsettings.json
│   │   ├── appsettings.Development.json
│   │   ├── Controllers/
│   │   ├── Endpoints/
│   │   └── Extensions/
│   ├── MyApp.Domain/
│   │   ├── MyApp.Domain.csproj
│   │   ├── Entities/
│   │   ├── Interfaces/
│   │   └── ValueObjects/
│   └── MyApp.Infrastructure/
│       ├── MyApp.Infrastructure.csproj
│       ├── Data/
│       ├── Repositories/
│       └── Services/
├── tests/
│   └── MyApp.Tests/
│       ├── MyApp.Tests.csproj
│       └── UnitTests/
└── docker-compose.yml
```

### Step 4: Central Package Management

**Directory.Packages.props:**

```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <!-- ASP.NET Core -->
    <PackageVersion Include="Microsoft.AspNetCore.OpenApi" Version="8.0.0" />
    <PackageVersion Include="Swashbuckle.AspNetCore" Version="6.5.0" />

    <!-- Entity Framework -->
    <PackageVersion Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
    <PackageVersion Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.0.0" />

    <!-- Validation -->
    <PackageVersion Include="FluentValidation" Version="11.9.0" />
    <PackageVersion Include="FluentValidation.DependencyInjectionExtensions" Version="11.9.0" />

    <!-- Testing -->
    <PackageVersion Include="xunit" Version="2.6.5" />
    <PackageVersion Include="xunit.runner.visualstudio" Version="2.5.6" />
    <PackageVersion Include="Moq" Version="4.20.70" />
    <PackageVersion Include="FluentAssertions" Version="6.12.0" />
    <PackageVersion Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
  </ItemGroup>
</Project>
```

**Directory.Build.props:**

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  </PropertyGroup>
</Project>
```

### Step 5: Minimal API Setup

**Program.cs:**

```csharp
using MyApp.Api.Extensions;
using MyApp.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddInfrastructure(builder.Configuration);
builder.Services.AddApplicationServices();

var app = builder.Build();

// Configure pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();

// Map endpoints
app.MapUserEndpoints();
app.MapHealthEndpoints();

app.Run();

// For integration tests
public partial class Program { }
```

### Step 6: Configuration

**appsettings.json:**

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=myapp;Username=postgres;Password=postgres"
  },
  "Jwt": {
    "Secret": "your-secret-key-at-least-32-characters",
    "Issuer": "myapp",
    "Audience": "myapp",
    "ExpiryMinutes": 60
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  }
}
```

**Strongly-typed configuration:**

```csharp
public record JwtSettings
{
    public required string Secret { get; init; }
    public required string Issuer { get; init; }
    public required string Audience { get; init; }
    public int ExpiryMinutes { get; init; } = 60;
}

// In Program.cs
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));
```

---

## Templates

**.gitignore:**

```
# Build results
bin/
obj/

# User-specific files
*.user
*.suo
*.userosscache
*.sln.docstates

# IDE
.vs/
.idea/
*.code-workspace

# NuGet
*.nupkg
.nuget/

# Test results
TestResults/
coverage/

# Environment
.env
appsettings.*.local.json
```

**.editorconfig:**

```ini
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.cs]
dotnet_sort_system_directives_first = true
csharp_new_line_before_open_brace = all
csharp_new_line_before_else = true
csharp_new_line_before_catch = true
csharp_new_line_before_finally = true
csharp_indent_case_contents = true
csharp_space_after_keywords_in_control_flow_statements = true
csharp_style_var_for_built_in_types = false:warning
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_prefer_braces = true:warning
csharp_prefer_simple_using_statement = true:suggestion
csharp_style_prefer_primary_constructors = true:suggestion

[*.{csproj,props,targets}]
indent_size = 2
```

**Dockerfile:**

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["src/MyApp.Api/MyApp.Api.csproj", "src/MyApp.Api/"]
COPY ["src/MyApp.Domain/MyApp.Domain.csproj", "src/MyApp.Domain/"]
COPY ["src/MyApp.Infrastructure/MyApp.Infrastructure.csproj", "src/MyApp.Infrastructure/"]
COPY ["Directory.Build.props", "."]
COPY ["Directory.Packages.props", "."]
RUN dotnet restore "src/MyApp.Api/MyApp.Api.csproj"
COPY . .
RUN dotnet build "src/MyApp.Api/MyApp.Api.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "src/MyApp.Api/MyApp.Api.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyApp.Api.dll"]
```

---

## Examples

### Minimal API Endpoints

```csharp
public static class UserEndpoints
{
    public static void MapUserEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/api/users")
            .WithTags("Users")
            .RequireAuthorization();

        group.MapGet("/", GetUsers);
        group.MapGet("/{id:int}", GetUser);
        group.MapPost("/", CreateUser);
        group.MapPut("/{id:int}", UpdateUser);
        group.MapDelete("/{id:int}", DeleteUser);
    }

    private static async Task<IResult> GetUsers(
        IUserService userService,
        [AsParameters] UserQuery query)
    {
        var users = await userService.GetAllAsync(query);
        return Results.Ok(users);
    }

    private static async Task<IResult> CreateUser(
        IUserService userService,
        IValidator<CreateUserRequest> validator,
        CreateUserRequest request)
    {
        var validation = await validator.ValidateAsync(request);
        if (!validation.IsValid)
        {
            return Results.ValidationProblem(validation.ToDictionary());
        }

        var user = await userService.CreateAsync(request);
        return Results.Created($"/api/users/{user.Id}", user);
    }
}
```

---

## Common Mistakes

1. **Not enabling nullable** - Always enable nullable reference types
2. **Missing async/await** - Use async throughout
3. **No central package management** - Use Directory.Packages.props
4. **Ignoring warnings** - Treat warnings as errors
5. **No .editorconfig** - Enforce code style

---

## Checklist

- [ ] .NET 8+ SDK installed
- [ ] Solution structure created
- [ ] Central package management
- [ ] Nullable reference types enabled
- [ ] .editorconfig configured
- [ ] TreatWarningsAsErrors enabled
- [ ] Dockerfile ready
- [ ] .gitignore complete

---

## Next Steps

- M-CS-002: ASP.NET Core Patterns
- M-CS-003: C# Testing with xUnit
- M-CS-004: C# Code Quality

---

*Methodology M-CS-001 v1.0*
