from AskPy import Ask
import urllib
from urllib import request
import json


def lambda_handler(event, context):
    global ask
    ask = Ask(event)

    skill_name = "School"
    reprompt_text = " Ask me the subjects"

    ask.skill_name = skill_name
    ask.reprompt_text = reprompt_text

    def get_classes(slots, isToday=True):
        passwd = "123passwd456"

        if 'value' in slots["day_week"]:
            weekDay = slots["day_week"]["value"].title()
        elif 'value' in slots["day"]:
            weekDay = '*' if slots["day"]["value"] == "today" else '**'
        else:
            weekDay = '*' if isToday else '**'

        d = urllib.request.urlopen('http://etblaky.tk/api/school/subjects/' + passwd + '/' + weekDay).read()
        data = json.loads(d)

        return data

    @ask.on_launch
    def launch():

        subjectData = get_classes(None)

        subjectPhrase = "You have " + ', '.join(subjectData["subjects"])[::-1].replace(',', " and"[::-1], 1)[::-1] + " today. "
        return "Good Morning. " + subjectPhrase


    @ask.on_intent("classes")
    def classes(slots):

        data = get_classes(slots, False)

        return {
            "card_name": "Subjects",
            "card_body": "You have " + ', '.join(data["subjects"])[::-1].replace(',', " and"[::-1], 1)[::-1] + " on " + data["day"] + ".",
            "speech_output": "You have " + ', '.join(data["subjects"])[::-1].replace(',', " and"[::-1], 1)[::-1] + " on " + data["day"] + ".",
            "reprompt_text": "Sorry, I didn't understand you."
        }

    @ask.on_intent("verifyHave")
    def verify_have(slots):

        classes = get_classes(slots, False)["subjects"]

        return {
            "card_name": "Subjects",
            "card_body": "Yes, you do have." if slots["class"]["value"].title() in classes else "No, you dont have.",
            "speech_output": "Yes, you do have." if slots["class"]["value"].title() in classes else "No, you dont have.",
            "reprompt_text": "Sorry, I didn't understand you."
        }


    @ask.on_help
    def help():
        return "Just say: Alexa, ask School the subjects of tomorrow"


    @ask.on_stop
    def stop():
        return "Ok"

    print(ask.output)
    return ask.output
