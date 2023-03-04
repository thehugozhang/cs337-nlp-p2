# CH3FB0T - Virtual Cooking Contextual Assistant Chatbot (cs337-nlp-p2)

Developed for COMP_SCI 337 Natural Language Processing at [Northwestern University](https://www.northwestern.edu/).

## Description

Meet CH3FB0T! This project is a contexual assistant chatbot that can interpret any online recipe URL and promptly respond to queries about it.

## Getting Started

### Dependencies

Built and tested on Python v3.9.12 and pip v23.0.1.

This system depends on the following third-party modules.
* [Rasa](https://rasa.com/docs/rasa/installation/installing-rasa-open-source)
* [Recipe Scrapers](https://pypi.org/project/recipe-scrapers/)
* [Ingredient Parser (Zestful Client)](https://pypi.org/project/zestful-parse-ingredient/)

### Installing

Specific installation instructions can be found below.

* To install Rasa. *Note: Rasa only supports Python versions 3.7, 3.8, 3.9, and 3.10.*
```
pip3 install rasa
```

* To install Recipe Scrapers:
```
pip3 install recipe-scrapers
```

* To install Ingredient Parser (Zestful Client):
```
pip3 install zestful-parse-ingredient
```
### Installation debugging

In certain situations, some Rasa dependencies may need to be individually installed. For more information, see this [git issue](https://github.com/OpenZeppelin/nile/issues/105).

* To install Greenlet:
```
pip3 install greenlet==1.1.2
```

## Executing the system

### Via Command Line
To communicate with CH3FB0T via the command line, simply run the following command in the root directory.

```
rasa shell
```

### Via Slack Channel
A Slack workspace and custom app have been setup to provide an easy interface to communicate with CH3FB0T.

To communicate with CH3FB0T via Slack, run the following commands in the root directory.

* First, you must replace the empty values with the required Slack App tokens for CH3FB0T in `credentials.yml`. For the course instructor/TAs of 337, these values will be provided. For anyone else viewing this repository, you can create your own workspace to generate your own unique values.

```
# Replace these values!
slack:
 slack_token: "<your slack token>"
 slack_channel: "<the slack channel>"
 slack_signing_secret: "<your slack signing secret>"
```

* Rasa communicates using the 5005 port. To make this port publicly available on the internet, you can use ngrok. More information: [Rasa Docs](https://rasa.com/docs/rasa/messaging-and-voice-channels#testing-channels-on-your-local-machine).
```
ngrok http 5005
```
* Next, run the following command to start CH3FB0T.
```
rasa run
```
* Voila! Open the Slack workspace and invite CH3FB0T to start chatting.

### Execution notes
* In order to communicate with CH3FB0T over Slack, the ngrok tunnel must be set as the Slack app's Request URL per the [Rasa Docs](https://rasa.com/docs/rasa/connectors/slack).

* If using a virtual environment, make sure to enable it first (prior to the above steps) using:
```
source ./venv/bin/activate
```

## Help

For any additional troubleshooting assistance, please reach out to [hugozhang2023@u.northwestern.edu](mailto:hugozhang2023@u.northwestern.edu).

## Results