"""
This file holds the functions that handle the requests' bodies,
as well as the data included in them, after they are processed and edited accordingly.
"""


def clear_request_body():
    clear_data = {}
    return clear_data


def titles_request_body(role_names, permission_names):
    name_data = [
        {
            "majorDimension": "COLUMNS",
            "range": "A2",
            "values": [role_names]
        },  # Fills the first column with all of the role names.
        {
            "majorDimension": "ROWS",
            "range": "B1",
            "values": [permission_names]
        },
        ]  # Fills the first column with all of the permission names.

    request_body = {
        "data": name_data,
        "valueInputOption": "RAW"
    }
    return request_body


def values_request_body(permission_values):
    permission_data = []
    for i in range(len(permission_values)):  # Creates a data list for the request in a smart way, so as to make the size of the request dynamic, depending on the amount of roles and permissions.
        permission_data.append({"majorDimension": "ROWS", "range": "B" + str(i + 2), "values": [list(permission_values[i].values())]})

    request_body = {
        "data": permission_data,
        "valueInputOption": "RAW"
    }
    return request_body


"""
Converts all the True/False values to ✔ and ❌ for user friendliness.
"""
def permission_values_to_emojis(permission_values, permission_names):
    for i in range(len(permission_values)):
        if permission_values[i]["administrator"]:
            for perm_name in permission_names:
                permission_values[i][perm_name] = "✔️"
        else:
            for perm_name in permission_names:
                if permission_values[i][perm_name]:
                    permission_values[i][perm_name] = "✔️"
                else:
                    permission_values[i][perm_name] = "❌"
    return permission_values
