import json
import os
import time
import random

import markdown
import requests
import pprint

# Import the framework
from flask import Flask
from flask import render_template, request, url_for, redirect
from flask_restful import Api


class Interface:
    # Interface class handles all connections
    @staticmethod
    def dev_guide(method):
        """HTML documentation about the API"""

        # Render dev readme when receiving GET request
        if method == "GET":
            # Open the README file
            with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
                # Read the content of the file
                content = markdown_file.read()

                # Convert to HTML
                return markdown.markdown(content, extensions=['tables'])

    @staticmethod
    def invalid_path(method):
        if method == "GET":
            return render_template('invalid_url.html')

    def webapp(self, method, form):
        """
        Web App interface, handles GET and POST requests
        :return: HTML template of result page with score
        """
        # Render submit_page when receiving GET request
        if method == 'GET':
            return render_template('submit_page.html')

        # Handle POST request
        if method == 'POST':
            # Get URL from POST request form
            url = form['url']
            print(url)
            # Get HTML from URL
            html = requests.get(url).content.decode().strip()
            # Parse webpage with web scraper
            page_data = WebScraper(html).scrape()
            # Construct dictionary containing URL and page_data from web scraping
            attribute_dict = {
                'url': url,
                'post_data': None,
                'page_data': page_data
            }
            print(attribute_dict)
            # Call detection service with json object converted from dictionary
            authenticity_score = self.__authenticity_detector(json.dumps(attribute_dict))
            # Render result_page with authenticity score from detection service
            return render_template('result_page.html', score=authenticity_score[0], test=authenticity_score[1])

    def native_app(self, method, form):
        """
        Native App interface, handles POST requests
        :return: HTML template of result page with score
        """

        # Handle POST request
        if method == 'POST':
            # Get URL from POST request form
            url = form['url']
            # Get HTML from URL
            html = requests.get(url).content.decode().strip()
            # Parse webpage with web scraper
            page_data = WebScraper(html).scrape()
            # Construct dictionary containing URL, post_data from POST request, and page_data from web scraping
            attribute_dict = {
                'url': url,
                'post_data': {
                    'account_name': form.get('post_author'),
                    'user_name': form.get('user_name'),
                    'post_date': form.get('post_date'),
                    'post_date_time': form.get('post_date_time'),
                    'account_age': form.get('account_age'),
                    'profile_picture': form.get('profile_picture')
                },
                'page_data': page_data
            }
            # Call detection service with json object converted from dictionary
            authenticity_score = self.__authenticity_detector(json.dumps(attribute_dict))
            # Render result_page with authenticity score from detection service
            return render_template('result_page.html', score=authenticity_score)

    @staticmethod
    def __authenticity_detector(json_deliverable):
        """
        Sends json object containing data to be screened in authenticity detector
        :param json_deliverable: json object
        :return: authenticity float score
        """

        # TODO REPLACE PLACEHOLDER CODE
        json_obj = json.loads(json_deliverable)
        pprint.pprint(json_obj)
        result = random.uniform(0, 1).__round__(4) # detect_authenticity(json_obj)
        return result, json_obj


class WebScraper:
    # WebScraper takes HTML file and scrapes for data
    page_data_dict = {
        "title": None,
        "subtitle": None,
        "authors": None,
        "publisher": None,
        "publish_date": None,
        "publish_date_time": None,
        "body": None,
        "citation_urls": None,
        "html": None
    }
    html = None

    def __init__(self, html):
        self.html = html

    def scrape(self):
        # Find page's embedded json file and convert it to dictionary to extract data
        if self.html.find('application/ld+json') != -1:
            start = self.html.find("{", self.html.find('application/ld+json'))
            end = self.__index_of_section_end(self.html, "{", "}", start)
            page_json = json.loads(self.html[start:end])

            pprint.pprint(page_json)
            # Parse page's json data for information and add it to the dict
            self.page_data_dict["title"] = self.__find_title(page_json)
            self.page_data_dict["subtitle"] = self.__find_subtitle(page_json)
            self.page_data_dict["authors"] = self.__find_authors(page_json)
            self.page_data_dict["publisher"] = self.__find_publisher(page_json)
            self.page_data_dict["publish_date"] = self.__find_publish_date(page_json)
            self.page_data_dict["publish_date_time"] = self.__find_publish_date_time(page_json)

        # Find article body in page html, add data to dict
        body_text, links = self.__find_and_parse_body(self.html)
        self.page_data_dict["body"] = body_text
        self.page_data_dict["citation_urls"] = links

        # Dump full HTML content into dict
        # TODO uncomment below before deploying
        # self.page_data_dict["html"] = self.html

        return self.page_data_dict

    @staticmethod
    def __find_title(data):
        """
        Parse json data for title
        :data: json containing page data
        :return: string title, or None
        """
        title = None
        if "headline" in data:
            title = data["headline"]
        if "title" in data:
            title = data['title']
        if "name" in data:
            title = data['name']

        return title

    @staticmethod
    def __find_subtitle(data):
        """
        Parse json data for subtitle
        :data: json containing page data
        :return: string subtitle, or None
        """
        subtitle = None
        if 'description' in data:
            subtitle = data['description']
        if 'subtitle' in data:
            subtitle = data['subtitle']
        return subtitle

    def __find_authors(self, data):
        """
        Parse json data for authors
        :data: json containing page data
        :return: list of strings of authors, or None
        """
        authors = []
        if 'by' in data:
            authors.append(self.__strip_all(str(data['author'])))
        if 'author' in data:
            authors.append(self.__strip_all(str(data['author'])))
        if 'authors' in data:
            authors = data['authors']
        if len(authors) == 0:
            authors = None
        return authors

    @staticmethod
    def __strip_all(text):
        text = text.strip()
        text = text.strip("[")
        text = text.strip("]")
        text = text.strip("'")
        text = text.strip('"')
        return text

    @staticmethod
    def __find_publisher(data):
        """
        Parse json data for publisher
        :data: json containing page data
        :return: string publisher, or None
        """
        publisher = None
        if 'publisher' in data:
            publisher = data['publisher']
        if type(publisher) is dict:
            if 'name' in publisher:
                publisher = publisher['name']
            else:
                str_publisher = str(publisher)
                publisher = str_publisher[str_publisher.find("www.") + 4: str_publisher.find(".com") + 4]
        return publisher

    @staticmethod
    def __find_publish_date(data):
        date = None
        if 'datePublished' in data:
            date = data['datePublished']
        if date is not None and date.find("T") == -1:
            return date
        return None

    @staticmethod
    def __find_publish_date_time(data):
        date_time = None
        if 'datePublished' in data:
            date_time = data['datePublished']
        if date_time is not None and date_time.find("T"):
            return date_time
        return None

    @staticmethod
    def __index_of_section_end(html, start_str, end_str, start_index):
        last = start_index + 1
        open_count = 1
        while open_count > 0:
            start = html.find(start_str, last)
            close = html.find(end_str, last)
            if start != -1 and start < close:
                open_count += 1
                last = start + 1
            else:
                open_count -= 1
                last = close + 1
        return last

    def __find_and_parse_body(self, html):
        find_ps = []
        paragraph_list = []
        links = []
        for _ in range(0, 10):
            find_ps.append(html.find("<p "))
        if html.find('<p ') != -1:
            first_p = find_ps[0]
            end_div = self.__index_of_section_end(html, "<div", "</div", first_p)
            last_p = html.rfind("</p", 0, end_div) + 3
            body_section = html[first_p:last_p]

            for index, letter in enumerate(body_section):
                if body_section[index:index + 2] == "<p":
                    start = index
                elif body_section[index:index + 3] == "</p":
                    p_line = body_section[start:index]
                    p_start = p_line.find(">") + 1
                    paragraph = p_line[p_start:index]
                    if len(paragraph) != 0 and paragraph[len(paragraph) - 1] == ">":
                        continue
                    if paragraph.find("<") != -1:
                        # text, link = find_links(paragraph)
                        # links.append(link)
                        # paragraph = text
                        continue
                    paragraph_list.append(paragraph)

        # for p in paragraph_list:
        # print(p)
        if len(links) == 0:
            links = None
        return paragraph_list, links

    def __find_links(self, text):
        new_text = ""
        print(text)
        start = 0
        end = 0
        while start != -1:
            start = text.find("<")
            new_text += text[end:start]
            end = self.__index_of_section_end(text, "<", ">", start)
            text = text[end:]

        print(text[start:end])
        return None


# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)
app.static_folder = 'static'


@app.route('/dev', methods=['GET'])
def dev_guide():
    """HTML documentation about the API at the '/dev' url path"""
    return Interface().dev_guide(request.method)


@app.route('/invalid_url', methods=['GET'])
def invalid_path():
    """Handles redirect to invalid url html"""
    return Interface().invalid_path(request.method)


@app.route('/', methods=['GET', 'POST'])
def webapp():
    """
    Web App interface at the '/' url path. Handles GET and POST requests
    :return: HTML template of result page with score
    """
    return Interface().webapp(request.method, request.form)


@app.route('/api', methods=['POST'])
def native_app():
    """
    Native App interface at the '/api' url path. Handles POST requests
    :return: HTML template of result page with score
    """
    return Interface().native_app(request.method, request.form)
