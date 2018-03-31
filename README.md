# Statistical sentiment analysis of Twitter as a review platform

Reviews being the most important thing in deciding whether
to visit a place or not and having a genuine review is the
most essential part. Generally, reviews available on websites
and platform such as Yelp are more inclined to the
positive aspects of a place. Moreover, the amount of usage
of social media platforms has increased also, these platforms
contain posts which expresses user’s opinion in a better way.
Twitter being an important contributor, understanding the
reliability of such tweets of being reviews is also important.
To examine this, we have devised various approaches using
natural language processing to analyze the tweets and obtain
a statistical analysis of the same based on metadata
obtains from tweets.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites and Installation

STEP 1: Download and install Python3 on your machine

* You can download python3 installer from their official website [here](https://www.python.org/downloads/)
* Once the setup is downloaded, follow the instructions to install the same.

STEP 2: Additional Dependencies

* JsonPickle:

  Run the following command on terminal to install the dependency.

  ``pip3 install jsonpickle``

  If you want to explore other installation methods please visit the module's documentation [here](https://jsonpickle.github.io/#download-install)

* TweePy:

  Run the following command on terminal to install the dependency.

  ``pip3 install tweepy``

  If you want to explore other installation methods please visit the module's documentation [here](http://docs.tweepy.org/en/v3.4.0/install.html)

STEP 3: Cloning the repository

Run the following command on terminal to clone the repository or optionally you can use any other git management tool

``git clone https://github.com/ankit13jain/Twitter-Mining.git``

STEP 4: Getting Access to Twitter API Credentials

* If you don't already have a Twitter Account "Create a Twitter Account!" *:|*
* Open the Twitter Dev Apps website from [here](https://apps.twitter.com/). Click on "Create new App"

![Create New App](/readme_files/app_home.png)
* Fill out the required details in the form and click on "Create your Twitter Application"

![Fill details](/readme_files/app_new.png)
* Get the API_KEY and API_SECRET from the "Keys and Access Tokens" tab

![Fill details](/readme_files/app_keys.png)
* Create a file with name 'credential.json' and paste the following content

  ``{
    "API_KEY": "YOUR_API_KEY",
    "API_SECRET": "YOUR_API_SECRET"
  }``

## Running the code

* Change the working directory to

  ``... Twitter-Mining/scripts``

* Now being in scripts folder run the following command on terminal

  ``python3 tweet_mining.py "LOCATION_OR_THING_YOU_WANT_TWEETS_FOR"``

* All the data will be extracted in json format containing the metadata mentioned [here](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets#example-response). These json files are zipped together to save disk space and moved into 'data' folder

![Output](/readme_files/output.png)

## Authors

* **Chirag Jain** - *er.chiragjain92@gmail.com* - [github](http://github.com/CJ8664)
* **Ankit Jain** - *ankit13jain@gmail.com* - [github](http://github.com/ankit13jain)
* **Nirav Jain** - *niravr7@gmail.com* - [github](http://github.com/niravjain)
* **Rishabh Jain** - *rishabh05apr@gmail.com* - [github](https://github.com/Rishabh05apr)
* **Pratik Kumar Jain** - *kumathpratik@gmail.com* - [github](https://github.com/pratikkumar-jain)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details

## More about the research, references and inspiration for the project
