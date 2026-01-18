# M-JAVA-003: Java Testing with JUnit 5

## Metadata
- **Category:** Development/Backend/Java
- **Difficulty:** Intermediate
- **Tags:** #dev, #java, #testing, #junit, #methodology
- **Agent:** faion-test-agent

---

## Problem

Java testing requires significant boilerplate. Mocking frameworks have learning curves. Integration tests are slow without proper setup. You need patterns that make testing productive.

## Promise

After this methodology, you will write JUnit 5 tests that are readable, maintainable, and fast. You will use Mockito effectively and run integration tests with Testcontainers.

## Overview

Modern Java testing uses JUnit 5, Mockito for mocking, AssertJ for assertions, and Testcontainers for integration tests.

---

## Framework

### Step 1: Dependencies

**Maven:**

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>postgresql</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>testcontainers-bom</artifactId>
            <version>1.19.3</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Step 2: Unit Test Structure

```java
package com.example.myapp.service;

import com.example.myapp.dto.CreateUserRequest;
import com.example.myapp.dto.UserResponse;
import com.example.myapp.entity.User;
import com.example.myapp.exception.EmailAlreadyExistsException;
import com.example.myapp.mapper.UserMapper;
import com.example.myapp.repository.UserRepository;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private UserMapper userMapper;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Captor
    private ArgumentCaptor<User> userCaptor;

    @Nested
    @DisplayName("create")
    class CreateTests {

        @Test
        @DisplayName("should create user with valid data")
        void shouldCreateUserWithValidData() {
            // Arrange
            CreateUserRequest request = new CreateUserRequest();
            request.setEmail("test@example.com");
            request.setName("Test User");
            request.setPassword("password123");

            User user = new User();
            user.setEmail(request.getEmail());
            user.setName(request.getName());

            User savedUser = new User();
            savedUser.setId(1L);
            savedUser.setEmail(request.getEmail());
            savedUser.setName(request.getName());

            UserResponse expectedResponse = new UserResponse(1L, "test@example.com", "Test User", null);

            when(userRepository.existsByEmail(request.getEmail())).thenReturn(false);
            when(userMapper.toEntity(request)).thenReturn(user);
            when(passwordEncoder.encode(request.getPassword())).thenReturn("encoded");
            when(userRepository.save(any(User.class))).thenReturn(savedUser);
            when(userMapper.toResponse(savedUser)).thenReturn(expectedResponse);

            // Act
            UserResponse result = userService.create(request);

            // Assert
            assertThat(result).isNotNull();
            assertThat(result.email()).isEqualTo("test@example.com");

            verify(userRepository).save(userCaptor.capture());
            assertThat(userCaptor.getValue().getPassword()).isEqualTo("encoded");
        }

        @Test
        @DisplayName("should throw when email already exists")
        void shouldThrowWhenEmailExists() {
            // Arrange
            CreateUserRequest request = new CreateUserRequest();
            request.setEmail("existing@example.com");

            when(userRepository.existsByEmail(request.getEmail())).thenReturn(true);

            // Act & Assert
            assertThatThrownBy(() -> userService.create(request))
                    .isInstanceOf(EmailAlreadyExistsException.class)
                    .hasMessageContaining("existing@example.com");

            verify(userRepository, never()).save(any());
        }
    }
}
```

### Step 3: Parameterized Tests

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;

class EmailValidatorTest {

    @ParameterizedTest
    @ValueSource(strings = {
        "test@example.com",
        "user.name@domain.org",
        "user+tag@example.com"
    })
    @DisplayName("should accept valid emails")
    void shouldAcceptValidEmails(String email) {
        assertThat(EmailValidator.isValid(email)).isTrue();
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"invalid", "missing@", "@nodomain.com"})
    @DisplayName("should reject invalid emails")
    void shouldRejectInvalidEmails(String email) {
        assertThat(EmailValidator.isValid(email)).isFalse();
    }

    @ParameterizedTest
    @CsvSource({
        "100, USD, $100.00",
        "50, EUR, 50.00 EUR",
        "1000, JPY, 1000 JPY"
    })
    @DisplayName("should format currency correctly")
    void shouldFormatCurrency(int amount, String currency, String expected) {
        assertThat(CurrencyFormatter.format(amount, currency)).isEqualTo(expected);
    }

    @ParameterizedTest
    @MethodSource("provideUserTestData")
    @DisplayName("should validate user data")
    void shouldValidateUserData(String name, String email, boolean expected) {
        assertThat(UserValidator.isValid(name, email)).isEqualTo(expected);
    }

    static Stream<Arguments> provideUserTestData() {
        return Stream.of(
            Arguments.of("John", "john@example.com", true),
            Arguments.of("", "john@example.com", false),
            Arguments.of("John", "invalid", false)
        );
    }
}
```

### Step 4: Controller Tests

```java
package com.example.myapp.controller;

import com.example.myapp.dto.CreateUserRequest;
import com.example.myapp.dto.UserResponse;
import com.example.myapp.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.Instant;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private UserService userService;

    @Test
    void shouldCreateUser() throws Exception {
        // Arrange
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("test@example.com");
        request.setName("Test User");
        request.setPassword("password123");

        UserResponse response = new UserResponse(1L, "test@example.com", "Test User", Instant.now());

        when(userService.create(any(CreateUserRequest.class))).thenReturn(response);

        // Act & Assert
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.email").value("test@example.com"));
    }

    @Test
    void shouldReturnValidationErrors() throws Exception {
        // Arrange
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("invalid");

        // Act & Assert
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_ERROR"))
                .andExpect(jsonPath("$.errors.email").exists());
    }
}
```

### Step 5: Integration Tests with Testcontainers

```java
package com.example.myapp;

import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
abstract class BaseIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

```java
package com.example.myapp.controller;

import com.example.myapp.BaseIntegrationTest;
import com.example.myapp.dto.CreateUserRequest;
import com.example.myapp.repository.UserRepository;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.*;

import static org.assertj.core.api.Assertions.assertThat;

class UserControllerIntegrationTest extends BaseIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }

    @Test
    void shouldCreateAndRetrieveUser() {
        // Create user
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("test@example.com");
        request.setName("Test User");
        request.setPassword("password123");

        ResponseEntity<String> createResponse = restTemplate.postForEntity(
                "/api/v1/users",
                request,
                String.class
        );

        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);

        // Verify in database
        assertThat(userRepository.findByEmail("test@example.com")).isPresent();
    }
}
```

### Step 6: Test Configuration

**src/test/resources/application-test.yml:**

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
  jpa:
    hibernate:
      ddl-auto: create-drop
  sql:
    init:
      mode: never

logging:
  level:
    org.springframework: WARN
    com.example.myapp: DEBUG
```

---

## Templates

### Test Factory

```java
public class UserTestFactory {

    public static User.UserBuilder aUser() {
        return User.builder()
                .email("test@example.com")
                .name("Test User")
                .password("encoded");
    }

    public static CreateUserRequest.Builder aCreateUserRequest() {
        return CreateUserRequest.builder()
                .email("test@example.com")
                .name("Test User")
                .password("password123");
    }
}

// Usage
User user = UserTestFactory.aUser()
        .email("custom@example.com")
        .build();
```

---

## Examples

### Testing Async Methods

```java
@Test
void shouldProcessAsync() {
    // Arrange
    CompletableFuture<String> future = asyncService.process("input");

    // Act & Assert
    assertThat(future)
            .succeedsWithin(Duration.ofSeconds(5))
            .isEqualTo("processed");
}
```

### Verifying Method Calls

```java
@Test
void shouldCallDependencies() {
    // Act
    userService.create(request);

    // Assert order
    InOrder inOrder = inOrder(userRepository, emailService);
    inOrder.verify(userRepository).save(any(User.class));
    inOrder.verify(emailService).sendWelcome(any(User.class));
}
```

---

## Common Mistakes

1. **Not using MockitoExtension** - Required for @Mock annotations
2. **Mixing unit and integration tests** - Keep them separate
3. **Slow tests** - Use @WebMvcTest over @SpringBootTest when possible
4. **No test isolation** - Clean up between tests
5. **Ignoring async behavior** - Use proper async assertions

---

## Checklist

- [ ] JUnit 5 configured
- [ ] Mockito for unit tests
- [ ] AssertJ for assertions
- [ ] @WebMvcTest for controllers
- [ ] Testcontainers for integration
- [ ] Test factories for data
- [ ] CI runs all tests
- [ ] Coverage reports

---

## Next Steps

- M-JAVA-004: Java Code Quality
- M-JAVA-002: Spring Boot Patterns
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-JAVA-003 v1.0*
