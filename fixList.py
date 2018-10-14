#!/usr/bin/env python2.7
'''
STATUS:
[X] Take FIX message from user and then insert into an array
[X] Add array modification feature 10/14

QA:
[X] Application works as expected

NOTE: Need to add syntax validation. That might need to be added to the FIX Validator as well. IF user violates expected syntax like wrong or no delimiter this will break. NEEDS TAG=VALUE,TAG=VALUE

'''
print("\n"*100)
print("FIX Array v3")
print("SYNTAX: \'TAG=VALUE,TAG=VALUE\'")

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
#print (myList)   #Prints entire list

#As proof on concept, will change anything to show it can be done. In this case changing the MsgType which is illogical but serves it's educational purpose:

#Prompt user for new MsgType
input_newMsgType=raw_input("Enter new MsgType: ")

#myList.insert(1,input_newMsgType) #Inserts a NEW item into list; NOT replace
myList[1]=input_newMsgType

print (myList)


'''
NOTES:

print (myList)   #Prints entire list

print myList[1]  #Prints index 1  
'''

