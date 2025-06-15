import ast
import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

from flake8.api import legacy as flake8

from ..components.definitions import Constraint, Rule, Selector
from ..config import FullRuleConfig, ShortRuleConfig
from ..output import Console, LogLevel


class CheckSyntaxRule(Rule):
    """Handles the 'check_syntax' short rule. Its logic is handled by the core."""

    def __init__(self, config: ShortRuleConfig, console: Console):
        self.config = config
        self._console = console

    def execute(self, tree: ast.Module | None, source_code: str | None = None) -> bool:
        """Returns True, as syntax validation is a prerequisite."""
        self._console.print(f"Rule {self.config.rule_id}: Syntax is valid.", level=LogLevel.DEBUG)
        return True


class CheckLinterRule(Rule):
    """Handles the 'check_linter_pep8' short rule using the flake8 legacy API."""

    def __init__(self, config: ShortRuleConfig, console: Console):
        """Initializes a PEP8 linter check rule handler."""
        self.config = config
        self._console = console
        self.DEFAULT_IGNORE = ["E501", "W503"]

    def execute(self, tree: ast.Module | None, source_code: str | None = None) -> bool:
        """Executes the flake8 linter by writing the source to a temporary file."""
        if not source_code:
            self._console.print("Source code is empty, skipping PEP8 check.", level="WARNING")
            return True

        self._console.print(f"Rule {self.config.rule_id}: Running flake8 linter...", level="DEBUG")

        # Создаем временный файл с расширением .py
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as tmp_file:
            tmp_file.write(source_code)
            tmp_filepath = tmp_file.name

        tmp_path = Path(tmp_filepath)

        try:
            # 1. Собираем список игнорируемых ошибок
            ignore_list = list(set(self.config.params.get("ignore", []) + self.DEFAULT_IGNORE))

            # 2. Создаем StyleGuide
            style_guide = flake8.get_style_guide(
                ignore=ignore_list,
                select=self.config.params.get("select", []),
                max_line_length=120,
            )

            # 3. Перехватываем вывод flake8
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                report = style_guide.check_files([str(tmp_path)])

            # 5. Проверяем результат
            if report.total_errors > 0:
                linter_output = output_buffer.getvalue().strip()
                self._console.print(
                    f"Flake8 found {report.total_errors} issue(s). Full report in DEBUG logs.", level="DEBUG"
                )
                self._console.print(linter_output, level="DEBUG")
                return False

            self._console.print("PEP8 check passed.", level="DEBUG")
            return True
        finally:
            # 6. Гарантированно удаляем временный файл
            if tmp_path.exists():
                tmp_path.unlink()


class FullRuleHandler(Rule):
    """Handles a full rule with a selector and a constraint."""

    def __init__(self, config: FullRuleConfig, selector: Selector, constraint: Constraint, console: Console):
        """Initializes a full rule handler."""
        self.config = config
        self._selector = selector
        self._constraint = constraint
        self._console = console

    def execute(self, tree: ast.Module | None, source_code: str | None = None) -> bool:
        """Executes the rule by running the selector and applying the constraint."""
        if not tree:
            # Большинство полных правил требуют AST
            self._console.print("AST not available, skipping rule.", level="WARNING")
            return True

        self._console.print(f"Applying selector: {self._selector.__class__.__name__}", level="DEBUG")
        selected_nodes = self._selector.select(tree)

        self._console.print(f"Applying constraint: {self._constraint.__class__.__name__}", level="DEBUG")
        return self._constraint.check(selected_nodes)
