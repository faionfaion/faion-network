# Living Documentation Templates

Copy-paste templates and configurations for Docs-as-Code implementation.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [GitHub Actions Workflows](#github-actions-workflows)
3. [MkDocs Configuration](#mkdocs-configuration)
4. [Docusaurus Configuration](#docusaurus-configuration)
5. [Vale Configuration](#vale-configuration)
6. [Spectral Configuration](#spectral-configuration)
7. [OpenAPI Template](#openapi-template)
8. [AsyncAPI Template](#asyncapi-template)
9. [ADR Template](#adr-template)
10. [LLM Optimization Files](#llm-optimization-files)

---

## Project Structure

### Recommended Directory Layout

```
project/
├── docs/
│   ├── index.md                    # Documentation home
│   ├── getting-started/
│   │   ├── index.md
│   │   ├── installation.md
│   │   └── quickstart.md
│   ├── guides/
│   │   ├── index.md
│   │   └── ...
│   ├── reference/
│   │   ├── index.md
│   │   ├── api/                    # Generated API docs
│   │   └── cli.md
│   ├── decisions/                  # ADRs
│   │   ├── index.md
│   │   ├── 0001-use-typescript.md
│   │   └── template.md
│   ├── _assets/
│   │   └── images/
│   └── _includes/                  # Reusable snippets
│       └── ...
├── openapi.yaml                    # API specification
├── mkdocs.yml                      # MkDocs config
├── .vale.ini                       # Vale config
├── .markdownlint.json              # Markdown lint config
├── .spectral.yaml                  # API linting rules
├── llms.txt                        # LLM index
└── .github/
    └── workflows/
        └── docs.yml                # Documentation CI
```

---

## GitHub Actions Workflows

### Complete Documentation CI

```yaml
# .github/workflows/docs.yml
name: Documentation CI

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'openapi.yaml'
      - 'mkdocs.yml'
      - '.vale.ini'
  pull_request:
    paths:
      - 'docs/**'
      - 'openapi.yaml'
      - 'mkdocs.yml'
      - '.vale.ini'

jobs:
  lint:
    name: Lint Documentation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint Markdown
        uses: DavidAnson/markdownlint-cli2-action@v16
        with:
          globs: 'docs/**/*.md'

      - name: Lint Prose with Vale
        uses: errata-ai/vale-action@v2
        with:
          files: docs/
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  validate-api:
    name: Validate API Spec
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint OpenAPI with Spectral
        uses: stoplightio/spectral-action@v0.8
        with:
          file_glob: 'openapi.yaml'

  check-links:
    name: Check Links
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check Markdown Links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'
          config-file: '.markdown-link-check.json'

  build:
    name: Build Documentation
    runs-on: ubuntu-latest
    needs: [lint, validate-api]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install mkdocs-material mkdocs-awesome-pages-plugin

      - name: Build docs
        run: mkdocs build --strict

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/

  deploy:
    name: Deploy Documentation
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### PR Preview Deployment

```yaml
# .github/workflows/docs-preview.yml
name: Documentation Preview

on:
  pull_request:
    paths:
      - 'docs/**'
      - 'openapi.yaml'
      - 'mkdocs.yml'

jobs:
  preview:
    name: Deploy Preview
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install mkdocs-material

      - name: Build docs
        run: mkdocs build

      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v3
        with:
          publish-dir: './site'
          production-deploy: false
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy from PR #${{ github.event.number }}"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

---

## MkDocs Configuration

### mkdocs.yml (Material Theme)

```yaml
# mkdocs.yml
site_name: Project Documentation
site_url: https://docs.example.com
site_description: Comprehensive project documentation
site_author: Your Team

repo_name: org/project
repo_url: https://github.com/org/project
edit_uri: edit/main/docs/

theme:
  name: material
  language: en
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.instant.prefetch
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.path
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.code.annotate
    - content.tabs.link
  icon:
    repo: fontawesome/brands/github

plugins:
  - search:
      separator: '[\s\-,:!=\[\]()"/]+|(?!\b)(?=[A-Z][a-z])|\.(?!\d)|&[lg]t;'
  - awesome-pages
  - tags

markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/org/project
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/org
  version:
    provider: mike
  analytics:
    provider: google
    property: G-XXXXXXXXXX

nav:
  - Home: index.md
  - Getting Started:
    - getting-started/index.md
    - Installation: getting-started/installation.md
    - Quickstart: getting-started/quickstart.md
  - Guides:
    - guides/index.md
  - Reference:
    - reference/index.md
    - API: reference/api/
    - CLI: reference/cli.md
  - Decisions: decisions/
```

---

## Docusaurus Configuration

### docusaurus.config.js

```javascript
// docusaurus.config.js
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Project Documentation',
  tagline: 'Comprehensive project documentation',
  favicon: 'img/favicon.ico',
  url: 'https://docs.example.com',
  baseUrl: '/',

  organizationName: 'org',
  projectName: 'project',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/org/project/edit/main/',
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Project',
        logo: {
          alt: 'Project Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docs',
            position: 'left',
            label: 'Documentation',
          },
          {
            href: 'https://github.com/org/project',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        copyright: `Copyright ${new Date().getFullYear()} Org. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['bash', 'json', 'yaml', 'python', 'typescript'],
      },
      algolia: {
        appId: 'YOUR_APP_ID',
        apiKey: 'YOUR_SEARCH_API_KEY',
        indexName: 'project',
        contextualSearch: true,
      },
    }),

  plugins: [
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'api',
        docsPluginId: 'classic',
        config: {
          api: {
            specPath: 'openapi.yaml',
            outputDir: 'docs/reference/api',
            sidebarOptions: {
              groupPathsBy: 'tag',
            },
          },
        },
      },
    ],
  ],

  themes: ['docusaurus-theme-openapi-docs'],
};

export default config;
```

---

## Vale Configuration

### .vale.ini

```ini
# .vale.ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

Vocab = Project

# File types to check
[*.md]
BasedOnStyles = Vale, Microsoft, Project

# Ignore code blocks
BlockIgnores = (?s) *(`{3}.*?`{3}|`[^`]*`)

# Ignore frontmatter
TokenIgnores = (?s)^---.*?---

[*.rst]
BasedOnStyles = Vale, Microsoft, Project

# Skip certain files
[docs/_build/**]
BasedOnStyles =

[CHANGELOG.md]
BasedOnStyles =
```

### Custom Vale Rules

Create `.vale/styles/Project/` folder:

```yaml
# .vale/styles/Project/Terminology.yml
extends: substitution
message: "Use '%s' instead of '%s'."
level: error
ignorecase: true
swap:
  backend: back-end
  frontend: front-end
  repo: repository
  config: configuration
  docs: documentation
```

```yaml
# .vale/styles/Project/Headings.yml
extends: capitalization
message: "Use sentence case for headings."
level: warning
match: $title
style: sentence
```

```yaml
# .vale/styles/Project/ProductNames.yml
extends: existence
message: "Always capitalize '%s' correctly."
level: error
raw:
  - GitHub
  - JavaScript
  - TypeScript
  - Python
  - Docker
  - Kubernetes
```

### Vocabulary File

```txt
# .vale/styles/Vocab/Project/accept.txt
API
CLI
JSON
YAML
REST
GraphQL
OAuth
JWT
SDK
UI
UX
```

---

## Spectral Configuration

### .spectral.yaml

```yaml
# .spectral.yaml
extends:
  - spectral:oas
  - spectral:asyncapi

rules:
  # Require description for operations
  operation-description: error

  # Require examples
  oas3-valid-media-example: error

  # Consistent naming
  operation-operationId-valid-in-url: error

  # Security
  operation-security-defined: error

  # Response codes
  operation-success-response: error

  # Custom rules
  path-params-camelCase:
    description: Path parameters must be camelCase
    given: "$..parameters[?(@.in == 'path')]"
    severity: error
    then:
      field: name
      function: casing
      functionOptions:
        type: camel

  request-body-required:
    description: POST/PUT/PATCH should have request body
    given: "$.paths.*.post,$.paths.*.put,$.paths.*.patch"
    severity: warn
    then:
      field: requestBody
      function: truthy

  response-has-content:
    description: 2xx responses should have content
    given: "$.paths.*.*.responses[?(@property.match(/^2/))]"
    severity: warn
    then:
      field: content
      function: truthy
```

---

## OpenAPI Template

### openapi.yaml

```yaml
# openapi.yaml
openapi: 3.1.0

info:
  title: Project API
  version: 1.0.0
  description: |
    Project API documentation.

    ## Authentication

    All endpoints require Bearer token authentication.

    ## Rate Limiting

    - 1000 requests per minute per API key
    - 429 response when limit exceeded
  contact:
    name: API Support
    email: api@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging
  - url: http://localhost:8000/v1
    description: Local development

tags:
  - name: Users
    description: User management operations
  - name: Items
    description: Item CRUD operations

security:
  - bearerAuth: []

paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      description: Returns a paginated list of users.
      tags:
        - Users
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
              example:
                data:
                  - id: "123"
                    email: user@example.com
                    name: John Doe
                page: 1
                limit: 20
                total: 100
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      operationId: createUser
      summary: Create a user
      description: Creates a new user account.
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
            example:
              email: user@example.com
              name: John Doe
              password: securepassword123
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /users/{userId}:
    get:
      operationId: getUser
      summary: Get a user
      description: Returns a single user by ID.
      tags:
        - Users
      parameters:
        - $ref: '#/components/parameters/UserIdParam'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token from /auth/login endpoint

  parameters:
    PageParam:
      name: page
      in: query
      description: Page number
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      description: Items per page
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    UserIdParam:
      name: userId
      in: path
      required: true
      description: User ID
      schema:
        type: string
        format: uuid

  schemas:
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
          description: Unique identifier
        email:
          type: string
          format: email
          description: Email address
        name:
          type: string
          description: Full name
        createdAt:
          type: string
          format: date-time
          description: Creation timestamp

    CreateUser:
      type: object
      required:
        - email
        - name
        - password
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        password:
          type: string
          format: password
          minLength: 8

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object
          additionalProperties: true

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: BAD_REQUEST
            message: Invalid input data

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Authentication required

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: Resource not found
```

---

## AsyncAPI Template

### asyncapi.yaml

```yaml
# asyncapi.yaml
asyncapi: 3.0.0

info:
  title: Project Events API
  version: 1.0.0
  description: |
    Asynchronous events published by the Project service.

    ## Connection

    Connect via WebSocket or subscribe to the message broker.

servers:
  production:
    host: events.example.com:443
    protocol: wss
    description: Production WebSocket server

  development:
    host: localhost:8080
    protocol: ws
    description: Local development

channels:
  user/created:
    address: user/created
    messages:
      UserCreated:
        $ref: '#/components/messages/UserCreated'
    description: Published when a new user is created

  user/updated:
    address: user/updated
    messages:
      UserUpdated:
        $ref: '#/components/messages/UserUpdated'
    description: Published when user data is updated

operations:
  publishUserCreated:
    action: send
    channel:
      $ref: '#/channels/user~1created'
    summary: Publish user created event
    messages:
      - $ref: '#/channels/user~1created/messages/UserCreated'

  publishUserUpdated:
    action: send
    channel:
      $ref: '#/channels/user~1updated'
    summary: Publish user updated event
    messages:
      - $ref: '#/channels/user~1updated/messages/UserUpdated'

components:
  messages:
    UserCreated:
      name: UserCreated
      title: User Created Event
      contentType: application/json
      payload:
        $ref: '#/components/schemas/UserCreatedPayload'

    UserUpdated:
      name: UserUpdated
      title: User Updated Event
      contentType: application/json
      payload:
        $ref: '#/components/schemas/UserUpdatedPayload'

  schemas:
    UserCreatedPayload:
      type: object
      required:
        - eventId
        - timestamp
        - data
      properties:
        eventId:
          type: string
          format: uuid
        timestamp:
          type: string
          format: date-time
        data:
          type: object
          required:
            - userId
            - email
          properties:
            userId:
              type: string
              format: uuid
            email:
              type: string
              format: email

    UserUpdatedPayload:
      type: object
      required:
        - eventId
        - timestamp
        - data
      properties:
        eventId:
          type: string
          format: uuid
        timestamp:
          type: string
          format: date-time
        data:
          type: object
          required:
            - userId
            - changes
          properties:
            userId:
              type: string
              format: uuid
            changes:
              type: object
              additionalProperties: true
```

---

## ADR Template

### docs/decisions/template.md

```markdown
# ADR-NNNN: Title

## Status

Proposed | Accepted | Deprecated | Superseded by [ADR-XXXX](XXXX-title.md)

## Date

YYYY-MM-DD

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

What becomes easier or more difficult to do because of this change?

### Positive

- Benefit 1
- Benefit 2

### Negative

- Drawback 1
- Drawback 2

### Neutral

- Other impact 1

## Alternatives Considered

### Alternative 1

Description and why it was rejected.

### Alternative 2

Description and why it was rejected.

## References

- [Link to relevant documentation]()
- [Link to discussion]()
```

---

## LLM Optimization Files

### llms.txt

```txt
# Project Documentation

> Project is a tool for doing X. This file provides an index of documentation for LLM consumption.

## Overview

- [Getting Started](docs/getting-started/index.md): Installation and quickstart guide
- [API Reference](docs/reference/api/index.md): Complete API documentation
- [Guides](docs/guides/index.md): How-to guides for common tasks

## Full Documentation

For complete documentation, see [llms-full.txt](llms-full.txt).

## Key Concepts

- **Concept 1**: Brief explanation
- **Concept 2**: Brief explanation
- **Concept 3**: Brief explanation

## Quick Example

```python
from project import Client

client = Client(api_key="your-key")
result = client.do_something()
print(result)
```

## Links

- Documentation: https://docs.example.com
- GitHub: https://github.com/org/project
- API: https://api.example.com
```

### llms-full.txt Generator Script

```python
#!/usr/bin/env python3
"""Generate llms-full.txt from documentation."""

import os
from pathlib import Path

DOCS_DIR = Path("docs")
OUTPUT_FILE = Path("llms-full.txt")
EXCLUDED = {"_build", "_assets", "node_modules"}

def collect_docs():
    """Collect all markdown files."""
    docs = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        if any(part in path.parts for part in EXCLUDED):
            continue
        docs.append(path)
    return docs

def generate_llms_full():
    """Generate the llms-full.txt file."""
    docs = collect_docs()

    with open(OUTPUT_FILE, "w") as f:
        f.write("# Project - Full Documentation\n\n")
        f.write("This file contains all project documentation for LLM consumption.\n\n")
        f.write("---\n\n")

        for doc in docs:
            relative_path = doc.relative_to(DOCS_DIR)
            f.write(f"## {relative_path}\n\n")
            f.write(doc.read_text())
            f.write("\n\n---\n\n")

    print(f"Generated {OUTPUT_FILE} with {len(docs)} documents")

if __name__ == "__main__":
    generate_llms_full()
```

---

## Markdown Link Check Configuration

### .markdown-link-check.json

```json
{
  "ignorePatterns": [
    {
      "pattern": "^http://localhost"
    },
    {
      "pattern": "^http://127.0.0.1"
    }
  ],
  "replacementPatterns": [
    {
      "pattern": "^/docs",
      "replacement": "{{BASEURL}}/docs"
    }
  ],
  "httpHeaders": [
    {
      "urls": ["https://github.com"],
      "headers": {
        "Accept-Encoding": "zstd, br, gzip, deflate"
      }
    }
  ],
  "timeout": "10s",
  "retryOn429": true,
  "retryCount": 3,
  "fallbackRetryDelay": "30s",
  "aliveStatusCodes": [200, 206]
}
```

---

## Pre-commit Configuration

### .pre-commit-config.yaml

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json

  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.39.0
    hooks:
      - id: markdownlint
        args: ["--fix"]

  - repo: https://github.com/errata-ai/vale
    rev: v3.4.2
    hooks:
      - id: vale
        args: ["--config=.vale.ini"]
        files: \.(md|rst)$

  - repo: https://github.com/stoplightio/spectral
    rev: v6.11.1
    hooks:
      - id: spectral
        args: ["lint", "openapi.yaml"]
        files: openapi\.yaml$
```

---

*Copy these templates and customize for your project.*
