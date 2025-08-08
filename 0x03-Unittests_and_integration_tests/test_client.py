#!/usr/bin/env python3
"""Unit test for GithubOrgClient.org"""

# test_client.py

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from utils import access_nested_map


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.

    This test suite covers:
    - Accessing the public repositories URL via _public_repos_url
    - Retrieving public repositories via public_repos()
    - Ensuring proper use of memoization and mocking
    """
    def test_public_repos_url(self):
        expected_url = "https://api.github.com/orgs/testorg/repos"
        payload = {"repos_url": expected_url}

        with patch.object(
            GithubOrgClient,
            "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            return_value="https://api.github.com/orgs/testorg/repos"
        ) as mock_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )


if __name__ == "__main__":
    unittest.main()
