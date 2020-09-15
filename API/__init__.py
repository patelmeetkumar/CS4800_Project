import json
import os
import markdown

# Import the framework
from flask import Flask, request
from flask_restful import Api

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


@app.route('/')
def index():
    """HTML documentation about the API"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


# @app.route('/')
# def get():
#     """GET request"""

def web_scraper(url):
    """
    Scrapes a webpage for necessary components for detection services
    :param url: URL for webpage to be scraped
    :return: JSON of components that have been scraped
    """
    json_deliverable = {}

    # CODE GOES HERE

    return json.dumps(json_deliverable)
