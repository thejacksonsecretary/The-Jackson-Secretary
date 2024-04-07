import google.generativeai as genai
import ast
from datetime import date
import json

def addToDB(user, newData):
    with open("data_file.json", "r") as file:
        data_string = file.read()
    data = json.loads(data_string)
    if (user in data.keys()) == False:
        data[user]=[]
    for i in newData:
        data[user].append(i)
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)

def bgInfoStringGenerator(userData):
  bgInfoString = ""
  for i in range(len(userData)):
    bgInfoString = bgInfoString + userData[i][0] + "," + userData[i][1] + "," + userData[i][2]+";"
  return bgInfoString

def dumpTruck(user):
    with open("data_file.json", "r") as file:
        data_string = file.read()
    data = json.loads(data_string)
    return data[user]

def prompt(prompt, user):
    #Obtain userData
    with open("data_file.json", "r") as file:
        data_string = file.read()
    data = json.loads(data_string)
    if user in data.keys():
        data[user]
    else:
        data[user] = []
    userData = data[user]

    #Produce the first model response (for user viewing)
    promptString = ''' You will receive a prompt. There are several types of prompts: querying, scheduling, and shifting.You will also be given some context (the user’s calendar) in the format [event, startTime, endTime]. Times will be given in the YYYY-MM-DDhh:mm format such that hh begins from 01 to 24. A querying prompt asks about items already in schedule. These are your “Can I fit in [event] at [time] on [date]?” or “What do I have on [date] at [time]?” prompts. A scheduling prompt tells you about new events or asks you to schedule new events. These are your “I have [event] at [time] on [date]” or “Schedule an [event] at [time] on some arbitrary [date]” prompts. A shifting prompt asks you to change the time of an event or to cancel an event. These are your “Change the scheduling of [event] from [day & time] to [day & time]” or “Cancel [event] on [date]” prompts. Context: [["birthday party", "2024-04-0620:00", "2024-04-0702:00"], ["conference", "2024-04-0810:00", "2024-04-0818:00"]]
    The examples above are only for format reference; they do not reflect the user's actual schedule.''' + "Context:" + str(userData) + '''Here is your prompt:''' + prompt + ''' Today's date is ''' + str(date.today())
    print(promptString)
    genai.configure(transport='grpc')
    name = "tunedModels/generate-num-9053"
    model = genai.GenerativeModel(model_name = name)
    responseForUser = (model.generate_content(promptString)).text
    print(responseForUser)
    #Potentially sort the contents of a request.
    promptString = '''You will receive one of three types of prompts. A querying prompt asks about items already in schedule. These are your “Can I fit in [event] at [time] on [date]?” or “What do I have on [date] at [time]?” prompts. Simply return an empty Python list if you receive a query prompt. A scheduling prompt tells you about new events or asks you to schedule new events. These are your “I have [event] at [time] on [date]” or “Schedule an [event] at [time] on some arbitrary [date]” prompts. Given a scheduling prompt, return a multi-dimensional list of the following format [[firstEvent, startTime, endTime], [secondEvent, startTime, endTime]]. Remember that every entry is a string. Start times and end Times should be written using the format YYYY-MM-DDhh:mm such that hh (hours) go from 01 to 24. For instance, “Schedule my duck hunting session for 9:30 AM to 10:30 AM on June 7, 2024” becomes [[“duck hunting”, “2024-06-0709:30”,“2024-06-0710:30”]]. Another example is “I will be going to school from 8:00 AM to 3:00 PM on January 5th 2025. I will then go skiing that day from 6 PM to 9 PM” becomes [[“school”, “2025-01-0508:00”,“2025-01-0515:00”],[“skiing”, “2025-01-0518:00”, “2025-01-0521:00”]]A shifting prompt asks you to change the time of an event or to cancel an event. These are your “Change the scheduling of [event] from [day & time] to [day & time]” or “Cancel [event] on [date]” prompts. Make edits to the context below. For instance, “Cancel my skiing on December 7 2025” would turn [[“exercise”, “2025-12-0706:00”, “2025-12-0709:00”],[“skiing”, “2025-12-0718:00”, “2025-12-0721:00”]] into [[“skiing”, “2025-12-0718:00”, “2025-12-0721:00”]]. An empty list context represents nothing having been scheduled yet.
Context: ''' + str(userData) + '''Prompt:''' + prompt + ''' Today's date is ''' + str(date.today())
    genai.configure(transport='grpc')
    name = "tunedModels/generate-num-2260"
    model = genai.GenerativeModel(model_name = name)
    userData = ast.literal_eval((model.generate_content(promptString)).text)
    data[user] = userData
    if data[user] != []:
        with open("data_file.json", "w") as write_file:
            json.dump(data, write_file)
    return responseForUser
