"""Integration tests for typo detection with the validation system."""

import json
import unittest
from pathlib import Path

from src.code_validator.config import AppConfig, LogLevel
from src.code_validator.core import StaticValidator
from src.code_validator.output import Console, setup_logging


class TestTypoDetectionIntegration(unittest.TestCase):
    """Integration tests for typo detection with the full validation system."""
    
    def setUp(self):
        """Set up test environment."""
        self.logger = setup_logging(LogLevel.DEBUG)
        self.console = Console(self.logger, is_quiet=True)
        
        # Create test files
        self.test_code = '''
class Hero:
    def __init__(self):
        self.scale = 1.0
        self.sped = 300  # Typo: should be 'speed'
        self.health = 100
        self.center_x = 50
        self.centre_y = 50  # Typo: should be 'center_y'

def proces_data():  # Typo: should be 'process_data'
    pass
'''
        
        self.test_rules = {
            "validation_rules": [
                {
                    "rule_id": 1,
                    "message": "Required attribute 'self.speed' not found in Hero.__init__.",
                    "check": {
                        "selector": {
                            "type": "assignment",
                            "name": "self.speed",
                            "in_scope": {
                                "class": "Hero",
                                "method": "__init__"
                            }
                        },
                        "constraint": {
                            "type": "is_required"
                        }
                    }
                },
                {
                    "rule_id": 2,
                    "message": "Required attribute 'self.center_y' not found in Hero.__init__.",
                    "check": {
                        "selector": {
                            "type": "assignment",
                            "name": "self.center_y",
                            "in_scope": {
                                "class": "Hero",
                                "method": "__init__"
                            }
                        },
                        "constraint": {
                            "type": "is_required"
                        }
                    }
                },
                {
                    "rule_id": 3,
                    "message": "Required function 'process_data' not found.",
                    "check": {
                        "selector": {
                            "type": "function_def",
                            "name": "process_data",
                            "in_scope": "global"
                        },
                        "constraint": {
                            "type": "is_required"
                        }
                    }
                }
            ]
        }
    
    def test_typo_detection_in_validation(self):
        """Test that typo detection works during full validation."""
        # Create temporary files
        code_path = Path("temp_typo_test.py")
        rules_path = Path("temp_typo_rules.json")
        
        code_path.write_text(self.test_code, encoding="utf-8")
        rules_path.write_text(json.dumps(self.test_rules, indent=2), encoding="utf-8")
        
        try:
            config = AppConfig(
                solution_path=code_path,
                rules_path=rules_path,
                log_level=LogLevel.DEBUG,
                is_quiet=True,
                exit_on_first_error=False,
            )
            
            validator = StaticValidator(config, self.console)
            result = validator.run()
            
            # Validation should fail due to typos
            self.assertFalse(result, "Validation should fail due to typos")
            self.assertEqual(len(validator.failed_rules_id), 3, "All 3 rules should fail")
            
            # Check that failed rules have the expected IDs
            failed_ids = [rule.config.rule_id for rule in validator.failed_rules_id]
            self.assertIn(1, failed_ids, "Rule 1 (self.speed) should fail")
            self.assertIn(2, failed_ids, "Rule 2 (self.center_y) should fail")
            self.assertIn(3, failed_ids, "Rule 3 (process_data) should fail")
            
        finally:
            # Clean up temporary files
            code_path.unlink(missing_ok=True)
            rules_path.unlink(missing_ok=True)
    
    def test_typo_suggestions_in_logs(self):
        """Test that typo suggestions appear in debug logs."""
        # Create temporary files
        code_path = Path("temp_typo_log_test.py")
        rules_path = Path("temp_typo_log_rules.json")
        
        # Simple test case with one clear typo
        simple_code = '''
class Hero:
    def __init__(self):
        self.sped = 300  # Should be 'speed'
'''
        
        simple_rules = {
            "validation_rules": [
                {
                    "rule_id": 1,
                    "message": "Required attribute 'self.speed' not found.",
                    "check": {
                        "selector": {
                            "type": "assignment",
                            "name": "self.speed",
                            "in_scope": {
                                "class": "Hero",
                                "method": "__init__"
                            }
                        },
                        "constraint": {
                            "type": "is_required"
                        }
                    }
                }
            ]
        }
        
        code_path.write_text(simple_code, encoding="utf-8")
        rules_path.write_text(json.dumps(simple_rules, indent=2), encoding="utf-8")
        
        try:
            # Capture console output
            import io
            import sys
            from contextlib import redirect_stderr
            
            captured_output = io.StringIO()
            
            # Create logger that writes to our captured output
            import logging
            test_logger = logging.getLogger("test_typo")
            test_logger.setLevel(LogLevel.DEBUG)
            
            # Clear any existing handlers
            test_logger.handlers.clear()
            
            # Add handler that writes to our captured output
            handler = logging.StreamHandler(captured_output)
            handler.setLevel(LogLevel.DEBUG)
            test_logger.addHandler(handler)
            
            console = Console(test_logger, is_quiet=True)
            
            config = AppConfig(
                solution_path=code_path,
                rules_path=rules_path,
                log_level=LogLevel.DEBUG,
                is_quiet=True,
                exit_on_first_error=False,
            )
            
            validator = StaticValidator(config, console)
            result = validator.run()
            
            # Get the captured log output
            log_output = captured_output.getvalue()
            
            # Validation should fail
            self.assertFalse(result)
            
            # Check that typo detection information appears in logs
            # Note: The exact format may vary, so we check for key indicators
            self.assertTrue(
                "typo" in log_output.lower() or "suggestion" in log_output.lower(),
                f"Expected typo detection info in logs. Got: {log_output}"
            )
            
        finally:
            # Clean up temporary files
            code_path.unlink(missing_ok=True)
            rules_path.unlink(missing_ok=True)
    
    def test_no_false_positives(self):
        """Test that typo detection doesn't trigger false positives."""
        # Code with correct names - no typos
        correct_code = '''
class Hero:
    def __init__(self):
        self.speed = 300
        self.health = 100
        self.center_x = 50
        self.center_y = 50

def process_data():
    pass
'''
        
        code_path = Path("temp_correct_test.py")
        rules_path = Path("temp_correct_rules.json")
        
        code_path.write_text(correct_code, encoding="utf-8")
        rules_path.write_text(json.dumps(self.test_rules, indent=2), encoding="utf-8")
        
        try:
            config = AppConfig(
                solution_path=code_path,
                rules_path=rules_path,
                log_level=LogLevel.DEBUG,
                is_quiet=True,
                exit_on_first_error=False,
            )
            
            validator = StaticValidator(config, self.console)
            result = validator.run()
            
            # Validation should pass - no typos, all required elements present
            self.assertTrue(result, "Validation should pass with correct code")
            self.assertEqual(len(validator.failed_rules_id), 0, "No rules should fail")
            
        finally:
            # Clean up temporary files
            code_path.unlink(missing_ok=True)
            rules_path.unlink(missing_ok=True)
    
    def test_performance_with_large_scope(self):
        """Test that typo detection performs reasonably with large scopes."""
        # Create code with many attributes to test performance limits
        large_code = '''
class LargeClass:
    def __init__(self):
        # Create many attributes to test performance
'''
        
        # Add many attributes
        for i in range(100):
            large_code += f"        self.attribute_{i} = {i}\n"
        
        # Add the typo at the end
        large_code += "        self.sped = 300  # Should be 'speed'\n"
        
        large_rules = {
            "validation_rules": [
                {
                    "rule_id": 1,
                    "message": "Required attribute 'self.speed' not found.",
                    "check": {
                        "selector": {
                            "type": "assignment",
                            "name": "self.speed",
                            "in_scope": {
                                "class": "LargeClass",
                                "method": "__init__"
                            }
                        },
                        "constraint": {
                            "type": "is_required"
                        }
                    }
                }
            ]
        }
        
        code_path = Path("temp_large_test.py")
        rules_path = Path("temp_large_rules.json")
        
        code_path.write_text(large_code, encoding="utf-8")
        rules_path.write_text(json.dumps(large_rules, indent=2), encoding="utf-8")
        
        try:
            import time
            start_time = time.time()
            
            config = AppConfig(
                solution_path=code_path,
                rules_path=rules_path,
                log_level=LogLevel.CRITICAL,  # Reduce log noise
                is_quiet=True,
                exit_on_first_error=False,
            )
            
            validator = StaticValidator(config, self.console)
            result = validator.run()
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Should complete in reasonable time (less than 5 seconds)
            self.assertLess(execution_time, 5.0, 
                          f"Typo detection took too long: {execution_time:.2f}s")
            
            # Should still find the typo
            self.assertFalse(result, "Should still detect the typo in large scope")
            
        finally:
            # Clean up temporary files
            code_path.unlink(missing_ok=True)
            rules_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()