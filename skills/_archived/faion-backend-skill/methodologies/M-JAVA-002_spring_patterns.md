# M-JAVA-002: Spring Boot Patterns

## Metadata
- **Category:** Development/Backend/Java
- **Difficulty:** Intermediate
- **Tags:** #dev, #java, #spring, #patterns, #methodology
- **Agent:** faion-code-agent

---

## Problem

Spring Boot makes starting easy but organizing large applications is challenging. Controllers become bloated, services mix concerns, and testing becomes difficult. You need patterns that scale.

## Promise

After this methodology, you will build Spring Boot applications with clear architecture. Your code will be testable, maintainable, and follow Spring best practices.

## Overview

Modern Spring Boot uses layered architecture, DTOs, MapStruct for mapping, and clean exception handling. This methodology covers patterns for REST APIs.

---

## Framework

### Step 1: Layer Architecture

```
Controller → Service → Repository → Entity
    ↓           ↓           ↓
   DTO       Domain       Entity
```

**Rules:**
- Controllers handle HTTP only
- Services contain business logic
- Repositories handle data access
- DTOs for external communication
- Entities for persistence

### Step 2: Controller Layer

```java
package com.example.myapp.controller;

import com.example.myapp.dto.CreateUserRequest;
import com.example.myapp.dto.UserResponse;
import com.example.myapp.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public ResponseEntity<List<UserResponse>> list(
            @RequestParam(required = false) String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {

        List<UserResponse> users = userService.findAll(search, page, size);
        return ResponseEntity.ok(users);
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> get(@PathVariable Long id) {
        UserResponse user = userService.findById(id);
        return ResponseEntity.ok(user);
    }

    @PostMapping
    public ResponseEntity<UserResponse> create(
            @Valid @RequestBody CreateUserRequest request) {

        UserResponse user = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> update(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {

        UserResponse user = userService.update(id, request);
        return ResponseEntity.ok(user);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

### Step 3: DTOs with Validation

**CreateUserRequest.java:**

```java
package com.example.myapp.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class CreateUserRequest {

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be 2-100 characters")
    private String name;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;
}
```

**UserResponse.java (using records):**

```java
package com.example.myapp.dto;

import java.time.Instant;

public record UserResponse(
    Long id,
    String email,
    String name,
    Instant createdAt
) {}
```

### Step 4: Service Layer

```java
package com.example.myapp.service;

import com.example.myapp.dto.*;
import com.example.myapp.entity.User;
import com.example.myapp.exception.ResourceNotFoundException;
import com.example.myapp.exception.EmailAlreadyExistsException;
import com.example.myapp.mapper.UserMapper;
import com.example.myapp.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    public List<UserResponse> findAll(String search, int page, int size) {
        return userRepository.findBySearch(search, PageRequest.of(page, size))
                .map(userMapper::toResponse)
                .getContent();
    }

    public UserResponse findById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", id));

        return userMapper.toResponse(user);
    }

    @Transactional
    public UserResponse create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailAlreadyExistsException(request.getEmail());
        }

        User user = userMapper.toEntity(request);
        user.setPassword(passwordEncoder.encode(request.getPassword()));

        user = userRepository.save(user);

        return userMapper.toResponse(user);
    }

    @Transactional
    public UserResponse update(Long id, UpdateUserRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", id));

        userMapper.updateEntity(request, user);
        user = userRepository.save(user);

        return userMapper.toResponse(user);
    }

    @Transactional
    public void delete(Long id) {
        if (!userRepository.existsById(id)) {
            throw new ResourceNotFoundException("User", id);
        }

        userRepository.deleteById(id);
    }
}
```

### Step 5: MapStruct Mapper

```java
package com.example.myapp.mapper;

import com.example.myapp.dto.*;
import com.example.myapp.entity.User;
import org.mapstruct.*;

@Mapper(componentModel = "spring")
public interface UserMapper {

    UserResponse toResponse(User user);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "password", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    User toEntity(CreateUserRequest request);

    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntity(UpdateUserRequest request, @MappingTarget User user);
}
```

### Step 6: Exception Handling

**GlobalExceptionHandler.java:**

```java
package com.example.myapp.exception;

import org.springframework.http.*;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import java.time.Instant;
import java.util.Map;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
                HttpStatus.NOT_FOUND.value(),
                "NOT_FOUND",
                ex.getMessage(),
                Instant.now()
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(EmailAlreadyExistsException.class)
    public ResponseEntity<ErrorResponse> handleEmailExists(EmailAlreadyExistsException ex) {
        ErrorResponse error = new ErrorResponse(
                HttpStatus.CONFLICT.value(),
                "CONFLICT",
                ex.getMessage(),
                Instant.now()
        );
        return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ValidationErrorResponse> handleValidation(
            MethodArgumentNotValidException ex) {

        Map<String, String> errors = ex.getBindingResult().getFieldErrors().stream()
                .collect(Collectors.toMap(
                        FieldError::getField,
                        FieldError::getDefaultMessage,
                        (a, b) -> a
                ));

        ValidationErrorResponse error = new ValidationErrorResponse(
                HttpStatus.BAD_REQUEST.value(),
                "VALIDATION_ERROR",
                "Validation failed",
                errors,
                Instant.now()
        );

        return ResponseEntity.badRequest().body(error);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneral(Exception ex) {
        ErrorResponse error = new ErrorResponse(
                HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "INTERNAL_ERROR",
                "An unexpected error occurred",
                Instant.now()
        );
        return ResponseEntity.internalServerError().body(error);
    }
}
```

**ErrorResponse.java:**

```java
package com.example.myapp.exception;

import java.time.Instant;

public record ErrorResponse(
    int status,
    String code,
    String message,
    Instant timestamp
) {}

public record ValidationErrorResponse(
    int status,
    String code,
    String message,
    Map<String, String> errors,
    Instant timestamp
) {}
```

---

## Templates

### Repository with Custom Query

```java
package com.example.myapp.repository;

import com.example.myapp.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);

    @Query("""
        SELECT u FROM User u
        WHERE (:search IS NULL OR
               LOWER(u.name) LIKE LOWER(CONCAT('%', :search, '%')) OR
               LOWER(u.email) LIKE LOWER(CONCAT('%', :search, '%')))
        """)
    Page<User> findBySearch(@Param("search") String search, Pageable pageable);
}
```

### Configuration Properties

```java
@ConfigurationProperties(prefix = "app")
@Validated
public record AppProperties(
    @NotBlank String name,
    @NotNull Security security,
    @NotNull Cors cors
) {
    public record Security(
        @NotBlank String jwtSecret,
        @Positive int jwtExpirationMs
    ) {}

    public record Cors(
        List<String> allowedOrigins
    ) {}
}

// Usage
@EnableConfigurationProperties(AppProperties.class)
@SpringBootApplication
public class Application {}
```

---

## Examples

### Specification for Dynamic Queries

```java
public class UserSpecification {

    public static Specification<User> hasName(String name) {
        return (root, query, cb) ->
            name == null ? null :
            cb.like(cb.lower(root.get("name")), "%" + name.toLowerCase() + "%");
    }

    public static Specification<User> hasStatus(UserStatus status) {
        return (root, query, cb) ->
            status == null ? null :
            cb.equal(root.get("status"), status);
    }

    public static Specification<User> createdAfter(Instant date) {
        return (root, query, cb) ->
            date == null ? null :
            cb.greaterThan(root.get("createdAt"), date);
    }
}

// Usage
Specification<User> spec = Specification
    .where(UserSpecification.hasName(search))
    .and(UserSpecification.hasStatus(status));

userRepository.findAll(spec, pageable);
```

---

## Common Mistakes

1. **Business logic in controllers** - Use services
2. **Exposing entities** - Use DTOs
3. **Missing @Transactional** - Required for writes
4. **N+1 queries** - Use JOIN FETCH or EntityGraph
5. **Generic exception handling** - Create specific exceptions

---

## Checklist

- [ ] Controllers handle HTTP only
- [ ] DTOs for all inputs/outputs
- [ ] MapStruct for mapping
- [ ] Validation on DTOs
- [ ] Global exception handler
- [ ] Transactional services
- [ ] Custom repositories for complex queries

---

## Next Steps

- M-JAVA-003: Java Testing
- M-JAVA-004: Java Code Quality
- M-API-001: REST API Design

---

*Methodology M-JAVA-002 v1.0*
