import dataclasses
from typing import Any, Type, TypeVar

from ..config import ConstraintConfig, FullRuleCheck, FullRuleConfig, SelectorConfig, ShortRuleConfig
from ..exceptions import RuleParsingError
from ..output import Console
from ..rules_library.basic_rules import CheckLinterRule, CheckSyntaxRule, FullRuleHandler
from ..rules_library.constraint_logic import (
    IsForbiddenConstraint,
    IsRequiredConstraint,
    MustBeTypeConstraint,
    MustHaveArgsConstraint,
    MustInheritFromConstraint,
    NameMustBeInConstraint,
    ValueMustBeInConstraint,
)
from ..rules_library.selector_nodes import (
    AssignmentSelector,
    AstNodeSelector,
    ClassDefSelector,
    FunctionCallSelector,
    FunctionDefSelector,
    ImportStatementSelector,
    LiteralSelector,
    UsageSelector,
)
from .definitions import Constraint, Rule, Selector

T = TypeVar("T")


def _create_dataclass_from_dict(cls: Type[T], data: dict[str, Any]) -> T:
    """Safely creates a dataclass instance from a dictionary, ignoring extra keys."""
    expected_fields = {f.name for f in dataclasses.fields(cls)}
    filtered_data = {k: v for k, v in data.items() if k in expected_fields}
    return cls(**filtered_data)


class RuleFactory:
    def __init__(self, console: Console):
        self._console = console
        self._selector_factory = SelectorFactory()
        self._constraint_factory = ConstraintFactory()

    def create(self, rule_config: dict[str, Any]) -> Rule:
        rule_id = rule_config.get("rule_id")
        try:
            if "type" in rule_config:
                config = _create_dataclass_from_dict(ShortRuleConfig, rule_config)
                return self._create_short_rule(config)

            elif "check" in rule_config:
                raw_selector_cfg = rule_config["check"]["selector"]
                raw_constraint_cfg = rule_config["check"]["constraint"]

                selector = self._selector_factory.create(raw_selector_cfg)
                constraint = self._constraint_factory.create(raw_constraint_cfg)

                selector_cfg = _create_dataclass_from_dict(SelectorConfig, raw_selector_cfg)
                constraint_cfg = _create_dataclass_from_dict(ConstraintConfig, raw_constraint_cfg)
                check_cfg = FullRuleCheck(selector=selector_cfg, constraint=constraint_cfg)
                config = FullRuleConfig(
                    rule_id=rule_config["rule_id"],
                    message=rule_config["message"],
                    check=check_cfg,
                    is_critical=rule_config.get("is_critical", False),
                )

                # 4. Создаем и возвращаем обработчик
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
    @staticmethod
    def create(selector_config: dict[str, Any]) -> Selector:
        config = _create_dataclass_from_dict(SelectorConfig, selector_config)

        match config.type:
            case "function_def":
                return FunctionDefSelector(name=config.name, in_scope_config=config.in_scope)
            case "class_def":
                return ClassDefSelector(name=config.name, in_scope_config=config.in_scope)
            case "import_statement":
                return ImportStatementSelector(name=config.name, in_scope_config=config.in_scope)
            case "function_call":
                return FunctionCallSelector(name=config.name, in_scope_config=config.in_scope)
            case "assignment":
                return AssignmentSelector(name=config.name, in_scope_config=config.in_scope)
            case "usage":
                return UsageSelector(name=config.name, in_scope_config=config.in_scope)
            case "literal":
                return LiteralSelector(name=config.name, in_scope_config=config.in_scope)
            case "ast_node":
                return AstNodeSelector(node_type=config.node_type, in_scope_config=config.in_scope)
            case _:
                raise RuleParsingError(f"Unknown selector type: '{config.type}'")


class ConstraintFactory:
    """Creates constraint objects from raw dictionary configuration."""

    @staticmethod
    def create(constraint_config: dict[str, Any]) -> Constraint:
        config = _create_dataclass_from_dict(ConstraintConfig, constraint_config)

        match config.type:
            case "is_required":
                return IsRequiredConstraint(count=config.count)
            case "is_forbidden":
                return IsForbiddenConstraint()
            case "must_inherit_from":
                return MustInheritFromConstraint(parent_name=config.parent_name)
            case "must_be_type":
                return MustBeTypeConstraint(expected_type=config.expected_type)
            case "must_have_args":
                return MustHaveArgsConstraint(count=config.count, names=config.names, exact_match=config.exact_match)
            case "name_must_be_in":
                return NameMustBeInConstraint(allowed_names=config.allowed_names)
            case "value_must_be_in":
                return ValueMustBeInConstraint(allowed_values=config.allowed_values)
            case _:
                raise RuleParsingError(f"Unknown constraint type: '{config.type}'")
