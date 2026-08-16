# JUnit Testing (Spring Boot)

## Summary

**One-sentence:** Layered Spring Boot testing with JUnit 5 + Mockito + AssertJ — @WebMvcTest controllers, plain Mockito services, @DataJpaTest repositories with Testcontainers, Jacoco coverage gate in CI.

**One-paragraph:** Layered testing strategy for Spring Boot 3 applications using JUnit 5 + Mockito + AssertJ. Tests use Spring slices to isolate concerns: `@WebMvcTest(Controller.class)` for HTTP contract, plain `@ExtendWith(MockitoExtension.class)` for service logic, `@DataJpaTest` with Testcontainers Postgres for repositories, `@SpringBootTest` once per module for cross-layer integration. Tests follow `methodUnderTest_state_expectedBehaviour`; assertions use AssertJ on collections; async waits use Awaitility, never `Thread.sleep`. Jacoco enforces line ≥ 70 % / branch ≥ 60 % in CI; mutation testing (Pitest) covers payment / auth / billing paths.

**Ефективно для:**

- Spring Boot apps with REST controllers needing HTTP contract tests.
- Service-layer unit tests requiring Mockito mocks for repository / password encoder / mapper.
- Repository-layer tests with real SQL via `@DataJpaTest` + Testcontainers.
- Teams enforcing coverage gates (line ≥ 70 %, branch ≥ 60 %) via Jacoco.
- Refactor projects that need a safety net before agents modify the service layer.

## Applies If (ALL must hold)

- Spring Boot 3 service standardised on JUnit 5 + Mockito + AssertJ.
- Codebase has separable controller, service, repository layers.
- CI infrastructure can run Docker (for Testcontainers).

## Skip If (ANY kills it)

- Reactive Spring (WebFlux) — `@WebMvcTest` does not apply; use `WebTestClient` + `StepVerifier`.
- Pure library projects with no Spring context — plain JUnit 5 + Mockito suffices.
- Spring Boot < 2.4 targets — test infrastructure here assumes JUnit 5 + AssertJ + recent Boot versions.
- Performance benchmarks — use JMH, not example-based tests.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| SUT class list | Java classpath | dev |
| Coverage thresholds | YAML | platform team |
| Container runtime | Docker on dev/CI hosts | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[java-spring-boot]] | Umbrella for service layering. |
| [[java-jpa-hibernate]] | Drives `@DataJpaTest` configuration for repositories. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: naming-convention, layer-slice-assignment, assertj-over-junit-assert, awaitility-not-thread-sleep, testcontainers-not-h2, jacoco-gate-in-ci, parameterizedtest-for-boundaries | 1300 |
| `content/02-output-contract.xml` | essential | JSON Schema for the test-plan manifest + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns: mocking-wrong-layer, argument-matcher-mixing, mockbean-on-non-bean, springboottest-everywhere, mockedstatic-leak, missing-rollback, manual-collaborator-construction, void-async-test, deprecated-mockbean | 1300 |
| `content/04-procedure.xml` | essential | 5-step procedure: assign-layer-slice → controller tests → service tests → repository tests → coverage gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `generate-controller-test` | sonnet | MockMvc + jsonPath assertion synthesis. |
| `generate-service-test` | sonnet | Per-branch Mockito stubbing. |
| `audit-springboottest-usage` | haiku | Mechanical scan for `@SpringBootTest` on slice tests. |
| `generate-parametric-cases` | sonnet | Choosing @ValueSource vs @CsvSource vs @MethodSource per boundary set. |

## Templates

| File | Purpose |
|------|---------|
| `templates/controller-test.java` | @WebMvcTest skeleton with MockMvc + jsonPath assertions. |
| `templates/service-test.java` | Mockito-only unit test skeleton with AssertJ. |
| `templates/RepositoryTests.java` | @DataJpaTest repository slice skeleton with Testcontainers Postgres + @ServiceConnection. |
| `templates/IntegrationTests.java` | @SpringBootTest(RANDOM_PORT) end-to-end skeleton with TestRestTemplate + Testcontainers. |
| `templates/jacoco-gate.sh` | CI wrapper enforcing line/branch thresholds against `jacoco.xml`. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-java-junit-testing.py` | Validate the test-plan manifest against the JSON Schema. | Pre-commit; CI on every methodology PR. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[java-spring-boot]]
- [[java-jpa-hibernate]]
- [[java-spring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (layer under test, persistence dependency, mock target) to a rule from `01-core-rules.xml`. Use it before authoring or refactoring a Spring Boot test.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/controller-test.java`

```java
// @WebMvcTest controller test skeleton
// Replace: UserController, UserService, CreateUserRequest, UserResponse

package com.example.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @MockBean  private UserService userService;

    @Test
    void methodUnderTest_state_expectedBehavior() throws Exception {
        // Arrange
        CreateUserRequest request = new CreateUserRequest("John Doe", "john@example.com", "pass");
        UserResponse response = new UserResponse(1L, "John Doe", "john@example.com");
        when(userService.create(any(CreateUserRequest.class))).thenReturn(response);

        // Act + Assert
        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("John Doe"));
    }
}
```

### `templates/service-test.java`

```java
// @ExtendWith(MockitoExtension) service unit test skeleton
// Replace: UserService, UserRepository, UserMapper, PasswordEncoder

package com.example.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock private UserRepository userRepository;
    @Mock private UserMapper     userMapper;
    @Mock private PasswordEncoder passwordEncoder;
    @InjectMocks private UserService userService;

    private User      user;
    private UserResponse userResponse;

    @BeforeEach
    void setUp() {
        user = User.builder()
                .id(1L).name("John Doe").email("john@example.com").password("encoded")
                .build();
        userResponse = new UserResponse(1L, "John Doe", "john@example.com");
    }

    @Test
    void findById_whenUserNotExists_throwsException() {
        // Arrange
        when(userRepository.findById(999L)).thenReturn(Optional.empty());

        // Act + Assert
        assertThatThrownBy(() -> userService.findById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("User");
    }

    @Test
    void create_encodesPassword() {
        // Arrange
        CreateUserRequest request = new CreateUserRequest("John", "john@example.com", "plaintext");
        when(passwordEncoder.encode("plaintext")).thenReturn("encoded");
        when(userMapper.toEntity(request)).thenReturn(user);
        when(userRepository.save(any(User.class))).thenReturn(user);
        when(userMapper.toResponse(user)).thenReturn(userResponse);

        // Act
        userService.create(request);

        // Assert
        verify(passwordEncoder).encode("plaintext");
    }
}
```

### `templates/jacoco-gate.sh`

```bash
# jacoco-gate.sh — fail CI if Jacoco coverage drops below thresholds.
# Usage: jacoco-gate.sh path/to/jacoco.xml [LINE_PCT] [BRANCH_PCT]
# Defaults: LINE=70, BRANCH=60
set -euo pipefail

XML="${1:?usage: jacoco-gate.sh JACOCO_XML [LINE] [BRANCH]}"
LINE="${2:-70}"
BRANCH="${3:-60}"

python3 - "$XML" "$LINE" "$BRANCH" <<'PY'
import sys, xml.etree.ElementTree as ET

xml_path, line_t, branch_t = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
tree = ET.parse(xml_path).getroot()

def pct(counter):
    miss = int(counter.attrib.get("missed", 0))
    cov  = int(counter.attrib.get("covered", 0))
    total = miss + cov
    return (cov / total * 100) if total else 100.0

line_cov   = next((pct(c) for c in tree.findall("counter") if c.attrib["type"] == "LINE"),   100.0)
branch_cov = next((pct(c) for c in tree.findall("counter") if c.attrib["type"] == "BRANCH"), 100.0)

print(f"line={line_cov:.1f}% branch={branch_cov:.1f}%")

fails = []
if line_cov   < line_t:   fails.append(f"line {line_cov:.1f}% < {line_t}%")
if branch_cov < branch_t: fails.append(f"branch {branch_cov:.1f}% < {branch_t}%")

if fails:
    print("FAIL:", "; ".join(fails))
    sys.exit(1)
print("OK")
PY
```

### `templates/RepositoryTests.java`

```java
package faion.infra.orders;

import faion.domain.orders.Order;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Testcontainers
class OrderRepositoryTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    private OrderRepository repository;

    @Test
    void save_and_findById_returnsAggregateWithItems() {
        Order saved = repository.save(new Order("Alice"));

        var found = repository.findByIdWithItems(saved.getId());

        assertThat(found).isPresent();
        assertThat(found.get().getCustomerName()).isEqualTo("Alice");
    }
}
```

### `templates/IntegrationTests.java`

```java
package faion.app;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class OrdersIntegrationTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    private TestRestTemplate rest;

    @Test
    void createAndGetOrder_endToEnd() {
        ResponseEntity<String> created = rest.postForEntity(
            "/api/orders",
            new CreateOrderRequest("Alice"),
            String.class
        );
        assertThat(created.getStatusCode()).isEqualTo(HttpStatus.CREATED);

        ResponseEntity<String> got = rest.getForEntity(created.getHeaders().getLocation(), String.class);
        assertThat(got.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(got.getBody()).contains("Alice");
    }

    record CreateOrderRequest(String customerName) {}
}
```
