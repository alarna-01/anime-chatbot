#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic chatbot design --- for your own modifications

"""
#######################################################
# Initialise Wikipedia agent
#######################################################
import wikipedia
import nltk
import csv
import aiml
import pandas
from nltk.sem.logic import *
from nltk.sem import Expression
from nltk.inference import ResolutionProver
read_expr = Expression.fromstring

import json, requests
APIkey = "5403a1e0442ce1dd18cb1bf7c40e776f" 
#  Initialise AIML agent

# Create a Kernel object. No string encoding (all I/O is unicode)
kern = aiml.Kernel()
kern.setTextEncoding(None)
kern.bootstrap(learnFiles="mybot-basic.xml")


kb=[]
data = pandas.read_csv('animekb.csv', header=None)
[kb.append(read_expr(row)) for row in data[0]]

integrity_check = ResolutionProver().prove(None, kb, verbose=False)
if integrity_check:
    print("Error, contradiction found in kb")
    quit()

# Define the path to your Q&A CSV file
csv_file_path = "C:/Users/Alarn/OneDrive - Nottingham Trent University/Year 3/ARTIFICIAL INTELLIGENCE/Coursework/generalanime.csv"

# Initialize an empty list to store the Q&A pairs
qa_pairs = []

# Read the CSV file using the csv module
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        question, answer = row
        qa_pairs.append({"question": question, "answer": answer})
        


# Welcome user
print("Welcome to this chat bot. Please feel free to ask questions from me!")

#######################################################
# Main loop
#######################################################
answer = ""
while True:
    #get user input
    try:
        userInput = input("> ")
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break
    #pre-process user input and determine response agent (if needed)
    responseAgent = 'aiml'
    
    for pair in qa_pairs:
        if userInput == pair["question"]:
            answer = pair["answer"]
            break    
    else:
        #activate selected response agent
        if responseAgent == 'aiml':
            answer = kern.respond(userInput)
    #post-process the answer for commands
    if answer[0] == '#':
        params = answer[1:].split('$')
        cmd = int(params[0])
        if cmd == 0:
            print(params[1])
            break
        elif cmd == 1:
            try:
                wSummary = wikipedia.summary(params[1], sentences=3,auto_suggest=False)
                print(wSummary)
            except:
                print("Sorry, I do not know that. Be more specific!")
        elif cmd == 2:
            succeeded = False
            api_url = r"http://api.openweathermap.org/data/2.5/weather?q="
            response = requests.get(api_url + params[1] + r"&units=metric&APPID="+APIkey)
            if response.status_code == 200:
                response_json = json.loads(response.content)
                if response_json:
                    t = response_json['main']['temp']
                    tmi = response_json['main']['temp_min']
                    tma = response_json['main']['temp_max']
                    hum = response_json['main']['humidity']
                    wsp = response_json['wind']['speed']
                    wdir = response_json['wind']['deg']
                    conditions = response_json['weather'][0]['description']
                    print("The temperature is", t, "°C, varying between", tmi, "and", tma, "at the moment, humidity is", hum, "%, wind speed ", wsp, "m/s,", conditions)
                    succeeded = True
            if not succeeded:
                print("Sorry, I could not resolve the location you gave me.")
                
        elif cmd == 31: # if input pattern is "I know that * is *"
            object,subject=params[1].split(' is ')
            expr=read_expr(subject + '(' + object + ')')
           
            kb.append(expr) 
            integrity_check = ResolutionProver().prove(None, kb, verbose=False)
            
            if not integrity_check:
                print("Okay! I'll remember that", object, "is", subject)
            else:
                print("Sorry! This contradicts with what i know!")
                kb.pop()
        
        elif cmd == 32: # if the input pattern is "check that * is *"
            object,subject=params[1].split(' is ')
            expr=read_expr(subject + '(' + object + ')')
            answer=ResolutionProver().prove(expr, kb, verbose=True)
            if answer:
               print('Correct.')
            else:
              kb.append(expr)
              integrity_check = ResolutionProver().prove(None, kb, verbose=False)

              if integrity_check:
                  print("Incorrect")
              else:
                  print("Sorry, I don't know :(")
              kb.pop()
              
        elif cmd == 99:
            print("I did not get that, please try again.")
    else:
        print(answer)