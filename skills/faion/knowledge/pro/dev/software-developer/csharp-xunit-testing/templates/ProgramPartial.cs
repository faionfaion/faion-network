// purpose: make Program visible to test assembly so WebApplicationFactory<Program> compiles
// consumes: nothing
// produces: partial declaration appended to Program.cs
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~30 tokens when loaded as reference

// Append to the bottom of the API project's Program.cs:

public partial class Program { }
