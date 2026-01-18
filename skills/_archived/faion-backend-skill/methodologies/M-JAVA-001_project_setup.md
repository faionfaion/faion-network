# M-JAVA-001: Java Project Setup with Maven/Gradle

## Metadata
- **Category:** Development/Backend/Java
- **Difficulty:** Beginner
- **Tags:** #dev, #java, #backend, #maven, #gradle, #methodology
- **Agent:** faion-code-agent

---

## Problem

Java projects require careful build configuration. Maven and Gradle have different strengths and learning curves. JDK version management causes compatibility issues across teams.

## Promise

After this methodology, you will have a professional Java project with proper build configuration, dependency management, and project structure.

## Overview

Modern Java (21+) uses Maven or Gradle for builds, follows standard project layouts, and leverages modern language features. This methodology covers setup for both Spring Boot and vanilla Java.

---

## Framework

### Step 1: JDK Version Management

```bash
# Install SDKMAN
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# List available JDKs
sdk list java

# Install specific version
sdk install java 21.0.2-tem

# Use specific version
sdk use java 21.0.2-tem

# Set default
sdk default java 21.0.2-tem

# Create .sdkmanrc for project
echo "java=21.0.2-tem" > .sdkmanrc
```

### Step 2: Initialize Project

**Spring Boot with Maven:**

```bash
# Using Spring Initializr
curl https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d language=java \
  -d bootVersion=3.2.0 \
  -d baseDir=my-app \
  -d groupId=com.example \
  -d artifactId=my-app \
  -d name=my-app \
  -d description=My%20Application \
  -d packageName=com.example.myapp \
  -d javaVersion=21 \
  -d dependencies=web,data-jpa,postgresql,validation \
  -o my-app.zip

unzip my-app.zip && cd my-app
```

**Spring Boot with Gradle:**

```bash
curl https://start.spring.io/starter.zip \
  -d type=gradle-project \
  -d language=java \
  -d bootVersion=3.2.0 \
  -d baseDir=my-app \
  -d groupId=com.example \
  -d artifactId=my-app \
  -d name=my-app \
  -d packageName=com.example.myapp \
  -d javaVersion=21 \
  -d dependencies=web,data-jpa,postgresql,validation \
  -o my-app.zip
```

### Step 3: Project Structure

```
my-app/
├── pom.xml (or build.gradle)
├── .sdkmanrc
├── .gitignore
├── README.md
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/myapp/
│   │   │       ├── MyAppApplication.java
│   │   │       ├── config/
│   │   │       │   └── SecurityConfig.java
│   │   │       ├── controller/
│   │   │       │   └── UserController.java
│   │   │       ├── service/
│   │   │       │   └── UserService.java
│   │   │       ├── repository/
│   │   │       │   └── UserRepository.java
│   │   │       ├── entity/
│   │   │       │   └── User.java
│   │   │       ├── dto/
│   │   │       │   ├── UserRequest.java
│   │   │       │   └── UserResponse.java
│   │   │       └── exception/
│   │   │           └── ResourceNotFoundException.java
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       └── application-prod.yml
│   └── test/
│       └── java/
│           └── com/example/myapp/
│               ├── controller/
│               └── service/
└── docker-compose.yml
```

### Step 4: Maven Configuration

**pom.xml:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>my-app</name>

    <properties>
        <java.version>21</java.version>
        <mapstruct.version>1.5.5.Final</mapstruct.version>
    </properties>

    <dependencies>
        <!-- Spring Boot Starters -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- MapStruct -->
        <dependency>
            <groupId>org.mapstruct</groupId>
            <artifactId>mapstruct</artifactId>
            <version>${mapstruct.version}</version>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>postgresql</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </path>
                        <path>
                            <groupId>org.mapstruct</groupId>
                            <artifactId>mapstruct-processor</artifactId>
                            <version>${mapstruct.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### Step 5: Gradle Configuration

**build.gradle:**

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
}

group = 'com.example'
version = '0.0.1-SNAPSHOT'

java {
    sourceCompatibility = '21'
}

configurations {
    compileOnly {
        extendsFrom annotationProcessor
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'org.mapstruct:mapstruct:1.5.5.Final'

    compileOnly 'org.projectlombok:lombok'
    runtimeOnly 'org.postgresql:postgresql'

    annotationProcessor 'org.projectlombok:lombok'
    annotationProcessor 'org.mapstruct:mapstruct-processor:1.5.5.Final'

    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.testcontainers:postgresql'
}

tasks.named('test') {
    useJUnitPlatform()
}
```

### Step 6: Application Configuration

**application.yml:**

```yaml
spring:
  application:
    name: my-app

  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

  datasource:
    url: ${DATABASE_URL:jdbc:postgresql://localhost:5432/myapp}
    username: ${DATABASE_USERNAME:postgres}
    password: ${DATABASE_PASSWORD:postgres}
    driver-class-name: org.postgresql.Driver

  jpa:
    hibernate:
      ddl-auto: validate
    open-in-view: false
    properties:
      hibernate:
        format_sql: true

server:
  port: ${SERVER_PORT:8080}

logging:
  level:
    root: INFO
    com.example.myapp: DEBUG
    org.hibernate.SQL: DEBUG
```

---

## Templates

**.gitignore:**

```
# Build
target/
build/
*.class
*.jar
*.war

# IDE
.idea/
*.iml
.vscode/
.settings/
.project
.classpath

# Gradle
.gradle/
gradle-app.setting

# Logs
*.log

# Environment
.env
```

**Dockerfile:**

```dockerfile
# Build stage
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline
COPY src src
RUN ./mvnw package -DskipTests

# Run stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## Examples

### Main Application

```java
package com.example.myapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MyAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyAppApplication.class, args);
    }
}
```

### Entity with Lombok

```java
package com.example.myapp.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.Instant;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String password;

    @Column(name = "created_at")
    private Instant createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = Instant.now();
    }
}
```

---

## Common Mistakes

1. **Not using SDKMAN** - Ensures JDK consistency
2. **Open-in-view enabled** - Disable for API projects
3. **Missing validation** - Always validate input
4. **Fat controllers** - Use service layer
5. **No profiles** - Separate dev/prod config

---

## Checklist

- [ ] SDKMAN with .sdkmanrc
- [ ] Java 21+ configured
- [ ] Maven or Gradle set up
- [ ] Spring Boot configured
- [ ] Application profiles created
- [ ] Dockerfile ready
- [ ] .gitignore complete

---

## Next Steps

- M-JAVA-002: Spring Boot Patterns
- M-JAVA-003: Java Testing
- M-JAVA-004: Java Code Quality

---

*Methodology M-JAVA-001 v1.0*
