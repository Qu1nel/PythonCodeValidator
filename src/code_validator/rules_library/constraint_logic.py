import ast
from typing import Any

from ..components.definitions import Constraint


def _get_full_name(node: ast.AST) -> str | None:
    """Helper to get a full name like 'self.x' or 'my_var' from a node."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        # Рекурсивно собираем имя, например, 'self.player.x'
        base = _get_full_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


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
            "set": set,
            "tuple": tuple,
        }
        self.constructor_map = {
            "str": "str",
            "int": "int",
            "float": "float",
            "list": "list",
            "dict": "dict",
            "bool": "bool",
            "set": "set",
            "tuple": "tuple",
        }

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if the assigned value has the expected Python type."""
        if not nodes or not self.expected_type:
            return False

        expected_py_type = self.type_map.get(self.expected_type)
        if not expected_py_type:
            return False  # Неизвестный тип в правиле

        for node in nodes:
            value_node = getattr(node, "value", None)
            if value_node is None:
                continue

            is_match = False
            # 1. Проверяем литералы (самый частый случай)
            try:
                assigned_value = ast.literal_eval(value_node)
                if isinstance(assigned_value, expected_py_type):
                    is_match = True
            except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                # Не литерал, идем дальше
                pass

            if is_match:
                continue  # С этим узлом все хорошо, переходим к следующему

            # 2. Если не литерал, проверяем вызов конструктора (e.g., list())
            if isinstance(value_node, ast.Call):
                func_name = getattr(value_node.func, "id", None)
                expected_constructor = self.constructor_map.get(self.expected_type)
                if func_name == expected_constructor:
                    is_match = True

            # Если после всех проверок совпадения нет, то правило провалено
            if not is_match:
                return False

        # Если мы прошли весь цикл и не вышли, значит все узлы прошли проверку
        return True


class NameMustBeInConstraint(Constraint):
    def __init__(self, **kwargs: Any):
        self.allowed_names = set(kwargs.get("allowed_names", []))

    @staticmethod
    def _get_name(node: ast.AST) -> str | None:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            return _get_full_name(target)  # Используем глобальный helper
        return getattr(node, "name", getattr(node, "id", None))

    def check(self, nodes: list[ast.AST]) -> bool:
        for node in nodes:
            name_to_check = self._get_name(node)
            if name_to_check and name_to_check not in self.allowed_names:
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


class MustHaveArgsConstraint(Constraint):
    """Checks that a FunctionDef node has a specific signature."""

    def __init__(self, **kwargs: Any):
        self.expected_count: int | None = kwargs.get("count")
        self.expected_names: list[str] | None = kwargs.get("names")
        # По умолчанию требуем строгого совпадения, если заданы имена
        self.exact_match: bool = kwargs.get("exact_match", True)

    def check(self, nodes: list[ast.AST]) -> bool:
        """Checks if the function signature matches the criteria."""
        if not nodes:
            return True

        if not all(isinstance(node, ast.FunctionDef) for node in nodes):
            return False

        for node in nodes:
            actual_arg_names = [arg.arg for arg in node.args.args]  # type: ignore

            # Проверяем, является ли функция методом (есть ли родитель-класс)
            # и если да, удаляем 'self' или 'cls'
            if hasattr(node, "parent") and isinstance(node.parent, ast.ClassDef):
                if actual_arg_names:
                    actual_arg_names.pop(0)

            # --- Логика проверки ---
            if self.expected_names is not None:
                if self.exact_match:
                    if actual_arg_names != self.expected_names:
                        return False
                else:
                    if not set(self.expected_names).issubset(set(actual_arg_names)):
                        return False
            elif self.expected_count is not None:
                if len(actual_arg_names) != self.expected_count:
                    return False
            else:
                return False

        return True
