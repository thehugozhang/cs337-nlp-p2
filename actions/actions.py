from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

###############################################################
# Recipe parsing / slot memory utterance.
###############################################################

class ActionParseRecipe(Action):

    def name(self) -> Text:
        return "action_parse_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Great! Please provide a recipe URL to get started.")

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