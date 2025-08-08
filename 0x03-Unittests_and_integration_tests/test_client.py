#!/usr/bin/env python3
"""Unit tests and integration tests for GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.

    This test suite covers:
    - Accessing the public repositories URL via _public_repos_url
    - Retrieving public repositories via public_repos()
    - Checking license keys via has_license()
    - Ensuring proper use of memoization and mocking
    """

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct URL.

        This method mocks the GithubOrgClient.org property to ensure
        that the _public_repos_url method extracts the 'repos_url'
        field correctly from the organization payload.
        """
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
        """
        Test that public_repos returns the list of repository names.

        This method mocks both the _public_repos_url and get_json
        to simulate retrieving a list of repositories from the API.
        """
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns True if the repo's license matches
        the given license_key, otherwise False.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos using fixtures.

    Only external requests are mocked; internal logic is tested end-to-end.
    """

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and set up fixture responses."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/testorg":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all repo names."""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters by license key."""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


class MockResponse:
    """Mocked response object for requests.get().json()."""
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


if __name__ == "__main__":
    unittest.main()
