# FIX Protocol Experiments - My Notebook
# Just testing some ideas and concepts for FIX message handling
# Started: March 15, 2018

import re

# Convert between different FIX message delimiters
def convert_fix_delimiter(fix_message, current_delimiter=None):
    """
    Converts FIX messages between different delimiters to the standard SOH character.
    
    This function takes a FIX message with any delimiter and converts it to use
    the standard SOH (ASCII 001) delimiter that most FIX engines expect.
    
    Args:
        fix_message: The FIX message string to convert
        current_delimiter: What delimiter is currently used. If not provided, 
                          we'll try to figure it out automatically
    
    Returns:
        The converted FIX message with SOH delimiters
    """
    # This is the SOH character - ASCII code 1
    # Have to use chr(1) since SOH is a special control character
    SOH_CHAR = chr(1)  # Equivalent to '\x01' or '\001'
    
    # If user didn't tell us what delimiter is used, try to detect it
    if current_delimiter == None:
        # List of delimiters people commonly use instead of SOH
        delimiters = ['|', '^', '~', ',', ';', '\t']
        
        # Try to find the delimiter by looking at the message structure
        for delim in delimiters:
            # Look for typical FIX header pattern with the delimiter
            pattern = '8=FIX\\.\\d\\.\\d%s9=\\d+' % re.escape(delim)
            if re.search(pattern, fix_message):
                current_delimiter = delim
                print "Found delimiter: '%s'" % delim
                break
        
        # If we couldn't find a delimiter, check if SOH is already there
        if current_delimiter == None:
            if SOH_CHAR in fix_message:
                print "Message already uses SOH delimiter"
                return fix_message
            else:
                # Couldn't figure out the delimiter
                raise ValueError("Couldn't detect what delimiter is being used in the FIX message")
    
    # If message already uses SOH, just return it unchanged
    if current_delimiter == SOH_CHAR:
        return fix_message
    
    # Convert the message by replacing all delimiters with SOH
    converted_message = fix_message.replace(current_delimiter, SOH_CHAR)
    
    return converted_message


# Function to get the message type from a FIX message
def get_message_type(fix_message, delimiter=None):
    """
    Extract the message type (tag 35) from a FIX message
    """
    # Make sure we're working with SOH delimiters
    standardized_msg = convert_fix_delimiter(fix_message, delimiter)
    SOH_CHAR = chr(1)
    
    # Split the message into fields
    fields = standardized_msg.split(SOH_CHAR)
    
    # Look for tag 35 (MsgType)
    for field in fields:
        if field.startswith("35="):
            return field[3:]  # Return everything after "35="
    
    return None  # Tag 35 not found


# Original function from my early experiments
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


# Better version using dictionary - cleaner approach
def check_msg_type_improved(fix_message, delimiter=None):
    """Check what type of FIX message we're dealing with"""
    # Dictionary of message types and their descriptions
    msg_types = {
        "0": "Heartbeat",
        "1": "Test Request",
        "2": "Resend Request",
        "3": "Reject",
        "4": "Sequence Reset",
        "5": "Logout",
        "6": "Indication of Interest",
        "7": "Advertisement",
        "8": "Execution Report",
        "9": "Order Cancel Reject",
        "A": "Logon",
        "D": "New Order - Single",
        "F": "Order Cancel Request",
        "G": "Order Cancel/Replace Request"
    }
    
    # Get the message type
    msg_type = get_message_type(fix_message, delimiter)
    
    # Return the description if we know it
    if msg_type in msg_types:
        return msg_types[msg_type]
    else:
        return "Unknown message type: " + str(msg_type)


# Test the functions with some sample messages
if __name__ == "__main__":
    # Test with a pipe-delimited message
    test_msg = "8=FIX.4.2|9=123|35=D|11=ORD12345|55=AAPL|54=1|38=100|40=2|44=135.25|"
    print "Testing with message:", test_msg
    
    # Extract and check message type
    msg_type = check_msg_type_improved(test_msg, "|")
    print "Message type:", msg_type
    
    # Test with another message format
    test_msg2 = "8=FIX.4.4^9=65^35=8^49=SELLER^56=BUYER^52=20230315-12:45:30^150=0^39=0^"
    print "\nTesting with message:", test_msg2
    
    # Extract and check message type
    msg_type2 = check_msg_type_improved(test_msg2, "^")
    print "Message type:", msg_type2

    # TODO: Add ability to parse all fields in the message
    # TODO: Add checksum validation
    # TODO: Create class to represent a FIX message with getters/setters for fields
