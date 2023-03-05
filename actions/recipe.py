from recipe_scrapers import scrape_me
from number_parser import parse_ordinal
import requests
import json

# NLTK configuration.
import nltk
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk import word_tokenize, pos_tag

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

def what_is_wiki_summary(query):
    # Retrieve a wikipedia summary and image from provided query.
    url = "https://wiki-briefs.p.rapidapi.com/search"

    query_string = {"q" : query, "topk" : "1"}

    headers = {
        "X-RapidAPI-Key": "dce9755f64mshe61076df41050e4p1e1571jsn25bf332ab4e6",
        "X-RapidAPI-Host": "wiki-briefs.p.rapidapi.com"
    }

    wiki_summary_response = requests.request("GET", url, headers=headers, params=query_string)
    wiki_summary_json = json.loads(wiki_summary_response.text)

    return wiki_summary_json

def substitute_ingredient(query):
    # Retrieve potential substitute ingredients from provided query.
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/substitutes"

    query_string = {"ingredientName" : query}

    headers = {
        "X-RapidAPI-Key": "dce9755f64mshe61076df41050e4p1e1571jsn25bf332ab4e6",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    substitute_ingredient_response = requests.request("GET", url, headers=headers, params=query_string)
    substitute_ingredient_json = json.loads(substitute_ingredient_response.text)

    return substitute_ingredient_json


# Original source from https://github.com/thehugozhang/cs337-nlp-p1/blob/main/regex_system.py.
def pos_tag_text(text, lowercase=True, filter_stop_words=False):
    if (lowercase): text = text.lower()

    words = word_tokenize(text)

    if filter_stop_words: words = [word for word in words if word.casefold() not in stop_words]

    words = nltk.pos_tag(words)

    return words

# Original source from https://github.com/thehugozhang/cs337-nlp-p1/blob/main/regex_system.py.
def chunk_tagged_text(text_list, chunk_rule, draw_tree=False):
    chunk_parser = nltk.RegexpParser(chunk_rule)
    tree = chunk_parser.parse(text_list)
    if draw_tree: tree.draw()

    results = []
    for subtree in tree.subtrees(filter=lambda t: t.label() == chunk_rule.split(':')[0]):
        extracted_text = []
        for pos_tuple in subtree[0:]:
            extracted_text.append(pos_tuple[0])
        results.append(" ".join(extracted_text))
    
    return results

def get_vague_how_to(substep):
    tagged_substep = pos_tag_text(substep, True, False)

    # Entity Name chunking RegEx.
    # Grammar rule: a verb (dice) followed a determiner (optional) and any number of nouns (tomato).
    # Ex. Dice (VB) the (DT) tomato (NN).
    inferred_entity_grammar = """How-To Query: {<VB><DT>?<JJ>*<NN|NNS|NNP|NNPS>}"""
    entities = chunk_tagged_text(tagged_substep, inferred_entity_grammar, False)
    print("Detected vague entities:", entities)

    return entities