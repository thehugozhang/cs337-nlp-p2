from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

# Relative import of custom recipe parsing functions.
from .recipe import parse_recipe, parse_ingredients

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

            dispatcher.utter_message("Great, let's cook {} which has {} steps! What would you like to know?".format(recipe_name, recipe_steps))

            # Set slot values with parsed information so CH3FB0T can "remember" data about the recipe.
            return [
                SlotSet("recipe_name", recipe_name),
                SlotSet("recipe_steps", recipe_steps),
                SlotSet("recipe_steps_list", recipe_steps_list),
                SlotSet("recipe_current_step", 0),
                SlotSet("recipe_ingredients_list", recipe_ingredients),
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

class ActionPreviousStep(Action):

    def name(self) -> Text:
        return "action_previous_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement previous step here.")

        return []

class ActionNextStep(Action):

    def name(self) -> Text:
        return "action_next_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement next step here.")

        return []

class ActionNthStep(Action):

    def name(self) -> Text:
        return "action_nth_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement nth step here.")

        return []

class ActionRepeatStep(Action):

    def name(self) -> Text:
        return "action_repeat_step"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Implement repeat step here.")

        return []