import requests
import os
from flask import request, jsonify, Blueprint, render_template
from .github_apis import fetch_repo_contents, generate_markdown
from .utils.github_utils import convert_repo_url_to_api_endpoint, get_user_and_repo_from_url

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return render_template('index.html')

@api.route('/fetch-branches', methods=['POST'])
def fetch_branches():
    data = request.json

    # Extract user and repo from the request data
    user, repo = get_user_and_repo_from_url(data.get('repo_url'))

    # Construct the GitHub API URL for fetching branches
    branches_url = f"https://api.github.com/repos/{user}/{repo}/branches"

    # Make a request to the GitHub API to fetch the branches
    headers = {
        'Authorization': 'token ' + os.environ.get('GITHUB_TOKEN')
    }
    response = requests.get(branches_url, headers=headers)

    if response.status_code == 200:
        branches = response.json()
        # Extract just the names of the branches
        branch_names = [branch['name'] for branch in branches]
        return jsonify(branch_names)
    else:
        # Handle errors or no branches found
        return jsonify({"error": "Failed to fetch branches"}), response.status_code

@api.route('/generate-markdown', methods=['POST'])
def generate_linked_markdown():
    data = request.json  # Get JSON data from request
    repo_url = data.get("repo_url")
    branch = data.get("branch")

    if not repo_url:
        return jsonify({"error": "No repo URL provided"}), 400

    # Assuming repo_url is directly usable or transform it as needed
    try:
        contents_api_url = convert_repo_url_to_api_endpoint(repo_url, branch)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    # Fetch the contents of the repo
    contents = fetch_repo_contents(contents_api_url)
    if contents is None:
        return jsonify({"error": "Failed to fetch repo contents or Invalid repo URL"}), 500

    # Generate the markdown
    linked_markdown = generate_markdown(contents)

    # Return the linked markdown as JSON
    return jsonify({"linkedMarkdown": linked_markdown})