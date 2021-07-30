"""
This file holds functions that return the link of the picture/link requested by the main function.
Mainly created to keep the main file clean from enormous links.
Instead of using a local file and uploading it everytime, it grabs the link.
"""


def picture(image_name=None):
    images = {
        "SUCCESS": "https://i.imgur.com/sp2zmN9.png",
        "ERROR": "https://i.imgur.com/lLlHVPq.png",
        "GSHEET": "https://i.imgur.com/u9PgNkk.png"
    }
    return images[image_name]


def color(color_type=None):
    colors = {
        "GREEN": 0x14F200,
        "RED": 0xE10E0E
    }
    return colors[color_type]


def link(link_type=None):
    links = {
        "SPREADSHEET": "https://docs.google.com/spreadsheets/d/",
        "SCOPE": ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"],
        "TUTORIAL": "https://i.imgur.com/wG2DgC9.png"
    }
    return links[link_type]
