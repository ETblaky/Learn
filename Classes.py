import boto3
from datetime import datetime
from datetime import timedelta
import pytz

client = boto3.client('sdb', region_name='us-west-2', aws_access_key_id='{}',
                      aws_secret_access_key='{}')


def get_day(slots):
    if 'value' in slots["day_week"]:
        weekDay = slots["day_week"]["value"].title()
    elif 'value' in slots["day"]:
        weekDay = get_today() if slots["day"]["value"] == "today" else get_tomorrow()
    else:
        weekDay = get_tomorrow()
    return weekDay


def get_today():
    return datetime.now(pytz.timezone(zone="America/Sao_Paulo")).strftime('%A')


def get_tomorrow():
    return (datetime.now(pytz.timezone(zone="America/Sao_Paulo")) + timedelta(days=1)).strftime('%A')


def get_classes(day):
    response = client.get_attributes(
        DomainName='learn-subjects',
        ItemName=day
    )
    return response["Attributes"]


def find_index(dicts, key, value):
    class Null:
        pass

    for i, d in enumerate(dicts):
        if d.get(key, Null) == value:
            return i


def reorder(raw_classes):
    classes = []
    raw_classes = raw_classes
    for i in range(1, 6):
        classes.append(raw_classes[find_index(raw_classes, 'Name', str(i))]["Value"])

    return classes


def stringfy(reordered):
    final_response = reordered[0] + ", " + reordered[1] + ", " + reordered[2] + ", " + reordered[3] + " and " + reordered[4]
    return final_response


def get_response(slots):
    return stringfy(reorder(get_classes(get_day(slots))))
