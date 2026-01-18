# M-CS-003: C# Testing with xUnit

## Metadata
- **Category:** Development/Backend/C#
- **Difficulty:** Intermediate
- **Tags:** #dev, #csharp, #testing, #xunit, #methodology
- **Agent:** faion-test-agent

---

## Problem

.NET testing requires understanding of xUnit patterns, mocking with Moq, and integration testing with WebApplicationFactory. You need patterns that make testing productive.

## Promise

After this methodology, you will write xUnit tests that are readable, maintainable, and catch real bugs. You will test units, integration, and APIs effectively.

## Overview

Modern C# testing uses xUnit as the test framework, Moq for mocking, FluentAssertions for readable assertions, and Testcontainers for integration tests.

---

## Framework

### Step 1: Test Project Setup

**MyApp.Tests.csproj:**

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" />
    <PackageReference Include="xunit" />
    <PackageReference Include="xunit.runner.visualstudio" />
    <PackageReference Include="Moq" />
    <PackageReference Include="FluentAssertions" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" />
    <PackageReference Include="Testcontainers.PostgreSql" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\MyApp.Api\MyApp.Api.csproj" />
  </ItemGroup>
</Project>
```

### Step 2: Unit Test Structure

```csharp
using FluentAssertions;
using Moq;
using MyApp.Application.Users.Commands;
using MyApp.Domain.Entities;
using MyApp.Domain.Interfaces;
using Xunit;

namespace MyApp.Tests.Application.Users;

public class CreateUserCommandHandlerTests
{
    private readonly Mock<IUserRepository> _userRepositoryMock;
    private readonly Mock<IPasswordHasher> _passwordHasherMock;
    private readonly Mock<IUnitOfWork> _unitOfWorkMock;
    private readonly CreateUserCommandHandler _handler;

    public CreateUserCommandHandlerTests()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _passwordHasherMock = new Mock<IPasswordHasher>();
        _unitOfWorkMock = new Mock<IUnitOfWork>();

        _handler = new CreateUserCommandHandler(
            _userRepositoryMock.Object,
            _passwordHasherMock.Object,
            _unitOfWorkMock.Object);
    }

    [Fact]
    public async Task Handle_WithValidInput_ShouldCreateUser()
    {
        // Arrange
        var command = new CreateUserCommand(
            "test@example.com",
            "Test User",
            "password123");

        _userRepositoryMock
            .Setup(x => x.ExistsByEmailAsync(command.Email, It.IsAny<CancellationToken>()))
            .ReturnsAsync(false);

        _passwordHasherMock
            .Setup(x => x.Hash(command.Password))
            .Returns("hashed");

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        result.IsSuccess.Should().BeTrue();
        result.Value.Email.Should().Be("test@example.com");

        _userRepositoryMock.Verify(
            x => x.Add(It.Is<User>(u => u.Email == "test@example.com")),
            Times.Once);

        _unitOfWorkMock.Verify(
            x => x.SaveChangesAsync(It.IsAny<CancellationToken>()),
            Times.Once);
    }

    [Fact]
    public async Task Handle_WithDuplicateEmail_ShouldReturnFailure()
    {
        // Arrange
        var command = new CreateUserCommand(
            "existing@example.com",
            "Test User",
            "password123");

        _userRepositoryMock
            .Setup(x => x.ExistsByEmailAsync(command.Email, It.IsAny<CancellationToken>()))
            .ReturnsAsync(true);

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        result.IsFailure.Should().BeTrue();
        result.Error.Code.Should().Be("User.EmailExists");

        _userRepositoryMock.Verify(x => x.Add(It.IsAny<User>()), Times.Never);
    }
}
```

### Step 3: Test Data Builders

```csharp
namespace MyApp.Tests.Builders;

public class UserBuilder
{
    private string _email = "test@example.com";
    private string _name = "Test User";
    private string _passwordHash = "hashed";

    public UserBuilder WithEmail(string email)
    {
        _email = email;
        return this;
    }

    public UserBuilder WithName(string name)
    {
        _name = name;
        return this;
    }

    public User Build()
    {
        return User.Create(_email, _name, _passwordHash);
    }

    public static implicit operator User(UserBuilder builder) => builder.Build();
}

// Usage
var user = new UserBuilder()
    .WithEmail("custom@example.com")
    .WithName("Custom User")
    .Build();
```

### Step 4: Theory Tests

```csharp
public class EmailValidatorTests
{
    [Theory]
    [InlineData("test@example.com", true)]
    [InlineData("user.name@domain.org", true)]
    [InlineData("invalid", false)]
    [InlineData("", false)]
    [InlineData(null, false)]
    public void IsValid_ShouldValidateCorrectly(string? email, bool expected)
    {
        // Act
        var result = EmailValidator.IsValid(email);

        // Assert
        result.Should().Be(expected);
    }

    [Theory]
    [MemberData(nameof(GetValidationTestData))]
    public void Validate_ShouldReturnExpectedErrors(
        CreateUserCommand command,
        bool shouldBeValid,
        string[] expectedErrors)
    {
        // Arrange
        var validator = new CreateUserCommandValidator();

        // Act
        var result = validator.Validate(command);

        // Assert
        result.IsValid.Should().Be(shouldBeValid);
        if (!shouldBeValid)
        {
            result.Errors.Select(e => e.PropertyName)
                .Should().Contain(expectedErrors);
        }
    }

    public static IEnumerable<object[]> GetValidationTestData()
    {
        yield return new object[]
        {
            new CreateUserCommand("valid@email.com", "Name", "password123"),
            true,
            Array.Empty<string>()
        };
        yield return new object[]
        {
            new CreateUserCommand("", "Name", "password123"),
            false,
            new[] { "Email" }
        };
        yield return new object[]
        {
            new CreateUserCommand("valid@email.com", "", "short"),
            false,
            new[] { "Name", "Password" }
        };
    }
}
```

### Step 5: Integration Tests

```csharp
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Testcontainers.PostgreSql;

namespace MyApp.Tests.Integration;

public class IntegrationTestBase : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres = new PostgreSqlBuilder()
        .WithImage("postgres:16-alpine")
        .WithDatabase("testdb")
        .WithUsername("test")
        .WithPassword("test")
        .Build();

    protected HttpClient Client { get; private set; } = null!;
    protected WebApplicationFactory<Program> Factory { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();

        Factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                builder.ConfigureServices(services =>
                {
                    // Replace database connection
                    services.Configure<DatabaseSettings>(opts =>
                    {
                        opts.ConnectionString = _postgres.GetConnectionString();
                    });
                });
            });

        Client = Factory.CreateClient();
    }

    public async Task DisposeAsync()
    {
        await _postgres.StopAsync();
        await Factory.DisposeAsync();
    }
}
```

```csharp
public class UsersApiTests : IntegrationTestBase
{
    [Fact]
    public async Task CreateUser_WithValidData_ShouldReturnCreated()
    {
        // Arrange
        var request = new CreateUserCommand(
            "test@example.com",
            "Test User",
            "password123");

        // Act
        var response = await Client.PostAsJsonAsync("/api/users", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);

        var user = await response.Content.ReadFromJsonAsync<UserResponse>();
        user.Should().NotBeNull();
        user!.Email.Should().Be("test@example.com");
    }

    [Fact]
    public async Task CreateUser_WithInvalidData_ShouldReturnBadRequest()
    {
        // Arrange
        var request = new CreateUserCommand("", "", "");

        // Act
        var response = await Client.PostAsJsonAsync("/api/users", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }
}
```

### Step 6: Test Fixtures

```csharp
public class DatabaseFixture : IAsyncLifetime
{
    public ApplicationDbContext Context { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        Context = new ApplicationDbContext(options);
        await Context.Database.EnsureCreatedAsync();

        // Seed test data
        Context.Users.Add(User.Create("seeded@example.com", "Seeded User", "hash"));
        await Context.SaveChangesAsync();
    }

    public async Task DisposeAsync()
    {
        await Context.DisposeAsync();
    }
}

[CollectionDefinition("Database")]
public class DatabaseCollection : ICollectionFixture<DatabaseFixture> { }

[Collection("Database")]
public class UserRepositoryTests
{
    private readonly DatabaseFixture _fixture;

    public UserRepositoryTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task GetByEmail_ShouldReturnUser()
    {
        // Arrange
        var repository = new UserRepository(_fixture.Context);

        // Act
        var user = await repository.GetByEmailAsync("seeded@example.com");

        // Assert
        user.Should().NotBeNull();
    }
}
```

---

## Templates

### Custom Assertions

```csharp
public static class ResultAssertions
{
    public static void ShouldBeSuccess<T>(this Result<T> result)
    {
        result.IsSuccess.Should().BeTrue(
            because: $"Expected success but got error: {result.Error}");
    }

    public static void ShouldBeFailure<T>(this Result<T> result, string errorCode)
    {
        result.IsFailure.Should().BeTrue();
        result.Error.Code.Should().Be(errorCode);
    }
}

// Usage
result.ShouldBeSuccess();
result.ShouldBeFailure("User.NotFound");
```

---

## Examples

### Testing with Time

```csharp
public interface IDateTimeProvider
{
    DateTime UtcNow { get; }
}

public class TestDateTimeProvider : IDateTimeProvider
{
    public DateTime UtcNow { get; set; } = DateTime.UtcNow;
}

[Fact]
public void Token_ShouldExpireAfter24Hours()
{
    // Arrange
    var dateTime = new TestDateTimeProvider { UtcNow = new DateTime(2024, 1, 1) };
    var token = Token.Create(userId: 1, dateTime);

    // Act - simulate time passing
    dateTime.UtcNow = dateTime.UtcNow.AddHours(25);

    // Assert
    token.IsExpired(dateTime).Should().BeTrue();
}
```

---

## Common Mistakes

1. **Shared test state** - Use fixtures properly
2. **Testing implementation** - Test behavior
3. **No async assertions** - Use FluentAssertions async
4. **Slow integration tests** - Use containers
5. **Missing Theory data** - Test edge cases

---

## Checklist

- [ ] xUnit configured
- [ ] Moq for mocking
- [ ] FluentAssertions for assertions
- [ ] Test data builders
- [ ] Integration tests with containers
- [ ] Collection fixtures for shared resources
- [ ] CI runs all tests
- [ ] Coverage reports

---

## Next Steps

- M-CS-004: C# Code Quality
- M-CS-002: ASP.NET Core Patterns
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-CS-003 v1.0*
