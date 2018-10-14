#!/usr/bin/python2.7
'''
------# ! / usr /bin/env python
'''
#Validate valid order or non-order(reject) & Identify message type

import time
from six.moves import input
import os
clear = lambda: os.system('clear')



input_TryAgain = 'n'
StopRun = 'no'

while StopRun != 'yes':

	#Prompt User for FIX message
	input_InFIXMsg = raw_input("Enter FIX Message: ")

	#Validate message

	while input_InFIXMsg not in ['35=D', '35=8']:
		clear()
		print("ERROR: **Invalid message type**")
		print('')
		input_TryAgain = raw_input ("Enter Again?\n[y/n] ")
		
		if input_TryAgain == ('y'):
			StopRun = ('no')
			print('Looping...')
			time.sleep(1)
			clear()
			break

		if input_TryAgain == ('n'): #This logic works when valid FIX message; because default TryAgainset above to no?
			StopRun = ('yes')
			break
print("\n"*100)
print('FIX Engine validator now OFFLINE!')


#End Program
