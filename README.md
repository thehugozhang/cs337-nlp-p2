# <span style="color:#4E2A84">**CH3FB0T**</span> - Virtual Cooking Contextual Assistant Chatbot (cs337-nlp-p2)

Developed for COMP_SCI 337 Natural Language Processing at [Northwestern University](https://www.northwestern.edu/).

## Description

Meet <span style="color:#4E2A84">**CH3FB0T**</span>! This project is a contexual assistant chatbot that can interpret any online recipe URL and promptly respond to queries about it.

Click the thumbnails below to watch the Youtube demonstrations.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=dQDzthvpEE4" target="_blank"><img src="http://img.youtube.com/vi/dQDzthvpEE4/0.jpg" 
alt="Youtube Demonstration Part 1" width="240" height="180" border="10" /></a>

<a href="http://www.youtube.com/watch?feature=player_embedded&v=bIXci0jNfiw" target="_blank"><img src="http://img.youtube.com/vi/bIXci0jNfiw/0.jpg" 
alt="Youtube Demonstration Part 2" width="240" height="180" border="10" /></a>

## Getting Started

### Dependencies

Built and tested on Python v3.9.12 and pip v23.0.1.

This system depends on the following third-party modules.
* [Rasa](https://rasa.com/docs/rasa/installation/installing-rasa-open-source)
* [Recipe Scrapers](https://pypi.org/project/recipe-scrapers/)
* [NLTK](https://www.nltk.org/install.html)
* [number-parser](https://github.com/scrapinghub/number-parser)
* [Ingredient Parser](https://ingredient-parser.readthedocs.io/en/latest/)

### Installing

Specific installation instructions can be found below.

* To install Rasa. *Note: Rasa only supports Python versions 3.7, 3.8, 3.9, and 3.10.*
```
pip3 install rasa
```

* To install NLTK:
```
pip3 install nltk
```

* To install Recipe Scrapers:
```
pip3 install recipe-scrapers
```

* To install number-parser:
```
pip3 install number-parser
```

* To install Ingredient Parser:
```
python -m pip install ingredient-parser-nlp
```

### Installation debugging

In certain situations, some Rasa dependencies may need to be individually installed or removed. For more information, see this [git issue](https://github.com/OpenZeppelin/nile/issues/105).

* To install Greenlet:
```
pip3 install greenlet==1.1.2
```
* To install Colorama:
```
pip3 install colorama
```

* For some recipes, you may encounter an `asyncio` open bug in Rasa 3.3.x where shell output may be blocked from logging. The following command removes the problematic dependency causing the bug. For more information, see this [git issue](https://github.com/RasaHQ/rasa/issues/11575).
```
pip3 uninstall uvloop
```

### Third-Party APIs

Additionally, this project depends on several external APIs for its advanced functionality. *Note: Exceeding these free rate limits could result in some CH3FB0T functionalities being unavailable until the next day.*

* [Youtube Search Results](https://rapidapi.com/marindelija/api/youtube-search-results/)
    * **Purpose:** For retrieving most relevant Youtube results for how-to queries.
    * **Rate:** 100 requests / day.
* [Wiki Briefs](https://rapidapi.com/dfskGT/api/wiki-briefs/)
    * **Purpose:** For retrieving summaries and images of what-is queries.
    * **Rate:** unlimited. 
* [Spoonacular API](https://spoonacular.com/food-api/)
    * **Purpose:** For querying substitute ingredient matches.
    * **Rate:** 50 request / day.

For anyone viewing this repository after March 20, 2023, you will need to provide your own API keys for the above services to run **CH3FB0T**.

## Executing the system

### Via Command Line
To communicate with <span style="color:#4E2A84">**CH3FB0T**</span> via the command line, simply run the following commands in the root directory.

* First, train the model.

```
rasa train
```

* Next, start the actions server (to communicate with recipe-parsing backend) and run the chatbot in shell! *Note: CH3FB0T may take ~1-2 minutes to initialize.*

```
rasa run actions & rasa shell
```

### Via Local Slack Channel
A Slack workspace and custom app have been setup to provide an easy interface to communicate with <span style="color:#4E2A84">**CH3FB0T**</span>.

To communicate with <span style="color:#4E2A84">**CH3FB0T**</span> via Slack, run the following commands in the root directory.

* First, you must replace the empty values with the required Slack App tokens for <span style="color:#4E2A84">**CH3FB0T**</span> in `credentials.yml`. For the course instructor/TAs of 337, these values will be provided. For anyone else viewing this repository, you can create your own workspace to generate your own unique values.

```
# Replace these values!
slack:
 slack_token: "<your slack token>"
 slack_channel: "<the slack channel>"
 slack_signing_secret: "<your slack signing secret>"
```

* Next, train the model if you haven't already.

```
rasa train
```

* Next, run the following command to start <span style="color:#4E2A84">**CH3FB0T**</span>.
```
rasa run & rasa run actions
```

* Rasa communicates using your local 5005 port. To make this port publicly available on the internet to communicate with Slack, you can use ngrok. More information: [Rasa Docs](https://rasa.com/docs/rasa/messaging-and-voice-channels#testing-channels-on-your-local-machine).
    * After creating a tunnel using the command below, make sure to replace the Request URL in Event Subscriptions on Slack's Your Apps section with the ngrok.io Forwarding URL, followed by the path ending `/webhooks/slack/webhook`.
```
ngrok http 5005
```

* Voila! Open the Slack workspace and invite <span style="color:#4E2A84">**CH3FB0T**</span> to start chatting.

### Execution notes
* In order to communicate with <span style="color:#4E2A84">**CH3FB0T**</span> over Slack, the ngrok tunnel must be set as the Slack app's Request URL per the [Rasa Docs](https://rasa.com/docs/rasa/connectors/slack).

* If using a virtual environment, make sure to enable it first (prior to the above steps) using:
```
source ./venv/bin/activate
```

* If you are rerunning `rasa run actions`, make sure to kill the previous version on the same port by running:
```
kill -9 $(lsof -ti:5055)
```

* OSError: [Errno 48] error while attempting to bind on address ('0.0.0.0', 5005): address already in use
```
kill -9 $(lsof -ti:5005)
```

## Help

For any additional troubleshooting assistance, please reach out to [hugozhang2023@u.northwestern.edu](mailto:hugozhang2023@u.northwestern.edu).