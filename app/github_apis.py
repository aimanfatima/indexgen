import requests

def fetch_repo_contents(api_url):
    headers = {
    }
    response = requests.get(api_url, headers=headers)  # Add authentication headers if needed
    if response.status_code == 200:
        return response.json()
    else:
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
