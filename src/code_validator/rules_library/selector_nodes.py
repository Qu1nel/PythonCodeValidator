import ast
from typing import Any

from ..components.definitions import Selector
from ..components.scope_handler import find_scope_node
from ..rules_library.constraint_logic import _get_full_name


class ScopedSelector(Selector):
    """An abstract base class for selectors that support scoping."""

    def __init__(self, **kwargs: Any):
        self.in_scope_config = kwargs.get("in_scope")

    def _get_search_tree(self, tree: ast.Module) -> ast.AST | None:
        """Determines the root node for the search based on the scope config."""
        if not self.in_scope_config or self.in_scope_config == "global":
            return tree

        scope_node = find_scope_node(tree, self.in_scope_config)
        return scope_node

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Abstract select method to be implemented by subclasses."""
        raise NotImplementedError


class FunctionDefSelector(ScopedSelector):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.name_to_find = kwargs.get("name")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        search_tree = self._get_search_tree(tree)
        if not search_tree:
            return []

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            if isinstance(node, ast.FunctionDef):
                if self.name_to_find == "*" or node.name == self.name_to_find:
                    found_nodes.append(node)
        return found_nodes


class ClassDefSelector(ScopedSelector):
    """Selects class definition (class) nodes from an AST."""

    def __init__(self, **kwargs: Any):
        """Initializes the selector."""
        super().__init__(**kwargs)
        self.name_to_find = kwargs.get("name")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.ClassDef nodes that match the criteria."""
        search_tree = self._get_search_tree(tree)
        if not search_tree:
            return []

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            if isinstance(node, ast.ClassDef):
                if self.name_to_find == "*" or node.name == self.name_to_find:
                    found_nodes.append(node)
        return found_nodes


class ImportStatementSelector(ScopedSelector):
    """Selects import nodes (import or from...import) from an AST."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.module_name_to_find = kwargs.get("name")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all import-related nodes that match the criteria."""
        if not self.module_name_to_find:
            return []

        search_tree = self._get_search_tree(tree)
        if not search_tree:
            return []

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Проверяем 'os' в 'import os.path'
                    module_parts = alias.name.split(".")
                    if alias.name.startswith(self.module_name_to_find) or self.module_name_to_find in module_parts:
                        found_nodes.append(node)
                        break
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith(self.module_name_to_find):
                    found_nodes.append(node)

        return found_nodes


class FunctionCallSelector(ScopedSelector):
    """Selects function call nodes from an AST."""

    def __init__(self, **kwargs: Any):
        """Initializes the selector."""
        super().__init__(**kwargs)
        self.name_to_find = kwargs.get("name")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.Call nodes that match the criteria."""
        search_tree = self._get_search_tree(tree)
        if not search_tree:
            return []

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            if isinstance(node, ast.Call):
                # Используем наш helper, чтобы получить полное имя вызываемого объекта
                full_name = _get_full_name(node.func)
                if full_name and full_name == self.name_to_find:
                    found_nodes.append(node)
        return found_nodes


class AssignmentSelector(ScopedSelector):
    """Selects assignment nodes (e.g., x = 5, self.y = 10)."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.target_name_to_find = kwargs.get("name")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.Assign or ast.AnnAssign nodes matching the target name."""
        search_tree = self._get_search_tree(tree)
        if not search_tree:
            return []

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


class UsageSelector(ScopedSelector):
    """Selects nodes where a variable or attribute is used (read)."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.variable_name_to_find = kwargs.get("name")

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all ast.Name nodes (in load context) matching the name."""
        search_tree = self._get_search_tree(tree)
        if not search_tree:
            return []

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            # Проверяем и простые имена, и атрибуты, когда их "читают"
            if isinstance(node, (ast.Name, ast.Attribute)) and isinstance(getattr(node, "ctx", None), ast.Load):
                full_name = _get_full_name(node)
                if full_name and full_name == self.variable_name_to_find:
                    found_nodes.append(node)
        return found_nodes


class LiteralSelector(ScopedSelector):
    """Selects literal nodes, attempting to ignore docstrings."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.literal_type = kwargs.get("name")  # 'name' - это наш унифицированный ключ

    def select(self, tree: ast.Module) -> list[ast.AST]:
        search_tree = self._get_search_tree(tree)
        if not search_tree:
            return []

        type_map = {"number": (int, float), "string": (str,)}
        expected_py_types = type_map.get(self.literal_type)
        if not expected_py_types:
            return []

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            # Мы ищем только узлы Constant
            if not isinstance(node, ast.Constant):
                continue

            # Проверяем тип значения внутри константы
            if not isinstance(node.value, expected_py_types):
                continue

            # --- ЛОГИКА ИГНОРИРОВАНИЯ ДОКСТРИНГОВ ---
            # Если у узла есть родитель и этот родитель - Expr,
            # то велика вероятность, что это докстринг или "висячая" строка.
            # Настоящие "магические" строки обычно являются аргументами функций
            # или значениями в присваиваниях.
            if hasattr(node, "parent") and isinstance(node.parent, ast.Expr):
                continue  # Пропускаем этот узел, считая его докстрингом.

            found_nodes.append(node)

        return found_nodes


class AstNodeSelector(ScopedSelector):
    """Selects AST nodes directly by their class name (e.g., 'For', 'While')."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        node_type_arg = kwargs.get("node_type")

        # Поддерживаем и одну строку, и список строк
        if isinstance(node_type_arg, list):
            self.node_types_to_find = tuple(getattr(ast, nt) for nt in node_type_arg if hasattr(ast, nt))
        elif isinstance(node_type_arg, str) and hasattr(ast, node_type_arg):
            self.node_types_to_find = (getattr(ast, node_type_arg),)
        else:
            self.node_types_to_find = ()

    def select(self, tree: ast.Module) -> list[ast.AST]:
        """Finds all AST nodes that are instances of the specified types."""
        search_tree = self._get_search_tree(tree)
        if not search_tree or not self.node_types_to_find:
            return []

        found_nodes: list[ast.AST] = []
        for node in ast.walk(search_tree):
            if isinstance(node, self.node_types_to_find):
                found_nodes.append(node)
        return found_nodes
