import json

def extract_values(data):
    values = []
    if isinstance(data, dict):
        for value in data.values():
            values.extend(extract_values(value))
    elif isinstance(data, list):
       # for item in data:
        if isinstance(data, list):
            values.append(json.dumps(data))
        else:
            values.extend(extract_values(data))
    else:
        values.append(data)
    return values

data = {
    "beauty_title": "Some Title",
    "title": "Ну и ну",
    "other_titles": "Other Titles",
    "connect": "Some Connection",
    "add_time": "2022-01-01",
    "user": {
        "email": "UUUUUU",
        "fam": "XXXXXXX",
        "name": "XXXXX",
        "otc": "XXXXXX",
        "phone": "VVVVVVVV"
    },
    "coords": {
        "latitude": "888.888",
        "longitude": "444.444",
        "height": "5000"
    },
    "level": {
        "winter": "High",
        "summer": "Low",
        "autumn": "Medium",
        "spring": "Low"
    },
    "images": ["image1.jpg", "image2.jpg"]
}

values_list = extract_values(data)

print(values_list)


# def extract_values(data):
#     values = []
#     if isinstance(data, dict):
#         for value in data.values():
#             values.extend(extract_values(value))
#     # elif isinstance(data, list):
#     #     for item in data:
#     #         values.extend(extract_values(item))
#     else:
#         values.append(data)
#     return values
#
# data = {
#     'beauty_title': 'Some Title',
#     'title': 'Ну и ну',
#     'other_titles': 'Other Titles',
#     'connect': 'Some Connection',
#     'add_time': '2022-01-01',
#     'coords': {
#               'latitude': '888.888',
#               'longitude': '444.444',
#               'height': '5000'
#               },
#     'level': {
#               'winter': 'High',
#               'summer': 'Low',
#               'autumn': 'Medium',
#               'spring': 'Low'
#               },
#     'images': ['image1.jpg', 'image2.jpg']
# }
#
#
# values_list = extract_key(data)
# print(values_list)

# def extract_keys(data):
#     keys = []
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if not isinstance(value, dict):
#                 keys.append(key)
#             else:
#                 keys.extend(extract_keys(value))
#     return keys
#
# data = {
#     "beauty_title": "Some Title",
#     "title": "Ну и ну",
#     "other_titles": "Other Titles",
#     "connect": "Some Connection",
#     "add_time": "2022-01-01",
#     "user": {
#         "email": "UUUUUU",
#         "fam": "XXXXXXX",
#         "name": "XXXXX",
#         "otc": "XXXXXX",
#         "phone": "VVVVVVVV"
#     },
#     "coords": {
#         "latitude": "888.888",
#         "longitude": "444.444",
#         "height": "5000"
#     },
#     "level": {
#         "winter": "High",
#         "summer": "Low",
#         "autumn": "Medium",
#         "spring": "Low"
#     },
#     "images": ["image1.jpg", "image2.jpg"]
# }
#
# keys_list = extract_keys(data)
# print(keys_list)
