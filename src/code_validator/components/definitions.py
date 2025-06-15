import ast
from typing import Protocol, runtime_checkable

from ..config import FullRuleConfig, ShortRuleConfig


@runtime_checkable
class Selector(Protocol):
    """Defines the interface for any object that can select AST nodes."""

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Selects and returns a list of relevant AST nodes."""
        ...


@runtime_checkable
class Constraint(Protocol):
    """Defines the interface for any object that can check a list of AST nodes."""

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if the given list of nodes satisfies the constraint."""
        ...


@runtime_checkable
class Rule(Protocol):
    """Defines the interface for any executable validation rule."""

    config: FullRuleConfig | ShortRuleConfig

    def execute(self, tree: ast.Module | None, source_code: str | None = None) -> bool:
        """Executes the validation rule."""
        ...
