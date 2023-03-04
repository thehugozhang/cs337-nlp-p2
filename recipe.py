from recipe_scrapers import scrape_me
import parse_ingredient
import json

scraper = scrape_me('https://www.foodnetwork.com/recipes/onigiri-rice-balls-recipe-1969274')

# Q: What if the recipe site I want to extract information from is not listed below?
# A: You can give it a try with the wild_mode option! If there is Schema/Recipe available it will work just fine.
# scraper = scrape_me('https://www.feastingathome.com/tomato-risotto/', wild_mode=True)

print(scraper.title())
print("\n")
print(scraper.ingredients())
print("\n")
print(scraper.instructions())
print("\n")
print(scraper.instructions_list())
print("\n")
print(scraper.yields())
print("\n")
print(scraper.to_json())
print("\n")
print(scraper.nutrients())  # if available

ingredients = parse_ingredient.parse_multiple(scraper.ingredients())
print(json.dumps(ingredients.as_dict()))