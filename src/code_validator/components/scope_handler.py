import ast
from typing import Any


def find_scope_node(tree: ast.Module, scope_config: dict[str, Any]) -> ast.AST | None:
    """Finds a specific scope node (class or function) within the AST."""

    # Ищем класс
    class_name = scope_config.get("class")
    if class_name:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                # Если нужен только класс, возвращаем его
                if "method" not in scope_config:
                    return node

                # Если нужен метод, ищем его внутри найденного класса
                method_name = scope_config.get("method")
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == method_name:
                        return item
                return None  # Класс нашли, а метод в нем - нет

    # Ищем глобальную функцию
    function_name = scope_config.get("function")
    if function_name:
        for node in tree.body:  # Ищем только на верхнем уровне
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return node

    return None
