import ast


def enrich_ast_with_parents(tree: ast.Module) -> None:
    """Walks the AST and adds a 'parent' attribute to each node."""
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
