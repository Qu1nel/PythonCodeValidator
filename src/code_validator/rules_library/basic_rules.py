import ast
import subprocess
import sys

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
    """Handles the 'check_linter_pep8' short rule by running flake8 as a subprocess."""

    def __init__(self, config: ShortRuleConfig, console: Console):
        self.config = config
        self._console = console

    def execute(self, tree: ast.Module | None, source_code: str | None = None) -> bool:
        """Executes the flake8 linter on the source code via a subprocess."""
        if not source_code:
            self._console.print("Source code is empty, skipping PEP8 check.", level="WARNING")
            return True

        self._console.print(f"Rule {self.config.rule_id}: Running flake8 linter...", level="DEBUG")

        # 1. Собираем аргументы для flake8
        params = self.config.params
        args = [
            sys.executable,  # Путь к текущему интерпретатору python
            "-m",
            "flake8",
            "-",  # Специальный флаг, говорящий flake8 читать из stdin
        ]

        if select_list := params.get("select"):
            args.append(f"--select={','.join(select_list)}")
        elif ignore_list := params.get("ignore"):
            args.append(f"--ignore={','.join(ignore_list)}")

        try:
            # 2. Запускаем flake8 как отдельный процесс
            #    - передаем код через stdin
            #    - перехватываем stdout и stderr
            process = subprocess.run(
                args,
                input=source_code,
                capture_output=True,
                text=True,  # Работаем с текстом, а не байтами
                encoding="utf-8",
                check=False,  # Не выбрасывать исключение при ненулевом коде выхода
            )

            # 3. Анализируем результат
            if process.returncode != 0 and process.stdout:
                # Если flake8 вернул ненулевой код и что-то напечатал, значит есть ошибки
                linter_output = process.stdout.strip()
                self._console.print(f"Flake8 found issues:\n{linter_output}", level="DEBUG")
                return False
            elif process.returncode != 0:
                # Если код ненулевой, но вывод пустой, значит произошла ошибка в самом flake8
                self._console.print(f"Flake8 exited with code {process.returncode}:\n{process.stderr}", level="ERROR")
                return False

            self._console.print("PEP8 check passed.", level="DEBUG")
            return True

        except FileNotFoundError:
            self._console.print("flake8 not found. Is it installed in the venv?", level="CRITICAL")
            return False
        except Exception as e:
            self._console.print(f"An unexpected error occurred while running flake8: {e}", level="CRITICAL")
            return False


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
