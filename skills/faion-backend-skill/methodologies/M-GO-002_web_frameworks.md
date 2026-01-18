# M-GO-002: Go Web Frameworks

## Metadata
- **Category:** Development/Backend/Go
- **Difficulty:** Intermediate
- **Tags:** #dev, #go, #backend, #web, #gin, #echo, #methodology
- **Agent:** faion-code-agent

---

## Problem

The Go standard library is powerful but verbose for web APIs. Writing middleware, routing, and validation from scratch is time-consuming. You need a framework that adds convenience without sacrificing performance.

## Promise

After this methodology, you will build REST APIs with Gin or Echo that are fast, well-structured, and maintainable. You will know when to use each framework.

## Overview

Gin and Echo are the most popular Go web frameworks. Both are fast and well-documented. This methodology covers patterns that work with either.

---

## Framework

### Step 1: Choose Framework

| Feature | Gin | Echo |
|---------|-----|------|
| Performance | Excellent | Excellent |
| Community | Larger | Growing |
| Middleware | Rich ecosystem | Built-in |
| Validation | go-playground/validator | Built-in |
| Best for | REST APIs | REST APIs, WebSocket |

**Install Gin:**
```bash
go get github.com/gin-gonic/gin
```

**Install Echo:**
```bash
go get github.com/labstack/echo/v4
```

### Step 2: Basic Server

**Gin:**

```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    r.GET("/health", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{"status": "ok"})
    })

    r.Run(":8080")
}
```

**Echo:**

```go
package main

import (
    "net/http"
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()

    e.Use(middleware.Logger())
    e.Use(middleware.Recover())

    e.GET("/health", func(c echo.Context) error {
        return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
    })

    e.Start(":8080")
}
```

### Step 3: Route Groups

**Gin:**

```go
func SetupRoutes(r *gin.Engine) {
    // API v1 group
    v1 := r.Group("/api/v1")
    {
        users := v1.Group("/users")
        {
            users.GET("", listUsers)
            users.GET("/:id", getUser)
            users.POST("", createUser)
            users.PUT("/:id", updateUser)
            users.DELETE("/:id", deleteUser)
        }

        products := v1.Group("/products")
        {
            products.GET("", listProducts)
            products.GET("/:id", getProduct)
        }
    }

    // Protected routes
    auth := v1.Group("/admin")
    auth.Use(authMiddleware())
    {
        auth.GET("/stats", getStats)
    }
}
```

**Echo:**

```go
func SetupRoutes(e *echo.Echo) {
    v1 := e.Group("/api/v1")

    users := v1.Group("/users")
    users.GET("", listUsers)
    users.GET("/:id", getUser)
    users.POST("", createUser)
    users.PUT("/:id", updateUser)
    users.DELETE("/:id", deleteUser)

    admin := v1.Group("/admin")
    admin.Use(authMiddleware)
    admin.GET("/stats", getStats)
}
```

### Step 4: Request Handling

**Gin:**

```go
type CreateUserRequest struct {
    Email    string `json:"email" binding:"required,email"`
    Name     string `json:"name" binding:"required,min=2,max=100"`
    Password string `json:"password" binding:"required,min=8"`
}

func createUser(c *gin.Context) {
    var req CreateUserRequest

    // Bind and validate
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Path parameter
    id := c.Param("id")

    // Query parameter
    page := c.DefaultQuery("page", "1")

    // Header
    token := c.GetHeader("Authorization")

    // Create user
    user, err := userService.Create(req)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusCreated, user)
}
```

**Echo:**

```go
type CreateUserRequest struct {
    Email    string `json:"email" validate:"required,email"`
    Name     string `json:"name" validate:"required,min=2,max=100"`
    Password string `json:"password" validate:"required,min=8"`
}

func createUser(c echo.Context) error {
    var req CreateUserRequest

    // Bind
    if err := c.Bind(&req); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }

    // Validate
    if err := c.Validate(&req); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }

    // Path parameter
    id := c.Param("id")

    // Query parameter
    page := c.QueryParam("page")

    // Create user
    user, err := userService.Create(req)
    if err != nil {
        return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
    }

    return c.JSON(http.StatusCreated, user)
}
```

### Step 5: Middleware

**Gin Custom Middleware:**

```go
func LoggingMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()

        // Process request
        c.Next()

        // Log after request
        latency := time.Since(start)
        status := c.Writer.Status()

        log.Printf("%s %s %d %v",
            c.Request.Method,
            c.Request.URL.Path,
            status,
            latency,
        )
    }
}

func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized,
                gin.H{"error": "missing authorization header"})
            return
        }

        // Validate token
        claims, err := validateToken(token)
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized,
                gin.H{"error": "invalid token"})
            return
        }

        // Store user in context
        c.Set("user_id", claims.UserID)
        c.Next()
    }
}

// Usage
r.Use(LoggingMiddleware())
protected.Use(AuthMiddleware())
```

**Echo Custom Middleware:**

```go
func LoggingMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
    return func(c echo.Context) error {
        start := time.Now()

        err := next(c)

        latency := time.Since(start)
        log.Printf("%s %s %d %v",
            c.Request().Method,
            c.Request().URL.Path,
            c.Response().Status,
            latency,
        )

        return err
    }
}

func AuthMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
    return func(c echo.Context) error {
        token := c.Request().Header.Get("Authorization")
        if token == "" {
            return echo.NewHTTPError(http.StatusUnauthorized, "missing token")
        }

        claims, err := validateToken(token)
        if err != nil {
            return echo.NewHTTPError(http.StatusUnauthorized, "invalid token")
        }

        c.Set("user_id", claims.UserID)
        return next(c)
    }
}
```

### Step 6: Error Handling

**Gin Custom Error Handler:**

```go
type APIError struct {
    Code    string `json:"code"`
    Message string `json:"message"`
}

func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        if len(c.Errors) > 0 {
            err := c.Errors.Last()

            var apiErr *APIError
            if errors.As(err.Err, &apiErr) {
                c.JSON(http.StatusBadRequest, apiErr)
                return
            }

            c.JSON(http.StatusInternalServerError,
                APIError{Code: "INTERNAL", Message: "Internal error"})
        }
    }
}
```

**Echo Custom Error Handler:**

```go
func CustomHTTPErrorHandler(err error, c echo.Context) {
    code := http.StatusInternalServerError
    message := "Internal server error"

    var he *echo.HTTPError
    if errors.As(err, &he) {
        code = he.Code
        message = he.Message.(string)
    }

    c.JSON(code, map[string]interface{}{
        "error": map[string]interface{}{
            "code":    code,
            "message": message,
        },
    })
}

// Usage
e.HTTPErrorHandler = CustomHTTPErrorHandler
```

---

## Templates

### Complete API Structure

```
internal/
├── handler/
│   ├── handler.go      # Handler container
│   ├── user.go         # User handlers
│   └── product.go      # Product handlers
├── middleware/
│   ├── auth.go
│   ├── logging.go
│   └── cors.go
├── router/
│   └── router.go       # Route setup
└── server/
    └── server.go       # Server configuration
```

**internal/handler/handler.go:**

```go
package handler

type Handler struct {
    userService    *service.UserService
    productService *service.ProductService
}

func New(
    userService *service.UserService,
    productService *service.ProductService,
) *Handler {
    return &Handler{
        userService:    userService,
        productService: productService,
    }
}
```

---

## Examples

### File Upload (Gin)

```go
func uploadFile(c *gin.Context) {
    file, err := c.FormFile("file")
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "file required"})
        return
    }

    // Save file
    dst := filepath.Join("uploads", file.Filename)
    if err := c.SaveUploadedFile(file, dst); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, gin.H{"filename": file.Filename})
}
```

### WebSocket (Echo)

```go
import "github.com/gorilla/websocket"

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool { return true },
}

func websocketHandler(c echo.Context) error {
    ws, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
    if err != nil {
        return err
    }
    defer ws.Close()

    for {
        _, msg, err := ws.ReadMessage()
        if err != nil {
            break
        }
        ws.WriteMessage(websocket.TextMessage, msg)
    }

    return nil
}
```

---

## Common Mistakes

1. **Not validating input** - Always use binding tags
2. **Blocking in handlers** - Use goroutines for long tasks
3. **Not handling panics** - Use recovery middleware
4. **Shared state in handlers** - Use dependency injection
5. **Ignoring context cancellation** - Pass context to services

---

## Checklist

- [ ] Framework chosen (Gin or Echo)
- [ ] Route groups organized
- [ ] Request validation configured
- [ ] Error handling standardized
- [ ] Middleware chain set up
- [ ] Graceful shutdown implemented
- [ ] CORS configured

---

## Next Steps

- M-GO-003: Go Testing
- M-GO-004: Go Error Handling
- M-API-001: REST API Design

---

*Methodology M-GO-002 v1.0*
