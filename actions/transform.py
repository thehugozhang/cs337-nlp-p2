from ingredient_parser import parse_multiple_ingredients, parse_ingredient
import pprint

def construct_substitute_ingredient(previous, substitutee_product, substitute_dict, recipe_time, recipe_ingredients, recipe_steps, original_recipe_steps):
    """Converts an ingredient with its substitute and adjusts the recipe using its parameters."""
    # Shallow copies to prevent changing after assignment.
    shallow_recipe_time = recipe_time
    shallow_recipe_ingredients = recipe_ingredients
    shallow_recipe_steps = recipe_steps

    # Get substitute values for current ingredient.
    substitute_type = substitute_dict["substitution"]
    substitute_ratio = substitute_dict["ratio"]
    substitute_unit = substitute_dict["unit"]
    substitute_sentence = substitute_dict["sentence"]
    substitute_comment = substitute_dict["comment"]
    # Get additional prep time, ingredients, and steps for substitution (if any).
    substitute_added_time = substitute_dict["additions"]["prep_time"]
    substitute_added_ingredients = substitute_dict["additions"]["ingredients"]
    substitute_added_steps = substitute_dict["additions"]["steps"]

    # Update current ingredient name.
    previous["name"] = previous["name"].lower().replace(substitutee_product, substitute_type)

    # Adjust original ingredient quantity using substitute ratio and unit.
    previous["quantity"] = "{:.2f}".format((float(previous["quantity"]) * substitute_ratio))
    if substitute_unit is not None:
        previous["unit"] = substitute_unit

    # Update original ingredient dictionary using substitute values.
    if substitute_comment is not None:
        previous["comment"] = substitute_comment
    if substitute_sentence is not None:
        previous["sentence"] = previous["quantity"] + substitute_sentence
    else:
        previous["sentence"] = previous["sentence"].lower().replace(substitutee_product, substitute_type).capitalize()

    # Add additional prep time to recipe.
    shallow_recipe_time += substitute_added_time

    # Add additional steps to recipe.
    shallow_recipe_steps = substitute_added_steps + shallow_recipe_steps

    # Parse new ingredients and add to ingredient list.
    for new_ingredient in substitute_added_ingredients:
        shallow_recipe_ingredients.append(parse_ingredient(new_ingredient))

    return shallow_recipe_time, shallow_recipe_ingredients, shallow_recipe_steps

def gather_sentences(updated_ingredients):
    updated_recipe_ingredient_sentences = []
    for ingredient_dict in updated_ingredients:
        updated_recipe_ingredient_sentences.append(ingredient_dict["sentence"])
    return updated_recipe_ingredient_sentences

def transform_recipe(substitutes_lexicon, recipe_time, recipe_ingredients, recipe_steps):
    # Original value recipe values.
    original_recipe_prep_time = recipe_time
    original_recipe_ingredients = recipe_ingredients
    original_recipe_parsed_ingredients = parse_multiple_ingredients(original_recipe_ingredients)
    original_recipe_instructions = recipe_steps

    # Updated value recipe values.
    updated_recipe_prep_time = original_recipe_prep_time
    updated_recipe_ingredients = original_recipe_ingredients.copy()
    updated_recipe_parsed_ingredients = sorted(original_recipe_parsed_ingredients.copy(), key=lambda d: d['name'])
    updated_recipe_instructions = original_recipe_instructions.copy()

    print(original_recipe_parsed_ingredients)
    for ingredient_dict in original_recipe_parsed_ingredients:
        for substitutee, substitute_dict in substitutes_lexicon.items():
            if substitutee in ingredient_dict["name"].lower():
                updated_recipe_prep_time, updated_recipe_parsed_ingredients, updated_recipe_instructions = construct_substitute_ingredient(ingredient_dict, substitutee, substitute_dict, updated_recipe_prep_time, updated_recipe_parsed_ingredients, updated_recipe_instructions, original_recipe_instructions)
                break

    # Final check through for any remaining references.
    for substitutee, substitute_dict in substitutes_lexicon.items():
        for index, step in enumerate(updated_recipe_instructions):
            step = step.lower()
            if substitutee in step:
                temp_step = step.replace(substitutee, substitute_dict["substitution"]).capitalize()
                updated_recipe_instructions[index] = '. '.join(sentence.capitalize() for sentence in temp_step.split('. '))

    return updated_recipe_prep_time, gather_sentences(updated_recipe_parsed_ingredients), updated_recipe_instructions

