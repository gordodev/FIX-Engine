#!/usr/bin/python2.7
'''
------# ! / usr /bin/env python
'''
#Validate valid order or non-order(reject) & Identify message type

import time
from six.moves import input

input_TryAgain = 'no'
StopRun = 'no'

while StopRun != 'yes':

	#Prompt User for FIX message
	input_InFIXMsg = raw_input("Enter FIX Message: ")

	#Validate message

	while input_InFIXMsg not in ['35=D', '35=8']:
		print("Invalid message type. Please try again.")
		input_TryAgain = raw_input ("Enter Again: ")
		if input_TryAgain == ('yes'):
			StopRun = ('no')
			print('You just entered yes so I\'m giving ya another chance...')
			print('')
			print('Never gonna Give you up - Rick Astley!')
			time.sleep(2)
'''
The logic below can never work because the only way to get down here is if the validation fails at which point the default TryAgain value is used. Setting the value here is pointless as the loop ends here, so whatever value you set never gets seen! :)
'''
#	if input_TryAgain == ('yes'):
#		StopRun = ('no')
#		print('Never gonna Give you up - Rick Astley!')
#		time.sleep(2)
#	if input_TryAgain == ('no'): #This logic works when valid FIX message; because default TryAgainset above to no?
#		StopRun = ('yes')
#		print('End of Program!')
#		exit
'''
NOTE: I think the code is only getting to next section for fail condition
Note the indentation. The if below is not alligned with code above.
'''

    #       userInput = input ("Enter again?: ")
    #       userInput = userInput.lower ("")
    #       break();

   # if input_TryAgain == ('yes'):
    #        StopRun = ('no')
