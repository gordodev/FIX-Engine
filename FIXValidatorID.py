#!/usr/bin/env python

#Validate valid order or non-order(reject) & Identify message type

import time
import os 

os.system('clear')

input_TryAgain = 'n'
StopRun = 'n'


while StopRun != 'y':

        #Prompt User for FIX message
        input_InFIXMsg = raw_input("Enter FIX Message: ")

        #Validate message

        while input_InFIXMsg not in ['35=D', '35=8']:
                print("ERROR: **Invalid message type**.")
		print('')
                input_TryAgain = raw_input ("Enter Again?\n[y/n] ")
        

		if input_TryAgain == ('y'):
       			StopRun = ('n')
         	#	print('Never gonna Give you up - Rick Astley!')
        	#	time.sleep(2)
			break
		if input_TryAgain == ('n'):
         		StopRun = ('y')
          		print('End of Program!')
			os.system('clear')
			break

'''
NOTE: I think the code is only getting to next section for fail condition
Note the indentation. The if below is not alligned with code above.
'''
