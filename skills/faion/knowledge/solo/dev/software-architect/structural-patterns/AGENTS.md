# Structural Patterns

## Summary

Structural patterns define how classes and objects are composed into larger structures using inheritance and object composition. The seven GoF structural patterns are Adapter, Bridge, Composite, Decorator, Facade, Proxy, and Flyweight. All four "wrapping" patterns (Adapter, Proxy, Decorator, Bridge) involve surrounding an object but serve distinct purposes: Adapter converts an interface, Proxy controls access, Decorator adds behavior, Bridge separates abstraction from implementation. Select by problem, not by name recognition.

## Why

Without structural patterns, adding features through inheritance creates class explosions; adding them through ad-hoc composition creates tangled, untestable code. Structural patterns provide tested compositions: Decorator for stacking middleware, Facade for hiding subsystem complexity, Adapter for integrating legacy/third-party APIs, Proxy for lazy loading and access control. Each pattern applies a specific SOLID principle (OCP for Decorator/Composite/Proxy, DIP for all, Composition over Inheritance for Decorator/Bridge/Composite).

## When To Use

- Adapter: integrating third-party library, legacy API, or protocol with an incompatible interface
- Bridge: needing independent variation in both abstraction and implementation dimensions (designed up-front)
- Composite: representing hierarchical/tree structures (file systems, UI component trees, org charts)
- Decorator: adding cross-cutting behavior (logging, caching, auth) without subclassing; building middleware chains
- Facade: simplifying a complex subsystem for callers; library entry points; API gateway behavior in-process
- Proxy: lazy loading expensive objects; access control; caching; remote object representation; audit logging
- Flyweight: very large numbers of similar objects where most state is shared (text rendering, game particles)

## When NOT To Use

- Adapter: when the interface mismatch is small enough to handle with a single conversion function
- Bridge: when there is only one implementation dimension — adds unnecessary indirection
- Composite: when the tree structure is trivial (depth 1) or never traversed uniformly
- Decorator: when the number of combinations is small and fixed — direct subclassing is clearer
- Facade: when the subsystem is already simple or when the facade would hide information callers need
- Proxy: when simple delegation or a plain function call suffices — proxy adds a maintenance surface
- Flyweight: when object count is small or when extrinsic state computation offsets the memory savings

## Content

| File | What's inside |
|------|---------------|
| `content/01-adapter-bridge-composite.xml` | Adapter, Bridge, Composite — intent, participants, when-to-use, timing rules (Adapter = retrofit, Bridge = up-front) |
| `content/02-decorator-facade-proxy.xml` | Decorator, Facade, Proxy — intent, proxy types (Virtual/Protection/Remote/Cache/Logging), stacking rules |
| `content/03-flyweight-and-selection.xml` | Flyweight (intrinsic vs extrinsic state); pattern selection matrix; wrapping patterns comparison; SOLID mapping |

## Templates

| File | Purpose |
|------|---------|
| `templates/adapter.py` | Python class Adapter wrapping a legacy Adaptee to a Target interface |
| `templates/decorator.py` | Python function-decorator and class-decorator examples with stacking |
| `templates/proxy.py` | Python virtual proxy with lazy initialization and cache proxy |
| `templates/facade.py` | Python Facade hiding a multi-class subsystem behind a single interface |
