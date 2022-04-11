import json
def look():
    with open("class_data.json", "r") as f:
        data = json.load(f)
        # print("加载完成：")
        # print(data)
    return data


def save_qq(data):
    with open("class_data.json", "w") as f:
        json.dump(data, f)


# 增加函数
def add_qq(class_id, qq_id):
    del_qq(qq_id)
    class_data = look()
    if (class_id not in class_data):
        class_data[class_id] = [qq_id]
    else:
        class_data[class_id].append(qq_id)
    save_qq(class_data)
    # print("增加后：")
    # print(class_data)


# 删除函数
def del_qq(qq_id):
    class_data = look()
    for i in class_data:
        if (class_data[i].count(qq_id) != 0):
            class_data[i].remove(qq_id)
    save_qq(class_data)
    # print("删除后：")
    # print(class_data)


# 找同一个班级的qq号
def find_qqs(class_id):
    class_data = look()
    qqs = class_data[class_id]
    return qqs

