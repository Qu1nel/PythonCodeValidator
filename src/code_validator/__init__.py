"""Code Validator: A flexible framework for static code analysis."""

from .config import AppConfig, ExitCode
from .core import StaticValidator
from .exceptions import RuleParsingError, ValidationFailedError

__all__ = [
    "StaticValidator",
    "AppConfig",
    "ExitCode",
    "ValidationFailedError",
    "RuleParsingError",
]
__version__ = "0.1.0"
