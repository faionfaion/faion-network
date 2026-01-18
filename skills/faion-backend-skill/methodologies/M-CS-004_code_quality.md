# M-CS-004: C# Code Quality

## Metadata
- **Category:** Development/Backend/C#
- **Difficulty:** Beginner
- **Tags:** #dev, #csharp, #quality, #analyzers, #methodology
- **Agent:** faion-code-agent

---

## Problem

C# codebases need consistent style and static analysis. Without enforcement, code quality degrades. Security issues hide in complex code.

## Promise

After this methodology, your C# code will be consistent, secure, and maintainable. Roslyn analyzers will catch bugs before production.

## Overview

.NET code quality uses Roslyn analyzers, StyleCop, and SonarAnalyzer. This methodology covers the complete quality stack.

---

## Framework

### Step 1: Enable Built-in Analyzers

**Directory.Build.props:**

```xml
<Project>
  <PropertyGroup>
    <EnableNETAnalyzers>true</EnableNETAnalyzers>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <Nullable>enable</Nullable>
  </PropertyGroup>
</Project>
```

### Step 2: Add Analyzer Packages

**Directory.Packages.props:**

```xml
<ItemGroup>
  <!-- Style -->
  <PackageVersion Include="StyleCop.Analyzers" Version="1.1.118" />

  <!-- Quality -->
  <PackageVersion Include="SonarAnalyzer.CSharp" Version="9.16.0.82469" />
  <PackageVersion Include="Roslynator.Analyzers" Version="4.7.0" />
  <PackageVersion Include="Meziantou.Analyzer" Version="2.0.127" />

  <!-- Security -->
  <PackageVersion Include="SecurityCodeScan.VS2019" Version="5.6.7" />
</ItemGroup>
```

**In each .csproj:**

```xml
<ItemGroup>
  <PackageReference Include="StyleCop.Analyzers" PrivateAssets="all" />
  <PackageReference Include="SonarAnalyzer.CSharp" PrivateAssets="all" />
  <PackageReference Include="Roslynator.Analyzers" PrivateAssets="all" />
</ItemGroup>
```

### Step 3: EditorConfig for Style

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
# Organize usings
dotnet_sort_system_directives_first = true
dotnet_separate_import_directive_groups = false

# this. preferences
dotnet_style_qualification_for_field = false:warning
dotnet_style_qualification_for_property = false:warning
dotnet_style_qualification_for_method = false:warning
dotnet_style_qualification_for_event = false:warning

# Language keywords vs BCL types
dotnet_style_predefined_type_for_locals_parameters_members = true:warning
dotnet_style_predefined_type_for_member_access = true:warning

# Parentheses
dotnet_style_parentheses_in_arithmetic_binary_operators = always_for_clarity:suggestion
dotnet_style_parentheses_in_relational_binary_operators = always_for_clarity:suggestion

# Expression-level preferences
dotnet_style_object_initializer = true:warning
dotnet_style_collection_initializer = true:warning
dotnet_style_explicit_tuple_names = true:warning
dotnet_style_prefer_inferred_tuple_names = true:suggestion
dotnet_style_prefer_auto_properties = true:warning
dotnet_style_prefer_conditional_expression_over_assignment = true:suggestion
dotnet_style_prefer_conditional_expression_over_return = true:suggestion

# Null-checking
dotnet_style_coalesce_expression = true:warning
dotnet_style_null_propagation = true:warning
dotnet_style_prefer_is_null_check_over_reference_equality_method = true:warning

# C# style
csharp_style_var_for_built_in_types = false:warning
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_style_var_elsewhere = true:suggestion

# Expression-bodied members
csharp_style_expression_bodied_methods = when_on_single_line:suggestion
csharp_style_expression_bodied_constructors = false:suggestion
csharp_style_expression_bodied_properties = true:suggestion
csharp_style_expression_bodied_indexers = true:suggestion
csharp_style_expression_bodied_accessors = true:suggestion
csharp_style_expression_bodied_lambdas = true:suggestion
csharp_style_expression_bodied_local_functions = false:suggestion

# Pattern matching
csharp_style_pattern_matching_over_is_with_cast_check = true:warning
csharp_style_pattern_matching_over_as_with_null_check = true:warning
csharp_style_prefer_switch_expression = true:suggestion
csharp_style_prefer_pattern_matching = true:suggestion
csharp_style_prefer_not_pattern = true:suggestion

# Null-checking
csharp_style_throw_expression = true:warning
csharp_style_conditional_delegate_call = true:warning

# Code block
csharp_prefer_braces = true:warning
csharp_prefer_simple_using_statement = true:suggestion

# 'using' directive
csharp_using_directive_placement = outside_namespace:warning

# New line preferences
csharp_new_line_before_open_brace = all
csharp_new_line_before_else = true
csharp_new_line_before_catch = true
csharp_new_line_before_finally = true
csharp_new_line_before_members_in_object_initializers = true
csharp_new_line_before_members_in_anonymous_types = true

# Indentation
csharp_indent_case_contents = true
csharp_indent_switch_labels = true
csharp_indent_block_contents = true
csharp_indent_braces = false

# Spacing
csharp_space_after_cast = false
csharp_space_after_keywords_in_control_flow_statements = true
csharp_space_between_method_call_parameter_list_parentheses = false
csharp_space_between_method_declaration_parameter_list_parentheses = false

# Naming conventions
dotnet_naming_rule.interface_should_be_begins_with_i.severity = warning
dotnet_naming_rule.interface_should_be_begins_with_i.symbols = interface
dotnet_naming_rule.interface_should_be_begins_with_i.style = begins_with_i

dotnet_naming_symbols.interface.applicable_kinds = interface
dotnet_naming_style.begins_with_i.required_prefix = I
dotnet_naming_style.begins_with_i.capitalization = pascal_case

dotnet_naming_rule.types_should_be_pascal_case.severity = warning
dotnet_naming_rule.types_should_be_pascal_case.symbols = types
dotnet_naming_rule.types_should_be_pascal_case.style = pascal_case

dotnet_naming_symbols.types.applicable_kinds = class, struct, enum
dotnet_naming_style.pascal_case.capitalization = pascal_case

# Analyzer rules
dotnet_diagnostic.CA1062.severity = warning  # Validate arguments of public methods
dotnet_diagnostic.CA1303.severity = none     # Do not pass literals as localized parameters
dotnet_diagnostic.CA1707.severity = warning  # Identifiers should not contain underscores
dotnet_diagnostic.CA2007.severity = warning  # Consider calling ConfigureAwait
```

### Step 4: StyleCop Configuration

**stylecop.json:**

```json
{
  "$schema": "https://raw.githubusercontent.com/DotNetAnalyzers/StyleCopAnalyzers/master/StyleCop.Analyzers/StyleCop.Analyzers/Settings/stylecop.schema.json",
  "settings": {
    "documentationRules": {
      "companyName": "MyCompany",
      "copyrightText": "Copyright (c) {companyName}. All rights reserved.",
      "documentExposedElements": false,
      "documentInternalElements": false,
      "documentPrivateElements": false,
      "documentInterfaces": true
    },
    "orderingRules": {
      "usingDirectivesPlacement": "outsideNamespace",
      "systemUsingDirectivesFirst": true
    },
    "layoutRules": {
      "newlineAtEndOfFile": "require"
    }
  }
}
```

### Step 5: Code Coverage

**coverlet.runsettings:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<RunSettings>
  <DataCollectionRunSettings>
    <DataCollectors>
      <DataCollector friendlyName="XPlat Code Coverage">
        <Configuration>
          <Format>opencover,cobertura</Format>
          <ExcludeByFile>**/Migrations/*.cs</ExcludeByFile>
          <ExcludeByAttribute>Obsolete,GeneratedCodeAttribute,CompilerGeneratedAttribute</ExcludeByAttribute>
        </Configuration>
      </DataCollector>
    </DataCollectors>
  </DataCollectionRunSettings>
</RunSettings>
```

```bash
# Run tests with coverage
dotnet test --collect:"XPlat Code Coverage" --settings coverlet.runsettings

# Generate report
dotnet tool install -g dotnet-reportgenerator-globaltool
reportgenerator -reports:"**/coverage.cobertura.xml" -targetdir:"coveragereport" -reporttypes:Html
```

### Step 6: CI Configuration

**.github/workflows/quality.yml:**

```yaml
name: Quality

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Restore
        run: dotnet restore

      - name: Build
        run: dotnet build --no-restore --warnaserror

      - name: Test with coverage
        run: |
          dotnet test --no-build \
            --collect:"XPlat Code Coverage" \
            --settings coverlet.runsettings

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: "**/coverage.cobertura.xml"
          fail_ci_if_error: true

      - name: Security scan
        run: dotnet list package --vulnerable --include-transitive
```

---

## Templates

### Global Suppressions

**GlobalSuppressions.cs:**

```csharp
using System.Diagnostics.CodeAnalysis;

// Suppress specific rules for entire project
[assembly: SuppressMessage(
    "Style",
    "IDE0058:Expression value is never used",
    Justification = "Logger calls don't need result")]

[assembly: SuppressMessage(
    "Design",
    "CA1062:Validate arguments of public methods",
    Scope = "namespaceanddescendants",
    Target = "~N:MyApp.Tests")]
```

### Local Suppressions

```csharp
// Suppress for method
[SuppressMessage("Security", "CA5350:Do Not Use Weak Cryptographic Algorithms",
    Justification = "Used for non-security checksum")]
public string ComputeChecksum(byte[] data) { ... }

// Suppress inline
#pragma warning disable CA1062
public void Process(string input)
{
    // input is validated by caller
}
#pragma warning restore CA1062
```

---

## Examples

### Format on Save (VS Code)

**.vscode/settings.json:**

```json
{
  "editor.formatOnSave": true,
  "[csharp]": {
    "editor.defaultFormatter": "ms-dotnettools.csharp"
  },
  "omnisharp.enableRoslynAnalyzers": true,
  "omnisharp.enableEditorConfigSupport": true
}
```

---

## Common Mistakes

1. **Suppressing all warnings** - Fix issues, don't suppress
2. **Missing nullable** - Enable nullable reference types
3. **No CI enforcement** - Quality gates must block
4. **Ignoring security warnings** - Address security issues
5. **Inconsistent editorconfig** - Share across solution

---

## Checklist

- [ ] Built-in analyzers enabled
- [ ] StyleCop configured
- [ ] SonarAnalyzer added
- [ ] EditorConfig complete
- [ ] TreatWarningsAsErrors enabled
- [ ] Code coverage threshold
- [ ] CI runs all checks
- [ ] Security scanning enabled

---

## Next Steps

- M-CS-001: C# Project Setup
- M-CS-003: C# Testing with xUnit
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-CS-004 v1.0*
