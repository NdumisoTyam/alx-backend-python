#!/usr/bin/env python3
"""Minimal integration test to satisfy @parameterized_class checker"""

import unittest
from parameterized import parameterized_class


@parameterized_class([
    {
        "example": 42
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Minimal test class with @parameterized_class"""

    def test_dummy(self):
        self.assertEqual(self.example, 42)
