from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

# Relative import of custom recipe parsing/transforming functions.
from .recipe import parse_recipe, parse_ingredients, alnum_parse_ordinal, retrieve_youtube_video, what_is_wiki_summary, substitute_ingredient, get_vague_how_to, get_duration
from .transform import transform_recipe
from .lexicon import meat_substitutions, unhealthy_substitutions

###############################################################
# Recipe parsing / slot memory utterance.
###############################################################

class ActionParseRecipe(Action):

    def name(self) -> Text:
        return "action_parse_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Parse recipe from inferred slot value.
        recipe_url = tracker.get_slot('recipe_url')
        print("Parsed URL:", recipe_url)

        try:
            recipe_json = parse_recipe(recipe_url)
        except:
            dispatcher.utter_message("Hmmm, I don't recognize that recipe schema. Do you have an alternative recipe from a different source?")
            return []
        else:
            recipe_name = recipe_json["title"]
            recipe_steps = len(recipe_json["instructions_list"])
            recipe_steps_list = recipe_json["instructions_list"]
            recipe_ingredients = recipe_json["ingredients"]
            recipe_prep_time = recipe_json["prep_time"]

            dispatcher.utter_message("Great, let's cook {} which has {} steps! What would you like to know?".format(recipe_name, recipe_steps))

            # Set slot values with parsed information so CH3FB0T can "remember" data about the recipe.
            return [
                SlotSet("recipe_name", recipe_name),
                SlotSet("recipe_steps", recipe_steps),
                SlotSet("recipe_steps_list", recipe_steps_list),
                SlotSet("recipe_current_step", 0),
                SlotSet("recipe_ingredients_list", recipe_ingredients),
                SlotSet("recipe_prep_time", recipe_prep_time),
            ]

###############################################################
# Recipe retrieval utterances.
###############################################################

class ActionRetrieveSteps(Action):

    def name(self) -> Text:
        return "action_retrieve_steps"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        recipe_name = tracker.get_slot('recipe_name')
        recipe_steps_list = tracker.get_slot('recipe_steps_list')

        steps_text = "Here are all the steps to make {}:\n\n".format(recipe_name)
        for index, step in enumerate(recipe_steps_list):
            steps_text += (str(index + 1)) + ". " + step + "\n"
        steps_text += "\nI can help walk you through each step from start to finish or you can jump directly to a later step by specifying a number!"

        dispatcher.utter_message(text=steps_text)

        return []

class ActionRetrieveIngredients(Action):

    def name(self) -> Text:
        return "action_retrieve_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        recipe_name = tracker.get_slot('recipe_name')
        recipe_ingredients_list = tracker.get_slot('recipe_ingredients_list')

        ingredients_text = "Here are all the ingredients you will need to make {}:\n\n".format(recipe_name)
        for index, ingredient in enumerate(recipe_ingredients_list):
            ingredients_text += (str(index + 1)) + ". " + ingredient + "\n"
        ingredients_text += "\nAs you are cooking, I can remind you of the quantities and other preparation notes for any specific ingredient. Don't hesitate to ask!"

        dispatcher.utter_message(text=ingredients_text)

        return []

###############################################################
# Navigation utterances.
###############################################################

class ActionNextStep(Action):

    def name(self) -> Text:
        return "action_next_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        recipe_steps = tracker.get_slot('recipe_steps')
        recipe_steps_list = tracker.get_slot('recipe_steps_list')
        recipe_current_step = tracker.get_slot('recipe_current_step')
        # Additional step count for display purposes (versus internal indexing).
        recipe_current_step_display = recipe_current_step + 1

        # Increment next step(s).
        recipe_current_step = recipe_current_step + 1
        recipe_current_step_display = recipe_current_step_display + 1

        if recipe_current_step == recipe_steps:
            dispatcher.utter_message(text="You've already reached the end of the recipe! There are no other steps, except to enjoy your meal :D")
            # Reverse increment.
            recipe_current_step = recipe_current_step - 1
            recipe_current_step_display = recipe_current_step_display - 1
        elif recipe_current_step == recipe_steps - 1:
            dispatcher.utter_message(text="Here is the last step of the recipe:\n\nStep {}. {}".format(recipe_current_step_display, recipe_steps_list[recipe_current_step]))
        else:
            dispatcher.utter_message(text="Here is the next step of the recipe:\n\nStep {}. {}".format(recipe_current_step_display, recipe_steps_list[recipe_current_step]))
        
        return [SlotSet("recipe_current_step", recipe_current_step)]

class ActionPreviousStep(Action):

    def name(self) -> Text:
        return "action_previous_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        recipe_steps = tracker.get_slot('recipe_steps')
        recipe_steps_list = tracker.get_slot('recipe_steps_list')
        recipe_current_step = tracker.get_slot('recipe_current_step')
        # Additional step count for display purposes (versus internal indexing).
        recipe_current_step_display = recipe_current_step + 1

        # Increment next step(s).
        recipe_current_step = recipe_current_step - 1
        recipe_current_step_display = recipe_current_step_display - 1

        if recipe_current_step == -1:
            dispatcher.utter_message(text="You are at the start of the recipe. Ask about the next step to start cooking!")
            # Reverse decrement.
            recipe_current_step = recipe_current_step + 1
            recipe_current_step_display = recipe_current_step_display + 1
        elif recipe_current_step == 0:
            dispatcher.utter_message(text="Here is the first step of the recipe:\n\nStep {}. {}".format(recipe_current_step_display, recipe_steps_list[recipe_current_step]))
        else:
            dispatcher.utter_message(text="Here is the previous step of the recipe:\n\nStep {}. {}".format(recipe_current_step_display, recipe_steps_list[recipe_current_step]))
        
        return [SlotSet("recipe_current_step", recipe_current_step)]

class ActionNthStep(Action):

    def name(self) -> Text:
        return "action_nth_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        recipe_steps = tracker.get_slot('recipe_steps')
        recipe_steps_list = tracker.get_slot('recipe_steps_list')
        recipe_current_step = tracker.get_slot('recipe_current_step')
        nth_utterance = tracker.get_slot('nth_utterance')

        try:
            # Additional step count for display purposes (versus internal indexing).
            nth_index = alnum_parse_ordinal(nth_utterance) - 1
            recipe_current_step_display = nth_index + 1

            try:
                dispatcher.utter_message(text="Here is the {} step of the recipe:\n\nStep {}. {}".format(nth_utterance, recipe_current_step_display, recipe_steps_list[nth_index]))
                return [SlotSet("recipe_current_step", nth_index)]
            except IndexError:
                dispatcher.utter_message(text="The {} step doesn't exist in the recipe! There are only {} total steps to choose from.".format(nth_utterance, recipe_steps))
        except:
            dispatcher.utter_message(text="Hmmm, I am unable to retrieve that step. Perhaps try navigating the steps one-by-one or pick a different step number.")

class ActionRepeatStep(Action):

    def name(self) -> Text:
        return "action_repeat_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        recipe_steps_list = tracker.get_slot('recipe_steps_list')
        recipe_current_step = tracker.get_slot('recipe_current_step')

        # Additional step count for display purposes (versus internal indexing).
        recipe_current_step_display = recipe_current_step + 1

        dispatcher.utter_message(text="Of course! Here is the same step of the recipe again:\n\nStep {}. {}".format(recipe_current_step_display, recipe_steps_list[recipe_current_step]))
        
        return []

###############################################################
# Specific how-to utterances.
###############################################################

class ActionHowTo(Action):

    def name(self) -> Text:
        return "action_how_to"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        how_to_query = tracker.get_slot('how_to_query')
        recipe_steps_list = tracker.get_slot('recipe_steps_list')
        recipe_current_step = tracker.get_slot('recipe_current_step')

        recipe_current_step_display = recipe_current_step + 1
        current_step_text = recipe_steps_list[recipe_current_step]

        if how_to_query is None:
            vague_entities = get_vague_how_to(current_step_text)
            if len(vague_entities) > 0:
                dispatcher.utter_message(text="I was able to infer the following intermediate steps from Step {} that you may be confused about:".format(recipe_current_step_display))
                for entity in vague_entities:
                    dispatcher.utter_message(text="* {}".format(entity))
                formatted_query = "how+to+" + vague_entities[0].replace(" ", "+")    
                youtube_link = retrieve_youtube_video(formatted_query)
                dispatcher.utter_message(text="Here is a relevant Youtube video that may help clarify the process:\n\n{}".format(youtube_link))
        else:
            formatted_query = "how+to+" + how_to_query.replace(" ", "+")    
            youtube_link = retrieve_youtube_video(formatted_query)
            dispatcher.utter_message(text="Sure! Here's the most relevant Youtube tutorial I could find on how to {}:\n\n{}".format(how_to_query, youtube_link))
        
        return [SlotSet("how_to_query", None)]

###############################################################
# Specific what-is utterances.
###############################################################

class ActionWhatIs(Action):

    def name(self) -> Text:
        return "action_what_is"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        what_is_query = tracker.get_slot('what_is_query')

        if what_is_query is None:
            dispatcher.utter_message(text="Hmm, I am not sure what you are referring to... Could you be more specific?")
        else:
            wiki_summary_json = what_is_wiki_summary(what_is_query)
            summary_title = wiki_summary_json["title"]
            summary_image = wiki_summary_json["image"]
            summary_text = wiki_summary_json["summary"][0]

            dispatcher.utter_message(text="Let's find out together! Here's what I was able to summarize from reading about *{}* on Wikipedia.".format(summary_title))
            dispatcher.utter_message(image = summary_image)
            dispatcher.utter_message(text=">{}".format(summary_text))
            dispatcher.utter_message(text="Hope this was helpful! Anything else you'd like to ask?")

        return [SlotSet("what_is_query", None)]

###############################################################
# Ingredient how-much utterances.
###############################################################

class ActionHowMuch(Action):

    def name(self) -> Text:
        return "action_how_much"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        how_much_query = tracker.get_slot('how_much_query')
        recipe_ingredients_list = tracker.get_slot('recipe_ingredients_list')
        ingredients_json = parse_ingredients(recipe_ingredients_list)
        
        found_ingredient = False
        if how_much_query is None:
            dispatcher.utter_message(text="Hmm, I am not sure what you are referring to... Could you be more specific?")
        else:
            for individual_ingredient in ingredients_json["ingredients"]:
                if how_much_query in individual_ingredient["name"]:
                    dispatcher.utter_message(text="According to the recipe, you need {} {}(s) of {}. Hope this helps!".format(individual_ingredient["quantity"], individual_ingredient["unit"], individual_ingredient["name"]))
                    found_ingredient = True
        
        if not found_ingredient and how_much_query is not None:
            dispatcher.utter_message(text="This recipe does not use {}! Are you looking at the correct recipe?".format(how_much_query))

        return [SlotSet("how_much_query", None)]

###############################################################
# Recipe how-long utterances.
###############################################################

class ActionHowLong(Action):

    def name(self) -> Text:
        return "action_how_long"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        how_long_query = tracker.get_slot('how_long_query')

        recipe_steps_list = tracker.get_slot('recipe_steps_list')
        recipe_current_step = tracker.get_slot('recipe_current_step')

        recipe_current_step_display = recipe_current_step + 1
        current_step_text = recipe_steps_list[recipe_current_step]

        duration = get_duration(current_step_text, how_long_query)

        if duration is None:
            dispatcher.utter_message(text="Hmm, I was unable to find a specific duration for how long you should {}. Maybe try rereading that step?".format(how_long_query))
        else:
            dispatcher.utter_message(text="Let me check for you! Here's what I found for this step:\n\n>{}\n\nHope this helps!".format(duration))
            
        return [SlotSet("how_long_query", None)]

###############################################################
# Individual ingredient substitute utterances.
###############################################################

class ActionSubstitute(Action):

    def name(self) -> Text:
        return "action_substitute"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve values from slots.
        substitute_query = tracker.get_slot('substitute_query')

        if substitute_query is None:
            dispatcher.utter_message(text="Hmm, I am not sure what you are referring to... Could you be more specific?")
        else:
            substitute_ingredient_json = substitute_ingredient(substitute_query)
            if substitute_ingredient_json["status"] == "success":
                dispatcher.utter_message(text="Great question! Here are {} some possible substitutes and their proportions I found for {}:".format(len(substitute_ingredient_json["substitutes"]), substitute_query))
                for substitute in substitute_ingredient_json["substitutes"]:
                    dispatcher.utter_message(text="* {}".format(substitute))

            else:
                dispatcher.utter_message(text="Hmm, I was unable to find any suitable substitutes for {}.".format(substitute_query))

        return [SlotSet("substitute_query", None)]

###############################################################
# Recipe transformation utterances.
###############################################################

class ActionToVegetarian(Action):

    def name(self) -> Text:
        return "action_transform_to_vegetarian"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve values from slots.
        recipe_prep_time = tracker.get_slot('recipe_prep_time')
        recipe_ingredients_list = tracker.get_slot('recipe_ingredients_list')
        recipe_steps_list = tracker.get_slot('recipe_steps_list')

        # Transform recipe and retrieve updated values.
        updated_recipe_prep_time, updated_recipe_ingredients_list, updated_recipe_steps_list, = transform_recipe(meat_substitutions, recipe_prep_time, recipe_ingredients_list, recipe_steps_list)

        ingredients_text = "Of course! Here is the vegetarian version of the recipe ingredient list:\n\n"
        for index, ingredient in enumerate(updated_recipe_ingredients_list):
            ingredients_text += (str(index + 1)) + ". " + ingredient + "\n"
        ingredients_text += "\nHope this helps!"

        dispatcher.utter_message(text=ingredients_text)
        return []

class ActionFromVegetarian(Action):

    def name(self) -> Text:
        return "action_transform_from_vegetarian"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement from vegetarian.")
        
        return []

class ActionToHealthy(Action):

    def name(self) -> Text:
        return "action_transform_to_healthy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement to healthy.")
        
        return []
        
class ActionFromHealthy(Action):

    def name(self) -> Text:
        return "action_transform_from_healthy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement from healthy.")
        
        return []
        
class ActionToSouthAsian(Action):

    def name(self) -> Text:
        return "action_transform_to_south_asian"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement to South Asian.")
        
        return []
        
class ActionHalfServing(Action):

    def name(self) -> Text:
        return "action_transform_half_serving"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement to half serving.")
        
        return []
        
class ActionDoubleServing(Action):

    def name(self) -> Text:
        return "action_transform_double_serving"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement to double serving.")
        
        return []