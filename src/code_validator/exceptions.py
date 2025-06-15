class CodeValidatorError(Exception):
    """Base exception for all errors raised by this application."""


class RuleParsingError(CodeValidatorError):
    """Raised when a validation rule in the JSON file is malformed."""

    def __init__(self, message: str, rule_id: int | str | None = None):
        self.rule_id = rule_id
        if rule_id:
            super().__init__(f"Error parsing rule '{rule_id}': {message}")
        else:
            super().__init__(f"Error parsing rules file: {message}")


class ValidationFailedError(CodeValidatorError):
    """Raised to signal that the source code did not pass validation."""
