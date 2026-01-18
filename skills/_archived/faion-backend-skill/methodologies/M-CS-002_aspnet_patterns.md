# M-CS-002: ASP.NET Core Patterns

## Metadata
- **Category:** Development/Backend/C#
- **Difficulty:** Intermediate
- **Tags:** #dev, #csharp, #aspnet, #patterns, #methodology
- **Agent:** faion-code-agent

---

## Problem

ASP.NET Core applications can become disorganized without clear patterns. Business logic spreads across controllers. Testing becomes difficult. You need architecture that scales.

## Promise

After this methodology, you will build ASP.NET Core applications with clean architecture. Your code will be testable, maintainable, and follow modern C# patterns.

## Overview

Modern ASP.NET Core uses minimal APIs or controllers, Mediator pattern (MediatR), and Result types for error handling.

---

## Framework

### Step 1: Clean Architecture

```
┌─────────────────────────────────────┐
│           Presentation              │
│  (Controllers, Minimal APIs, DTOs)  │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│           Application               │
│    (Use Cases, Commands, Queries)   │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│             Domain                  │
│      (Entities, Value Objects)      │
└─────────────────────────────────────┘
                  ▲
┌─────────────────┴───────────────────┐
│          Infrastructure             │
│    (Database, External Services)    │
└─────────────────────────────────────┘
```

### Step 2: Entity with Domain Logic

```csharp
namespace MyApp.Domain.Entities;

public class User
{
    public int Id { get; private set; }
    public string Email { get; private set; } = null!;
    public string Name { get; private set; } = null!;
    public string PasswordHash { get; private set; } = null!;
    public DateTime CreatedAt { get; private set; }
    public DateTime? UpdatedAt { get; private set; }

    private User() { } // For EF Core

    public static User Create(string email, string name, string passwordHash)
    {
        if (string.IsNullOrWhiteSpace(email))
            throw new ArgumentException("Email is required", nameof(email));

        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Name is required", nameof(name));

        return new User
        {
            Email = email.ToLowerInvariant(),
            Name = name,
            PasswordHash = passwordHash,
            CreatedAt = DateTime.UtcNow
        };
    }

    public void UpdateName(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Name is required", nameof(name));

        Name = name;
        UpdatedAt = DateTime.UtcNow;
    }
}
```

### Step 3: Result Pattern

```csharp
namespace MyApp.Domain.Common;

public class Result
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public Error Error { get; }

    protected Result(bool isSuccess, Error error)
    {
        if (isSuccess && error != Error.None)
            throw new InvalidOperationException();
        if (!isSuccess && error == Error.None)
            throw new InvalidOperationException();

        IsSuccess = isSuccess;
        Error = error;
    }

    public static Result Success() => new(true, Error.None);
    public static Result Failure(Error error) => new(false, error);
    public static Result<T> Success<T>(T value) => new(value, true, Error.None);
    public static Result<T> Failure<T>(Error error) => new(default!, false, error);
}

public class Result<T> : Result
{
    public T Value { get; }

    protected internal Result(T value, bool isSuccess, Error error)
        : base(isSuccess, error)
    {
        Value = value;
    }
}

public record Error(string Code, string Message)
{
    public static readonly Error None = new(string.Empty, string.Empty);
    public static readonly Error NotFound = new("NotFound", "Resource not found");
    public static readonly Error Validation = new("Validation", "Validation error");
}
```

### Step 4: MediatR Commands

**CreateUserCommand.cs:**

```csharp
using MediatR;
using MyApp.Domain.Common;

namespace MyApp.Application.Users.Commands;

public record CreateUserCommand(
    string Email,
    string Name,
    string Password
) : IRequest<Result<UserResponse>>;

public record UserResponse(
    int Id,
    string Email,
    string Name,
    DateTime CreatedAt
);
```

**CreateUserCommandHandler.cs:**

```csharp
using MediatR;
using MyApp.Domain.Common;
using MyApp.Domain.Entities;
using MyApp.Domain.Interfaces;

namespace MyApp.Application.Users.Commands;

public class CreateUserCommandHandler
    : IRequestHandler<CreateUserCommand, Result<UserResponse>>
{
    private readonly IUserRepository _userRepository;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IUnitOfWork _unitOfWork;

    public CreateUserCommandHandler(
        IUserRepository userRepository,
        IPasswordHasher passwordHasher,
        IUnitOfWork unitOfWork)
    {
        _userRepository = userRepository;
        _passwordHasher = passwordHasher;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<UserResponse>> Handle(
        CreateUserCommand request,
        CancellationToken cancellationToken)
    {
        if (await _userRepository.ExistsByEmailAsync(request.Email, cancellationToken))
        {
            return Result.Failure<UserResponse>(
                new Error("User.EmailExists", "Email already registered"));
        }

        var passwordHash = _passwordHasher.Hash(request.Password);
        var user = User.Create(request.Email, request.Name, passwordHash);

        _userRepository.Add(user);
        await _unitOfWork.SaveChangesAsync(cancellationToken);

        return Result.Success(new UserResponse(
            user.Id,
            user.Email,
            user.Name,
            user.CreatedAt
        ));
    }
}
```

### Step 5: Validation with FluentValidation

```csharp
using FluentValidation;

namespace MyApp.Application.Users.Commands;

public class CreateUserCommandValidator : AbstractValidator<CreateUserCommand>
{
    public CreateUserCommandValidator()
    {
        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email is required")
            .EmailAddress().WithMessage("Invalid email format")
            .MaximumLength(255);

        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MinimumLength(2).WithMessage("Name must be at least 2 characters")
            .MaximumLength(100);

        RuleFor(x => x.Password)
            .NotEmpty().WithMessage("Password is required")
            .MinimumLength(8).WithMessage("Password must be at least 8 characters");
    }
}
```

**Validation Pipeline Behavior:**

```csharp
using FluentValidation;
using MediatR;

namespace MyApp.Application.Common.Behaviors;

public class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!_validators.Any())
        {
            return await next();
        }

        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));

        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();

        if (failures.Count != 0)
        {
            throw new ValidationException(failures);
        }

        return await next();
    }
}
```

### Step 6: Controller/Endpoint Integration

**UsersController.cs:**

```csharp
using MediatR;
using Microsoft.AspNetCore.Mvc;
using MyApp.Application.Users.Commands;
using MyApp.Application.Users.Queries;

namespace MyApp.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly ISender _sender;

    public UsersController(ISender sender)
    {
        _sender = sender;
    }

    [HttpGet]
    public async Task<IActionResult> GetAll(
        [FromQuery] GetUsersQuery query,
        CancellationToken cancellationToken)
    {
        var result = await _sender.Send(query, cancellationToken);
        return Ok(result);
    }

    [HttpGet("{id:int}")]
    public async Task<IActionResult> Get(int id, CancellationToken cancellationToken)
    {
        var result = await _sender.Send(new GetUserQuery(id), cancellationToken);

        return result.IsSuccess
            ? Ok(result.Value)
            : NotFound(result.Error);
    }

    [HttpPost]
    public async Task<IActionResult> Create(
        CreateUserCommand command,
        CancellationToken cancellationToken)
    {
        var result = await _sender.Send(command, cancellationToken);

        return result.IsSuccess
            ? CreatedAtAction(nameof(Get), new { id = result.Value.Id }, result.Value)
            : BadRequest(result.Error);
    }
}
```

---

## Templates

### Repository Interface

```csharp
namespace MyApp.Domain.Interfaces;

public interface IUserRepository
{
    Task<User?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<User?> GetByEmailAsync(string email, CancellationToken cancellationToken = default);
    Task<bool> ExistsByEmailAsync(string email, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<User>> GetAllAsync(CancellationToken cancellationToken = default);
    void Add(User user);
    void Update(User user);
    void Remove(User user);
}
```

### EF Core Repository

```csharp
namespace MyApp.Infrastructure.Repositories;

public class UserRepository : IUserRepository
{
    private readonly ApplicationDbContext _context;

    public UserRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {
        return await _context.Users.FindAsync([id], cancellationToken);
    }

    public void Add(User user) => _context.Users.Add(user);
    public void Update(User user) => _context.Users.Update(user);
    public void Remove(User user) => _context.Users.Remove(user);
}
```

---

## Examples

### Global Exception Handler

```csharp
using FluentValidation;
using Microsoft.AspNetCore.Diagnostics;

app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        var exception = context.Features.Get<IExceptionHandlerFeature>()?.Error;

        var (statusCode, error) = exception switch
        {
            ValidationException ve => (400, new
            {
                Code = "Validation",
                Message = "Validation failed",
                Errors = ve.Errors.Select(e => new { e.PropertyName, e.ErrorMessage })
            }),
            _ => (500, new
            {
                Code = "Internal",
                Message = "An error occurred"
            } as object)
        };

        context.Response.StatusCode = statusCode;
        await context.Response.WriteAsJsonAsync(error);
    });
});
```

---

## Common Mistakes

1. **Business logic in controllers** - Use handlers
2. **Exposing entities** - Use DTOs/responses
3. **Ignoring cancellation** - Pass CancellationToken
4. **Sync over async** - Use async throughout
5. **Missing validation** - Validate all input

---

## Checklist

- [ ] Clean architecture layers
- [ ] MediatR for CQRS
- [ ] FluentValidation
- [ ] Result pattern for errors
- [ ] Repository pattern
- [ ] Unit of work
- [ ] Global exception handling

---

## Next Steps

- M-CS-003: C# Testing with xUnit
- M-CS-004: C# Code Quality
- M-API-001: REST API Design

---

*Methodology M-CS-002 v1.0*
