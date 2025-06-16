from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import Any


class ExitCode(IntEnum):
    SUCCESS = 0
    VALIDATION_FAILED = 1
    FILE_NOT_FOUND = 2
    JSON_ERROR = 3
    UNEXPECTED_ERROR = 10


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class AppConfig:
    solution_path: Path
    rules_path: Path
    log_level: LogLevel
    is_silent: bool
    stop_on_first_fail: bool


@dataclass(frozen=True)
class SelectorConfig:
    type: str
    name: str | None = None
    node_type: str | list[str] | None = None
    in_scope: str | dict[str, Any] | None = None


@dataclass(frozen=True)
class ConstraintConfig:
    type: str
    count: int | None = None
    parent_name: str | None = None
    expected_type: str | None = None
    allowed_names: list[str] | None = None
    allowed_values: list[Any] | None = None
    names: list[str] | None = None
    exact_match: bool | None = None


@dataclass(frozen=True)
class FullRuleCheck:
    selector: SelectorConfig
    constraint: ConstraintConfig


@dataclass(frozen=True)
class ShortRuleConfig:
    rule_id: int
    type: str
    message: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FullRuleConfig:
    rule_id: int
    message: str
    check: FullRuleCheck
    is_critical: bool = False


ValidationRuleConfig = ShortRuleConfig | FullRuleConfig
