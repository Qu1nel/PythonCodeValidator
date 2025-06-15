import ast
from typing import Any

from ..components.definitions import Constraint


class IsRequiredConstraint(Constraint):
    """Checks that at least one node was found by the selector."""

    def __init__(self, **kwargs: Any):
        """Initializes the constraint.

        Args:
            **kwargs: Configuration for the constraint, e.g., 'count'.
        """
        self.expected_count = kwargs.get("count")

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if the list of nodes is not empty or matches expected count."""
        if self.expected_count is not None:
            return len(nodes) == self.expected_count

        return len(nodes) > 0


class MustInheritFromConstraint(Constraint):
    """Checks that a ClassDef node inherits from a specific parent class."""

    def __init__(self, **kwargs: Any):
        """Initializes the constraint."""
        self.parent_name_to_find = kwargs.get("parent_name")

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if the found class node inherits from the specified parent."""
        if not self.parent_name_to_find:
            # Если parent_name не указан в правиле, не можем ничего проверить
            return False

        # Это ограничение осмысленно только для одного найденного класса
        if len(nodes) != 1:
            return False

        node = nodes[0]
        if not isinstance(node, ast.ClassDef):
            return False  # Должен быть узел класса

        # Проходим по всем базовым классам
        for base in node.bases:
            # Базовый класс может быть простым именем (ast.Name)
            if isinstance(base, ast.Name) and base.id == self.parent_name_to_find:
                return True
            # Или атрибутом (ast.Attribute), как в arcade.Window
            if isinstance(base, ast.Attribute):
                # Собираем полное имя, например, "arcade.Window"
                full_name = self._get_full_attribute_name(base)
                if full_name == self.parent_name_to_find:
                    return True

        return False

    @staticmethod
    def _get_full_attribute_name(node: ast.Attribute) -> str:
        """Recursively builds the full attribute name, e.g., 'arcade.Window'."""
        parts = []
        current_node = node
        while isinstance(current_node, ast.Attribute):
            parts.append(current_node.attr)
            current_node = current_node.value

        if isinstance(current_node, ast.Name):
            parts.append(current_node.id)

        return ".".join(reversed(parts))


class IsForbiddenConstraint(Constraint):
    """Checks that no nodes were found by the selector."""

    def __init__(self, **kwargs: Any):
        """Initializes the constraint."""
        # У этого ограничения нет параметров, но __init__ нужен для единообразия
        pass

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if the list of nodes is empty."""
        return len(nodes) == 0


class MustBeTypeConstraint(Constraint):
    """Checks the type of the value in an assignment."""

    def __init__(self, **kwargs: Any):
        self.expected_type = kwargs.get("expected_type")
        self.type_map = {
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "bool": bool,
        }

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if the assigned value has the expected Python type."""
        if not nodes or not self.expected_type:
            return False

        for node in nodes:
            # Узел может быть Assign или AnnAssign, нам нужно поле value
            value_node = getattr(node, "value", None)
            if value_node is None:
                continue  # Пропускаем присваивания без значения (например, `x: int`)

            # ast.unparse() доступен с Python 3.9 и может быть полезен,
            # но безопаснее работать с ast.literal_eval.
            try:
                assigned_value = ast.literal_eval(value_node)
                expected_py_type = self.type_map.get(self.expected_type)
                if not isinstance(assigned_value, expected_py_type):
                    return False
            except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                # literal_eval не может обработать сложные выражения, это нормально.
                # В этом случае мы пропускаем проверку для этого узла.
                # Для более сложных случаев понадобится более глубокий анализ.
                continue

        return True


class NameMustBeInConstraint(Constraint):
    """Checks if the name of a found node is in an allowed list."""

    def __init__(self, **kwargs: Any):
        self.allowed_names = set(kwargs.get("allowed_names", []))

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if all found node names are in the allowed set."""
        for node in nodes:
            # Имя может быть в разных атрибутах в зависимости от типа узла
            node_name = getattr(node, "name", None) or getattr(node, "id", None)
            if node_name and node_name not in self.allowed_names:
                return False
        return True


class ValueMustBeInConstraint(Constraint):
    """Checks if the value of a found literal node is in an allowed list."""

    def __init__(self, **kwargs: Any):
        """Initializes the constraint."""
        self.allowed_values = set(kwargs.get("allowed_values", []))

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if all found literal values are in the allowed set."""
        if not self.allowed_values:
            # Если список разрешенных значений пуст, любое найденное значение - ошибка.
            return not nodes

        for node in nodes:
            # Мы ожидаем, что сюда придут только ast.Constant узлы
            if isinstance(node, ast.Constant):
                if node.value not in self.allowed_values:
                    return False
            else:
                # Если пришел узел другого типа, считаем это провалом правила
                return False
        return True
