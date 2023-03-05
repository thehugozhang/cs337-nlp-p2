from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

# Relative import of custom recipe parsing functions.
from .recipe import parse_recipe, parse_ingredients, alnum_parse_ordinal

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
        dispatcher.utter_message(text='Implement specific how-to queries: "{}".'.format(how_to_query))
        
        return [SlotSet("how_to_query", None)]