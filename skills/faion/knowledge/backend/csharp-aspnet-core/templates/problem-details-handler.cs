// purpose: .NET 8+ IExceptionHandler mapping domain exceptions to RFC 7807 ProblemDetails
// consumes: domain exception types (NotFoundException, ValidationException, ...)
// produces: a single ProblemDetails error contract for every failing request
// depends-on: content/01-core-rules.xml rule problem-details-error-contract
// token-budget-impact: ~350 tokens when loaded as context
// ProblemDetailsHandler.cs
// .NET 8+ IExceptionHandler — maps domain exceptions to RFC 7807 ProblemDetails.
// Register in Program.cs:
//   builder.Services.AddProblemDetails();
//   builder.Services.AddExceptionHandler<ProblemDetailsHandler>();
//   app.UseExceptionHandler();
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;

public class ProblemDetailsHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext ctx, Exception ex, CancellationToken ct)
    {
        var pd = ex switch
        {
            NotFoundException nf =>
                new ProblemDetails { Status = 404, Title = nf.Message },
            ValidationException ve =>
                new ProblemDetails { Status = 422, Title = "Validation failed",
                                     Detail = ve.Message },
            UnauthorizedAccessException =>
                new ProblemDetails { Status = 403, Title = "Forbidden" },
            _ => new ProblemDetails { Status = 500, Title = "An unexpected error occurred" }
        };

        ctx.Response.StatusCode = pd.Status!.Value;
        await ctx.Response.WriteAsJsonAsync(pd, ct);
        return true;
    }
}
