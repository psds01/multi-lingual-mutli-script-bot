# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from action_utterance_templates import templates


def get_template(action_name, language, script, templates=templates):
    return templates[action_name][language][script]


def get_language_and_script(tracker):
    """Return script and language from the latest user message."""
    script = "latin"
    language = "en"
    for event in reversed(tracker.events):
        if event.get("event") == "user":
            parse_data = event['parse_data']
            language = parse_data['language']['name']
            script = parse_data['script']
            break
    return language, script


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language, script = get_language_and_script(tracker)
        dispatcher.utter_message(get_template(self.name(), language, script))
        return []


class ActionCheerUp(Action):

    def name(self) -> Text:
        return "action_cheer_up"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        language, script = get_language_and_script(tracker)
        dispatcher.utter_template(
            "{}_{}_utter_cheer_up".format(language, script), tracker)

        return []


class ActionDidThatHelp(Action):

    def name(self) -> Text:
        return "action_did_that_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        language, script = get_language_and_script(tracker)
        dispatcher.utter_message(get_template(self.name(), language, script))

        return []


class ActionHappy(Action):

    def name(self) -> Text:
        return "action_happy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        language, script = get_language_and_script(tracker)
        dispatcher.utter_message(get_template(self.name(), language, script))

        return []


class ActionGoodbye(Action):

    def name(self) -> Text:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        language, script = get_language_and_script(tracker)
        dispatcher.utter_message(get_template(self.name(), language, script))

        return []
