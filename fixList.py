#!/usr/bin/env python2.7
'''
STATUS:
[X] Take FIX message from user and then insert into an array
[X] Add array modification feature 10/14
[X] Basic error handling for input format
QA:
[X] Application works as expected
NOTE: Need to add syntax validation. That might need to be added to the FIX Validator as well. IF user violates expected syntax like wrong or no delimiter this will break. NEEDS TAG=VALUE,TAG=VALUE
'''

def Convert(string):
    """Convert comma-separated string to list."""
    if not string:
        return []
    li = list(string.split(","))
    return li

def validate_fix_format(fix_msg):
    """Basic validation for FIX message format."""
    if not fix_msg:
        return False
    
    # Check if message contains at least one TAG=VALUE pair
    if "=" not in fix_msg:
        return False
    
    # Check each item has the TAG=VALUE format
    for item in fix_msg.split(","):
        if "=" not in item:
            return False
    
    return True

# Clear screen and show program header
print("\n"*100)
print("FIX Array v3.1")
print("SYNTAX: 'TAG=VALUE,TAG=VALUE'")

# Main program loop to allow retrying
while True:
    try:
        # Prompt User for FIX message
        input_InFIXMsg = raw_input("Enter FIX Message (or 'q' to quit): ")
        
        # Exit condition
        if input_InFIXMsg.lower() == 'q':
            print("Exiting program.")
            break
        
        # Validate input format
        if not validate_fix_format(input_InFIXMsg):
            print("Error: Invalid FIX message format. Please use TAG=VALUE,TAG=VALUE format.")
            continue
        
        # Parse contents of input_InFIXMsg
        print("You entered \"" + input_InFIXMsg + "\"")
        
        str1 = input_InFIXMsg
        myList = Convert(str1)
        print(myList)
        
        # Check if list has at least two elements
        if len(myList) < 2:
            print("Warning: FIX message has fewer than 2 fields. Cannot modify MsgType.")
            continue
            
        # Prompt user for new MsgType
        input_newMsgType = raw_input("Enter new MsgType (or 'skip' to keep current): ")
        
        if input_newMsgType.lower() != 'skip':
            # Validate new MsgType has proper format
            if "=" not in input_newMsgType:
                print("Warning: New MsgType doesn't contain '='. Adding 35= prefix.")
                input_newMsgType = "35=" + input_newMsgType
                
            myList[1] = input_newMsgType
            print("Updated message:")
            print(myList)
            
    except IndexError:
        print("Error: Unable to modify the specified field. Message may be too short.")
    except Exception as e:
        print("An unexpected error occurred: " + str(e))

'''
NOTES:
print (myList)   #Prints entire list
print myList[1]  #Prints index 1  
'''
