# M-JAVA-004: Java Code Quality

## Metadata
- **Category:** Development/Backend/Java
- **Difficulty:** Beginner
- **Tags:** #dev, #java, #quality, #checkstyle, #methodology
- **Agent:** faion-code-agent

---

## Problem

Java codebases become inconsistent without enforced standards. Code reviews spend time on formatting instead of logic. Security vulnerabilities hide in complex code.

## Promise

After this methodology, your Java code will be consistent, secure, and maintainable. Static analysis will catch bugs before production.

## Overview

Java code quality uses Checkstyle for style, SpotBugs for bugs, and OWASP for security. This methodology covers the complete quality stack.

---

## Framework

### Step 1: Checkstyle

**Maven:**

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <version>3.3.1</version>
    <configuration>
        <configLocation>checkstyle.xml</configLocation>
        <consoleOutput>true</consoleOutput>
        <failsOnError>true</failsOnError>
    </configuration>
    <executions>
        <execution>
            <id>validate</id>
            <phase>validate</phase>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

**checkstyle.xml:**

```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">

<module name="Checker">
    <property name="charset" value="UTF-8"/>
    <property name="severity" value="error"/>

    <module name="FileLength">
        <property name="max" value="500"/>
    </module>

    <module name="FileTabCharacter"/>

    <module name="TreeWalker">
        <!-- Naming -->
        <module name="ConstantName"/>
        <module name="LocalVariableName"/>
        <module name="MemberName"/>
        <module name="MethodName"/>
        <module name="PackageName"/>
        <module name="ParameterName"/>
        <module name="TypeName"/>

        <!-- Imports -->
        <module name="AvoidStarImport"/>
        <module name="IllegalImport"/>
        <module name="RedundantImport"/>
        <module name="UnusedImports"/>

        <!-- Size -->
        <module name="LineLength">
            <property name="max" value="120"/>
        </module>
        <module name="MethodLength">
            <property name="max" value="50"/>
        </module>
        <module name="ParameterNumber">
            <property name="max" value="5"/>
        </module>

        <!-- Whitespace -->
        <module name="EmptyForIteratorPad"/>
        <module name="GenericWhitespace"/>
        <module name="MethodParamPad"/>
        <module name="NoWhitespaceAfter"/>
        <module name="NoWhitespaceBefore"/>
        <module name="ParenPad"/>
        <module name="WhitespaceAfter"/>
        <module name="WhitespaceAround"/>

        <!-- Coding -->
        <module name="EmptyStatement"/>
        <module name="EqualsHashCode"/>
        <module name="HiddenField">
            <property name="ignoreSetter" value="true"/>
            <property name="ignoreConstructorParameter" value="true"/>
        </module>
        <module name="IllegalInstantiation"/>
        <module name="MissingSwitchDefault"/>
        <module name="SimplifyBooleanExpression"/>
        <module name="SimplifyBooleanReturn"/>

        <!-- Design -->
        <module name="FinalClass"/>
        <module name="HideUtilityClassConstructor"/>
        <module name="InterfaceIsType"/>
    </module>
</module>
```

### Step 2: SpotBugs

**Maven:**

```xml
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
    <version>4.8.3.0</version>
    <configuration>
        <effort>Max</effort>
        <threshold>Low</threshold>
        <xmlOutput>true</xmlOutput>
        <plugins>
            <plugin>
                <groupId>com.h3xstream.findsecbugs</groupId>
                <artifactId>findsecbugs-plugin</artifactId>
                <version>1.12.0</version>
            </plugin>
        </plugins>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

### Step 3: Error Prone

**Maven:**

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.12.1</version>
    <configuration>
        <compilerArgs>
            <arg>-XDcompilePolicy=simple</arg>
            <arg>-Xplugin:ErrorProne</arg>
        </compilerArgs>
        <annotationProcessorPaths>
            <path>
                <groupId>com.google.errorprone</groupId>
                <artifactId>error_prone_core</artifactId>
                <version>2.24.1</version>
            </path>
        </annotationProcessorPaths>
    </configuration>
</plugin>
```

### Step 4: JaCoCo for Coverage

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
        <execution>
            <id>check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### Step 5: OWASP Dependency Check

```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>9.0.8</version>
    <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>
    </configuration>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

### Step 6: SonarQube

**Maven:**

```xml
<plugin>
    <groupId>org.sonarsource.scanner.maven</groupId>
    <artifactId>sonar-maven-plugin</artifactId>
    <version>3.10.0.2594</version>
</plugin>
```

```bash
# Run analysis
mvn sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=mytoken
```

---

## Templates

### CI Configuration

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

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: maven

      - name: Checkstyle
        run: mvn checkstyle:check

      - name: SpotBugs
        run: mvn spotbugs:check

      - name: Build and Test
        run: mvn verify

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: target/site/jacoco/jacoco.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: maven

      - name: OWASP Dependency Check
        run: mvn dependency-check:check
```

### EditorConfig

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

[*.{xml,yml,yaml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

---

## Examples

### Suppressing Warnings

```java
// SpotBugs suppression
@SuppressFBWarnings(value = "NP_NULL_ON_SOME_PATH",
                    justification = "Validated in calling method")
public void process(String input) {
    // ...
}

// Checkstyle suppression
// CHECKSTYLE:OFF
@SuppressWarnings("checkstyle:MagicNumber")
private static final int BUFFER_SIZE = 8192;
// CHECKSTYLE:ON
```

### Custom Checkstyle Rules

```xml
<!-- Enforce specific annotation -->
<module name="MissingOverride"/>

<!-- Require Javadoc on public methods -->
<module name="MissingJavadocMethod">
    <property name="scope" value="public"/>
    <property name="allowMissingPropertyJavadoc" value="true"/>
</module>
```

---

## Common Mistakes

1. **Suppressing all warnings** - Fix issues, don't suppress
2. **Low coverage threshold** - Aim for 80%+
3. **No security scanning** - Run OWASP regularly
4. **Manual formatting** - Use IDE auto-format
5. **Ignoring CI failures** - Quality gates must block

---

## Checklist

- [ ] Checkstyle configured
- [ ] SpotBugs with FindSecBugs
- [ ] Error Prone enabled
- [ ] JaCoCo with coverage threshold
- [ ] OWASP Dependency Check
- [ ] CI runs all quality checks
- [ ] SonarQube integration (optional)
- [ ] EditorConfig for IDE

---

## Next Steps

- M-JAVA-001: Java Project Setup
- M-JAVA-003: Java Testing
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-JAVA-004 v1.0*
