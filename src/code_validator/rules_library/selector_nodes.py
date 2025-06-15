import ast
from typing import Any

from ..components.definitions import Selector
from ..components.scope_handler import find_scope_node


def _get_full_name(node: ast.AST) -> str | None:
    """Helper to get a full name like 'self.x' or 'my_var' from a node."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        # Рекурсивно собираем имя, например, 'self.player.x'
        base = _get_full_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


class ScopeVisitor(ast.NodeVisitor):
    """A NodeVisitor to find a specific scope (function or class) in the AST."""

    def __init__(self, scope_name: str):
        self.scope_name = scope_name
        self.scope_node: ast.AST | None = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name == self.scope_name:
            self.scope_node = node
        # Не идем глубже, чтобы не найти вложенные функции с тем же именем
        # self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == self.scope_name:
            self.scope_node = node
        # Здесь мы *должны* идти глубже, чтобы найти методы внутри класса
        self.generic_visit(node)


class FunctionDefSelector(Selector):
    """Selects function definition (def) nodes from an AST."""

    def __init__(self, **kwargs: Any):
        self.name_to_find = kwargs.get("name")
        self.in_scope_config = kwargs.get("in_scope")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.FunctionDef nodes that match the criteria."""
        search_tree: ast.AST = tree
        if self.in_scope_config and self.in_scope_config != "global":
            scope_node = find_scope_node(tree, self.in_scope_config)
            if not scope_node:
                return []  # Если скоуп не найден, то и внутри него ничего нет
            search_tree = scope_node

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            if isinstance(node, ast.FunctionDef):
                if self.name_to_find == "*" or node.name == self.name_to_find:
                    found_nodes.append(node)
        return found_nodes


class ClassDefSelector(Selector):
    """Selects class definition (class) nodes from an AST."""

    def __init__(self, **kwargs: Any):
        """Initializes the selector."""
        self.name_to_find = kwargs.get("name")
        self.in_scope_config = kwargs.get("in_scope")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.ClassDef nodes that match the criteria."""
        search_tree: ast.AST = tree
        if self.in_scope_config and self.in_scope_config != "global":
            scope_node = find_scope_node(tree, self.in_scope_config)
            if not scope_node:
                return []  # Если скоуп не найден, то и внутри него ничего нет
            search_tree = scope_node

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            if isinstance(node, ast.ClassDef):
                if self.name_to_find == "*" or node.name == self.name_to_find:
                    found_nodes.append(node)
        return found_nodes


class ImportStatementSelector(Selector):
    """Selects import nodes (import or from...import) from an AST."""

    def __init__(self, **kwargs: Any):
        """Initializes the selector.

        Args:
            **kwargs: Configuration, e.g., 'module_name'.
        """
        self.module_name_to_find = kwargs.get("module_name")
        self.in_scope_config = kwargs.get("in_scope")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all import-related nodes that match the criteria."""
        if not self.module_name_to_find:
            return []

        search_tree: ast.AST = tree
        if self.in_scope_config and self.in_scope_config != "global":
            scope_node = find_scope_node(tree, self.in_scope_config)
            if not scope_node:
                return []  # Если скоуп не найден, то и внутри него ничего нет
            search_tree = scope_node

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            # Случай 1: import module1, module2
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == self.module_name_to_find:
                        found_nodes.append(node)
                        break  # Достаточно одного совпадения на узел

            # Случай 2: from package import module
            elif isinstance(node, ast.ImportFrom):
                # node.module может быть None для относительных импортов,
                # например, `from . import utils`
                if node.module and node.module == self.module_name_to_find:
                    found_nodes.append(node)

        return found_nodes


class FunctionCallSelector(Selector):
    """Selects function call nodes from an AST."""

    def __init__(self, **kwargs: Any):
        """Initializes the selector."""
        self.name_to_find = kwargs.get("name")
        self.in_scope_config = kwargs.get("in_scope")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.Call nodes that match the criteria."""
        search_tree: ast.AST = tree
        if self.in_scope_config and self.in_scope_config != "global":
            scope_node = find_scope_node(tree, self.in_scope_config)
            if not scope_node:
                return []  # Если скоуп не найден, то и внутри него ничего нет
            search_tree = scope_node
        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            if isinstance(node, ast.Call):
                # Используем наш helper, чтобы получить полное имя вызываемого объекта
                full_name = _get_full_name(node.func)
                if full_name and full_name == self.name_to_find:
                    found_nodes.append(node)
        return found_nodes


class AssignmentSelector(Selector):
    """Selects assignment nodes (e.g., x = 5, self.y = 10)."""

    def __init__(self, **kwargs: Any):
        self.target_name_to_find = kwargs.get("target_name")
        self.in_scope_config = kwargs.get("in_scope")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.Assign or ast.AnnAssign nodes matching the target name."""
        search_tree: ast.AST = tree
        if self.in_scope_config and self.in_scope_config != "global":
            scope_node = find_scope_node(tree, self.in_scope_config)
            if not scope_node:
                return []  # Если скоуп не найден, то и внутри него ничего нет
            search_tree = scope_node
        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            # Мы поддерживаем и простое присваивание (x=5), и с аннотацией (x: int = 5)
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                # Целей присваивания может быть несколько (a = b = 5)
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    full_name = _get_full_name(target)
                    if full_name and (self.target_name_to_find == "*" or full_name == self.target_name_to_find):
                        found_nodes.append(node)
        return found_nodes


class UsageSelector(Selector):
    """Selects nodes where a variable or attribute is used (read)."""

    def __init__(self, **kwargs: Any):
        self.variable_name_to_find = kwargs.get("variable_name")
        self.in_scope_config = kwargs.get("in_scope")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.Name nodes (in load context) matching the name."""
        search_tree: ast.AST = tree
        if self.in_scope_config and self.in_scope_config != "global":
            scope_node = find_scope_node(tree, self.in_scope_config)
            if not scope_node:
                return []  # Если скоуп не найден, то и внутри него ничего нет
            search_tree = scope_node
        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            # Проверяем и простые имена, и атрибуты, когда их "читают"
            if isinstance(node, (ast.Name, ast.Attribute)) and isinstance(getattr(node, "ctx", None), ast.Load):
                full_name = _get_full_name(node)
                if full_name and full_name == self.variable_name_to_find:
                    found_nodes.append(node)
        return found_nodes


class LiteralSelector(Selector):
    """Selects literal nodes (ast.Constant) like numbers and strings."""

    def __init__(self, **kwargs: Any):
        """Initializes the selector."""
        self.literal_type = kwargs.get("literal_type")  # "number" или "string"
        self.in_scope_config = kwargs.get("in_scope")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.Constant nodes that match the type criteria."""

        type_map = {
            "number": (int, float),
            "string": (str,),
        }

        expected_py_types = type_map.get(self.literal_type)
        if not expected_py_types:
            return []  # Если тип литерала не задан или неверный, ничего не ищем

        search_tree: ast.AST = tree
        if self.in_scope_config and self.in_scope_config != "global":
            scope_node = find_scope_node(tree, self.in_scope_config)
            if not scope_node:
                return []  # Если скоуп не найден, то и внутри него ничего нет
            search_tree = scope_node
        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            # В Python 3.8+ все литералы, включая числа и строки, это ast.Constant
            if isinstance(node, ast.Constant):
                if isinstance(node.value, expected_py_types):
                    found_nodes.append(node)
        return found_nodes
