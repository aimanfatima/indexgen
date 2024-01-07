from flask import request, jsonify, Blueprint, render_template
from .github_apis import fetch_repo_contents, generate_markdown
from .utils.github_utils import convert_repo_url_to_api_endpoint

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return render_template('index.html')

@api.route('/generate-markdown', methods=['POST'])
def generate_linked_markdown():
    data = request.json  # Get JSON data from request
    repo_url = data.get("repo_url")

    if not repo_url:
        return jsonify({"error": "No repo URL provided"}), 400

    # Assuming repo_url is directly usable or transform it as needed
    try:
        contents_api_url = convert_repo_url_to_api_endpoint(repo_url)
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