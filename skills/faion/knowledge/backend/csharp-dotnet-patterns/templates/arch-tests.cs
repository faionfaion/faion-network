// purpose: NetArchTest fitness suite enforcing Clean Architecture layer direction
// consumes: solution layout from 02-output-contract.xml (Domain/Application/Infrastructure/Api)
// produces: xunit test gate that fails CI on layer leakage
// depends-on: content/01-core-rules.xml rule layer-direction
// token-budget-impact: ~250 tokens when loaded as context
// tests/MyApp.ArchitectureTests/LayerTests.cs
// Run via: dotnet test — required CI gate, not optional.
using NetArchTest.Rules;
using Xunit;

public class LayerTests
{
    private const string Domain         = "MyApp.Domain";
    private const string Application    = "MyApp.Application";
    private const string Infrastructure = "MyApp.Infrastructure";
    private const string Api            = "MyApp.Api";

    [Fact]
    public void Domain_does_not_reference_outer_layers() =>
        Assert.True(Types.InAssembly(typeof(MyApp.Domain.Entities.User).Assembly)
            .Should().NotHaveDependencyOnAny(
                Application, Infrastructure, Api,
                "Microsoft.EntityFrameworkCore", "MediatR", "AutoMapper")
            .GetResult().IsSuccessful);

    [Fact]
    public void Application_does_not_reference_infrastructure() =>
        Assert.True(Types.InAssembly(typeof(MyApp.Application.DependencyInjection).Assembly)
            .Should().NotHaveDependencyOn(Infrastructure)
            .GetResult().IsSuccessful);

    [Fact]
    public void Handlers_live_in_Application() =>
        Assert.True(Types.InCurrentDomain()
            .That().ImplementInterface(typeof(MediatR.IRequestHandler<,>))
            .Should().ResideInNamespace(Application)
            .GetResult().IsSuccessful);
}
