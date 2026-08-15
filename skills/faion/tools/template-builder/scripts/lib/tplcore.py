"""tplcore — the parsing, resolution and rendering shared by tpl-build and tpl-params.

Not a tool: a pack helper. `faion tools sync` materialises nested
`scripts/<sub>/*.py` alongside the pack, so both scripts load this file by
absolute path (importlib) rather than by module name — a bare import would
depend on sys.path[0] and would also read to the tool validator as a
non-stdlib dependency.

Everything here implements exactly two contracts and refuses the rest:

  * retrieval-content-contracts.md 2.2 — the `variables:` key: name, type,
    required, default, sensitive, placeholder, options, description.
  * retrieval-content-contracts.md 2.3 — `sections:` with
    `when: <var> in [<literal>, ...]` and nothing else.

The refusals are the point. A general template language on an assembler that
runs on behalf of other accounts is a server-side template injection surface,
so every construct outside the two contracts above raises TplError naming the
construct instead of being interpreted.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

# ---------------------------------------------------------------- errors

STORE_REL = Path(".faion") / "template-params.json"
STORE_VERSION = 1


class TplError(Exception):
    """A refusal. The message names what was refused and why."""


class ValueRefused(TplError):
    """A supplied value was refused: sensitive, secret-shaped or ill-typed."""


class Unresolved(TplError):
    """Required parameters have no value. `.names` holds them, in order."""

    def __init__(self, names: list[str]) -> None:
        super().__init__("unresolved required parameters: " + ", ".join(names))
        self.names = names


# ------------------------------------------------------- header splitting

HEADER_KEYS = ("purpose", "consumes", "produces", "depends-on",
               "token-budget-impact", "variables", "sections")
_HEADER_KEY_LINE = re.compile(
    r"^\s*(purpose|consumes|produces|depends-on|token-budget-impact"
    r"|variables|sections)\s*:", re.MULTILINE)


def split_header(text: str) -> tuple[str, str]:
    """Split a template into (header text, body text).

    A leading `<!-- ... -->`, `/* ... */` or run of `#` / `//` line comments is
    the header only when it actually carries one of the six declared keys —
    otherwise a Markdown `# Heading` would be eaten as a comment header.
    Returns ("", text) when the template is static.
    """
    if "\x00" in text:
        raise TplError("template contains a NUL byte")
    body = text.lstrip("\n")
    if body.lstrip().startswith("{"):
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict) and "__faion_header__" in parsed:
            raise TplError(
                "JSON template with a __faion_header__ object: refused. This "
                "builder emits Markdown and HTML only (design 6); a JSON "
                "artefact is a different producer, not a flag on this one")
    for opener, closer, width in (("<!--", "-->", 4), ("/*", "*/", 2)):
        if not body.startswith(opener):
            continue
        end = body.find(closer)
        if end < 0:
            raise TplError(f"header opens with {opener} and never closes")
        head = body[width:end]
        if not _HEADER_KEY_LINE.search(head):
            return "", body
        return head, body[end + len(closer):]

    lines = body.split("\n")
    taken: list[str] = []
    for line in lines:
        if line.startswith("#"):
            taken.append(line.lstrip("#"))
        elif line.startswith("//"):
            taken.append(line[2:])
        else:
            break
    head = "\n".join(taken)
    if taken and _HEADER_KEY_LINE.search(head):
        return head, "\n".join(lines[len(taken):])
    return "", body


# ----------------------------------------------------- the YAML-ish subset

_TOP = re.compile(r"^([a-z][a-z0-9_-]*):\s?(.*)$")
_ITEM = re.compile(r"^ {2}- ([a-z][a-z0-9_-]*):\s?(.*)$")
_ITEM_CONT = re.compile(r"^ {4}([a-z][a-z0-9_-]*):\s?(.*)$")
_INT = re.compile(r"^-?\d+$")


def _scalar(raw: str, where: str):
    """One scalar. The unsupported YAML constructs are named, not guessed at."""
    raw = raw.strip()
    if raw.startswith(("|", ">")):
        raise TplError(f"{where}: block scalars (| and >) are not supported")
    if raw.startswith(("&", "*")):
        raise TplError(f"{where}: YAML anchors and aliases are not supported")
    if raw.startswith("!"):
        raise TplError(f"{where}: YAML tags are not supported")
    if raw.startswith("{"):
        raise TplError(f"{where}: flow mappings are not supported")
    if raw.startswith("["):
        if not raw.endswith("]"):
            raise TplError(f"{where}: unterminated flow list")
        inner = raw[1:-1]
        if "[" in inner or "]" in inner:
            raise TplError(f"{where}: nested flow lists are not supported")
        items = [i.strip() for i in inner.split(",") if i.strip()]
        return [_unquote(i) for i in items]
    if raw in ("true", "false"):
        return raw == "true"
    if _INT.fullmatch(raw):
        return int(raw)
    return _unquote(raw)


def _unquote(raw: str) -> str:
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    return raw


def parse_header(head: str) -> dict:
    """The header as a dict. Top-level scalars plus lists of flat mappings.

    Deliberately not a YAML parser: documents, multi-line scalars, nesting
    past one list of mappings, and duplicate keys are each refused by name.
    """
    out: dict = {}
    key: str | None = None
    item: dict | None = None
    for lineno, raw in enumerate(head.split("\n"), 1):
        if "\t" in raw:
            raise TplError(f"header line {lineno}: tab indentation")
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.strip() in ("---", "..."):
            raise TplError(f"header line {lineno}: YAML document markers are "
                           "not supported")
        top = _TOP.match(line)
        if top:
            name, value = top.group(1), top.group(2)
            if name in out:
                raise TplError(f"header line {lineno}: duplicate key {name!r}")
            key, item = name, None
            if value.strip() == "":
                out[name] = []
            else:
                out[name] = _scalar(value, f"header line {lineno}")
            continue
        entry = _ITEM.match(line)
        if entry:
            if key is None or not isinstance(out.get(key), list):
                raise TplError(f"header line {lineno}: list item outside a list key")
            item = {entry.group(1): _scalar(entry.group(2),
                                            f"header line {lineno}")}
            out[key].append(item)
            continue
        cont = _ITEM_CONT.match(line)
        if cont:
            if item is None:
                raise TplError(f"header line {lineno}: continuation before any "
                               "list item")
            if cont.group(1) in item:
                raise TplError(f"header line {lineno}: duplicate field "
                               f"{cont.group(1)!r} in one list item")
            item[cont.group(1)] = _scalar(cont.group(2),
                                          f"header line {lineno}")
            continue
        raise TplError(f"header line {lineno}: not a supported construct: "
                       f"{line.strip()[:60]!r}")
    return out


# ------------------------------------------------------- the declarations

VAR_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
VAR_TYPES = ("string", "integer", "boolean", "enum", "path", "text")
VAR_FIELDS = ("name", "type", "required", "default", "sensitive",
              "placeholder", "options", "description")
SEC_FIELDS = ("name", "description", "when")
DESC_MAX = 240

# Anything a richer template language would put in a condition. Each is named
# so the author reads a refusal, not a mis-evaluation.
_BAD_OPS = (
    (" not in ", "`not in`"), ("==", "`==`"), ("!=", "`!=`"), (">=", "`>=`"),
    ("<=", "`<=`"), (" and ", "`and`"), (" or ", "`or`"), (" not ", "`not`"),
    ("&&", "`&&`"), ("||", "`||`"), ("(", "a call or grouping"),
    ("|", "a filter"), ("~", "concatenation"), (" is ", "`is`"),
)
_WHEN = re.compile(r"^([a-z][a-z0-9_]{0,63})\s+in\s+\[([^\[\]]*)\]$")


def parse_when(expr: str, where: str) -> tuple[str, list[str]]:
    """`<var> in [<literal>, ...]` and nothing else."""
    text = expr.strip()
    for token, label in _BAD_OPS:
        if token in text:
            raise TplError(
                f"{where}: when clause uses {label}, which is not supported. "
                "The grammar is `<var> in [<literal>, ...]` and nothing else "
                "(2.3): branching a single `in` cannot express is two blocks")
    match = _WHEN.match(text)
    if not match:
        raise TplError(f"{where}: when clause {text!r} is not "
                       "`<var> in [<literal>, ...]`")
    literals = [_unquote(part.strip()) for part in match.group(2).split(",")
                if part.strip()]
    if not literals:
        raise TplError(f"{where}: when clause has an empty literal list")
    return match.group(1), literals


def parse_variables(header: dict, where: str) -> dict[str, dict]:
    """The `variables:` key, validated against 2.2. Order preserved."""
    raw = header.get("variables", [])
    if not isinstance(raw, list):
        raise TplError(f"{where}: `variables:` must be a list of mappings")
    out: dict[str, dict] = {}
    for index, decl in enumerate(raw, 1):
        at = f"{where}: variables[{index}]"
        if not isinstance(decl, dict):
            raise TplError(f"{at}: not a mapping")
        for field in decl:
            if field not in VAR_FIELDS:
                raise TplError(f"{at}: unknown field {field!r}; 2.2 declares "
                               + ", ".join(VAR_FIELDS))
        name = decl.get("name")
        if not isinstance(name, str) or not VAR_NAME.match(name):
            raise TplError(f"{at}: name {name!r} must match "
                           "^[a-z][a-z0-9_]{0,63}$")
        at = f"{where}: variable {name!r}"
        if name in out:
            raise TplError(f"{at}: declared twice")
        vtype = decl.get("type")
        if vtype not in VAR_TYPES:
            raise TplError(f"{at}: type {vtype!r} is not one of "
                           + ", ".join(VAR_TYPES))
        if not isinstance(decl.get("required"), bool):
            raise TplError(f"{at}: `required` is mandatory and boolean")
        desc = decl.get("description")
        if not isinstance(desc, str) or not desc.strip():
            raise TplError(f"{at}: `description` is mandatory — it is the "
                           "question a human is asked")
        if len(desc) > DESC_MAX:
            raise TplError(f"{at}: description is {len(desc)} chars, over the "
                           f"{DESC_MAX} cap")
        sensitive = decl.get("sensitive", False)
        if not isinstance(sensitive, bool):
            raise TplError(f"{at}: `sensitive` must be boolean")
        if sensitive and not str(decl.get("placeholder") or "").strip():
            raise TplError(f"{at}: sensitive: true requires `placeholder`")
        options = decl.get("options")
        if vtype == "enum":
            if not isinstance(options, list) or not options:
                raise TplError(f"{at}: type enum requires a non-empty "
                               "`options` list")
        elif options is not None:
            raise TplError(f"{at}: `options` is only meaningful on type enum")
        default = decl.get("default")
        if default is not None and not isinstance(default, (str, int, bool)):
            raise TplError(f"{at}: `default` must be a scalar")
        out[name] = {
            "name": name,
            "type": vtype,
            "required": bool(decl["required"]),
            "default": None if default is None else _as_text(default),
            "sensitive": sensitive,
            "placeholder": decl.get("placeholder"),
            "options": [_as_text(o) for o in options] if options else None,
            "description": desc,
        }
    return out


def parse_sections(header: dict, variables: dict[str, dict],
                   where: str) -> list[dict]:
    """The `sections:` key, validated against 2.3."""
    raw = header.get("sections", [])
    if not isinstance(raw, list):
        raise TplError(f"{where}: `sections:` must be a list of mappings")
    out: list[dict] = []
    seen: set[str] = set()
    for index, decl in enumerate(raw, 1):
        at = f"{where}: sections[{index}]"
        if not isinstance(decl, dict):
            raise TplError(f"{at}: not a mapping")
        for field in decl:
            if field not in SEC_FIELDS:
                raise TplError(f"{at}: unknown field {field!r}; 2.3 declares "
                               + ", ".join(SEC_FIELDS))
        name = decl.get("name")
        if not isinstance(name, str) or not VAR_NAME.match(name):
            raise TplError(f"{at}: name {name!r} must match "
                           "^[a-z][a-z0-9_]{0,63}$")
        if name in seen:
            raise TplError(f"{at}: section {name!r} declared twice")
        seen.add(name)
        when = decl.get("when")
        var, literals = (None, [])
        if when is not None:
            var, literals = parse_when(_as_text(when), f"{where}: section {name!r}")
            if var not in variables:
                raise TplError(f"{where}: section {name!r} tests undeclared "
                               f"variable {var!r}")
        out.append({"name": name, "description": decl.get("description"),
                    "var": var, "literals": literals})
    return out


def _as_text(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        raise TplError("a list is not a scalar value")
    return str(value)


# ------------------------------------------------------------- secret shapes

SECRET_PATTERNS = (
    ("a Stripe live key", re.compile(r"sk_live_[A-Za-z0-9]{8,}")),
    ("a Stripe test key", re.compile(r"sk_test_[A-Za-z0-9]{8,}")),
    ("a GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{16,}")),
    ("a GitHub fine-grained PAT", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("an AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("a Slack token", re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("a Google API key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("an OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9]{32,}")),
    ("a PEM private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("a JWT", re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.")),
)
# A separator-free run long enough to be a key. `/` and `.` are excluded so a
# path or a dotted identifier is not mistaken for base64.
_RUN = re.compile(r"[A-Za-z0-9+_=-]{32,}")
_HEX = re.compile(r"^[0-9a-fA-F]+$")


def _entropy(text: str) -> float:
    counts: dict[str, int] = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    total = len(text)
    return -sum((n / total) * math.log2(n / total) for n in counts.values())


def secret_shape(value: str) -> str | None:
    """Name the secret this value looks like, or None.

    Runs regardless of any `sensitive:` declaration — 2.2 asks for two
    independent checks, and a check that trusts the corpus is one check.
    """
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(value):
            return label
    for run in _RUN.findall(value):
        if _HEX.match(run) and len(run) >= 32 and _entropy(run) >= 3.0:
            return "a long hex secret"
        mixed = (any(c.isdigit() for c in run) and any(c.isupper() for c in run)
                 and any(c.islower() for c in run))
        if mixed and len(run) >= 32 and _entropy(run) >= 4.0:
            return "a long high-entropy string"
    return None


# ------------------------------------------------------------ the store

def store_path(project: Path) -> Path:
    return Path(project) / STORE_REL


def load_store(project: Path) -> dict:
    """The project parameter store, or an empty one."""
    path = store_path(project)
    if not path.is_file():
        return {"version": STORE_VERSION, "params": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TplError(f"{path}: not readable as JSON: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("params"), dict):
        raise TplError(f"{path}: not a parameter store "
                       "({'version': 1, 'params': {...}})")
    return data


def store_value(store: dict, name: str) -> str | None:
    entry = store.get("params", {}).get(name)
    if isinstance(entry, dict) and isinstance(entry.get("value"), str):
        return entry["value"]
    return None


def store_put(store: dict, decl: dict, value: str) -> str:
    """Record a parameter. Returns what was actually recorded, as a phrase.

    A sensitive parameter records its existence and its placeholder and never
    its value (2.2: the value never travels). A value that merely LOOKS like a
    secret is refused outright, whatever the declaration says.
    """
    name = decl["name"]
    shape = secret_shape(value)
    if shape:
        raise ValueRefused(
            f"{name}: the supplied value looks like {shape} and is refused "
            "regardless of its declaration — a secret is substituted locally, "
            "never assembled in")
    params = store.setdefault("params", {})
    if decl.get("sensitive"):
        params[name] = {"sensitive": True, "placeholder": decl["placeholder"]}
        return "placeholder only (sensitive)"
    params[name] = {"value": value}
    return "value"


def sync_declarations(store: dict, variables: dict[str, dict]) -> None:
    """Record that each sensitive parameter exists, and its placeholder.

    That is the whole of what a sensitive parameter is allowed to leave behind,
    and it also scrubs a value someone hand-edited into the store under a
    sensitive name.
    """
    params = store.setdefault("params", {})
    for name, decl in variables.items():
        if decl["sensitive"]:
            params[name] = {"sensitive": True,
                            "placeholder": decl["placeholder"]}


def remember(store: dict, variables: dict[str, dict], values: dict[str, str],
             origins: dict[str, str]) -> list[str]:
    """Persist the answers a run was GIVEN, and only those. Mutates `store`.

    Three exclusions, each for its own reason:

      * `store` — already there, so writing it back is a no-op that only risks
        reformatting the file.
      * `default` — persisting a declared default silently freezes it. A later
        change to the block's default would stop taking effect and there would
        be nothing in the project to explain why.
      * `placeholder` — a sensitive parameter. The value never travels, and the
        store gets its existence and its placeholder from sync_declarations.

    Writing goes through store_put, the same call tpl-params uses, so the
    secret-shape refusal cannot drift between the two tools.
    """
    written: list[str] = []
    for name, origin in origins.items():
        if origin != "explicit" or name not in variables:
            continue
        decl = variables[name]
        if decl["sensitive"]:
            continue
        store_put(store, decl, values[name])
        written.append(name)
    sync_declarations(store, variables)
    return sorted(written)


def save_store(project: Path, store: dict) -> Path:
    path = store_path(project)
    for name, entry in store.get("params", {}).items():
        if entry.get("sensitive") and "value" in entry:
            raise TplError(f"refusing to write store: {name!r} is sensitive "
                           "and carries a value")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


# --------------------------------------------------------- value checking

def check_type(decl: dict, value: str) -> None:
    name, vtype = decl["name"], decl["type"]
    if vtype == "integer" and not _INT.fullmatch(value.strip()):
        raise ValueRefused(f"{name}: type integer, got {value!r}")
    if vtype == "boolean" and value.strip() not in ("true", "false"):
        raise ValueRefused(f"{name}: type boolean, got {value!r} "
                           "(expected true or false)")
    if vtype == "enum" and value not in (decl["options"] or []):
        raise ValueRefused(f"{name}: type enum, got {value!r}; options are "
                           + ", ".join(decl["options"] or []))
    if vtype == "path" and not value.strip():
        raise ValueRefused(f"{name}: type path, got an empty value")


def accept_value(decl: dict, value: str) -> None:
    """Gate a value on its way in. Both checks, neither trusting the other."""
    if decl.get("sensitive"):
        raise ValueRefused(
            f"{decl['name']}: declared sensitive, so a value is never accepted "
            f"here — the build emits {decl['placeholder']!r} and you substitute "
            "the real value locally afterwards (2.2)")
    shape = secret_shape(value)
    if shape:
        raise ValueRefused(f"{decl['name']}: the supplied value looks like "
                           f"{shape}; a secret is never assembled in")
    check_type(decl, value)


# ------------------------------------------------------------- the body

SECTION_OPEN = re.compile(r"^[ \t]*<!--\s*faion:section\s+([a-z][a-z0-9_]{0,63})\s*-->[ \t]*$")
SECTION_CLOSE = re.compile(r"^[ \t]*<!--\s*faion:endsection\s*-->[ \t]*$")
MUSTACHE = re.compile(r"\{\{(.*?)\}\}", re.DOTALL)
_PLAIN_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


def scan_placeholders(body: str, where: str) -> set[str]:
    """Every `{{name}}` in the body. Any other construct is refused by name."""
    if "{%" in body:
        raise TplError(f"{where}: body carries a `{{%` statement tag. "
                       "Substitution is `{{name}}` only (2.3): no expressions, "
                       "loops, filters or nested partials")
    names: set[str] = set()
    for raw in MUSTACHE.findall(body):
        inner = raw.strip()
        if inner.startswith(("#", "/", "^", ">", "!", "&", "{")):
            raise TplError(f"{where}: `{{{{{inner[:24]}}}}}` is a Mustache "
                           "section, partial or raw-output tag. Substitution "
                           "is `{{name}}` only (2.3)")
        if "|" in inner:
            raise TplError(f"{where}: `{{{{{inner[:24]}}}}}` applies a filter. "
                           "Substitution is `{{name}}` only (2.3)")
        if not _PLAIN_NAME.match(inner):
            raise TplError(f"{where}: `{{{{{inner[:24]}}}}}` is not a bare "
                           "variable name matching ^[a-z][a-z0-9_]{0,63}$")
        names.add(inner)
    return names


def prune_sections(body: str, sections: list[dict], values: dict[str, str],
                   where: str) -> str:
    """Drop the marked sections whose `when` does not hold. No nesting."""
    declared = {s["name"]: s for s in sections}
    keep_stack: list[tuple[str, bool]] = []
    seen: set[str] = set()
    out: list[str] = []
    for lineno, line in enumerate(body.split("\n"), 1):
        opened = SECTION_OPEN.match(line)
        if opened:
            name = opened.group(1)
            if keep_stack:
                raise TplError(f"{where} line {lineno}: section {name!r} opens "
                               f"inside section {keep_stack[-1][0]!r}; nesting "
                               "is not supported (2.3)")
            if name not in declared:
                raise TplError(f"{where} line {lineno}: section marker {name!r} "
                               "is not declared under `sections:`")
            seen.add(name)
            section = declared[name]
            keep = True
            if section["var"] is not None:
                keep = values.get(section["var"], "") in section["literals"]
            keep_stack.append((name, keep))
            continue
        if SECTION_CLOSE.match(line):
            if not keep_stack:
                raise TplError(f"{where} line {lineno}: faion:endsection with "
                               "no open section")
            keep_stack.pop()
            continue
        if not keep_stack or keep_stack[-1][1]:
            out.append(line)
    if keep_stack:
        raise TplError(f"{where}: section {keep_stack[-1][0]!r} is never closed")
    for name in declared:
        if name not in seen:
            raise TplError(f"{where}: section {name!r} is declared and has no "
                           f"`<!-- faion:section {name} -->` marker in the body")
    return "\n".join(out)


VALUE_MARK = "\x01"
_MARK = re.compile("\x01(\\d+)\x01")


def _clean(value: str) -> str:
    """A value can never carry the renderer's own sentinels."""
    return str(value).replace("\x00", "").replace("\x01", "")


def substitute(body: str, values: dict[str, str]) -> str:
    """`{{name}}` -> value. Nothing recursive: a value is never re-scanned."""
    def swap(match: re.Match) -> str:
        return _clean(values.get(match.group(1).strip(), ""))
    return MUSTACHE.sub(swap, body)


def substitute_marked(body: str, values: dict[str, str]
                      ) -> tuple[str, list[str]]:
    """`{{name}}` -> an opaque sentinel, plus the values in sentinel order.

    This is what the HTML path uses. Source text and substituted values are two
    different trust levels, so they must not share one escaping pass: the
    renderer escapes source text entity-preservingly (a corpus template that
    already writes `&lt;artefact_id&gt;` must not become `&amp;lt;`), while a
    value is escaped unconditionally at the very end. Holding values as
    sentinels through the render is what keeps the two apart — and it also
    means a value can never open a heading, close a code fence or break out of
    a table cell, because by the time it exists the structure is already fixed.
    """
    marks: list[str] = []

    def swap(match: re.Match) -> str:
        marks.append(_clean(values.get(match.group(1).strip(), "")))
        return f"\x01{len(marks) - 1}\x01"
    return MUSTACHE.sub(swap, body), marks


# ------------------------------------------------------------- resolution

def resolve(variables: dict[str, dict], explicit: dict[str, str],
            store: dict, scope: set[str] | None = None
            ) -> tuple[dict[str, str], list[dict], dict[str, str]]:
    """Design 4: explicit -> store -> default -> ask.

    Returns (values, questions, origins). `questions` holds one entry per
    parameter that reached step 4 with nothing to fill it; a required parameter
    that lands there is refused by name by the caller and never substituted
    empty. `origins` names which step of the order filled each value —
    `explicit`, `store`, `default`, `placeholder` or `unfilled` — and is what
    lets the caller persist only the answers it was actually given.
    """
    values: dict[str, str] = {}
    origins: dict[str, str] = {}
    questions: list[dict] = []
    for name, decl in variables.items():
        if scope is not None and name not in scope:
            continue
        if decl["sensitive"]:
            # The value never travels. The build emits the placeholder and the
            # caller substitutes locally afterwards.
            values[name] = decl["placeholder"]
            origins[name] = "placeholder"
            continue
        if name in explicit:
            values[name] = explicit[name]
            origins[name] = "explicit"
            continue
        from_store = store_value(store, name)
        if from_store is not None:
            check_type(decl, from_store)
            values[name] = from_store
            origins[name] = "store"
            continue
        if decl["default"] is not None:
            check_type(decl, decl["default"])
            values[name] = decl["default"]
            origins[name] = "default"
            continue
        questions.append({
            "name": name,
            "type": decl["type"],
            "required": decl["required"],
            "question": decl["description"],
            "options": decl["options"],
            "compose": decl["type"] == "text",
        })
        if not decl["required"]:
            values[name] = ""
            origins[name] = "unfilled"
    return values, questions, origins


# ------------------------------------------------------- Markdown -> HTML

def escape_value(text: str) -> str:
    """Unconditional. Used for a substituted parameter value, for an attribute
    and for the title — every HTML-active character goes, `&` included, so a
    `<script>` in a value can never be anything but text."""
    return (text.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


_ENTITY = re.compile(
    r"&(?:[a-zA-Z][a-zA-Z0-9]{1,31}|#\d{1,7}|#[xX][0-9a-fA-F]{1,6});")


def escape_source(text: str) -> str:
    """Entity-preserving. Used for the template's OWN text, and only for that.

    A 58-file family in the corpus stores its placeholders already
    entity-escaped — the file literally holds `&lt;artefact_id&gt;`. Escaping
    that again gives `&amp;lt;artefact_id&amp;gt;`, and the reader sees the
    entities. So a well-formed character reference in SOURCE text passes
    through; everything else is escaped exactly as escape_value would.

    This deliberately does not apply to parameter values, which never reach
    this function: they are held as sentinels through the whole render and
    escaped unconditionally at the end. Two trust levels, two code paths.
    """
    parts: list[str] = []
    pos = 0
    for match in _ENTITY.finditer(text):
        parts.append(escape_value(text[pos:match.start()]))
        parts.append(match.group(0))
        pos = match.end()
    parts.append(escape_value(text[pos:]))
    return "".join(parts)


_SAFE_URL = re.compile(r"^(?:https?://|mailto:|#|/|\.{0,2}/)")
_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]*)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITAL = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")
_ITAL_U = re.compile(r"(?<![\w_])_([^_\n]+)_(?![\w_])")
_FENCE = re.compile(r"^\s*(```|~~~)\s*([A-Za-z0-9_+-]*)\s*$")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_HR = re.compile(r"^\s*(-{3,}|_{3,}|\*{3,})\s*$")
_UL = re.compile(r"^(\s*)[-*+]\s+(.*)$")
_OL = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
_TABLE_SEP = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")
_COMMENT_OPEN = re.compile(r"^\s*<!--")


def _inline(text: str, marks: list[str] | None = None) -> str:
    """Inline Markdown over SOURCE text. Code spans are lifted out first so
    nothing inside them is re-read as emphasis or as a link. Value sentinels
    pass through untouched and are resolved by the caller."""
    spans: list[str] = []

    def lift(match: re.Match) -> str:
        spans.append(match.group(1))
        return f"\x00{len(spans) - 1}\x00"

    text = _CODE.sub(lift, escape_source(text.replace("\x00", "")))

    def link(match: re.Match) -> str:
        label, url = match.group(1), match.group(2)
        # A parameter may supply an href, so resolve any sentinel BEFORE the
        # scheme check — the check must see the real URL, not an opaque mark.
        real = _MARK.sub(lambda m: (marks or [])[int(m.group(1))], url) \
            if marks else url
        # An href is opened only for a scheme this renderer vouches for.
        # javascript:, data: and vbscript: are rendered as text, not resolved.
        if not _SAFE_URL.match(real):
            return f"{label} ({url})"
        return f'<a href="{escape_value(real)}">{label}</a>'

    text = _LINK.sub(link, text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITAL.sub(r"<em>\1</em>", text)
    text = _ITAL_U.sub(r"<em>\1</em>", text)
    for index, span in enumerate(spans):
        text = text.replace(f"\x00{index}\x00", f"<code>{span}</code>")
    return text


def _row(line: str) -> list[str]:
    cells = line.strip()
    if cells.startswith("|"):
        cells = cells[1:]
    if cells.endswith("|"):
        cells = cells[:-1]
    return [c.strip() for c in cells.split("|")]


CSS = """:root{color-scheme:light dark}
body{margin:0 auto;max-width:52rem;padding:2rem 1.25rem;
font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
color:#1b1b1b;background:#fff}
h1,h2,h3,h4,h5,h6{line-height:1.25;margin:2rem 0 .6rem}
h1{font-size:1.9rem} h2{font-size:1.45rem} h3{font-size:1.15rem}
p,ul,ol,blockquote,table,pre{margin:0 0 1rem}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9em;
background:#f2f2f2;padding:.1em .3em;border-radius:3px}
pre{background:#f6f6f6;padding:.9rem 1rem;border-radius:5px;overflow-x:auto}
pre code{background:none;padding:0}
blockquote{border-left:3px solid #d0d0d0;margin-left:0;padding-left:1rem;
color:#4a4a4a}
table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}
th,td{border:1px solid #ddd;padding:.4rem .6rem;text-align:left}
th{background:#f6f6f6}
hr{border:0;border-top:1px solid #ddd;margin:2rem 0}
a{color:#0b57d0}
@media(prefers-color-scheme:dark){
body{color:#e6e6e6;background:#151515}
code{background:#242424} pre{background:#1d1d1d}
th{background:#1d1d1d} th,td{border-color:#333}
blockquote{border-left-color:#3a3a3a;color:#b0b0b0} a{color:#8ab4f8}}"""


def md_to_html(markdown: str, title: str,
               marks: list[str] | None = None) -> str:
    """A deliberately partial Markdown renderer: headings, paragraphs, lists,
    tables, fenced code, blockquotes, rules, links, emphasis and code spans.

    NOT CommonMark, and never described as such. Everything it does not
    recognise is escaped and emitted as text — which is also why raw HTML in
    the source is inert rather than passed through.

    `marks` is the sentinel table from substitute_marked. Source text is
    escaped entity-preservingly as it is rendered; the values arrive only in
    the final pass below, escaped unconditionally.
    """
    lines = markdown.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        fence = _FENCE.match(line)
        if fence:
            lang, index = fence.group(2), index + 1
            code: list[str] = []
            while index < len(lines) and not _FENCE.match(lines[index]):
                code.append(lines[index])
                index += 1
            index += 1
            attr = f' class="language-{escape_value(lang)}"' if lang else ""
            out.append(f"<pre><code{attr}>"
                       f"{escape_source(chr(10).join(code))}</code></pre>")
            continue
        if _COMMENT_OPEN.match(line):
            # A block-level HTML comment is dropped from the RENDERED view: the
            # .md is canonical and keeps it (the header block emits a real
            # five-key comment, which is the point of that block), but a
            # comment shown as body text in the HTML is just noise. Handled
            # here rather than by a global regex so a comment inside a fenced
            # code block still renders, and a value can neither form nor break
            # one — by now every value is an opaque sentinel.
            while index < len(lines) and "-->" not in lines[index]:
                index += 1
            index += 1
            continue
        if not line.strip():
            index += 1
            continue
        if _HR.match(line) and not _TABLE_SEP.match(line):
            out.append("<hr/>")
            index += 1
            continue
        heading = _HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{_inline(heading.group(2).strip(), marks)}"
                       f"</h{level}>")
            index += 1
            continue
        if line.lstrip().startswith(">"):
            quote: list[str] = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                quote.append(lines[index].lstrip()[1:].lstrip())
                index += 1
            out.append("<blockquote><p>" + _inline(" ".join(quote), marks)
                       + "</p></blockquote>")
            continue
        if (index + 1 < len(lines) and "|" in line
                and _TABLE_SEP.match(lines[index + 1])
                and "|" in lines[index + 1]):
            head = _row(line)
            index += 2
            body_rows: list[list[str]] = []
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                body_rows.append(_row(lines[index]))
                index += 1
            cells = "".join(f"<th>{_inline(c, marks)}</th>" for c in head)
            table = [f"<table><thead><tr>{cells}</tr></thead><tbody>"]
            for row in body_rows:
                table.append("<tr>" + "".join(f"<td>{_inline(c, marks)}</td>"
                                              for c in row) + "</tr>")
            table.append("</tbody></table>")
            out.append("".join(table))
            continue
        if _UL.match(line) or _OL.match(line):
            index = _render_list(lines, index, out, marks)
            continue
        para: list[str] = []
        while index < len(lines) and lines[index].strip() \
                and not _FENCE.match(lines[index]) \
                and not _HEADING.match(lines[index]) \
                and not _UL.match(lines[index]) and not _OL.match(lines[index]) \
                and not lines[index].lstrip().startswith(">") \
                and not _HR.match(lines[index]):
            para.append(lines[index].strip())
            index += 1
        out.append("<p>" + _inline(" ".join(para), marks) + "</p>")
    body = "\n".join(out)
    if marks:
        # The one place a parameter value becomes HTML. Unconditional escape,
        # no entity pass-through, no Markdown: a value is text.
        body = _MARK.sub(lambda m: escape_value(marks[int(m.group(1))]), body)
    return ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"/>"
            "<meta name=\"viewport\" content=\"width=device-width,"
            "initial-scale=1\"/>\n<title>" + escape_value(title)
            + "</title>\n<style>" + CSS + "</style></head>\n<body>\n" + body
            + "\n</body></html>\n")


def _render_list(lines: list[str], index: int, out: list[str],
                 marks: list[str] | None = None) -> int:
    """One list, with a single level of nesting. Deeper indents are flattened
    into that level rather than guessed at."""
    ordered = bool(_OL.match(lines[index]))
    base = len((_OL if ordered else _UL).match(lines[index]).group(1))
    tag = "ol" if ordered else "ul"
    items: list[str] = [f"<{tag}>"]
    nested = ""
    close = {"in-li": "</ul></li>", "bare": "</ul>"}
    while index < len(lines):
        match = _OL.match(lines[index]) or _UL.match(lines[index])
        if not match:
            break
        indent, text = len(match.group(1)), match.group(2)
        if indent > base:
            if not nested:
                # A nested list belongs INSIDE the item above it, so reopen
                # that <li> rather than emitting a <ul> as its sibling.
                if items[-1].endswith("</li>"):
                    items[-1] = items[-1][: -len("</li>")]
                    nested = "in-li"
                else:
                    nested = "bare"
                items.append("<ul>")
        elif nested:
            items.append(close[nested])
            nested = ""
        items.append(f"<li>{_inline(text, marks)}</li>")
        index += 1
    if nested:
        items.append(close[nested])
    items.append(f"</{tag}>")
    out.append("".join(items))
    return index


# --------------------------------------------------------------- sources

def load_template(path: Path) -> dict:
    """One template or block file, parsed into declarations plus body."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TplError(f"cannot read {path}: {exc}") from exc
    return parse_source(text, path.name)


def parse_source(text: str, where: str) -> dict:
    head, body = split_header(text)
    header = parse_header(head) if head else {}
    variables = parse_variables(header, where)
    sections = parse_sections(header, variables, where)
    return {"where": where, "header": header, "variables": variables,
            "sections": sections, "body": body}


def merge(sources: list[dict]) -> dict:
    """Concatenate block bodies and union their declarations.

    Two blocks declaring the same name differently is refused, not merged: a
    silent winner would make an assembled document depend on block order.
    """
    variables: dict[str, dict] = {}
    sections: list[dict] = []
    seen_sections: set[str] = set()
    bodies: list[str] = []
    for source in sources:
        for name, decl in source["variables"].items():
            if name in variables and variables[name] != decl:
                raise TplError(
                    f"{source['where']}: variable {name!r} is declared "
                    "differently by two blocks in this set; make the two "
                    "declarations identical or use two names")
            variables[name] = decl
        for section in source["sections"]:
            if section["name"] in seen_sections:
                existing = next(s for s in sections if s["name"] == section["name"])
                if existing != section:
                    raise TplError(f"{source['where']}: section "
                                   f"{section['name']!r} is declared "
                                   "differently by two blocks in this set")
                continue
            seen_sections.add(section["name"])
            sections.append(section)
        bodies.append(source["body"].strip("\n"))
    return {"where": "block set", "header": {}, "variables": variables,
            "sections": sections, "body": "\n\n".join(b for b in bodies if b)}


def resolve_blocks(root: Path | None, use: list[str]) -> list[Path]:
    """One ordered source list from `kind/name` block refs and `.md` file paths.

    Blocks cover the envelope and nothing more: measured over the corpus, 807
    of 9,278 distinct fragments recur at all and the median template shares no
    bytes with any other. So an assembly is normally blocks PLUS literal
    passthrough, and a literal file is a first-class entry in this list rather
    than a second mode — an entry ending `.md` is a path, anything else is
    `<kind>/<name>` under --blocks. That is also why a template whose identity
    section matches no block is not an error: it is assembled from literals.
    """
    paths: list[Path] = []
    for ref in use:
        ref = ref.strip()
        if not ref:
            continue
        if ref.endswith(".md"):
            literal = Path(ref)
            if not literal.is_file():
                raise TplError(f"no such file: {literal}")
            paths.append(literal)
            continue
        if root is None:
            raise TplError(f"block reference {ref!r} needs --blocks; only a "
                           "path ending .md is resolved without it")
        if ref.count("/") != 1:
            raise TplError(f"block reference {ref!r} is not `<kind>/<name>`")
        kind, name = ref.split("/")
        if not VAR_NAME.match(kind.replace("-", "_")) \
                or not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            raise TplError(f"block reference {ref!r}: kind and name must be "
                           "lowercase identifiers")
        path = root / kind / f"{name}.md"
        if not path.is_file():
            raise TplError(f"no such block: {path}")
        paths.append(path)
    if not paths:
        raise TplError("--use names no blocks")
    return paths
