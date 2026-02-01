# Development Methodologies - Testing

Testing patterns and best practices across all frameworks.

## Python Testing

### Django Testing with pytest

**Problem:** Inconsistent test patterns.

**Framework:**
```python
@pytest.mark.django_db
def test_activate_item_success(user, item):
    result = services.activate_user_item(
        user=user,
        item_code=item.code,
    )
    assert result.is_active is True
    assert result.user == user
```

**Agent:** faion-test-agent

---

## JavaScript/TypeScript Testing

### Frontend Testing

**Problem:** No test strategy.

**Framework:**
```typescript
// Component test with Testing Library
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

test('renders button with text', () => {
  render(<Button variant="primary">Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

**Agent:** faion-test-agent

---

## Backend Language Testing

### Ruby on Rails Testing

**Problem:** Slow, flaky tests.

**Framework:**
```ruby
RSpec.describe UserService do
  describe '#create' do
    let(:params) { { name: 'John', email: 'john@example.com' } }

    it 'creates user with valid params' do
      result = described_class.create(params)
      expect(result).to be_success
    end
  end
end
```

**Agent:** faion-test-agent

### PHP Laravel Testing

**Problem:** No test coverage.

**Framework:**
```php
class UserTest extends TestCase
{
    public function test_user_can_be_created(): void
    {
        $response = $this->postJson('/api/users', [
            'name' => 'John',
            'email' => 'john@example.com',
        ]);

        $response->assertStatus(201);
    }
}
```

**Agent:** faion-test-agent

### Java Spring Boot Testing

**Problem:** Complex test setup.

**Framework:**
```java
@SpringBootTest
class UserServiceTest {
    @Autowired
    private UserService userService;

    @Test
    void shouldCreateUser() {
        CreateUserDto dto = new CreateUserDto("John", "john@example.com");
        User result = userService.createUser(dto);
        assertThat(result.getName()).isEqualTo("John");
    }
}
```

**Agent:** faion-test-agent

### C# .NET Testing

**Problem:** Hard to test dependencies.

**Framework:**
```csharp
public class UserServiceTests
{
    [Fact]
    public async Task CreateAsync_ShouldReturnUser()
    {
        var mockRepo = new Mock<IUserRepository>();
        var service = new UserService(mockRepo.Object);

        var result = await service.CreateAsync(new CreateUserDto("John", "john@example.com"));

        Assert.Equal("John", result.Name);
    }
}
```

**Agent:** faion-test-agent

### Rust Testing

**Problem:** No test organization.

**Framework:**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_user() {
        let user = User::new("John", "john@example.com");
        assert_eq!(user.name, "John");
    }

    #[tokio::test]
    async fn test_async_fetch() {
        let result = fetch_data().await;
        assert!(result.is_ok());
    }
}
```

**Agent:** faion-test-agent

---

*Testing Methodologies - 9 Patterns*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate test cases from requirements | haiku | Pattern-based generation |
| Review test coverage gaps | sonnet | Requires code understanding |
| Design test architecture | opus | Complex coverage strategies |

