import google.generativeai as genai 
import ast 
from datetime import date 

def bgInfoStringGenerator(userData):
  bgInfoString = ""
  for i in range(len(userData)):
    bgInfoString = bgInfoString + userData[i][0] + "," + userData[i][1] + "," + userData[i][2]+";"
  return bgInfoString

def prompt(prompt, userData): 
    #Prepare background information
    bgInfoString = bgInfoStringGenerator(userData)
    #Prepare prompt
    promptString = '''A user's current calendar is given below in the format activity,startTime,endTime;activity,startTime,endTime. Return a response (and only the response) to the prompt you are given using the background information provided. \n'''
    promptString = promptString + "background information:" + bgInfoString + "\n"
    promptString = promptString + "prompt:" + prompt 
    #Response for user
    api_key = "AIzaSyC-rPRwYKWBTs6TE5kaRd83KBABujbrkSc"
    genai.configure(api_key=api_key)
    model=genai.GenerativeModel("gemini-pro")
    response=(model.generate_content(promptString)).text
    #Return a list about a new event (if applies). 
    orderingRequest = '''You will be given a prompt. You must order it.
I will give you some examples of the ordering I want to see: 
"Schedule my meeting for 7:00PM tomorrow. It will end at 9:00PM." -- [["meeting", "2024-04-0719:00", "2024-04-0711:00"]]

"Schedule my bungee jumping lesson for 8:00 PM tomorrow. I will stop bungee jumping at 8:30. I will then go to the food truck from 9:00 PM to 10:00 PM." -- [["bungee jumping", "2024-04-0620:00", "2024-04-0620:30"], ["food truck", "2024-04-0621:00", "2024-04-0622:00"]]

"I will be swimming tomorrow at 9:00. I will end at 10:00 AM." -- 
[["swimming", "2024-04-069:00", "2024-04-0610:00"]]

Basically, use [activity, startTime, endTime]
A group of events (minimum of one event in a group) must be denoted by []. Each event within must have its own []. ONLY RETURN THE ORDERED SEQUENCE. USE THE FORMAT YYYY-MM-DDhh:mm for time. Remember that that hh:mm's hour component goes from 01 to 24. Thus, 1:00 PM is actually 13:00.
If you cannot generate a response, return an empty Python list []. For your reference, today is''' + str(date.today()) +"Format like I told you to: " + prompt
    eventList = (model.generate_content(orderingRequest)).text
    eventList = ast.literal_eval(eventList)
    return (response, eventList)

print(prompt(input(),[["1 hour walk", "2024-04-0509:00", "2024-04-0510:00"],["friend's birthday party","2024-04-0517:00", "2024-04-0518:00"],["group chat ball check", "2024-04-0512:00","2024-04-0512:30"]]))