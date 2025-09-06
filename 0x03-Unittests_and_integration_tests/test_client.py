#!/usr/bin/env python3
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos
)


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"any": "value"}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )
        self.assertEqual(result, mock_get_json.return_value)

    def test_public_repos_url(self):
        fake = {"repos_url": "https://api.github.com/orgs/test/repos"}
        with patch.object(
            GithubOrgClient, "org",
            new_callable=PropertyMock,
            return_value=fake
        ):
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, fake["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = repos_payload
        with patch.object(
            GithubOrgClient, "_public_repos_url",
            new_callable=PropertyMock,
            return_value=org_payload["repos_url"]
        ) as mock_url:
            client = GithubOrgClient("holberton-schools")
            result = client.public_repos()

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(org_payload["repos_url"])
            self.assertEqual(result, expected_repos)

    @parameterized.expand([
        ({"license": {"key": "apache-2.0"}}, "apache-2.0", True),
        ({"license": {"key": "mit"}}, "apache-2.0", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [(org_payload, repos_payload, expected_repos, apache2_repos)]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Patch requests.get so .json() returns our fixtures
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def get_side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url == GithubOrgClient.ORG_URL.format(org=cls.org_payload["login"]):
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        cls.mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self):
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )