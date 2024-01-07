def convert_repo_url_to_api_endpoint(repo_url, branch='master'):
    """
    Convert a GitHub repo URL to the GitHub API contents URL.

    :param repo_url: URL of the GitHub repository (string)
    :param branch: Branch name (string), default is 'master'
    :return: API URL for the repository contents (string)
    """
    # Remove the trailing slash if it exists
    if repo_url.endswith('/'):
        repo_url = repo_url[:-1]

    # Split the URL to get individual components
    parts = repo_url.split('/')

    # Extract the username and repository name
    username = parts[-2]
    repository = parts[-1]

    # Construct the API URL
    api_url = f"https://api.github.com/repos/{username}/{repository}/contents?ref={branch}"
    print(api_url)
    return api_url

def get_user_and_repo_from_url(repo_url):
    # Remove the trailing slash if it exists
    if repo_url.endswith('/'):
        repo_url = repo_url[:-1]

    # Split the URL to get individual components
    parts = repo_url.split('/')

    # Extract the username and repository name
    username = parts[-2]
    repository = parts[-1]

    return username, repository