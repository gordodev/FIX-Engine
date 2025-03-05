#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FIX Protocol Message Validator

This module provides functionality to validate, parse and manipulate FIX Protocol messages.
It supports FIX 4.2, 4.4 and 5.0 message types with extensible validation rules.

Author: Your Name
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("FIXValidator")


class FIXValidator:
    """
    Class for validating and parsing Financial Information eXchange (FIX) protocol messages.
    
    This validator supports FIX versions 4.2, 4.4, and 5.0, providing functionality to:
    - Parse FIX messages into tag-value pairs
    - Validate message structure and content
    - Check required tags based on message type
    - Detect errors and provide detailed error messages
    """
    
    # FIX message delimiter
    SOH = '\u0001'  # Standard FIX delimiter (non-printable character)
    SOH_PRINTABLE = '|'  # Printable representation for display purposes
    
    # Common FIX tags
    TAG_BEGIN_STRING = 8
    TAG_BODY_LENGTH = 9
    TAG_MSG_TYPE = 35
    TAG_SENDER_COMP_ID = 49
    TAG_TARGET_COMP_ID = 56
    TAG_MSG_SEQ_NUM = 34
    TAG_SENDING_TIME = 52
    TAG_CHECKSUM = 10
    
    # FIX message types
    MSG_TYPES = {
        # Session level
        'A': 'Logon',
        '0': 'Heartbeat',
        '1': 'Test Request',
        '2': 'Resend Request',
        '3': 'Reject',
        '4': 'Sequence Reset',
        '5': 'Logout',
        
        # Application level - common types
        'D': 'New Order - Single',
        'G': 'Order Cancel/Replace Request',
        'F': 'Order Cancel Request',
        '8': 'Execution Report',
        '9': 'Order Cancel Reject',
        'AE': 'Trade Capture Report',
        'j': 'Business Message Reject'
    }
    
    # Minimum required tags for specific message types
    REQUIRED_TAGS = {
        'D': {TAG_MSG_TYPE, TAG_SENDER_COMP_ID, TAG_TARGET_COMP_ID, TAG_MSG_SEQ_NUM, 
              TAG_SENDING_TIME, 11, 21, 55, 54, 60, 40},  # New Order - Single
        '8': {TAG_MSG_TYPE, TAG_SENDER_COMP_ID, TAG_TARGET_COMP_ID, TAG_MSG_SEQ_NUM, 
              TAG_SENDING_TIME, 37, 17, 39, 150, 40},  # Execution Report
        'A': {TAG_MSG_TYPE, TAG_SENDER_COMP_ID, TAG_TARGET_COMP_ID, TAG_MSG_SEQ_NUM, 
              TAG_SENDING_TIME, 98, 108}  # Logon
    }
    
    # FIX versions and their begin strings
    FIX_VERSIONS = {
        'FIX.4.2': 'FIX.4.2',
        'FIX.4.4': 'FIX.4.4',
        'FIX.5.0': 'FIXT.1.1'
    }

    def __init__(self, default_version: str = 'FIX.4.4', use_printable_delimiter: bool = False):
        """
        Initialize the FIX validator with specified configuration.
        
        Args:
            default_version: Default FIX version to validate against ('FIX.4.2', 'FIX.4.4', 'FIX.5.0')
            use_printable_delimiter: If True, use pipe symbol (|) as delimiter for display/input
        """
        if default_version not in self.FIX_VERSIONS:
            raise ValueError(f"Unsupported FIX version: {default_version}. "
                            f"Supported versions: {', '.join(self.FIX_VERSIONS.keys())}")
        
        self.default_version = default_version
        self.delimiter = self.SOH_PRINTABLE if use_printable_delimiter else self.SOH
        self.last_error = None
        logger.info(f"FIXValidator initialized with {default_version}, "
                   f"{'printable' if use_printable_delimiter else 'standard'} delimiter")

    def parse_message(self, message: str) -> Dict[int, str]:
        """
        Parse a FIX message into a dictionary of tag-value pairs.
        
        Args:
            message: FIX message string
            
        Returns:
            Dictionary with integer tags as keys and string values
        """
        # Normalize the message delimiter
        if self.delimiter == self.SOH_PRINTABLE and self.SOH in message:
            message = message.replace(self.SOH, self.SOH_PRINTABLE)
        elif self.delimiter == self.SOH and self.SOH_PRINTABLE in message:
            message = message.replace(self.SOH_PRINTABLE, self.SOH)
        
        # Split message into tag=value pairs
        tag_value_pairs = message.split(self.delimiter)
        
        # Process each tag=value pair
        tag_value_dict = {}
        for pair in tag_value_pairs:
            if not pair.strip():
                continue
                
            parts = pair.split('=', 1)  # Split on first equals sign only
            if len(parts) != 2:
                logger.warning(f"Invalid tag-value pair: {pair}")
                continue
                
            try:
                tag = int(parts[0])
                value = parts[1]
                tag_value_dict[tag] = value
            except ValueError:
                logger.warning(f"Invalid tag (not an integer): {parts[0]}")
                
        return tag_value_dict

    def validate_message(self, message: str) -> Tuple[bool, Optional[str], Optional[Dict[int, str]]]:
        """
        Validate a FIX message for structure and content.
        
        Args:
            message: FIX message to validate
            
        Returns:
            Tuple of (is_valid, error_message, tag_value_dict)
        """
        try:
            # Parse the message
            tag_value_dict = self.parse_message(message)
            
            # Check for empty message
            if not tag_value_dict:
                return False, "Empty or invalid message format", None
            
            # Check for message type
            if self.TAG_MSG_TYPE not in tag_value_dict:
                return False, f"Missing required tag: {self.TAG_MSG_TYPE} (MsgType)", None
                
            msg_type = tag_value_dict[self.TAG_MSG_TYPE]
            
            # Check if message type is known
            if msg_type not in self.MSG_TYPES:
                return False, f"Unknown message type: {msg_type}", tag_value_dict
                
            # Check required fields for this message type
            if msg_type in self.REQUIRED_TAGS:
                missing_tags = self.REQUIRED_TAGS[msg_type] - set(tag_value_dict.keys())
                if missing_tags:
                    missing_tags_str = ', '.join(str(tag) for tag in missing_tags)
                    return False, f"Missing required tags for {self.MSG_TYPES[msg_type]}: {missing_tags_str}", tag_value_dict
            
            # Additional validation could be added here for specific message types
            
            return True, None, tag_value_dict
            
        except Exception as e:
            logger.error(f"Error validating message: {str(e)}")
            return False, f"Validation error: {str(e)}", None

    def create_message(self, msg_type: str, fields: Dict[int, str]) -> str:
        """
        Create a FIX message with proper structure and checksum.
        
        Args:
            msg_type: The message type (e.g., 'D' for New Order - Single)
            fields: Dictionary of tag-value pairs to include
            
        Returns:
            Complete FIX message string
        """
        # Ensure required fields are present
        combined_fields = fields.copy()
        
        # Add message type if not already present
        if self.TAG_MSG_TYPE not in combined_fields:
            combined_fields[self.TAG_MSG_TYPE] = msg_type
            
        # Add standard header fields if not present
        current_time = datetime.datetime.utcnow().strftime('%Y%m%d-%H:%M:%S.%f')[:-3]
        
        if self.TAG_BEGIN_STRING not in combined_fields:
            combined_fields[self.TAG_BEGIN_STRING] = self.FIX_VERSIONS[self.default_version]
            
        if self.TAG_SENDING_TIME not in combined_fields:
            combined_fields[self.TAG_SENDING_TIME] = current_time
            
        # Create message without body length and checksum
        msg_parts = []
        for tag, value in sorted(combined_fields.items()):
            # BeginString (8) should be first, then BodyLength (9), then MsgType (35)
            if tag != self.TAG_BODY_LENGTH and tag != self.TAG_CHECKSUM:
                msg_parts.append(f"{tag}={value}")
        
        # Join with delimiter
        msg_without_length = self.delimiter.join(msg_parts)
        
        # Calculate body length (will be inserted after BeginString)
        body_start_pos = msg_without_length.find(self.delimiter) + 1
        body_length = len(msg_without_length) - body_start_pos
        
        # Insert BodyLength after BeginString
        body_length_str = f"{self.TAG_BODY_LENGTH}={body_length}{self.delimiter}"
        msg_with_length = msg_without_length[:body_start_pos] + body_length_str + msg_without_length[body_start_pos:]
        
        # Calculate checksum (sum of ASCII values mod 256)
        if self.delimiter == self.SOH_PRINTABLE:
            # Convert to standard SOH for checksum calculation
            checksum_msg = msg_with_length.replace(self.SOH_PRINTABLE, self.SOH)
        else:
            checksum_msg = msg_with_length
            
        checksum = sum(ord(c) for c in checksum_msg) % 256
        checksum_str = f"{self.delimiter}{self.TAG_CHECKSUM}={checksum:03d}"
        
        return msg_with_length + checksum_str

    def get_message_type_name(self, msg_type: str) -> str:
        """
        Get the human-readable name for a FIX message type.
        
        Args:
            msg_type: The message type code (e.g., 'D', '8')
            
        Returns:
            Human-readable message type name or 'Unknown' if not found
        """
        return self.MSG_TYPES.get(msg_type, 'Unknown')
        
    def format_message_for_display(self, message: str) -> str:
        """
        Format a FIX message for human-readable display.
        
        Args:
            message: Raw FIX message
            
        Returns:
            Formatted message with tag descriptions
        """
        tag_value_dict = self.parse_message(message)
        
        # Common tag descriptions
        tag_descriptions = {
            self.TAG_BEGIN_STRING: "BeginString",
            self.TAG_BODY_LENGTH: "BodyLength",
            self.TAG_MSG_TYPE: "MsgType",
            self.TAG_SENDER_COMP_ID: "SenderCompID",
            self.TAG_TARGET_COMP_ID: "TargetCompID",
            self.TAG_MSG_SEQ_NUM: "MsgSeqNum",
            self.TAG_SENDING_TIME: "SendingTime",
            self.TAG_CHECKSUM: "CheckSum",
            11: "ClOrdID",
            21: "HandlInst",
            55: "Symbol",
            54: "Side",
            60: "TransactTime",
            40: "OrdType",
            38: "OrderQty",
            44: "Price",
            37: "OrderID",
            17: "ExecID",
            39: "OrdStatus",
            150: "ExecType",
            98: "EncryptMethod",
            108: "HeartBtInt"
        }
        
        # Build formatted output
        formatted_lines = []
        formatted_lines.append("FIX Message:")
        formatted_lines.append("-" * 80)
        
        # Get message type if available
        msg_type_name = ""
        if self.TAG_MSG_TYPE in tag_value_dict:
            msg_type = tag_value_dict[self.TAG_MSG_TYPE]
            msg_type_name = f" ({self.get_message_type_name(msg_type)})"
        
        formatted_lines.append(f"Message Type: {tag_value_dict.get(self.TAG_MSG_TYPE, 'Unknown')}{msg_type_name}")
        
        # Format each tag-value pair
        formatted_lines.append("-" * 80)
        formatted_lines.append("Tag\tName\t\tValue")
        formatted_lines.append("-" * 80)
        
        for tag, value in sorted(tag_value_dict.items()):
            tag_name = tag_descriptions.get(tag, "Unknown")
            formatted_lines.append(f"{tag}\t{tag_name}\t\t{value}")
            
        return "\n".join(formatted_lines)

    def extract_values(self, message: str, tags: List[int]) -> Dict[int, str]:
        """
        Extract specific tag values from a FIX message.
        
        Args:
            message: FIX message
            tags: List of tag IDs to extract
            
        Returns:
            Dictionary with extracted tag-value pairs
        """
        tag_value_dict = self.parse_message(message)
        return {tag: tag_value_dict.get(tag) for tag in tags if tag in tag_value_dict}


def main():
    """
    Command line interface for FIX message validation.
    """
    validator = FIXValidator(use_printable_delimiter=True)
    
    print("FIX Protocol Message Validator")
    print("=" * 50)
    print("Enter 'quit' or 'exit' to terminate")
    print("Enter a FIX message using | as the delimiter")
    print("Example: 8=FIX.4.4|35=D|49=SENDER|56=TARGET|34=1|52=20230315-12:30:45|11=ABC123|21=1|55=AAPL|54=1|60=20230315-12:30:45|40=2|")
    print("=" * 50)
    
    while True:
        try:
            message = input("\nEnter FIX message: ")
            if message.lower() in ('quit', 'exit'):
                break
                
            is_valid, error_msg, tag_value_dict = validator.validate_message(message)
            
            if is_valid:
                print("\nY Message is valid")
                if tag_value_dict and validator.TAG_MSG_TYPE in tag_value_dict:
                    msg_type = tag_value_dict[validator.TAG_MSG_TYPE]
                    print(f"Message Type: {msg_type} ({validator.get_message_type_name(msg_type)})")
                
                # Show formatted message
                print("\n" + validator.format_message_for_display(message))
            else:
                print(f"\nX Message is invalid: {error_msg}")
                
                if tag_value_dict:
                    print("\nPartial message content:")
                    for tag, value in sorted(tag_value_dict.items()):
                        print(f"Tag {tag}: {value}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
