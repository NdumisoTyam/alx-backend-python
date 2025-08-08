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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        # Arrange: mock return value for get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        # Act: patch _public_repos_url to return a dummy URL
        with patch.object(GithubOrgClient, "_public_repos_url", return_value="https://api.github.com/orgs/testorg/repos") as mock_url:
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # Assert: check repo names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Assert: check that mocks were called once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")

if __name__ == "__main__":
    unittest.main()
