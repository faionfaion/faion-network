# purpose: Command pattern template (Python).
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a behavioral-patterns artefact validating against scripts/validate-behavioral-patterns.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
"""
Command pattern in Python with undo/redo Invoker.

Use when: undo/redo, operation queuing, audit logging, saga steps.
Skip when: simple operations with no undo requirement — just call the function.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Command interface
# ---------------------------------------------------------------------------
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        """Perform the operation."""

    @abstractmethod
    def undo(self) -> None:
        """Reverse the operation."""


# ---------------------------------------------------------------------------
# Receiver: the object that performs the actual work
# ---------------------------------------------------------------------------
@dataclass
class TextEditor:
    content: str = ""

    def insert(self, text: str) -> None:
        self.content += text

    def delete(self, n: int) -> None:
        self.content = self.content[:-n] if n > 0 else self.content


# ---------------------------------------------------------------------------
# Concrete commands
# ---------------------------------------------------------------------------
@dataclass
class InsertTextCommand(Command):
    editor: TextEditor
    text: str

    def execute(self) -> None:
        self.editor.insert(self.text)

    def undo(self) -> None:
        self.editor.delete(len(self.text))


@dataclass
class DeleteTextCommand(Command):
    editor: TextEditor
    n: int
    _deleted: str = field(default="", init=False)

    def execute(self) -> None:
        self._deleted = self.editor.content[-self.n:] if self.n > 0 else ""
        self.editor.delete(self.n)

    def undo(self) -> None:
        self.editor.insert(self._deleted)


# ---------------------------------------------------------------------------
# Invoker: manages history and redo stacks
# ---------------------------------------------------------------------------
class Invoker:
    def __init__(self) -> None:
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # new command invalidates redo history

    def undo(self) -> bool:
        if not self._history:
            return False
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
        return True

    @property
    def can_undo(self) -> bool:
        return bool(self._history)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo_stack)


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    editor = TextEditor()
    invoker = Invoker()

    invoker.execute(InsertTextCommand(editor, "Hello"))
    invoker.execute(InsertTextCommand(editor, ", World"))
    print(editor.content)  # "Hello, World"

    invoker.undo()
    print(editor.content)  # "Hello"

    invoker.redo()
    print(editor.content)  # "Hello, World"

    invoker.execute(DeleteTextCommand(editor, 6))
    print(editor.content)  # "Hello"

    invoker.undo()
    print(editor.content)  # "Hello, World"
