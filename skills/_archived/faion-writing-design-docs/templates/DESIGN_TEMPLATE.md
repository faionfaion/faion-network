# Design Template

Шаблон для `design.md` фічі.

---

## Що таке design.md?

Design документ визначає **ЯК** будуємо фічу. Створюється після затвердження spec.md.

**Відмінність від spec:**
- **spec.md** — ЩО і ЧОМУ (бізнес вимоги)
- **design.md** — ЯК (технічна реалізація)

---

## Вимоги до design.md

**Обов'язкові розділи:**

- **Overview** — короткий опис підходу до реалізації
- **Architecture Decisions** — ключові технічні рішення з обґрунтуванням
- **Technical Approach** — компоненти, файли, залежності
- **Testing Strategy** — як будемо тестувати

**Опціональні:**

- **Database Changes** — якщо є міграції
- **Risks** — технічні ризики та мітігації
- **Performance Considerations** — якщо критично
- **Security Considerations** — якщо є нові вектори атак

---

## Шаблон

```markdown
# Design: {Назва фічі}

> Technical design для FEAT-{PROJECT}-{NNN}

## Overview

{2-3 речення: загальний підхід до реалізації}

---

## Architecture Decisions

### AD-1: {Назва рішення}

**Context:** {Яку проблему вирішуємо}

**Options:**
- **A: {Опція}** — {опис, плюси/мінуси}
- **B: {Опція}** — {опис, плюси/мінуси}

**Decision:** {Обране рішення}

**Rationale:** {Чому саме це рішення}

### AD-2: {Назва рішення}
...

---

## Technical Approach

### Components

{Діаграма або опис компонентів}

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   View      │ ──▶ │   Service   │ ──▶ │ Repository  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Data Flow

1. {Крок 1}
2. {Крок 2}
3. {Крок 3}

### Files

```
{path/to/file.py}              # CREATE — {опис}
{path/to/existing.py}          # MODIFY — {що змінюємо}
{path/to/tests/test_file.py}   # CREATE — {тести}
```

### Key Interfaces

```python
# {Назва інтерфейсу}
class {ServiceName}:
    def {method_name}(self, {params}) -> {ReturnType}:
        """
        {Опис методу}
        """
        pass
```

---

## Database Changes

### Migrations

```python
# {NNNN}_{migration_name}.py

class Migration:
    operations = [
        migrations.CreateModel(
            name='{ModelName}',
            fields=[
                ('id', models.BigAutoField(primary_key=True)),
                # ...
            ],
        ),
    ]
```

### Indexes

- `{index_name}` on `{table}({columns})` — {причина}

### Data Migration

{Якщо потрібна міграція даних}

---

## Testing Strategy

### Unit Tests
- `test_{component}_{scenario}` — {що тестуємо}

### Integration Tests
- `test_{flow}_integration` — {що тестуємо}

### Test Data
- {Fixtures або factories що потрібні}

---

## Risks

- **{Risk}** (Impact: High/Medium/Low)
  - Mitigation: {як уникнути}

---

## Performance Considerations

- {Consideration 1}
- {Consideration 2}

---

## Security Considerations

- {Consideration 1}
- {Consideration 2}

---

## Open Items

- [ ] {Що потрібно уточнити під час реалізації}
```

---

## Приклади Architecture Decisions

### Приклад 1: Вибір підходу до кешування

**Context:** Потрібно кешувати результати запитів до API провайдера

**Options:**
- **A: Redis** — швидкий, але додає інфраструктурну залежність
- **B: Django cache framework** — вже є, простіше, але менш гнучкий
- **C: In-memory (локальний dict)** — найпростіше, але не шариться між процесами

**Decision:** B: Django cache framework

**Rationale:** Вже налаштований Redis backend, не потрібно додаткової конфігурації. Для нашого use case достатньо.

### Приклад 2: Структура сервісу

**Context:** Де розмістити бізнес-логіку нової фічі

**Options:**
- **A: Новий сервіс** — ізоляція, але більше файлів
- **B: Розширити існуючий** — менше файлів, але може стати занадто великим

**Decision:** A: Новий сервіс `NotificationService`

**Rationale:** Логіка нотифікацій відрізняється від існуючих сервісів, краще ізолювати для простоти тестування.

---

## Checklist перед tasks

```
□ Всі Architecture Decisions мають rationale
□ Files список повний (CREATE/MODIFY)
□ Testing Strategy покриває основні сценарії
□ Risks ідентифіковані
□ Відповідає constitution проекту
```
