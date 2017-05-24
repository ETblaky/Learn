import boto3

client = boto3.client('sdb', region_name='us-west-2', aws_access_key_id='{}',
                      aws_secret_access_key='{}')


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
    final_response = reordered[0] + "," + reordered[0] + "," + reordered[0] + "," + reordered[0] + "and" + reordered[0]
    return final_response


def get_response(day):
    return stringfy(reorder(get_classes(day)))



print(reorder(get_classes("Monday")))
