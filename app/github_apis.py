import requests
import os
import logging

logger = logging.getLogger(__name__)

def fetch_repo_contents(api_url):
    logger.info(f"Fetching repo contents from: {api_url}")
    
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is not set in fetch_repo_contents")
        return None
    
    headers = {
        'Authorization': 'token ' + github_token
    }
    
    response = requests.get(api_url, headers=headers)  # Add authentication headers if needed
    logger.info(f"GitHub API response status: {response.status_code}")
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"GitHub API error response: {response.text}")
        logger.error(f"Response headers: {dict(response.headers)}")
        return None

def generate_markdown(contents, level=0):
    markdown = ""
    for content in contents:
        prefix = "    " * level  # Indentation
        if content['type'] == 'dir':
            # Recursively fetch and generate markdown for subdirectories
            subcontents = fetch_repo_contents(content['url'])
            markdown += f"{prefix}- [{content['name']}]({content['html_url']})\n"
            markdown += generate_markdown(subcontents, level + 1)
        else:
            # Generate markdown for a file
            markdown += f"{prefix}- [{content['name']}]({content['html_url']})\n"
    return markdown
