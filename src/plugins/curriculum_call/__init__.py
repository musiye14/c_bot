import json
import os
filename = 'src/plugins/curriculum_call/class_data.json'
def save(data):
    with open("src/plugins/curriculum_call/class_data.json", "w") as f:
        json.dump(data,f)

if not os.path.exists(filename):
    class_data={'':[""]}
    save(class_data)