from __future__ import annotations

class AppError(Exception):
    """Base class for all domain-specific errors in clevertools."""

class RecoverableError(AppError):
    """Error indicating the current operation can be skipped safely."""

class FatalError(AppError):
    """Error indicating execution should stop immediately."""

class ValidationError(RecoverableError):
    """Raised when input values fail semantic or structural validation."""

class ParseError(ValidationError):
    """Raised when a value or payload cannot be parsed into the expected format."""