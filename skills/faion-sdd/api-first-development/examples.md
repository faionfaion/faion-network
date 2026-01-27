# OpenAPI Specification Examples

Practical examples for common API patterns using OpenAPI 3.1.

## Basic CRUD API

Complete example of a resource management API.

```yaml
openapi: 3.1.0
info:
  title: Task Management API
  version: 1.0.0
  description: |
    REST API for managing tasks and projects.

    ## Authentication
    All endpoints require Bearer token authentication.

    ## Rate Limiting
    - 100 requests per minute for standard users
    - 1000 requests per minute for premium users

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Local development

security:
  - bearerAuth: []

tags:
  - name: Tasks
    description: Task management operations
  - name: Projects
    description: Project management operations

paths:
  /tasks:
    get:
      operationId: listTasks
      summary: List all tasks
      description: Retrieve a paginated list of tasks with optional filtering.
      tags:
        - Tasks
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
        - name: status
          in: query
          description: Filter by task status
          schema:
            $ref: '#/components/schemas/TaskStatus'
        - name: projectId
          in: query
          description: Filter by project ID
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskList'
              example:
                data:
                  - id: "550e8400-e29b-41d4-a716-446655440000"
                    title: "Implement user authentication"
                    status: "in_progress"
                    priority: "high"
                    createdAt: "2026-01-15T10:30:00Z"
                  - id: "550e8400-e29b-41d4-a716-446655440001"
                    title: "Write API documentation"
                    status: "todo"
                    priority: "medium"
                    createdAt: "2026-01-16T14:00:00Z"
                pagination:
                  page: 1
                  limit: 10
                  total: 42
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

    post:
      operationId: createTask
      summary: Create a new task
      description: Create a new task with the provided details.
      tags:
        - Tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTaskRequest'
            example:
              title: "Implement user authentication"
              description: "Add JWT-based authentication to the API"
              priority: "high"
              projectId: "550e8400-e29b-41d4-a716-446655440099"
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

  /tasks/{taskId}:
    parameters:
      - $ref: '#/components/parameters/TaskIdParam'

    get:
      operationId: getTask
      summary: Get a task by ID
      description: Retrieve detailed information about a specific task.
      tags:
        - Tasks
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'

    put:
      operationId: updateTask
      summary: Update a task
      description: Update all fields of an existing task.
      tags:
        - Tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateTaskRequest'
      responses:
        '200':
          description: Task updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'

    delete:
      operationId: deleteTask
      summary: Delete a task
      description: Permanently delete a task. This action cannot be undone.
      tags:
        - Tasks
      responses:
        '204':
          description: Task deleted successfully
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from /auth/login endpoint

  schemas:
    Task:
      type: object
      required:
        - id
        - title
        - status
        - createdAt
      properties:
        id:
          type: string
          format: uuid
          description: Unique task identifier
        title:
          type: string
          minLength: 1
          maxLength: 200
          description: Task title
        description:
          type: ['string', 'null']
          maxLength: 5000
          description: Detailed task description
        status:
          $ref: '#/components/schemas/TaskStatus'
        priority:
          $ref: '#/components/schemas/Priority'
        projectId:
          type: ['string', 'null']
          format: uuid
          description: Associated project ID
        assigneeId:
          type: ['string', 'null']
          format: uuid
          description: Assigned user ID
        dueDate:
          type: ['string', 'null']
          format: date-time
          description: Task due date
        createdAt:
          type: string
          format: date-time
          description: Creation timestamp
        updatedAt:
          type: ['string', 'null']
          format: date-time
          description: Last update timestamp

    TaskStatus:
      type: string
      enum:
        - todo
        - in_progress
        - review
        - done
        - cancelled
      description: Current task status

    Priority:
      type: string
      enum:
        - low
        - medium
        - high
        - urgent
      default: medium
      description: Task priority level

    CreateTaskRequest:
      type: object
      required:
        - title
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 5000
        priority:
          $ref: '#/components/schemas/Priority'
        projectId:
          type: string
          format: uuid
        assigneeId:
          type: string
          format: uuid
        dueDate:
          type: string
          format: date-time

    UpdateTaskRequest:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: ['string', 'null']
          maxLength: 5000
        status:
          $ref: '#/components/schemas/TaskStatus'
        priority:
          $ref: '#/components/schemas/Priority'
        projectId:
          type: ['string', 'null']
          format: uuid
        assigneeId:
          type: ['string', 'null']
          format: uuid
        dueDate:
          type: ['string', 'null']
          format: date-time

    TaskList:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Task'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      required:
        - page
        - limit
        - total
      properties:
        page:
          type: integer
          minimum: 1
        limit:
          type: integer
          minimum: 1
          maximum: 100
        total:
          type: integer
          minimum: 0

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Error code for programmatic handling
        message:
          type: string
          description: Human-readable error message
        details:
          type: array
          items:
            $ref: '#/components/schemas/ErrorDetail'
          description: Additional error details

    ErrorDetail:
      type: object
      required:
        - field
        - message
      properties:
        field:
          type: string
          description: Field that caused the error
        message:
          type: string
          description: Error message for this field

  parameters:
    PageParam:
      name: page
      in: query
      description: Page number for pagination
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      description: Number of items per page
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    TaskIdParam:
      name: taskId
      in: path
      required: true
      description: Unique task identifier
      schema:
        type: string
        format: uuid

  responses:
    BadRequest:
      description: Invalid request parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "VALIDATION_ERROR"
            message: "Request validation failed"
            details:
              - field: "title"
                message: "Title is required"

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "UNAUTHORIZED"
            message: "Authentication required"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "NOT_FOUND"
            message: "Task not found"

    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "INTERNAL_ERROR"
            message: "An unexpected error occurred"
```

## Authentication API

Example of JWT authentication endpoints.

```yaml
paths:
  /auth/register:
    post:
      operationId: registerUser
      summary: Register a new user
      tags:
        - Authentication
      security: []  # No auth required
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
                - name
              properties:
                email:
                  type: string
                  format: email
                  description: User email address
                password:
                  type: string
                  minLength: 8
                  maxLength: 128
                  description: User password (min 8 characters)
                name:
                  type: string
                  minLength: 1
                  maxLength: 100
                  description: User display name
      responses:
        '201':
          description: User registered successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: Email already registered
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/login:
    post:
      operationId: loginUser
      summary: Authenticate user
      tags:
        - Authentication
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: Authentication successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/refresh:
    post:
      operationId: refreshToken
      summary: Refresh access token
      tags:
        - Authentication
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - refreshToken
              properties:
                refreshToken:
                  type: string
                  description: Valid refresh token
      responses:
        '200':
          description: Token refreshed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          description: Invalid or expired refresh token

components:
  schemas:
    AuthResponse:
      type: object
      required:
        - accessToken
        - refreshToken
        - expiresIn
        - user
      properties:
        accessToken:
          type: string
          description: JWT access token
        refreshToken:
          type: string
          description: JWT refresh token
        expiresIn:
          type: integer
          description: Access token expiry in seconds
        user:
          $ref: '#/components/schemas/User'

    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time
```

## Webhooks (OpenAPI 3.1)

Example of webhook definitions.

```yaml
webhooks:
  taskCompleted:
    post:
      operationId: onTaskCompleted
      summary: Task completed webhook
      description: Triggered when a task is marked as done.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - event
                - timestamp
                - data
              properties:
                event:
                  type: string
                  const: "task.completed"
                timestamp:
                  type: string
                  format: date-time
                data:
                  $ref: '#/components/schemas/Task'
      responses:
        '200':
          description: Webhook received successfully

  taskAssigned:
    post:
      operationId: onTaskAssigned
      summary: Task assigned webhook
      description: Triggered when a task is assigned to a user.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - event
                - timestamp
                - data
              properties:
                event:
                  type: string
                  const: "task.assigned"
                timestamp:
                  type: string
                  format: date-time
                data:
                  type: object
                  required:
                    - task
                    - assignee
                  properties:
                    task:
                      $ref: '#/components/schemas/Task'
                    assignee:
                      $ref: '#/components/schemas/User'
      responses:
        '200':
          description: Webhook received successfully
```

## File Upload Example

```yaml
paths:
  /files:
    post:
      operationId: uploadFile
      summary: Upload a file
      tags:
        - Files
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              required:
                - file
              properties:
                file:
                  type: string
                  format: binary
                  description: File to upload (max 10MB)
                description:
                  type: string
                  maxLength: 500
                  description: Optional file description
      responses:
        '201':
          description: File uploaded successfully
          content:
            application/json:
              schema:
                type: object
                required:
                  - id
                  - url
                  - filename
                  - size
                properties:
                  id:
                    type: string
                    format: uuid
                  url:
                    type: string
                    format: uri
                  filename:
                    type: string
                  size:
                    type: integer
                    description: File size in bytes
                  mimeType:
                    type: string
        '400':
          description: Invalid file
        '413':
          description: File too large
```

## Polymorphic Types (oneOf)

```yaml
components:
  schemas:
    Notification:
      type: object
      required:
        - id
        - type
        - createdAt
        - payload
      properties:
        id:
          type: string
          format: uuid
        type:
          type: string
          enum:
            - task_assigned
            - comment_added
            - mention
        createdAt:
          type: string
          format: date-time
        read:
          type: boolean
          default: false
        payload:
          oneOf:
            - $ref: '#/components/schemas/TaskAssignedPayload'
            - $ref: '#/components/schemas/CommentAddedPayload'
            - $ref: '#/components/schemas/MentionPayload'
          discriminator:
            propertyName: type
            mapping:
              task_assigned: '#/components/schemas/TaskAssignedPayload'
              comment_added: '#/components/schemas/CommentAddedPayload'
              mention: '#/components/schemas/MentionPayload'

    TaskAssignedPayload:
      type: object
      required:
        - type
        - taskId
        - taskTitle
        - assignedBy
      properties:
        type:
          type: string
          const: "task_assigned"
        taskId:
          type: string
          format: uuid
        taskTitle:
          type: string
        assignedBy:
          $ref: '#/components/schemas/UserSummary'

    CommentAddedPayload:
      type: object
      required:
        - type
        - taskId
        - commentId
        - author
      properties:
        type:
          type: string
          const: "comment_added"
        taskId:
          type: string
          format: uuid
        commentId:
          type: string
          format: uuid
        author:
          $ref: '#/components/schemas/UserSummary'
        preview:
          type: string
          maxLength: 100

    MentionPayload:
      type: object
      required:
        - type
        - taskId
        - mentionedBy
      properties:
        type:
          type: string
          const: "mention"
        taskId:
          type: string
          format: uuid
        commentId:
          type: string
          format: uuid
        mentionedBy:
          $ref: '#/components/schemas/UserSummary'

    UserSummary:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        avatarUrl:
          type: ['string', 'null']
          format: uri
```

## Versioned API Example

Showing how to document a v2 API with breaking changes.

```yaml
openapi: 3.1.0
info:
  title: Task API
  version: 2.0.0
  description: |
    ## Breaking Changes in v2

    - `status` field values changed: `in-progress` -> `in_progress`
    - `created_at` renamed to `createdAt` (camelCase)
    - Pagination response structure changed

    ## Migration Guide

    See [Migration Guide](/docs/v2-migration) for details.

servers:
  - url: https://api.example.com/v2
    description: Production (v2)
  - url: https://api.example.com/v1
    description: Production (v1) - Deprecated
    x-deprecated: true
```
