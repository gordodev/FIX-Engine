#!/usr/bin/env python

#Validate valid order or non-order(reject) & Identify message type

#import time
#import os

def checkMsgType(Msg):
	#Function syntax check:
	#print("You entered \" "+Msg,"Can I? Kark Kani?")
	#print("You entered \""+Msg+"\"")
	
	#ID MsgType
	if Msg == "35=8":
		print("Execution")
	if Msg == "35=D":
		print("Order")
	if Msg == "35=F":
		print("Cancel request")
	if Msg == "35=3":
		print("Session reject")

#["35=D":"Order","35=8":"Execution","35=F":"Cancel request","35=3":"Session Reject"]
#Prompt User for FIX message
input_InFIXMsg = raw_input("Enter FIX Message: ")
checkMsgType(input_InFIXMsg)



