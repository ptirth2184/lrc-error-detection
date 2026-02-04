"""
Data Converter Module for LRC Error Detection System

This module handles conversion between text and binary formats with validation.
It provides utilities for converting ASCII text to binary representation,
validating binary strings, and formatting data for display and processing.

Educational Purpose:
- Demonstrates ASCII to binary conversion
- Shows how data is represented in binary form
- Provides validation for user input
"""

from typing import List, Tuple
import re


class DataConverter:
    """
    Handles conversion between text and binary formats with validation.
    
    This class provides methods to convert ASCII text to 8-bit binary representation,
    validate binary strings, format binary data for display, and divide binary data
    into fixed-size blocks for LRC processing.
    """
    
    def __init__(self):
        """Initialize the DataConverter"""
        pass
    
    def text_to_binary(self, text: str) -> List[str]:
        """
        Convert ASCII text to 8-bit binary representation.
        
        Each character is converted to its ASCII value, then to an 8-bit binary string.
        This demonstrates how text data is represented in binary form for transmission.
        
        Args:
            text (str): Input text string to convert
            
        Returns:
            List[str]: List of 8-bit binary strings, one per character
            
        Example:
            >>> converter = DataConverter()
            >>> converter.text_to_binary("Hi")
            ['01001000', '01101001']
        """
        if not text:
            return []
        
        binary_list = []
        for char in text:
            # Get ASCII value and convert to 8-bit binary
            ascii_val = ord(char)
            binary_str = format(ascii_val, '08b')  # 8-bit binary with leading zeros
            binary_list.append(binary_str)
        
        return binary_list
    
    def validate_binary(self, binary_str: str) -> bool:
        """
        Validate that a string contains only binary digits (0 and 1).
        
        This method checks if the input string is a valid binary representation
        by ensuring it contains only '0' and '1' characters.
        
        Args:
            binary_str (str): String to validate
            
        Returns:
            bool: True if string contains only 0s and 1s, False otherwise
            
        Example:
            >>> converter = DataConverter()
            >>> converter.validate_binary("01001000")
            True
            >>> converter.validate_binary("01002000")
            False
        """
        if not binary_str:
            return False
        
        # Use regex to check if string contains only 0s and 1s
        return bool(re.match(r'^[01]+$', binary_str))
    
    def format_binary_display(self, binary_data: List[str]) -> str:
        """
        Format binary data for UI-friendly display.
        
        Takes a list of binary strings and formats them for clear display
        in the user interface, with proper spacing and grouping.
        
        Args:
            binary_data (List[str]): List of binary strings
            
        Returns:
            str: Formatted string for display
            
        Example:
            >>> converter = DataConverter()
            >>> converter.format_binary_display(['01001000', '01101001'])
            '01001000 01101001'
        """
        if not binary_data:
            return ""
        
        return " ".join(binary_data)
    
    def binary_to_blocks(self, binary_data: str, block_size: int = 8) -> List[str]:
        """
        Divide binary data into fixed-size blocks with padding if necessary.
        
        This method takes a continuous binary string and divides it into blocks
        of the specified size. If the last block is incomplete, it's padded with
        zeros to reach the required size.
        
        Args:
            binary_data (str): Continuous binary string
            block_size (int): Size of each block in bits (default: 8)
            
        Returns:
            List[str]: List of binary blocks, each of size block_size
            
        Example:
            >>> converter = DataConverter()
            >>> converter.binary_to_blocks("010010000110100", 8)
            ['01001000', '01101000']
        """
        if not binary_data:
            return []
        
        if block_size <= 0:
            raise ValueError("Block size must be positive")
        
        # Remove any spaces or formatting from binary data
        clean_binary = binary_data.replace(" ", "").replace("\n", "")
        
        # Validate that it's binary data
        if not self.validate_binary(clean_binary):
            raise ValueError("Invalid binary data: contains non-binary characters")
        
        blocks = []
        
        # Divide into blocks of specified size
        for i in range(0, len(clean_binary), block_size):
            block = clean_binary[i:i + block_size]
            
            # Pad the last block with zeros if it's incomplete
            if len(block) < block_size:
                block = block.ljust(block_size, '0')
            
            blocks.append(block)
        
        return blocks
    
    def get_conversion_info(self, text: str) -> dict:
        """
        Get comprehensive conversion information for educational display.
        
        This method provides detailed information about the text-to-binary
        conversion process, including character-by-character breakdown.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Dictionary containing conversion details
        """
        if not text:
            return {
                'original_text': '',
                'character_count': 0,
                'binary_representation': [],
                'total_bits': 0,
                'conversion_table': []
            }
        
        binary_list = self.text_to_binary(text)
        conversion_table = []
        
        for i, char in enumerate(text):
            conversion_table.append({
                'character': char,
                'ascii_value': ord(char),
                'binary': binary_list[i],
                'position': i + 1
            })
        
        return {
            'original_text': text,
            'character_count': len(text),
            'binary_representation': binary_list,
            'total_bits': len(text) * 8,
            'conversion_table': conversion_table
        }