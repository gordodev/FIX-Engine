#!/usr/bin/env python2.7
'''
Take FIX message from user and then insert into an array
'''

#Prompt User for FIX message
input_InFIXMsg=raw_input("Enter FIX Message: ")

#Parse contents of input_InFIXMsg
print("You entered \"" + input_InFIXMsg + "\"")

def Convert(string):
	li = list(string.split(","))
	return li

str1 = input_InFIXMsg
print(Convert(str1))
myList = Convert(str1)
print('')
print (myList)
print ('')
print myList[1]
