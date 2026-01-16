# Spec Template

Шаблон для `spec.md` фічі.

---

## Вимоги до spec.md

**Обов'язкові розділи** (без них не approve):

- **Problem Statement** — Чому робимо? Без розуміння проблеми неможливо прийняти правильні рішення
- **User Stories** — Хто користувач і що хоче? Визначає scope
- **Functional Requirements** — Що система має робити? Конкретні функції
- **Out of Scope** — Що НЕ робимо? Обмежує scope creep

**Умовно-обов'язкові** (залежить від типу фічі):

- **API Contract** — якщо є нові endpoints
- **Data Model** — якщо є нові моделі або зміни в існуючих
- **UI/UX** — якщо є інтерфейс користувача
- **Integration Points** — якщо інтегруємось із зовнішніми системами

**Опціональні**:

- **Non-Functional Requirements** — специфічні вимоги до performance/security
- **Open Questions** — неясності (мають бути вирішені до approve)
- **Acceptance Criteria** — для складних фіч, як зрозуміти що готово

---

## Checklist перед approve

```
□ Problem Statement зрозумілий без контексту
□ User Stories покривають всіх користувачів
□ Functional Requirements конкретні (не "має працювати швидко")
□ Out of Scope визначений
□ Open Questions вирішені
□ API Contract є (якщо є endpoints)
□ Data Model є (якщо є зміни в БД)
```

---

## Мінімальний шаблон

Для простих фіч:

```markdown
# Feature: {Назва}

## Metadata
- **Status**: draft
- **Priority**: high
- **Created**: {date}

## Problem Statement

{1-3 речення: яку проблему вирішуємо, чому це важливо}

## User Stories

- As a {role}, I want {goal}, so that {benefit}

## Functional Requirements

### FR-1: {Назва}

{Що система має робити}

## Out of Scope

- {Що НЕ входить в цю фічу}
```

---

## Повний шаблон

Для складних фіч:

```markdown
# Feature: {Назва}

## Metadata
- **ID**: FEAT-{PROJECT}-{NNN}
- **Status**: draft | approved | in_progress | done
- **Priority**: critical | high | medium | low
- **Created**: {date}
- **Author**: {author}

## Problem Statement

{Опис проблеми. Чому це важливо? Який біль користувача?}

## User Stories

- As a {role}, I want {goal}, so that {benefit}
- As a {role}, I want {goal}, so that {benefit}

## Functional Requirements

### FR-1: {Назва вимоги}
- **Description**: {Що робить}
- **Trigger**: {Коли спрацьовує}
- **Input**: {Вхідні дані}
- **Output**: {Результат}
- **Business Rules**:
  - {Правило 1}
  - {Правило 2}

### FR-2: {Назва вимоги}
...

## Non-Functional Requirements

- **Performance**: {latency, throughput вимоги}
- **Security**: {auth, validation вимоги}
- **Scalability**: {очікуване навантаження}

## API Contract

### {METHOD} /api/v1/{resource}/

**Request:**
```json
{
  "field": "value"
}
```

**Response (200):**
```json
{
  "id": 1,
  "status": "created"
}
```

**Errors:**
- `400` — Validation error
- `404` — Resource not found
- `409` — Conflict

## Data Model

### New: {ModelName}
- `id` (BigAutoField) — Primary key
- `field_name` (Type) — Description
- `created_at` (DateTime) — Creation timestamp

### Modified: {ExistingModel}
- Add: `new_field` (Type) — Description
- Change: `old_field` — Description of change

## Integration Points

- **{External Service}**: {Для чого використовується}
- **{Internal Service}**: {Як взаємодіємо}

## Out of Scope

- {Функціонал що НЕ входить}
- {Інтеграція що відкладена}
- {UI елементи що будуть в наступній версії}

## Open Questions

- [ ] {Питання що потребує відповіді}
- [ ] {Невизначеність що блокує}

## Acceptance Criteria

- [ ] {Критерій 1 — як перевірити що готово}
- [ ] {Критерій 2}
- [ ] All tests pass
- [ ] Code review approved
```

---

## Поради

**Problem Statement:**
- Пиши від болю користувача, не від рішення
- "Користувачі втрачають гроші бо..." замість "Потрібно додати кнопку"

**User Stories:**
- Конкретні ролі: "касир", "адміністратор", не "користувач"
- Конкретні цілі: "побачити баланс", не "працювати з балансом"

**Functional Requirements:**
- Кожен FR — одна атомарна функція
- Має бути тестований: input → output
- Без технічних деталей реалізації

**Out of Scope:**
- Явно вказуй що відкладено на потім
- Це захист від scope creep
