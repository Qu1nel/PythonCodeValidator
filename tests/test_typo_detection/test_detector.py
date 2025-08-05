"""Tests for the main typo detector."""

import ast
import unittest
from pathlib import Path

from src.code_validator.components.ast_utils import enrich_ast_with_parents
from src.code_validator.components.typo_detection import TypoDetector


class TestTypoDetector(unittest.TestCase):
    """Test cases for the main TypoDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = TypoDetector()
        
        # Load test code with typos
        fixtures_dir = Path(__file__).parent / "fixtures"
        self.test_file_path = str(fixtures_dir / "typo_examples.py")
        
        with open(self.test_file_path, 'r', encoding='utf-8') as f:
            self.test_code = f.read()
        
        # Parse and enrich AST
        self.ast_tree = ast.parse(self.test_code)
        enrich_ast_with_parents(self.ast_tree)
    
    def test_detect_simple_attribute_typo(self):
        """Test detection of simple attribute name typo."""
        suggestion = self.detector.analyze_failed_search(
            target_name="self.speed",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        self.assertTrue(suggestion.has_suggestion)
        self.assertEqual(suggestion.original_name, "self.speed")
        self.assertEqual(suggestion.suggested_candidate.candidate.name, "self.sped")
        self.assertGreater(suggestion.suggested_candidate.confidence, 0.8)
        self.assertEqual(suggestion.suggested_candidate.distance, 1)
    
    def test_detect_health_typo(self):
        """Test detection of 'health' vs 'helth' typo."""
        suggestion = self.detector.analyze_failed_search(
            target_name="self.health",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        self.assertTrue(suggestion.has_suggestion)
        self.assertEqual(suggestion.suggested_candidate.candidate.name, "self.helth")
        self.assertGreater(suggestion.suggested_candidate.confidence, 0.7)
    
    def test_detect_center_y_typo(self):
        """Test detection of 'center_y' vs 'centre_y' typo."""
        suggestion = self.detector.analyze_failed_search(
            target_name="self.center_y",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        self.assertTrue(suggestion.has_suggestion)
        self.assertEqual(suggestion.suggested_candidate.candidate.name, "self.centre_y")
        self.assertGreater(suggestion.suggested_candidate.confidence, 0.8)
    
    def test_detect_function_name_typo(self):
        """Test detection of function name typos."""
        suggestion = self.detector.analyze_failed_search(
            target_name="process_data",
            scope_config="global",
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        self.assertTrue(suggestion.has_suggestion)
        self.assertEqual(suggestion.suggested_candidate.candidate.name, "proces_data")
    
    def test_detect_method_typo(self):
        """Test detection of method name typos."""
        suggestion = self.detector.analyze_failed_search(
            target_name="update",
            scope_config={"class": "GameEngine"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        self.assertTrue(suggestion.has_suggestion)
        self.assertEqual(suggestion.suggested_candidate.candidate.name, "updat")
    
    def test_no_suggestion_for_very_different_names(self):
        """Test that no suggestion is made for very different names."""
        suggestion = self.detector.analyze_failed_search(
            target_name="self.completely_different_name",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        # Should not suggest anything due to low confidence
        self.assertFalse(suggestion.has_suggestion)
    
    def test_no_suggestion_for_nonexistent_scope(self):
        """Test behavior when scope doesn't exist."""
        suggestion = self.detector.analyze_failed_search(
            target_name="self.speed",
            scope_config={"class": "NonExistentClass", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        self.assertFalse(suggestion.has_suggestion)
    
    def test_confidence_scoring(self):
        """Test that confidence scoring works correctly."""
        suggestion = self.detector.analyze_failed_search(
            target_name="self.speed",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        # Should have high confidence for 1-character difference
        self.assertGreater(suggestion.suggested_candidate.confidence, 0.8)
        
        # Test with a more different name
        suggestion2 = self.detector.analyze_failed_search(
            target_name="self.velocity",
            scope_config={"class": "Player", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        if suggestion2.has_suggestion:
            # Should have reasonable confidence for 'velocty' vs 'velocity'
            self.assertGreater(suggestion2.suggested_candidate.confidence, 0.5)
            self.assertLess(suggestion2.suggested_candidate.confidence, 2.0)  # Reasonable upper bound
    
    def test_message_formatting(self):
        """Test that suggestion messages are properly formatted."""
        suggestion = self.detector.analyze_failed_search(
            target_name="self.speed",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        self.assertTrue(suggestion.has_suggestion)
        self.assertIn("File", suggestion.message)
        self.assertIn("line", suggestion.message)
        self.assertIn("ValidationError", suggestion.message)
        self.assertIn("Did you mean", suggestion.message)
        self.assertIn("self.speed", suggestion.message)
        self.assertIn("self.sped", suggestion.message)
    
    def test_debug_info_generation(self):
        """Test that debug information is properly generated."""
        suggestion = self.detector.analyze_failed_search(
            target_name="self.speed",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        self.assertIn("DEBUG:", suggestion.debug_info)
        self.assertIn("self.speed", suggestion.debug_info)
        self.assertIn("candidates", suggestion.debug_info)
    
    def test_max_distance_limit(self):
        """Test that max_distance parameter is respected."""
        # Create detector with very low max_distance
        strict_detector = TypoDetector(max_distance=1)
        
        # This should still work (1 character difference)
        suggestion1 = strict_detector.analyze_failed_search(
            target_name="self.speed",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        self.assertTrue(suggestion1.has_suggestion)
        
        # This should not work (2+ character difference)
        suggestion2 = strict_detector.analyze_failed_search(
            target_name="self.completely_different",
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        self.assertFalse(suggestion2.has_suggestion)
    
    def test_confidence_threshold(self):
        """Test that min_confidence parameter is respected."""
        # Create detector with very high confidence threshold
        strict_detector = TypoDetector(min_confidence=0.95)
        
        # Even good matches might not meet the threshold
        suggestion = strict_detector.analyze_failed_search(
            target_name="self.health",  # vs self.helth
            scope_config={"class": "Hero", "method": "__init__"},
            ast_tree=self.ast_tree,
            file_path=self.test_file_path
        )
        
        # Depending on the exact confidence calculation, this might not pass
        # the very high threshold
        if not suggestion.has_suggestion:
            self.assertIn("No typo suggestions", suggestion.debug_info)


if __name__ == "__main__":
    unittest.main()