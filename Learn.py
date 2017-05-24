from AskPy import Ask
import Classes


def lambda_handler(event, context):
    global ask
    ask = Ask(event)

    skill_name = "School"
    reprompt_text = " Ask me the subjects"

    ask.skill_name = skill_name
    ask.reprompt_text = reprompt_text


    @ask.on_launch
    def launch():
        return "Just say: Alexa, ask Learn my classes tomorrow"


    @ask.on_intent("classes")
    def classes(slots):

        data = Classes.get_response(slots["class"]["value"].title())

        return {
            "card_name": "Subjects",
            "card_body": "You have " + data + ".",
            "speech_output": "You have " + data + ".",
            "reprompt_text": "Sorry, I didn't understand you."
        }

    @ask.on_intent("verifyHave")
    def verify_have(slots):

        data = Classes.reorder(Classes.get_classes(slots["class"]["value"].title()))

        return {
            "card_name": "Subjects",
            "card_body": "Yes, you do have." if slots["class"]["value"].title() in data else "No, you dont have.",
            "speech_output": "Yes, you do have." if slots["class"]["value"].title() in data else "No, you dont have.",
            "reprompt_text": "Sorry, I didn't understand you."
        }


    @ask.on_help
    def help():
        return "Just say: Alexa, ask Learn my classes tomorrow"


    @ask.on_stop
    def stop():
        return "Ok"

    print(ask.output)
    return ask.output
