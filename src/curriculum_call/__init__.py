import json


def save(data):
    with open("class_data.json", "w") as f:
        json.dump(data,f)
class_data={'':[""]}
save(class_data)