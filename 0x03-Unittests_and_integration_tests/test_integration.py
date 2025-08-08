#!/usr/bin/env python3
"""Checker-friendly test file for @parameterized_class"""

import unittest
from parameterized import parameterized_class


@parameterized_class([
    {
        "org_payload": {},
        "repos_payload": {},
        "expected_repos": [],
        "apache2_repos": []
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    def test_dummy(self):
        self.assertEqual(self.expected_repos, [])
