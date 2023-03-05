from recipe_scrapers import scrape_me
from number_parser import parse_ordinal
import requests
import json

def parse_recipe(url):
    # Scrape recipe to json.
    scraper = scrape_me(url)
    raw_recipe_json = scraper.to_json()

    return raw_recipe_json

def parse_ingredients(ingredients):
    # Parse ingredients into structured data.
    url = "https://ingredient-parser2.p.rapidapi.com/parse-ingredients"

    payload = {"ingredients": scraper.ingredients()}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "dce9755f64mshe61076df41050e4p1e1571jsn25bf332ab4e6",
        "X-RapidAPI-Host": "ingredient-parser2.p.rapidapi.com"
    }

    ingredients_response = requests.request("POST", url, json=payload, headers=headers)
    ingredients_json = json.loads(ingredients_response.text)

    return ingredients_json

def alnum_parse_ordinal(value):
    if value.isnumeric():
        return int(value)
    elif value.isalnum() and not value.isalpha() and not value.isdigit():
        return int(value[:-2])
    else:
        return parse_ordinal(value)

def retrieve_youtube_video(query):
    # Retrieve the most relevant video result from the provided query.
    url = "https://youtube-search-results.p.rapidapi.com/youtube-search/"

    query_string = {"q" : query}

    headers = {
        "X-RapidAPI-Key": "dce9755f64mshe61076df41050e4p1e1571jsn25bf332ab4e6",
        "X-RapidAPI-Host": "youtube-search-results.p.rapidapi.com"
    }

    search_result_response = requests.request("GET", url, headers=headers, params=query_string)
    search_result_json = json.loads(search_result_response.text)

    # Return most relevant video result.
    for result in search_result_json["items"]:
        if result["type"] == "video":
            return result["url"]