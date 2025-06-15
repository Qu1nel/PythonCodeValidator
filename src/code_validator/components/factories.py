from typing import Any

from ..config import ConstraintConfig, FullRuleCheck, FullRuleConfig, SelectorConfig, ShortRuleConfig
from ..exceptions import RuleParsingError
from ..output import Console
from ..rules_library.basic_rules import CheckLinterRule, CheckSyntaxRule, FullRuleHandler
from ..rules_library.constraint_logic import (
    IsForbiddenConstraint,
    IsRequiredConstraint,
    MustBeTypeConstraint,
    MustInheritFromConstraint,
    NameMustBeInConstraint,
    ValueMustBeInConstraint,
)
from ..rules_library.selector_nodes import (
    AssignmentSelector,
    ClassDefSelector,
    FunctionCallSelector,
    FunctionDefSelector,
    ImportStatementSelector,
    LiteralSelector,
    UsageSelector,
)
from .definitions import Constraint, Rule, Selector


class RuleFactory:
    """Creates rule handler objects from raw dictionary configuration."""

    def __init__(self, console: Console):
        self._console = console
        self._selector_factory = SelectorFactory()
        self._constraint_factory = ConstraintFactory()

    def create(self, rule_config: dict[str, Any]) -> Rule:
        """Creates a specific rule instance based on its configuration."""
        rule_id = rule_config.get("rule_id")
        try:
            if "type" in rule_config:
                config = ShortRuleConfig(**rule_config)
                return self._create_short_rule(config)
            elif "check" in rule_config:
                # --- ЛОГИКА ДЛЯ ПОЛНЫХ ПРАВИЛ ---
                # 1. Парсим конфиг в датаклассы для валидации
                check_config = FullRuleCheck(**rule_config["check"])
                config = FullRuleConfig(**rule_config)

                # 2. Создаем компоненты через другие фабрики
                selector = self._selector_factory.create(check_config.selector.__dict__)
                constraint = self._constraint_factory.create(check_config.constraint.__dict__)

                # 3. Создаем и возвращаем обработчик
                return FullRuleHandler(config, selector, constraint, self._console)
            else:
                raise RuleParsingError("Rule must contain 'type' or 'check' key.", rule_id)
        except (TypeError, KeyError, RuleParsingError) as e:
            raise RuleParsingError(f"Invalid config for rule '{rule_id}': {e}", rule_id) from e

    def _create_short_rule(self, config: ShortRuleConfig) -> Rule:
        """Dispatches creation of short-rule handlers."""
        if config.type == "check_syntax":
            return CheckSyntaxRule(config, self._console)
        elif config.type == "check_linter_pep8":
            return CheckLinterRule(config, self._console)
        else:
            raise RuleParsingError(f"Unknown short rule type: '{config.type}'", config.rule_id)


class SelectorFactory:
    """Creates selector objects from raw dictionary configuration."""

    @staticmethod
    def create(selector_config: dict[str, Any]) -> Selector:
        config = SelectorConfig(**selector_config)
        # Используем match-case для чистоты и расширяемости
        match config.type:
            case "function_def":
                return FunctionDefSelector(**selector_config)
            case "class_def":
                return ClassDefSelector(**selector_config)
            case "import_statement":
                return ImportStatementSelector(**selector_config)
            case "function_call":
                return FunctionCallSelector(**selector_config)
            case "assignment":
                return AssignmentSelector(**selector_config)
            case "usage":
                return UsageSelector(**selector_config)
            case "literal":
                return LiteralSelector(**selector_config)
            case _:
                raise RuleParsingError(f"Unknown selector type: '{config.type}'")


class ConstraintFactory:
    """Creates constraint objects from raw dictionary configuration."""

    @staticmethod
    def create(constraint_config: dict[str, Any]) -> Constraint:
        config = ConstraintConfig(**constraint_config)
        match config.type:
            case "is_required":
                return IsRequiredConstraint(**constraint_config)
            case "must_inherit_from":
                return MustInheritFromConstraint(**constraint_config)
            case "is_forbidden":
                return IsForbiddenConstraint(**constraint_config)
            case "must_be_type":
                return MustBeTypeConstraint(**constraint_config)
            case "name_must_be_in":
                return NameMustBeInConstraint(**constraint_config)
            case "value_must_be_in":
                return ValueMustBeInConstraint(**constraint_config)
            case _:
                raise RuleParsingError(f"Unknown constraint type: '{config.type}'")
