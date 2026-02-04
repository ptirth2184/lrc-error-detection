"""
Property-based tests for LRC calculation functionality.

These tests verify universal properties that should hold for all valid inputs
to the LRCCalculator class, ensuring correctness of the core LRC algorithm.
"""

import pytest
from hypothesis import given, strategies as st, assume
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.lrc_calculator import LRCCalculator


class TestLRCCalculatorProperties:
    """Property-based tests for LRCCalculator class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.calculator = LRCCalculator()
    
    # Feature: lrc-error-detection, Property 4: LRC Calculation Correctness
    @given(st.lists(
        st.text(alphabet='01', min_size=8, max_size=8),
        min_size=1,
        max_size=20
    ))
    def test_lrc_calculation_correctness_property(self, data_blocks):
        """
        **Property 4: LRC Calculation Correctness**
        For any set of data blocks, the LRC calculation should produce a result 
        equivalent to performing sequential bitwise XOR operations across all blocks, 
        starting with an initial value of 00000000.
        **Validates: Requirements 2.2**
        """
        lrc_result, steps = self.calculator.calculate_lrc(data_blocks)
        
        # Property: LRC result should be 8 bits
        assert len(lrc_result) == 8
        assert all(bit in '01' for bit in lrc_result)
        
        # Property: Manual XOR calculation should match LRC result
        manual_lrc = "00000000"
        for block in data_blocks:
            manual_lrc = self.calculator.xor_operation(manual_lrc, block)
        
        assert lrc_result == manual_lrc
        
        # Property: Steps should be recorded correctly
        assert len(steps) == len(data_blocks) + 2  # INIT + XOR steps + FINAL
        
        # Property: First step should be initialization
        assert steps[0]['operation'] == 'INIT'
        assert steps[0]['result'] == '00000000'
        
        # Property: Last step should be final result
        assert steps[-1]['operation'] == 'FINAL'
        assert steps[-1]['result'] == lrc_result
        
        # Property: Each XOR step should be valid
        for i in range(1, len(data_blocks) + 1):
            step = steps[i]
            assert step['operation'] == 'XOR'
            assert step['step_number'] == i
            # Verify XOR operation is correct
            expected_result = self.calculator.xor_operation(step['operand1'], step['operand2'])
            assert step['result'] == expected_result
    
    # Feature: lrc-error-detection, Property 10: Calculation Step Tracking
    @given(st.lists(
        st.text(alphabet='01', min_size=8, max_size=8),
        min_size=1,
        max_size=10
    ))
    def test_calculation_step_tracking_property(self, data_blocks):
        """
        **Property 10: Calculation Step Tracking**
        For any LRC calculation, the system should record each XOR operation step 
        with operands and results, enabling complete reconstruction of the calculation process.
        **Validates: Requirements 2.3, 6.2**
        """
        lrc_result, steps = self.calculator.calculate_lrc(data_blocks)
        
        # Property: Steps should enable complete reconstruction
        reconstructed_lrc = "00000000"
        
        # Skip INIT step (index 0) and FINAL step (last index)
        for i in range(1, len(steps) - 1):
            step = steps[i]
            
            # Property: Each step should have all required fields
            required_fields = ['step_number', 'operation', 'operand1', 'operand2', 'result', 'description']
            for field in required_fields:
                assert field in step
            
            # Property: Step should be an XOR operation
            assert step['operation'] == 'XOR'
            
            # Property: Operands should be valid binary strings
            assert all(bit in '01' for bit in step['operand1'])
            assert all(bit in '01' for bit in step['operand2'])
            assert len(step['operand1']) == 8
            assert len(step['operand2']) == 8
            
            # Property: Result should match XOR of operands
            expected_result = self.calculator.xor_operation(step['operand1'], step['operand2'])
            assert step['result'] == expected_result
            
            # Property: First operand should be previous LRC state
            assert step['operand1'] == reconstructed_lrc
            
            # Property: Second operand should be current data block
            block_index = step['step_number'] - 1
            assert step['operand2'] == data_blocks[block_index]
            
            # Update reconstructed LRC for next iteration
            reconstructed_lrc = step['result']
        
        # Property: Final reconstructed LRC should match calculated LRC
        assert reconstructed_lrc == lrc_result
    
    @given(
        st.lists(st.text(alphabet='01', min_size=8, max_size=8), min_size=1, max_size=10),
        st.text(alphabet='01', min_size=8, max_size=8)
    )
    def test_lrc_verification_property(self, data_blocks, received_lrc):
        """
        Property test for LRC verification accuracy.
        Verification should correctly identify matches and mismatches.
        """
        # Calculate the correct LRC for the data blocks
        correct_lrc, _ = self.calculator.calculate_lrc(data_blocks)
        
        # Test verification with correct LRC
        is_valid_correct, calc_lrc_correct, steps_correct = self.calculator.verify_lrc(data_blocks, correct_lrc)
        
        # Property: Verification with correct LRC should always pass
        assert is_valid_correct == True
        assert calc_lrc_correct == correct_lrc
        
        # Test verification with received LRC
        is_valid_received, calc_lrc_received, steps_received = self.calculator.verify_lrc(data_blocks, received_lrc)
        
        # Property: Verification result should match LRC comparison
        expected_valid = (correct_lrc == received_lrc)
        assert is_valid_received == expected_valid
        assert calc_lrc_received == correct_lrc
        
        # Property: Verification steps should include comparison step
        comparison_step = steps_received[-1]
        assert comparison_step['operation'] == 'COMPARE'
        assert comparison_step['operand1'] == correct_lrc
        assert comparison_step['operand2'] == received_lrc
        
        if expected_valid:
            assert comparison_step['result'] == 'MATCH'
            assert 'No Error' in comparison_step['description']
        else:
            assert comparison_step['result'] == 'MISMATCH'
            assert 'Error Detected' in comparison_step['description']
    
    @given(
        st.text(alphabet='01', min_size=8, max_size=8),
        st.text(alphabet='01', min_size=8, max_size=8)
    )
    def test_xor_operation_property(self, bit_string1, bit_string2):
        """
        Property test for XOR operation correctness.
        XOR should follow the mathematical definition of exclusive OR.
        """
        result = self.calculator.xor_operation(bit_string1, bit_string2)
        
        # Property: Result should be same length as inputs
        assert len(result) == len(bit_string1) == len(bit_string2)
        
        # Property: Result should contain only binary digits
        assert all(bit in '01' for bit in result)
        
        # Property: Each bit should follow XOR truth table
        for i in range(len(bit_string1)):
            bit1 = int(bit_string1[i])
            bit2 = int(bit_string2[i])
            expected_bit = str(bit1 ^ bit2)
            assert result[i] == expected_bit
        
        # Property: XOR is commutative (a ⊕ b = b ⊕ a)
        reverse_result = self.calculator.xor_operation(bit_string2, bit_string1)
        assert result == reverse_result
        
        # Property: XOR with self should yield all zeros
        self_xor = self.calculator.xor_operation(bit_string1, bit_string1)
        assert self_xor == '00000000'
    
    def test_empty_data_blocks_property(self):
        """
        Property test for empty data blocks.
        Empty input should return initial LRC value.
        """
        lrc_result, steps = self.calculator.calculate_lrc([])
        
        # Property: Empty blocks should return all zeros
        assert lrc_result == "00000000"
        assert len(steps) == 0
    
    def test_invalid_block_length_property(self):
        """
        Property test for invalid block lengths.
        Blocks of different lengths should raise ValueError.
        """
        # Create blocks with different lengths
        invalid_blocks = ['01010101', '101', '11110000']  # 8, 3, 8 bits
        
        with pytest.raises(ValueError, match="All data blocks must have the same length"):
            self.calculator.calculate_lrc(invalid_blocks)
    
    @given(st.lists(
        st.text(min_size=8, max_size=8).filter(lambda x: not all(c in '01' for c in x)),
        min_size=1,
        max_size=5
    ))
    def test_invalid_binary_blocks_property(self, invalid_blocks):
        """
        Property test for invalid binary blocks.
        Non-binary blocks should raise ValueError.
        """
        with pytest.raises(ValueError, match="Data blocks must contain only binary digits"):
            self.calculator.calculate_lrc(invalid_blocks)
    
    @given(
        st.text(alphabet='01', min_size=7, max_size=7),
        st.text(alphabet='01', min_size=8, max_size=8)
    )
    def test_xor_different_lengths_property(self, short_string, long_string):
        """
        Property test for XOR with different length strings.
        Should raise ValueError for mismatched lengths.
        """
        with pytest.raises(ValueError, match="Both bit strings must have the same length"):
            self.calculator.xor_operation(short_string, long_string)