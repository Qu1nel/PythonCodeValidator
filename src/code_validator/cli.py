"""Defines the command-line interface for the code validator.

This module is responsible for parsing command-line arguments, setting up the
application configuration, and orchestrating the main validation workflow. It acts
as the primary entry point for user interaction when the tool is called from
the terminal.

The main function, `run_from_cli`, handles the entire application lifecycle,
including robust top-level error handling to ensure meaningful exit codes.
"""

import argparse
import sys
from pathlib import Path

from . import __version__
from .config import AppConfig, ExitCode, LogLevel
from .core import StaticValidator
from .exceptions import CodeValidatorError
from .output import Console, setup_logging


def setup_arg_parser() -> argparse.ArgumentParser:
    """Creates and configures the argument parser for the CLI.

    This function defines all positional and optional arguments that the
    `validate-code` command accepts, including their types, help messages,
    and default values.

    Returns:
        argparse.ArgumentParser: A fully configured parser instance ready to
            process command-line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="validate-code",
        description="Validates a Python source file against a set of JSON rules.",
    )

    parser.add_argument("solution_path", type=Path, help="Path to the Python solution file to validate.")
    parser.add_argument("rules_path", type=Path, help="Path to the JSON file with validation rules.")

    parser.add_argument(
        "--log",
        type=LogLevel,
        default=LogLevel.ERROR,
        help=("Set the logging level for stderr (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL). Default: ERROR."),
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress all stdout output (validation errors and final verdict)."
    )
    parser.add_argument("--no-verdict", action="store_true", help="Suppress stdout output verdict, show failed rules.")
    parser.add_argument("--stop-on-first-fail", action="store_true", help="Stop after the first failed rule.")
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {__version__}")
    return parser


def run_from_cli() -> None:
    """Runs the full application lifecycle from the command line.

    This is the main entry point for the `validate-code` script. It performs
    the following steps:
    1. Parses command-line arguments.
    2. Initializes the logger, console, and configuration.
    3. Instantiates and runs the `StaticValidator`.
    4. Handles all top-level exceptions and exits with an appropriate status code.

    Raises:
        SystemExit: This function will always terminate the process with an
            exit code defined in the `ExitCode` enum.
    """
    parser = setup_arg_parser()
    args = parser.parse_args()

    logger = setup_logging(args.log)
    console = Console(logger, is_quiet=args.quiet, show_verdict=not args.no_verdict)
    console.print(f"Level of logging: {args.log}", level=LogLevel.DEBUG)
    config = AppConfig(
        solution_path=args.solution_path,
        rules_path=args.rules_path,
        log_level=args.log,
        is_quiet=args.quiet,
        stop_on_first_fail=args.stop_on_first_fail,
    )
    console.print(f"Config is: {config}", level=LogLevel.TRACE)

    try:
        console.print(f"Starting validation for: {config.solution_path}", level=LogLevel.INFO)
        validator = StaticValidator(config, console)

        console.print("Start of validation..", level=LogLevel.TRACE)
        is_valid = validator.run()
        console.print(f"End of validation with result: {is_valid = }", level=LogLevel.TRACE)

        if is_valid:
            console.print("Validation successful.", level=LogLevel.INFO, is_verdict=True)
            sys.exit(ExitCode.SUCCESS)
        else:
            console.print("Validation failed.", level=LogLevel.INFO, is_verdict=True)
            sys.exit(ExitCode.VALIDATION_FAILED)

    except CodeValidatorError as e:
        console.print("Error: Internal Error of validator!", level=LogLevel.CRITICAL)
        logger.exception(f"Traceback for CodeValidatorError: {e}")
        sys.exit(ExitCode.VALIDATION_FAILED)
    except FileNotFoundError as e:
        console.print(f"Error: File not found - {e.filename}!", level=LogLevel.CRITICAL)
        logger.exception(f"Traceback for FileNotFoundError: {e}")
        sys.exit(ExitCode.FILE_NOT_FOUND)
    except Exception as e:
        console.print(f"An unexpected error occurred: {e.__class__.__name__}!", level=LogLevel.CRITICAL)
        logger.exception(f"Traceback for unexpected error: {e}")
        sys.exit(ExitCode.UNEXPECTED_ERROR)
