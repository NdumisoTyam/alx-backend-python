#!/usr/bin/env python3
"""Fixtures for GithubOrgClient integration tests."""

org_payload = {
    "repos_url": "https://api.github.com/orgs/testorg/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
    {"name": "repo4", "license": None}
]

expected_repos = ["repo1", "repo2", "repo3", "repo4"]
apache2_repos = ["repo1", "repo3"]
