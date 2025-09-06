org_payload = {
    "login": "holberton-schools",
    "id": 12345,
    "repos_url": "https://api.github.com/orgs/holberton-schools/repos"
}
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
]
expected_repos = [repo["name"] for repo in repos_payload]
apache2_repos = [repo["name"] for repo in repos_payload if
                 repo["license"]["key"] == "apache-2.0"]