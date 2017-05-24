from __future__ import print_function


class Ask(object):
    def __init__(self, json):
        self.request_type = json['request']['type']
        self.output = "Sorry, something went wrong..."
        self.skill_name = ""
        self.reprompt_text = ""

        if self.request_type == 'IntentRequest':
            self.intent = json['request']['intent']
            self.intent_name = json['request']['intent']['name']
            self.intent_slots = None if 'slots' not in json['request']['intent'] else json['request']['intent']['slots']

    def on_launch(self, f):
        if self.request_type == 'LaunchRequest':
            self.output = build_response("Subjects", f(), f(), self.reprompt_text, True)
            return

    def on_intent(self, name):
        def decorator(f):
            try:
                value = self.intent_name
            except AttributeError:
                return

            if self.intent_name == name:
                result = f(self.intent_slots)
                self.output = build_response(
                    result["card_name"],
                    result["card_body"],
                    result["speech_output"],
                    result["reprompt_text"] + self.reprompt_text if result[
                                                                        "reprompt_text"] is not None else self.reprompt_text,
                    True
                )

        return decorator

    def on_stop(self, f):
        if 'intent_name' in locals() and self.intent_name == 'AMAZON.StopIntent':
            self.output = build_response("Stop", f(), f(), self.reprompt_text, True)
            return

    def on_help(self, f):
        if 'intent_name' in locals() and self.intent_name == 'AMAZON.HelpIntent':
            self.output = build_response("Help", f(), f(), self.reprompt_text, False)
            return


def build_response(card_title, card_body, speech_output, reprompt_text, should_end_session):
    return {
        'version': 'School',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': speech_output
            },
            'card': {
                'type': 'Simple',
                'title': card_title,
                'content': speech_output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }
    }
