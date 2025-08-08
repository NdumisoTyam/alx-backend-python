#!/usr/bin/env python3
"""Unit test for GithubOrgClient.org"""

# test_client.py

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    def test_public_repos_url(self):
        # Arrange: expected URL and mock payload
        expected_url = "https://api.github.com/orgs/testorg/repos"
        payload = {"repos_url": expected_url}

        # Act: patch the 'org' property to return the mock payload
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            # Assert: check that the result matches the expected URL
            self.assertEqual(result, expected_url)

if __name__ == "__main__":
    unittest.main()
