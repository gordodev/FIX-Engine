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
        
    Example:
        >>> msg = "8=FIX.4.2|9=123|35=D|"
        >>> convert_fix_delimiter(msg)
        '8=FIX.4.2\x019=123\x0135=D\x01'
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
