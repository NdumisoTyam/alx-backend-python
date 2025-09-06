#!/usr/bin/env python3
"""
client module
"""

from typing import Any, Dict, List
from utils import get_json


class GithubOrgClient:
    """Client to interact with the GitHub Organizations API."""
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    @property
    def org(self) -> Dict[str, Any]:
        """
        Retrieve the organization’s JSON payload from GitHub.

        Returns:
            The dict returned by utils.get_json for the org endpoint.
        """
        return get_json(self.ORG_URL.format(org=self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """
        Read off the `repos_url` field from the org payload.

        Returns:
            The URL to list this organization’s public repositories.
        """
        return self.org["repos_url"]

    def public_repos(self) -> List[str]:
        """
        Fetch the list of public repositories for the organization.

        Returns:
            A list of repository names.
        """
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

    @staticmethod
    def has_license(repo: Dict[str, Any], license_key: str) -> bool:
        """
        Determine whether a given repository dict has the specified license.

        Args:
            repo: A dict representing a single repo’s JSON.
            license_key: The license key to check for.

        Returns:
            True if repo["license"]["key"] == license_key, False otherwise.
        """
        return repo.get("license", {}).get("key") == license_key