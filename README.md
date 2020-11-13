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
### API Input for App Interface:
This API accepts POST requests as input. 
Send a POST request containing a JSON to ```https://naws.herokuapp.com/api``` to use the API. 
Use the following json keys for valid input.

**Minimum requirement is the `url` key containing a *String*.**

Apps can add the following attributes from social media posts:

|Attribute         |Type        |Description                                      |Specification/Example                |
|------------------|------------|-------------------------------------------------|-------------------------------------|
|`account_name`    |*String*    |User's actual name                               |John Smith                           |
|`user_name`       |*String*    |User's handle or user name                       |@john_smith                          |
|`post_date`       |*ISO String*|Date of post                                     |Use ISO format: `YYYY-MM-DD`         |
|`post_date_time`  |*ISO String*|Date and time of post                            |Use ISO format: `YYYY-MM-DDThh:mmTZD`|
|`account_age`     |*Float*     |Age of account in years                          |`4.3`                                |
|`profile_picture` |*Boolean*   |True if user has non-default profile picture     |`True`                               |

### API Output to Web/App:
This API returns a `float` confidence value from

`0` for **Fake** to `1` for **Real**

The Web/App client should use the confidence value to arbitrarily determine authenticity of submitted content.
For example, the client can decide that scores over 0.7 are Real, below 0.3 are Fake, and have an "Uncertain"
state in between, or alternatively present the user with a 0% to 100% score.

## Authenticity Detection Service Interface
### API Call to Authenticity Detection Services:
When this API calls your service, it will pass a json object. The json object may contain `null` values for any/all 
fields except the `url` key which will contain an article's url as a *String*.

Access the other json keys using the following structure:

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
|                |`html`             |*String*         |HTML Dump of a the webpage                  |<!doctype html><html lang="en"><head>...
      
        
### API Response from Authenticity Detection Services:
Return a `float` confidence value in a json object with the `score=` key. Score should be between `0` for
 **Fake** to `1` for **Real**

For decision-tree authenticity checking services, you may use intermediate values like 0.5 to indicate uncertainty.

## To request changes to or clarification about this API, please contact the Project Manager Meetkumar Patel on Discord
