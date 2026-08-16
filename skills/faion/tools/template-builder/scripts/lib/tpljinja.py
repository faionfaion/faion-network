"""tpljinja — the Jinja layer shared by tpl-jinja.py and tpl-render.py.

Not a tool: a pack helper. `faion tools sync` materialises nested
`scripts/<sub>/*.py` alongside the pack, so both scripts load this file by
absolute path (importlib) rather than by module name — the same reason
lib/tplcore.py is loaded that way.

Four things live here and nothing else:

  * **the guarded Jinja import.** Jinja is this pack's one declared dependency
    (meta.json `dependencies`, .aidocs/conventions/template-jinja-migration.md
    §4). A module-level `import jinja2` would make its absence a traceback; a
    guarded one makes it an install line the caller can act on. Nothing in this
    pack may import jinja2 at module level, and validate-tools.py enforces that.
  * **the two environments.** Markdown renders unescaped, HTML renders with
    autoescape on, and both are `SandboxedEnvironment` with `StrictUndefined`
    so a missing variable raises by name instead of rendering empty — the whole
    point of declaring variables at all.
  * **the schema layer**: draft-07 emission for the converter, and the subset
    check the renderer runs over a value map before it renders.
  * **the dictionary reference**: how a template schema points into
    skills/faion/templates/vars-dictionary.schema.json, and what it emits when
    that file is not there yet.

THE RULE THIS FILE EXISTS TO KEEP, from §0 of the convention:

    A template is a FILE's own bytes. A value is CONTEXT. Nothing rendered,
    and nothing a caller supplied, is ever handed back in as template source.

Jinja binds context, never source, so under that rule a value cannot become
syntax and the injection surface is zero. `render_file` therefore takes a
*path*, not a string: the only way to get template source into this module is
to read a file, which is what makes double rendering structurally impossible
rather than merely discouraged.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DEP_MODULE = "jinja2"
DEP_PACKAGE = "Jinja2>=3.0"
INSTALL_HINT = (
    "this tool needs Jinja, which is not installed. Install it with "
    "`python3 -m pip install 'Jinja2>=3.0'` (or `pipx inject` / your project's "
    "own venv) and run again. It is declared in the pack's meta.json under "
    "`dependencies` — the tool refuses to half-work without it.")

# The dictionary every template schema draws its canonical names from.
DICTIONARY_REL = "skills/faion/templates/vars-dictionary.schema.json"
DICTIONARY_TODO = (
    "vars-dictionary.schema.json was not present when this schema was "
    "generated, so every property below is a LOCAL definition. Re-point the "
    "ones the dictionary defines at it ($ref) before treating this schema as "
    "canonical.")

DRAFT07 = "http://json-schema.org/draft-07/schema#"

# retrieval-content-contracts 2.2 types mapped onto JSON Schema's. `enum`
# becomes a string with an `enum` keyword, `path` and `text` become strings —
# the extra meaning rides on x-faion-* rather than on an invented type.
JSON_TYPE = {"string": "string", "integer": "integer", "boolean": "boolean",
             "enum": "string", "path": "string", "text": "string"}

VAR_IN_TEMPLATE = re.compile(r"\{\{\s*([a-z][a-z0-9_]{0,63})\s*\}\}")


class JinjaMissing(Exception):
    """Jinja is not installed. Carries the install line, not a traceback."""


class ValuesRefused(Exception):
    """A value map was refused. `.reasons` holds one string per refusal."""

    def __init__(self, reasons: list[str]) -> None:
        super().__init__("; ".join(reasons))
        self.reasons = reasons


class SchemaBroken(Exception):
    """The schema file itself is not usable."""


# ------------------------------------------------------------ the import

def load_jinja():
    """`(jinja2, jinja2.sandbox)`, or JinjaMissing carrying the install line.

    The import is inside the function on purpose: see the module docstring.
    """
    try:
        import jinja2
        from jinja2 import sandbox
    except ImportError as exc:  # pragma: no cover - exercised by hand
        raise JinjaMissing(INSTALL_HINT) from exc
    return jinja2, sandbox


def environment(mods, autoescape: bool):
    """One sandboxed environment.

    `autoescape` is True for the HTML template and False for the Markdown one:
    escaping Markdown would turn every `<` a value carries into `&lt;` in a
    file whose whole point is that it is plain text. The HTML template is where
    a value can become markup, and that is where autoescape belongs.

    `StrictUndefined` is not negotiable. Jinja's default Undefined renders as
    the empty string, which is the exact hole — a document shipped with a
    missing field and no signal — that declaring variables exists to prevent.
    """
    jinja2, sandbox = mods
    return sandbox.SandboxedEnvironment(
        autoescape=autoescape,
        undefined=jinja2.StrictUndefined,
        keep_trailing_newline=True,
        auto_reload=False,
    )


def render_source(env, source: str, values: dict) -> str:
    """Render template SOURCE with VALUES as context.

    `source` must be a template file's own bytes. It is never a rendered
    result, never a value, never anything a caller supplied. Callers other
    than the self-test go through `render_file`, which cannot be handed
    anything else.
    """
    return env.from_string(source).render(**values)


def render_file(env, path: Path, values: dict) -> str:
    """The only rendering path a tool uses. Source comes from disk, values
    come from the caller, and the two can never swap places."""
    return render_source(env, Path(path).read_text(encoding="utf-8"), values)


def template_variables(source: str) -> set[str]:
    """Every `{{ name }}` a template source references. Regex, not Jinja's
    own `meta.find_undeclared_variables`, so the converter can call it with
    Jinja absent and both tools agree on the answer."""
    return set(VAR_IN_TEMPLATE.findall(source))


# --------------------------------------------------------- schema emission

def _coerce_default(vtype: str, raw):
    """A declared default in the type the schema says it has."""
    if raw is None:
        return None
    if vtype == "integer":
        try:
            return int(str(raw).strip())
        except ValueError:
            return str(raw)
    if vtype == "boolean":
        return str(raw).strip().lower() == "true"
    return str(raw)


def _title_of(name: str) -> str:
    return name.replace("_", " ").strip().capitalize()


def property_for(decl: dict) -> dict:
    """One draft-07 property from one 2.2-shaped declaration.

    `description` is the load-bearing field (§2): it is the question put to the
    author, and it is why a placeholder with no evidence for what it means is
    left undeclared rather than given an invented one.
    """
    vtype = decl.get("type", "string")
    prop: dict = {"type": JSON_TYPE.get(vtype, "string"),
                  "title": decl.get("title") or _title_of(decl["name"]),
                  "description": decl["description"]}
    if vtype == "enum" and decl.get("options"):
        prop["enum"] = list(decl["options"])
    default = _coerce_default(vtype, decl.get("default"))
    if default is not None:
        prop["default"] = default
    if vtype == "text":
        prop["x-faion-compose"] = True
    if decl.get("sensitive"):
        prop["x-faion-sensitive"] = True
        prop["x-faion-placeholder"] = decl.get("placeholder") or ""
    return prop


def load_dictionary(path: Path | None) -> dict:
    """The corpus variable dictionary's defs, or {} when it is not there.

    Absent is a normal state during the migration, not an error: the dictionary
    is authored in parallel. What is not allowed is pretending — a schema
    generated without it carries an x-faion-todo saying so.
    """
    if path is None or not Path(path).is_file():
        return {}
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemaBroken(f"{path}: not readable as JSON: {exc}") from exc
    defs = data.get("$defs")
    if not isinstance(defs, dict):
        defs = data.get("definitions")
    return defs if isinstance(defs, dict) else {}


def build_schema(decls: list[dict], *, schema_id: str, title: str,
                 description: str, dictionary: dict,
                 dictionary_ref: str | None) -> dict:
    """The `<name>.vars.schema.json` for one template.

    A property $refs into the dictionary when the dictionary defines that name,
    and carries a local definition otherwise. That is the §3 rule made
    mechanical: convergence is a dictionary entry existing, never this tool
    deciding that two names mean the same thing.

    **A hand-authored description outranks the dictionary's.** When the source
    template already declared this variable with its own `description`, the
    `$ref` is wrapped in `allOf` and the local text is kept beside it, so the
    entry still supplies type and enum while the specific wording survives.

    That rule was written after the first migration wave silently replaced three
    of them. `severity` in `dev/bug-report-quality-rubric` read *"Technical
    impact if nothing is done. Data loss or corruption is critical however few
    users hit it"* and became the dictionary's *"How bad is this finding if
    nothing is done about it?"* — accurate, generic, and strictly less useful.
    Under §1b the description is the WIRE FORMAT: it is the sentence an agent
    puts to a human, so overwriting a specific one with a generic one is a
    product regression, not a tidy-up. The dictionary exists to disambiguate
    NAMES; it was never meant to overwrite better copy.
    """
    properties: dict = {}
    required: list[str] = []
    refs = 0
    for decl in decls:
        name = decl["name"]
        if dictionary and name in dictionary and dictionary_ref:
            ref = {"$ref": f"{dictionary_ref}#/$defs/{name}"}
            # ONLY a hand-authored description outranks the dictionary. The
            # first version of this rule tested "the local text differs from the
            # entry's", which is true of every converter-DRAFTED description
            # too — so it fired universally and replaced 1,453 curated questions
            # with drafted text like "Version. From section 'Context'.". Under
            # §1b the description is the wire format, so that was a copy
            # regression across most of the corpus, not a tidy-up.
            authored = (decl.get("description") or "").strip() \
                if decl.get("authored") else ""
            if authored and authored != (dictionary[name].get("description") or "").strip():
                # draft-07 ignores keywords sibling to `$ref`, so the reference
                # goes under `allOf` where it still applies and `description`
                # is read normally.
                properties[name] = {"allOf": [ref], "description": authored}
            else:
                properties[name] = ref
            refs += 1
        else:
            properties[name] = property_for(decl)
        # A variable the renderer can fill from a default, or a sensitive one
        # that emits its placeholder, is not required of the CALLER — and
        # `required` here is a statement about the value map, not about the
        # document.
        #
        # Sensitivity is read from the DICTIONARY as well as the local
        # declaration. Reading only the local one put 638 of the corpus's 639
        # sensitive slots into `required`: the converter drafts a declaration
        # with `sensitive: False` and the entry it $refs is what actually
        # carries `x-faion-sensitive`. Under §1b the schema IS the wire format,
        # so the effect was not cosmetic — a client reading it asks a human for
        # exactly the values the server must refuse to accept, which is the one
        # class of data §2.2 exists to keep off a multi-tenant assembler.
        entry = dictionary.get(name) or {} if dictionary else {}
        sensitive = decl.get("sensitive") or entry.get("x-faion-sensitive")
        has_default = decl.get("default") is not None or "default" in entry
        if decl.get("required") and not has_default and not sensitive:
            required.append(name)
    schema = {
        "$schema": DRAFT07,
        "$id": schema_id,
        "title": title,
        "description": description,
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
    }
    if required:
        schema["required"] = sorted(required)
    if not dictionary:
        schema["x-faion-todo"] = DICTIONARY_TODO
    schema["x-faion-dictionary-refs"] = refs
    return schema


# ----------------------------------------------------------- schema checking

def _resolve_ref(ref: str, root: dict, base: Path | None) -> dict:
    """A `$ref` this checker can follow, or {} when it cannot.

    Unresolvable is deliberately not an error: during the migration a schema
    may point at a dictionary that has not landed yet, and refusing to render
    would make every converted template unusable until it does. The caller is
    told how many refs went unresolved.
    """
    pointer = ref
    doc = root
    if not ref.startswith("#"):
        # `partition` drops the separator, and a pointer that has lost its `#`
        # fails the check below and silently resolves to nothing — which reads
        # downstream as "the dictionary is not there yet" rather than as a bug.
        filename, _, rest = ref.partition("#")
        pointer = "#" + rest
        if base is None:
            return {}
        target = (Path(base) / filename).resolve()
        if not target.is_file():
            return {}
        try:
            doc = json.loads(target.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
    if not pointer.startswith("#/"):
        return {}
    node = doc
    for part in pointer[2:].split("/"):
        if not isinstance(node, dict) or part not in node:
            return {}
        node = node[part]
    return node if isinstance(node, dict) else {}


def _type_ok(value, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "string":
        return isinstance(value, str)
    if name == "array":
        return isinstance(value, list)
    return True


def prepare_values(schema: dict, values: dict, base: Path | None = None,
                   secret_shape=None) -> tuple[dict, list[str], int]:
    """(values ready to render, refusals, unresolved $ref count).

    Applies declared defaults, substitutes the placeholder for a sensitive
    variable, and refuses — by name — an unknown key, a missing required one,
    a wrong type, a value outside an `enum`, and (when `secret_shape` is
    supplied) anything shaped like a credential. Refusing by name is the whole
    contract: a build that silently drops a misspelt key is a document with a
    hole in it.
    """
    if not isinstance(schema, dict) or schema.get("type") != "object":
        raise SchemaBroken("schema is not a draft-07 object schema")
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise SchemaBroken("schema declares no `properties` object")
    refusals: list[str] = []
    unresolved = 0
    ready: dict = {}

    resolved: dict[str, dict] = {}
    for name, raw in properties.items():
        prop = raw
        if isinstance(raw, dict):
            refs = [raw["$ref"]] if "$ref" in raw else []
            # A property whose source template authored its own description
            # carries the reference under `allOf`, not at the top level —
            # build_schema puts it there precisely because draft-07 ignores a
            # keyword sibling to `$ref`. Reading only the top level therefore
            # missed 1,633 of the corpus's 1,677 dictionary references, and
            # with them the `type`, the `enum` and — for 619 slots across 478
            # templates — the `x-faion-sensitive` flag, so a named human's
            # value was accepted and rendered into the document instead of the
            # placeholder §2.2 requires.
            refs += [member["$ref"] for member in (raw.get("allOf") or [])
                     if isinstance(member, dict) and "$ref" in member]
            if refs:
                merged: dict = {}
                for ref in refs:
                    target = _resolve_ref(ref, schema, base)
                    if target:
                        merged.update(target)
                    else:
                        unresolved += 1
                # The authored keywords win, which is the same precedence
                # build_schema wrote them with.
                merged.update({key: value for key, value in raw.items()
                               if key not in ("$ref", "allOf")})
                prop = merged
        resolved[name] = prop if isinstance(prop, dict) else {}

    if schema.get("additionalProperties") is False:
        for name in sorted(set(values) - set(properties)):
            refusals.append(f"{name}: not declared by this template; declared "
                            "are " + (", ".join(sorted(properties)) or "(none)"))

    for name, prop in resolved.items():
        if prop.get("x-faion-sensitive"):
            if name in values:
                refusals.append(
                    f"{name}: declared sensitive, so a value is never accepted "
                    f"here — the render emits "
                    f"{prop.get('x-faion-placeholder', '')!r} and you "
                    "substitute the real value locally afterwards")
            ready[name] = prop.get("x-faion-placeholder", "")
            continue
        if name in values:
            value = values[name]
        elif "default" in prop:
            ready[name] = prop["default"]
            continue
        else:
            if name in schema.get("required", []):
                question = prop.get("description") or "no description declared"
                refusals.append(f"{name}: required and not supplied — ask: "
                                f"{question}")
            continue
        vtype = prop.get("type")
        if vtype == "integer" and isinstance(value, str) \
                and re.fullmatch(r"-?\d+", value.strip()):
            value = int(value.strip())
        if vtype == "boolean" and isinstance(value, str) \
                and value.strip().lower() in ("true", "false"):
            value = value.strip().lower() == "true"
        if vtype and not _type_ok(value, vtype):
            refusals.append(f"{name}: declared {vtype}, got "
                            f"{type(value).__name__} {value!r}")
            continue
        if "enum" in prop and value not in prop["enum"]:
            refusals.append(f"{name}: {value!r} is not one of "
                            + ", ".join(str(o) for o in prop["enum"]))
            continue
        if secret_shape is not None and isinstance(value, str):
            shape = secret_shape(value)
            if shape:
                refusals.append(f"{name}: the supplied value looks like "
                                f"{shape}; a secret is never rendered in")
                continue
        ready[name] = value
    return ready, refusals, unresolved


def load_schema(path: Path) -> dict:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemaBroken(f"{path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SchemaBroken(f"{path}: not a JSON object")
    return data


def dumps(schema: dict) -> str:
    """One canonical serialisation, so two runs produce the same bytes."""
    return json.dumps(schema, indent=2, ensure_ascii=False) + "\n"


# ------------------------------------------------------- external references

EXTERNAL_REF = re.compile(
    r"""(?:src|href|@import\s+url\(|url\()\s*=?\s*["']?\s*(?:https?:)?//""",
    re.IGNORECASE)
EXTERNAL_TAG = re.compile(r"<(?:link|script|iframe|img|object|embed)\b",
                          re.IGNORECASE)
# An `<a href="https://…">` is NAVIGATION, not a fetch: nothing is retrieved
# unless a reader clicks, and §1's requirement is that the document carries its
# own stylesheet, font and images — not that it may never cite a URL. The one
# href-carrying tag that DOES fetch is `<link>`, and EXTERNAL_TAG already names
# it, so exempting the anchor costs the gate nothing.
#
# Measured, not assumed: `md_to_html` emits a real `<a href>` for every
# Markdown link, and `dev/changelog-automation-conventional-commits` — a Keep a
# Changelog skeleton whose two canonical citations are its whole point — was
# refused whole by this rule with "the generated templates did not verify".
ANCHOR_TAG = re.compile(r"<a\b[^>]*>", re.IGNORECASE)


def external_references(html: str) -> list[str]:
    """Every way this HTML could FETCH off-box. §1 requires self-contained.

    Both a protocol-relative URL and a bare `<script>` are findings: the first
    fetches, the second is the tag a fetch would be added to next. A link a
    reader can click is neither — see ANCHOR_TAG.
    """
    found: list[str] = []
    anchors = [m.span() for m in ANCHOR_TAG.finditer(html)]
    for match in EXTERNAL_REF.finditer(html):
        if any(a <= match.start() < b for a, b in anchors):
            continue
        found.append(f"external reference at offset {match.start()}: "
                     f"{html[match.start():match.start() + 48]!r}")
    for match in EXTERNAL_TAG.finditer(html):
        found.append(f"fetching tag at offset {match.start()}: "
                     f"{html[match.start():match.start() + 24]!r}")
    return found
