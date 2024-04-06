import json

def convertDateString(isoInput):

    """Takes a string in YYYY-MM-DDhh:mm and returns a dictionary with the date details"""

    try:
        date = {
            "year": int(isoInput[0:4]),
            "month": int(isoInput[5:7]),
            "day": int(isoInput[8:10]),
            "hour": int(isoInput[10:12]),
            "minute": int(isoInput[13:15])
        }
    except:
        date = ""

    return date

def convertDateDict(date):
    return f"{date["year"]:04d}-{date["month"]:02d}-{date["day"]:02d}{date["hour"]:02d}{date["minute"]:02d}"

class calendarEvent:

    name = ""
    date = ""

    def __init__(self, json_input):

        """Loads in JSON with name and date attributes to a calendar object"""

        event_dict = json.load(json_input)
        self.name = event_dict["name"]
        self.date = convertDateInput(event_dict["date"])

    def get_json(self):
        event_dict = {
            "name": self.name,
            "date": convertDateDict(self.date)
        }
        return json.dumps(event_dict)
