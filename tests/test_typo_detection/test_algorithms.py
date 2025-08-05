"""Tests for string similarity algorithms."""

import unittest

from src.code_validator.components.typo_detection.algorithms import LevenshteinDistance


class TestLevenshteinDistance(unittest.TestCase):
    """Test cases for Levenshtein distance algorithm."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.algo = LevenshteinDistance()
    
    def test_identical_strings(self):
        """Test distance between identical strings."""
        self.assertEqual(self.algo.distance("speed", "speed"), 0)
        self.assertEqual(self.algo.similarity("speed", "speed"), 1.0)
    
    def test_empty_strings(self):
        """Test distance with empty strings."""
        self.assertEqual(self.algo.distance("", ""), 0)
        self.assertEqual(self.algo.distance("", "abc"), 3)
        self.assertEqual(self.algo.distance("abc", ""), 3)
        self.assertEqual(self.algo.similarity("", ""), 1.0)
    
    def test_single_character_operations(self):
        """Test single character insertions, deletions, substitutions."""
        # Single insertion
        self.assertEqual(self.algo.distance("sped", "speed"), 1)
        
        # Single deletion  
        self.assertEqual(self.algo.distance("speed", "sped"), 1)
        
        # Single substitution
        self.assertEqual(self.algo.distance("speed", "spend"), 1)
    
    def test_multiple_operations(self):
        """Test multiple character operations."""
        self.assertEqual(self.algo.distance("kitten", "sitting"), 3)
        self.assertEqual(self.algo.distance("saturday", "sunday"), 3)
    
    def test_similarity_scores(self):
        """Test similarity score calculations."""
        # Very similar strings
        similarity = self.algo.similarity("speed", "sped")
        self.assertGreaterEqual(similarity, 0.8)
        
        # Moderately similar strings
        similarity = self.algo.similarity("speed", "scale")
        self.assertGreater(similarity, 0.1)
        self.assertLess(similarity, 0.5)
        
        # Very different strings
        similarity = self.algo.similarity("speed", "xyz")
        self.assertLess(similarity, 0.1)
    
    def test_real_typo_examples(self):
        """Test with real-world typo examples."""
        # Common attribute typos
        self.assertEqual(self.algo.distance("self.speed", "self.sped"), 1)
        self.assertEqual(self.algo.distance("self.center_x", "self.centre_x"), 2)  # 'er' -> 're'
        self.assertEqual(self.algo.distance("self.health", "self.helth"), 1)  # 'ea' -> 'e'
        
        # Function name typos
        self.assertEqual(self.algo.distance("update", "updat"), 1)
        self.assertEqual(self.algo.distance("initialize", "initalize"), 1)
    
    def test_case_sensitivity(self):
        """Test that algorithm is case sensitive."""
        self.assertEqual(self.algo.distance("Speed", "speed"), 1)
        self.assertLess(self.algo.similarity("Speed", "speed"), 1.0)


if __name__ == "__main__":
    unittest.main()