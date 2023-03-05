from recipe_scrapers import scrape_me
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