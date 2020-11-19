"""
View UTSC laundry status from the command line


Example Output:

=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=
University Of Toronto - Scarborough Campus
Foley 1
2020-01-18 18:32:59

Washers
    01 ▕▒▒▒▒▒▒▒        ▏ 35 mins remaining
    02 ▕               ▏ Available

Dryers
    03 ▕               ▏ Available
    04 ▕               ▏ Available

"""

import json
from urllib.request import urlopen

key_objects = "objects"
key_percentage = "percentage"
key_time_remaining = "time_remaining"
key_time_left_lite = "time_left_lite"
key_appliance_desc = "appliance_desc"
key_appliance_type = "appliance_type"

def progress_bar_builder(percentage: float, width: int) -> str:
    left_char, right_char, filled_char, empty_char = "▕", "▏", "▒", " "

    result = ""
    result += left_char
    filled_width = min(int(width * percentage), width)
    empty_width = width - filled_width
    result += filled_width * filled_char
    result += empty_width * empty_char
    result += right_char

    return result


def get_status(school_id, room_id):
    school_id = str(school_id)
    room_id = str(room_id)
    ROOM_INFO_URL = "https://www.laundryview.com/api/c_room?loc={}&room={}".format(school_id, room_id)
    ROOM_DATA_URL = "https://www.laundryview.com/api/currentRoomData?school_desc_key={}&location={}".format(school_id, room_id)

    #from io import StringIO
    #import sys
    #output = StringIO()
    #sys.stdout = output
    output = ""

    school_name = ""
    try:
        room_info = json.loads(urlopen(ROOM_INFO_URL).read())
        school_name = room_info['school_name'].strip()
    except KeyError:
        raise ValueError("Property Not Found: " + school_id)

    room_name = ""
    try:
        for room in room_info['room_data']:
            if room['laundry_room_location'] == room_id:
                room_name = room['laundry_room_name'].strip()
                break
        else:
            raise KeyError
    except KeyError:
        raise ValueError("Room Not Found: " + room_id)

    output += school_name.title() + "\n" + room_name.title() + "\n"
    from datetime import datetime
    output += datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n"
    output += "\n"

    room_data = urlopen(ROOM_DATA_URL)
    room_data_object = json.loads(room_data.read())
    machines = room_data_object[key_objects]

    washers, dryers = [], []
    for machine in machines:
        if key_appliance_type not in machine:
            continue
        appliance_type = machine[key_appliance_type]
        if appliance_type == 'D':
            dryers.append(machine)
        elif appliance_type == "W":
            washers.append(machine)
        else:
            raise ValueError("Unknown appliance type: " + appliance_type)

    def compose_machine_info(machine) -> str:
        line = ""
        line += machine[key_appliance_desc] + " "
        line += progress_bar_builder(machine[key_percentage], width=15) + " "
        line += machine[key_time_left_lite]
        return line

    washers.sort(key=lambda x: int(x[key_appliance_desc]))
    dryers.sort(key=lambda x: int(x[key_appliance_desc]))

    if len(washers) > 0:
        output += "Washers\n"
        for washer in washers:
            output += "    " + compose_machine_info(washer) + "\n"
        output += "\n"

    if len(dryers) > 0:
        output += "Dryers\n"
        for dryer in dryers:
            output += "    " + compose_machine_info(dryer) + "\n"

    return output


if __name__ == '__main__':
    FOLEY = (7621, 8989892)

    print("=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=")
    print(get_status(*FOLEY))
