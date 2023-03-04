# Virtual Cooking Contextual Assistant Chatbot (cs337-nlp-p2)

Developed for COMP_SCI 337 Natural Language Processing at [Northwestern University](https://www.northwestern.edu/).

## Description

This project is a contexual assistant chatbot that can interpret any online recipe URL and promptly respond to queries about it.

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

### Executing the system

## Help

For any additional troubleshooting assistance, please reach out to [hugozhang2023@u.northwestern.edu](mailto:hugozhang2023@u.northwestern.edu).

## Results