"""
LRC Calculator Module for LRC Error Detection System

This module implements the core Longitudinal Redundancy Check (LRC) algorithm
with educational step-by-step visualization. It provides methods for calculating
LRC parity bytes using bitwise XOR operations and verifying data integrity.

Educational Purpose:
- Demonstrates bitwise XOR operations step-by-step
- Shows how parity bytes are calculated for error detection
- Provides detailed calculation tracking for learning
"""

from typing import List, Dict, Tuple


class LRCCalculator:
    """
    Implements the core LRC algorithm with educational step-by-step visualization.
    
    This class provides methods to calculate LRC parity bytes using bitwise XOR
    operations, verify received data integrity, and track each calculation step
    for educational purposes.
    """
    
    def __init__(self):
        """Initialize the LRC Calculator"""
        pass
    
    def calculate_lrc(self, data_blocks: List[str]) -> Tuple[str, List[Dict]]:
        """
        Calculate LRC parity byte using bitwise XOR operations with step tracking.
        
        The LRC is calculated by performing sequential XOR operations across all
        data blocks, starting with an initial value of 00000000. Each step is
        tracked for educational visualization.
        
        Args:
            data_blocks (List[str]): List of binary strings (data blocks)
            
        Returns:
            Tuple[str, List[Dict]]: (LRC byte, calculation steps)
            
        Example:
            >>> calculator = LRCCalculator()
            >>> blocks = ['01001000', '01100101']
            >>> lrc, steps = calculator.calculate_lrc(blocks)
            >>> print(lrc)
            '00101101'
        """
        if not data_blocks:
            return "00000000", []
        
        # Validate all blocks have the same length
        block_length = len(data_blocks[0])
        for block in data_blocks:
            if len(block) != block_length:
                raise ValueError("All data blocks must have the same length")
            if not all(bit in '01' for bit in block):
                raise ValueError("Data blocks must contain only binary digits")
        
        # Initialize LRC to all zeros
        lrc_byte = "0" * block_length
        calculation_steps = []
        
        # Add initialization step
        calculation_steps.append({
            'step_number': 0,
            'operation': 'INIT',
            'operand1': '',
            'operand2': '',
            'result': lrc_byte,
            'description': f'Initialize LRC to {lrc_byte}'
        })
        
        # Perform XOR operation for each data block
        for i, block in enumerate(data_blocks):
            previous_lrc = lrc_byte
            lrc_byte = self.xor_operation(lrc_byte, block)
            
            # Record this step
            calculation_steps.append({
                'step_number': i + 1,
                'operation': 'XOR',
                'operand1': previous_lrc,
                'operand2': block,
                'result': lrc_byte,
                'description': f'XOR LRC with Block {i + 1}: {previous_lrc} ⊕ {block} = {lrc_byte}'
            })
        
        # Add final step
        calculation_steps.append({
            'step_number': len(data_blocks) + 1,
            'operation': 'FINAL',
            'operand1': '',
            'operand2': '',
            'result': lrc_byte,
            'description': f'Final LRC byte: {lrc_byte}'
        })
        
        return lrc_byte, calculation_steps
    
    def verify_lrc(self, data_blocks: List[str], received_lrc: str) -> Tuple[bool, str, List[Dict]]:
        """
        Verify data integrity by recalculating LRC and comparing with received LRC.
        
        This method recalculates the LRC from the received data blocks and compares
        it with the received LRC byte to detect transmission errors.
        
        Args:
            data_blocks (List[str]): List of received data blocks
            received_lrc (str): Received LRC byte
            
        Returns:
            Tuple[bool, str, List[Dict]]: (is_valid, calculated_lrc, verification_steps)
            
        Example:
            >>> calculator = LRCCalculator()
            >>> blocks = ['01001000', '01100101']
            >>> is_valid, calc_lrc, steps = calculator.verify_lrc(blocks, '00101101')
            >>> print(is_valid)
            True
        """
        if not received_lrc or not all(bit in '01' for bit in received_lrc):
            raise ValueError("Received LRC must be a valid binary string")
        
        # Recalculate LRC from received data blocks
        calculated_lrc, calculation_steps = self.calculate_lrc(data_blocks)
        
        # Compare calculated vs received LRC
        is_valid = calculated_lrc == received_lrc
        
        # Create verification steps
        verification_steps = calculation_steps.copy()
        
        # Add comparison step
        verification_steps.append({
            'step_number': len(calculation_steps),
            'operation': 'COMPARE',
            'operand1': calculated_lrc,
            'operand2': received_lrc,
            'result': 'MATCH' if is_valid else 'MISMATCH',
            'description': f'Compare calculated LRC ({calculated_lrc}) with received LRC ({received_lrc}): {"MATCH - No Error" if is_valid else "MISMATCH - Error Detected"}'
        })
        
        return is_valid, calculated_lrc, verification_steps
    
    def xor_operation(self, bit_string1: str, bit_string2: str) -> str:
        """
        Perform bitwise XOR operation on two binary strings.
        
        This method performs XOR operation bit by bit on two binary strings
        of equal length, returning the result as a binary string.
        
        Args:
            bit_string1 (str): First binary string
            bit_string2 (str): Second binary string
            
        Returns:
            str: Result of XOR operation
            
        Example:
            >>> calculator = LRCCalculator()
            >>> result = calculator.xor_operation('01001000', '01100101')
            >>> print(result)
            '00101101'
        """
        if len(bit_string1) != len(bit_string2):
            raise ValueError("Both bit strings must have the same length")
        
        if not all(bit in '01' for bit in bit_string1 + bit_string2):
            raise ValueError("Bit strings must contain only binary digits")
        
        result = ""
        for i in range(len(bit_string1)):
            bit1 = int(bit_string1[i])
            bit2 = int(bit_string2[i])
            xor_result = bit1 ^ bit2
            result += str(xor_result)
        
        return result
    
    def format_calculation_steps(self, steps: List[Dict]) -> str:
        """
        Format calculation steps for educational display.
        
        This method takes the calculation steps and formats them into a
        human-readable string for display in the user interface.
        
        Args:
            steps (List[Dict]): List of calculation step dictionaries
            
        Returns:
            str: Formatted string representation of calculation steps
        """
        if not steps:
            return "No calculation steps available."
        
        formatted_output = "LRC Calculation Steps:\n"
        formatted_output += "=" * 50 + "\n"
        
        for step in steps:
            step_num = step.get('step_number', 0)
            operation = step.get('operation', '')
            description = step.get('description', '')
            
            if operation == 'INIT':
                formatted_output += f"Step {step_num}: {description}\n"
            elif operation == 'XOR':
                formatted_output += f"Step {step_num}: {description}\n"
            elif operation == 'FINAL':
                formatted_output += f"Step {step_num}: {description}\n"
            elif operation == 'COMPARE':
                formatted_output += f"Step {step_num}: {description}\n"
            
            formatted_output += "-" * 30 + "\n"
        
        return formatted_output
    
    def get_xor_truth_table(self) -> Dict[str, str]:
        """
        Get XOR truth table for educational purposes.
        
        Returns:
            Dict[str, str]: XOR truth table mapping
        """
        return {
            "0 ⊕ 0": "0",
            "0 ⊕ 1": "1", 
            "1 ⊕ 0": "1",
            "1 ⊕ 1": "0"
        }
    
    def analyze_error_detection_capability(self, original_blocks: List[str], 
                                         corrupted_blocks: List[str]) -> Dict:
        """
        Analyze the error detection capability by comparing original and corrupted data.
        
        This method calculates LRC for both original and corrupted data to demonstrate
        how LRC detects (or fails to detect) different types of errors.
        
        Args:
            original_blocks (List[str]): Original data blocks
            corrupted_blocks (List[str]): Corrupted data blocks
            
        Returns:
            Dict: Analysis results including error detection status
        """
        if len(original_blocks) != len(corrupted_blocks):
            raise ValueError("Original and corrupted block lists must have same length")
        
        # Calculate LRC for original data
        original_lrc, original_steps = self.calculate_lrc(original_blocks)
        
        # Calculate LRC for corrupted data  
        corrupted_lrc, corrupted_steps = self.calculate_lrc(corrupted_blocks)
        
        # Identify error positions
        error_positions = []
        for i, (orig, corr) in enumerate(zip(original_blocks, corrupted_blocks)):
            if orig != corr:
                for j, (orig_bit, corr_bit) in enumerate(zip(orig, corr)):
                    if orig_bit != corr_bit:
                        error_positions.append((i, j))
        
        # Determine if error is detected
        error_detected = original_lrc != corrupted_lrc
        
        return {
            'original_lrc': original_lrc,
            'corrupted_lrc': corrupted_lrc,
            'error_detected': error_detected,
            'error_positions': error_positions,
            'error_count': len(error_positions),
            'detection_result': 'Error Detected' if error_detected else 'Error Not Detected',
            'original_steps': original_steps,
            'corrupted_steps': corrupted_steps
        }