import json


def save(data):
    with open("src/curriculum_call/class_data.json.json", "w") as f:
        json.dump(data,f)
class_data={'':[""]}
save(class_data)