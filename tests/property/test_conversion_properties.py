"""
Property-based tests for data conversion functionality.

These tests verify universal properties that should hold for all valid inputs
to the DataConverter class, ensuring correctness across a wide range of scenarios.
"""

import pytest
from hypothesis import given, strategies as st, assume
import string
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.data_converter import DataConverter


class TestDataConverterProperties:
    """Property-based tests for DataConverter class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.converter = DataConverter()
    
    # Feature: lrc-error-detection, Property 1: Text to Binary Conversion Correctness
    @given(st.text(alphabet=string.printable, min_size=1, max_size=100))
    def test_text_to_binary_conversion_property(self, text):
        """
        **Property 1: Text to Binary Conversion Correctness**
        For any valid ASCII text string, converting it to binary should produce 
        exactly 8 bits per character, where each 8-bit sequence represents the 
        correct ASCII value of the corresponding character.
        **Validates: Requirements 1.1**
        """
        # Filter to ASCII printable characters only
        ascii_text = ''.join(char for char in text if ord(char) < 128)
        assume(len(ascii_text) > 0)  # Skip empty strings after filtering
        
        binary_result = self.converter.text_to_binary(ascii_text)
        
        # Property: Should produce exactly one 8-bit string per character
        assert len(binary_result) == len(ascii_text)
        
        # Property: Each binary string should be exactly 8 bits
        for binary_str in binary_result:
            assert len(binary_str) == 8
            assert all(bit in '01' for bit in binary_str)
        
        # Property: Each binary string should represent correct ASCII value
        for i, char in enumerate(ascii_text):
            expected_ascii = ord(char)
            actual_ascii = int(binary_result[i], 2)
            assert actual_ascii == expected_ascii
    
    # Feature: lrc-error-detection, Property 2: Binary Input Validation
    @given(st.text(min_size=1, max_size=100))
    def test_binary_validation_property(self, input_string):
        """
        **Property 2: Binary Input Validation**
        For any input string, the validation function should accept it if and 
        only if it contains only '0' and '1' characters.
        **Validates: Requirements 1.2, 1.3**
        """
        result = self.converter.validate_binary(input_string)
        
        # Property: Should return True if and only if string contains only 0s and 1s
        contains_only_binary = all(char in '01' for char in input_string)
        assert result == contains_only_binary
    
    # Feature: lrc-error-detection, Property 3: Block Division Consistency
    @given(
        st.text(alphabet='01', min_size=1, max_size=200),
        st.integers(min_value=1, max_value=32)
    )
    def test_block_division_property(self, binary_string, block_size):
        """
        **Property 3: Block Division Consistency**
        For any binary string and block size, dividing the string into blocks 
        should preserve all original bits, with proper padding applied to the 
        last block if necessary.
        **Validates: Requirements 2.1**
        """
        blocks = self.converter.binary_to_blocks(binary_string, block_size)
        
        # Property: All blocks except possibly the last should be exactly block_size
        for i, block in enumerate(blocks[:-1]):  # All but last block
            assert len(block) == block_size
            assert all(bit in '01' for bit in block)
        
        # Property: Last block should be exactly block_size (padded if necessary)
        if blocks:
            assert len(blocks[-1]) == block_size
            assert all(bit in '01' for bit in blocks[-1])
        
        # Property: Concatenating blocks (removing padding) should preserve original data
        concatenated = ''.join(blocks)
        # Remove trailing zeros that were added as padding
        original_length = len(binary_string)
        reconstructed = concatenated[:original_length]
        assert reconstructed == binary_string
        
        # Property: Number of blocks should be correct
        expected_blocks = (len(binary_string) + block_size - 1) // block_size
        assert len(blocks) == expected_blocks
    
    @given(st.text(alphabet='01', min_size=0, max_size=50))
    def test_format_binary_display_property(self, binary_data):
        """
        Property test for binary display formatting.
        The formatted output should preserve all binary data with space separation.
        """
        # Convert string to list of 8-bit blocks for testing
        if binary_data:
            blocks = self.converter.binary_to_blocks(binary_data, 8)
            formatted = self.converter.format_binary_display(blocks)
            
            # Property: Formatted string should contain all original data
            formatted_no_spaces = formatted.replace(' ', '')
            reconstructed = ''.join(blocks)
            assert formatted_no_spaces == reconstructed
            
            # Property: Should have correct number of spaces (one less than number of blocks)
            if len(blocks) > 1:
                space_count = formatted.count(' ')
                assert space_count == len(blocks) - 1
        else:
            # Empty input should produce empty output
            formatted = self.converter.format_binary_display([])
            assert formatted == ""
    
    @given(st.integers(min_value=-10, max_value=0))
    def test_invalid_block_size_property(self, invalid_block_size):
        """
        Property test for invalid block sizes.
        Block sizes <= 0 should raise ValueError.
        """
        with pytest.raises(ValueError, match="Block size must be positive"):
            self.converter.binary_to_blocks("01010101", invalid_block_size)
    
    @given(st.text(min_size=1, max_size=50).filter(lambda x: not all(c in '01' for c in x)))
    def test_invalid_binary_data_property(self, invalid_binary):
        """
        Property test for invalid binary data.
        Non-binary strings should raise ValueError when used in binary_to_blocks.
        """
        with pytest.raises(ValueError, match="Invalid binary data"):
            self.converter.binary_to_blocks(invalid_binary, 8)