#!/usr/bin/env python2.7
'''
Take FIX message from user and parse it into fields
NOTE: This is a simple experiment, not production code!
'''

def convert_delimiter(fix_msg, delimiter=None):
    '''
    Try to handle different delimiters people use when writing FIX messages
    SOH (ASCII 001) is standard but people use | ^ etc in readable formats
    '''
    # Real SOH character
    SOH = chr(1)
    
    # If no delimiter specified, try to guess
    if delimiter == None:
        # Common human-readable delimiters used instead of SOH
        if '|' in fix_msg:
            delimiter = '|'
        elif '^' in fix_msg:
            delimiter = '^'
        elif '~' in fix_msg:
            delimiter = '~'
        elif ',' in fix_msg:  # Not standard but in our test messages
            delimiter = ','
        else:
            # Default to SOH if can't detect
            delimiter = SOH
            
    # Convert to a standard delimiter for our processing
    # NOTE: In production would convert to real SOH, but using pipe for readability
    if delimiter != '|':
        fix_msg = fix_msg.replace(delimiter, '|')
        
    return fix_msg

# Get input from user
input_InFIXMsg = raw_input("Enter FIX Message (use commas, pipes, or ^ between fields): ")
print("You entered \"" + input_InFIXMsg + "\"")

# Standardize the delimiter
standardized_msg = convert_delimiter(input_InFIXMsg)
print("Standardized: " + standardized_msg)

# Parse into array (list)
def parse_fix_to_list(fix_string):
    '''Break FIX message into list of fields'''
    # Using pipe as our working delimiter
    li = list(fix_string.split("|"))
    return li

# Parse the message
myList = parse_fix_to_list(standardized_msg)
print('')
print("Full message as list:")
print(myList)

# Show a specific field if available
print('')
if len(myList) > 1:
    print("Second field: " + myList[1])
else:
    print("Message doesn't have enough fields")

# Extract message type if present
msgType = None
for field in myList:
    if field.startswith("35="):
        msgType = field[3:]  # Get everything after "35="
        break

if msgType:
    print('')
    print("Message type (35): " + msgType)
    
    # Show what the message type means
    # NOTE: Just a few common ones for testing
    if msgType == "D":
        print("This is a New Order - Single message")
    elif msgType == "8":
        print("This is an Execution Report message")
    elif msgType == "F":
        print("This is an Order Cancel Request message")
    elif msgType == "3":
        print("This is a Reject message")
    else:
        print("Unknown message type")
