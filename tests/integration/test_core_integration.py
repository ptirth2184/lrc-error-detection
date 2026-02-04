"""
Integration tests for core utilities validation.

These tests verify that DataConverter and LRCCalculator work together correctly
for the complete text-to-LRC workflow.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.data_converter import DataConverter
from modules.lrc_calculator import LRCCalculator


class TestCoreIntegration:
    """Integration tests for core utilities"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.converter = DataConverter()
        self.calculator = LRCCalculator()
    
    def test_text_to_lrc_workflow(self):
        """Test complete workflow from text input to LRC calculation"""
        # Input text
        text = "Hello"
        
        # Step 1: Convert text to binary
        binary_list = self.converter.text_to_binary(text)
        assert len(binary_list) == 5  # 5 characters
        assert all(len(binary) == 8 for binary in binary_list)  # 8 bits each
        
        # Step 2: Calculate LRC
        lrc_result, steps = self.calculator.calculate_lrc(binary_list)
        assert len(lrc_result) == 8  # LRC should be 8 bits
        assert len(steps) == 7  # INIT + 5 XOR + FINAL
        
        # Step 3: Verify LRC
        is_valid, calc_lrc, verify_steps = self.calculator.verify_lrc(binary_list, lrc_result)
        assert is_valid == True
        assert calc_lrc == lrc_result
        
        # Manual verification
        expected_lrc = "00000000"
        for binary in binary_list:
            expected_lrc = self.calculator.xor_operation(expected_lrc, binary)
        assert lrc_result == expected_lrc
    
    def test_binary_input_to_lrc_workflow(self):
        """Test workflow with direct binary input"""
        # Input binary string
        binary_string = "0100100001100101011011000110110001101111"  # "Hello" in binary
        
        # Step 1: Convert to blocks
        blocks = self.converter.binary_to_blocks(binary_string, 8)
        assert len(blocks) == 5  # 5 blocks of 8 bits each
        
        # Step 2: Calculate LRC
        lrc_result, steps = self.calculator.calculate_lrc(blocks)
        assert len(lrc_result) == 8
        
        # Step 3: Verify the result matches text conversion
        text_binary = self.converter.text_to_binary("Hello")
        text_lrc, _ = self.calculator.calculate_lrc(text_binary)
        assert lrc_result == text_lrc
    
    def test_error_detection_workflow(self):
        """Test error detection with corrupted data"""
        # Original data
        original_text = "Test"
        original_binary = self.converter.text_to_binary(original_text)
        original_lrc, _ = self.calculator.calculate_lrc(original_binary)
        
        # Corrupt one bit in the first block (flip the last bit)
        corrupted_binary = original_binary.copy()
        first_block = original_binary[0]
        # Flip the last bit: if it's '0' make it '1', if it's '1' make it '0'
        last_bit = '0' if first_block[-1] == '1' else '1'
        corrupted_binary[0] = first_block[:-1] + last_bit
        
        # Verify error detection
        is_valid, calc_lrc, steps = self.calculator.verify_lrc(corrupted_binary, original_lrc)
        assert is_valid == False  # Should detect error
        assert calc_lrc != original_lrc  # LRCs should differ
    
    def test_conversion_info_integration(self):
        """Test conversion info with LRC calculation"""
        text = "Hi"
        
        # Get conversion info
        info = self.converter.get_conversion_info(text)
        assert info['character_count'] == 2
        assert info['total_bits'] == 16
        assert len(info['conversion_table']) == 2
        
        # Use binary representation for LRC
        binary_blocks = info['binary_representation']
        lrc_result, steps = self.calculator.calculate_lrc(binary_blocks)
        
        # Verify consistency
        assert len(binary_blocks) == info['character_count']
        assert all(len(block) == 8 for block in binary_blocks)
    
    def test_format_display_integration(self):
        """Test formatted display with calculation steps"""
        text = "AB"
        binary_list = self.converter.text_to_binary(text)
        
        # Format binary display
        formatted_binary = self.converter.format_binary_display(binary_list)
        assert " " in formatted_binary  # Should have space separator
        
        # Calculate LRC and format steps
        lrc_result, steps = self.calculator.calculate_lrc(binary_list)
        formatted_steps = self.calculator.format_calculation_steps(steps)
        
        # Verify formatting
        assert "LRC Calculation Steps:" in formatted_steps
        assert "Step 0:" in formatted_steps  # INIT step
        assert "Step 1:" in formatted_steps  # First XOR step
        assert lrc_result in formatted_steps  # Final result should be present