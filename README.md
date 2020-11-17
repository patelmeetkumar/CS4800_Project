<a href="https://naws.herokuapp.com/" style="font-size: 42px">Return to News Authenticity Web Service</a>  
### CPP CS 4800.02 F20, Software Engineering Semester Project
  
## Project Roles & Members:
 
**Project Manager:** Meetkumar Patel  
**Software Developer:** David Lascelles  
**Software Developer:** Neeyati Ajmera  
**Quality Assurance:** Christian Batach  
**Business Analyst:** Jaskaranpreet Sidhu  
  
## Project: 
- RESTFUL Web API for interfacing between clients and detection services
- Web App client for the web service 


## Native App Interface

Native apps, such as Facebook or Twitter clients, can integrate with our Fake News Detection API 
if they have an eligible social media post. A social media post **must** contain an embedded link 
to a third party website, such as a news article. 

### API Input for App Interface:
This API accepts `POST` requests as input. 
Send a `POST` request containing a JSON to https://naws.herokuapp.com/api to use the API. 
Use the following JSON keys for valid input.

**Minimum requirement is the `url` key containing a *String*.**  
Not including a URL will result in an `HTTP 400 BAD REQUEST` response.
Social media posts that do not contain a link to a third party service are *not supported* by this API. 

Apps can optionally add the following attributes from social media posts to increase detection accuracy:

|Attribute         |Type        |Description                                      |Specification/Example                |
|------------------|------------|-------------------------------------------------|-------------------------------------|
|`account_name`    |*String*    |User's actual name                               |John Smith                           |
|`user_name`       |*String*    |User's handle or user name                       |@john_smith                          |
|`post_body`       |*String*    |The post body content                            |Wow, check out this news article!    |
|`post_date`       |*ISO String*|Date of post                                     |Use ISO format: `YYYY-MM-DD`         |
|`post_date_time`  |*ISO String*|Date and time of post                            |Use ISO format: `YYYY-MM-DDThh:mmTZD`|
|`account_age`     |*Float*     |Age of account in years                          |`4.3`                                |
|`profile_picture` |*Boolean*   |True if user has non-default profile picture     |`True`                               |

**Example JSON package**  
`{`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `url:https://www.example.com/news_article/`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `account_name:@test_account`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `user_name:Sally Smith`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `post_body:WOW! Look at this article!`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `post_date_time:2020-10-06T011:24PST`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `account_age:4.3`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `profile_picture:True`  
`}` 

### API Output to Web/App:
In the `POST` response, this API returns a four decimal `float` confidence value from

`0` for **Fake** to `1` for **Real**, for example `0.0428`

**Implementation Suggestions:**  
The Web/App client should use the confidence value to arbitrarily determine authenticity of submitted content.
For example, the client can decide that scores over 0.7 are Real, below 0.3 are Fake, and have an "Uncertain"
state in between, or alternatively present the user with a 0% to 100% score.

## Authenticity Detection Service Interface
Our API relies on integration with a detection service. In order to interface with a detection service, we require
a url endpoint that we call submit a `POST` request to. The detection service must be able to handle at minimum a
`url` key in the JSON package, and can optionally use additional parameters that are supplied to improve 
detection accuracy.
 
### API Call to Authenticity Detection Services:
When this API calls your service, it will pass a JSON object in a `POST` request. The JSON object may contain `null` 
values for any/all fields except the `url` key which will contain an article's url as a *String*.

Access the other JSON keys using the following structure:

|Parent Attribute|Child Attribute    |Type             |Description                                 |Specification/Example|
|----------------|-------------------|-----------------|--------------------------------------------|---------------------|
|`url`           |                   |*String*         |URL of article                              |https://www.google.com
|`post_data`     |          
|                |`account_name`     |*String*         |User's actual name                          |John Smith
|                |`user_name`        |*String*         |User's handle or user name                  |@john_smith
|                |`post_date`        |*ISO String*     |Date of post                                |Use ISO format: `YYYY-MM-DD`
|                |`post_date_time`   |*ISO String*     |Date and time of post                       |Use ISO format: `YYYY-MM-DDThh:mmTZD`
|                |`account_age`      |*Float*          |Age of account in years                     |`4.3`
|                |`profile_picture`  |*Boolean*        |True if user has non-default profile picture|`True`
|`page_data`     |           
|                |`title`            |*String*         |Title of the article                        |Breaking: World Peace Achieved
|                |`subtitle`         |*String*         |Subtitle of the article                     |World Leaders Agree to Peace Terms
|                |`authors`          |*List of Strings*|Authors of the article                      |John Smith, Jane Doe
|                |`publisher`        |*String*         |Publisher of the article                    |New York Times
|                |`publish_date`     |*ISO String*     |Publish date of the article                 |Use ISO format: `YYYY-MM-DD`
|                |`publish_date_time`|*ISO String*     |Publish date and time of the article        |Use ISO format: `YYYY-MM-DDThh:mmTZD`
|                |`body`             |*String*         |Contents of the article                     |Yesterday afternoon at a global summit, world leaders...
|                |`citation_urls`    |*List of Strings*|List of urls that are linked in the article |https://www.wikipedia.org, https://www.cnn.com
|                |`html`             |*String*         |HTML Dump of a the webpage                  |`<!doctype html><html lang="en"><head>...`

**Example JSON package**  
`{`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `url:https://www.example.com/news_article/`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `post_data: {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `account_name:@test_account`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `user_name:Sally Smith`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `post_body:WOW! Look at this article!`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `post_date_time:2020-10-06T011:24PST`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `account_age:4.3`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `profile_picture:True`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `}`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `page_data: {`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `title: End of the World Scheduled for Next Week`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `subtitle: Participants of the year 2020 are unsurprised `  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `authors: [Robert Joe, Joseph Bob]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `publisher: Really Real News Network`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `publish_date: null`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `publish_date_time:2020-10-05T09:53PST`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `body: As a horrible year comes to a close, nobody is surprised by the anouncement...`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `citation_urls: [http://www.wikipedia.org/, http://www.un.org/]`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `html:<!doctype html><html lang="en"><head>...`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`}`  
`}`  
        
### API Response from Authenticity Detection Services:
In your `POST` response, return a `float` confidence value in a JSON object with the `score:` key.  
Score should be between `0` for
 **Fake** to `1` for **Real** 
 
Your JSON response should be formatted as:  
`{score: 0.0428}`

For decision-tree authenticity checking services, you may use intermediate values like 0.5 to indicate uncertainty.

## To request changes to or clarification about this API, please contact the Project Manager Meetkumar Patel on Discord
