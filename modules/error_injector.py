"""
Error Injector Module for LRC Error Detection System

This module provides controlled error introduction with visualization
for educational demonstration of error detection capabilities.

Educational Purpose:
- Demonstrates different types of transmission errors
- Shows how bit-level errors affect data integrity
- Provides controlled error injection for testing LRC detection
"""

from typing import List, Tuple, Dict
import random
import copy


class ErrorInjector:
    """
    Provides controlled error introduction with visualization.
    
    This class offers methods to inject various types of errors into
    transmitted data, including single bit flips, multiple random errors,
    and targeted errors in specific locations.
    """
    
    def __init__(self):
        """Initialize the Error Injector"""
        self.error_history = []
        self.error_count = 0
    
    def flip_bit(self, binary_str: str, position: int) -> str:
        """
        Flip a single bit at the specified position.
        
        This method flips a bit from 0 to 1 or from 1 to 0 at the given
        position in a binary string.
        
        Args:
            binary_str (str): Binary string to modify
            position (int): Position of bit to flip (0-based)
            
        Returns:
            str: Binary string with flipped bit
            
        Example:
            >>> injector = ErrorInjector()
            >>> injector.flip_bit('01001000', 0)
            '11001000'
        """
        if not binary_str:
            raise ValueError("Binary string cannot be empty")
        
        if not all(bit in '01' for bit in binary_str):
            raise ValueError("String must contain only binary digits")
        
        if position < 0 or position >= len(binary_str):
            raise ValueError(f"Position {position} is out of range for string of length {len(binary_str)}")
        
        # Convert to list for easy modification
        bits = list(binary_str)
        
        # Flip the bit
        bits[position] = '0' if bits[position] == '1' else '1'
        
        return ''.join(bits)
    
    def generate_random_errors(self, data_length: int, error_count: int) -> List[int]:
        """
        Generate random error positions for error injection.
        
        This method generates a list of random positions where errors
        should be injected, ensuring no duplicate positions.
        
        Args:
            data_length (int): Total length of data in bits
            error_count (int): Number of errors to generate
            
        Returns:
            List[int]: List of positions where errors should be injected
            
        Example:
            >>> injector = ErrorInjector()
            >>> positions = injector.generate_random_errors(64, 3)
            >>> len(positions)
            3
        """
        if data_length <= 0:
            raise ValueError("Data length must be positive")
        
        if error_count < 0:
            raise ValueError("Error count cannot be negative")
        
        if error_count > data_length:
            raise ValueError("Error count cannot exceed data length")
        
        # Generate unique random positions
        positions = random.sample(range(data_length), error_count)
        return sorted(positions)
    
    def inject_manual_error(self, data: Dict, error_positions: List[Tuple[int, int]]) -> Dict:
        """
        Inject errors at manually specified positions.
        
        This method allows precise control over error injection by specifying
        exact block and bit positions where errors should occur.
        
        Args:
            data (Dict): Transmission package containing data blocks
            error_positions (List[Tuple[int, int]]): List of (block_index, bit_position) tuples
            
        Returns:
            Dict: Modified data package with errors injected
            
        Example:
            >>> injector = ErrorInjector()
            >>> data = {'data_blocks': ['01001000', '01100101'], 'lrc_byte': '00101101'}
            >>> errors = [(0, 0), (1, 7)]  # First bit of first block, last bit of second block
            >>> corrupted = injector.inject_manual_error(data, errors)
        """
        if not isinstance(data, dict) or 'data_blocks' not in data:
            raise ValueError("Data must be a dictionary with 'data_blocks' key")
        
        if not error_positions:
            return copy.deepcopy(data)
        
        # Create deep copy to avoid modifying original
        corrupted_data = copy.deepcopy(data)
        error_summary = []
        
        for block_index, bit_position in error_positions:
            # Validate block index
            if block_index < 0 or block_index >= len(corrupted_data['data_blocks']):
                raise ValueError(f"Block index {block_index} is out of range")
            
            # Get the block to modify
            original_block = corrupted_data['data_blocks'][block_index]
            
            # Validate bit position
            if bit_position < 0 or bit_position >= len(original_block):
                raise ValueError(f"Bit position {bit_position} is out of range for block {block_index}")
            
            # Flip the bit
            corrupted_block = self.flip_bit(original_block, bit_position)
            corrupted_data['data_blocks'][block_index] = corrupted_block
            
            # Record the error
            error_info = {
                'block_index': block_index,
                'bit_position': bit_position,
                'original_bit': original_block[bit_position],
                'corrupted_bit': corrupted_block[bit_position],
                'original_block': original_block,
                'corrupted_block': corrupted_block
            }
            error_summary.append(error_info)
            self.error_count += 1
        
        # Add error metadata
        corrupted_data.update({
            'errors_injected': True,
            'error_type': 'manual',
            'error_count': len(error_positions),
            'error_positions': error_positions,
            'error_summary': error_summary,
            'injection_id': len(self.error_history)
        })
        
        # Store in history
        self.error_history.append({
            'type': 'manual',
            'positions': error_positions,
            'summary': error_summary,
            'timestamp': self._get_timestamp()
        })
        
        return corrupted_data
    
    def inject_random_error(self, data: Dict, error_rate: float) -> Dict:
        """
        Inject random errors into the data based on error rate.
        
        This method randomly selects positions in the data blocks and
        injects errors based on the specified error rate.
        
        Args:
            data (Dict): Transmission package containing data blocks
            error_rate (float): Probability of error per bit (0.0 to 1.0)
            
        Returns:
            Dict: Modified data package with random errors injected
            
        Example:
            >>> injector = ErrorInjector()
            >>> data = {'data_blocks': ['01001000', '01100101'], 'lrc_byte': '00101101'}
            >>> corrupted = injector.inject_random_error(data, 0.1)  # 10% error rate
        """
        if not isinstance(data, dict) or 'data_blocks' not in data:
            raise ValueError("Data must be a dictionary with 'data_blocks' key")
        
        if not (0.0 <= error_rate <= 1.0):
            raise ValueError("Error rate must be between 0.0 and 1.0")
        
        if error_rate == 0.0:
            return copy.deepcopy(data)
        
        # Calculate total data length
        total_bits = sum(len(block) for block in data['data_blocks'])
        
        # Determine number of errors based on error rate
        expected_errors = int(total_bits * error_rate)
        if expected_errors == 0 and error_rate > 0:
            expected_errors = 1  # Ensure at least one error if rate > 0
        
        # Generate random error positions
        error_positions = []
        bit_index = 0
        
        for block_idx, block in enumerate(data['data_blocks']):
            for bit_idx in range(len(block)):
                if random.random() < error_rate:
                    error_positions.append((block_idx, bit_idx))
                bit_index += 1
        
        # If no errors were generated but rate > 0, force at least one
        if not error_positions and error_rate > 0:
            random_block = random.randint(0, len(data['data_blocks']) - 1)
            random_bit = random.randint(0, len(data['data_blocks'][random_block]) - 1)
            error_positions.append((random_block, random_bit))
        
        # Use manual injection to apply the random errors
        corrupted_data = self.inject_manual_error(data, error_positions)
        
        # Update metadata to reflect random injection
        corrupted_data.update({
            'error_type': 'random',
            'error_rate': error_rate,
            'expected_errors': expected_errors,
            'actual_errors': len(error_positions)
        })
        
        return corrupted_data
    
    def highlight_errors(self, original: str, corrupted: str) -> List[Tuple[int, str, str]]:
        """
        Identify and highlight differences between original and corrupted data.
        
        This method compares original and corrupted binary strings to identify
        the positions where errors occurred.
        
        Args:
            original (str): Original binary string
            corrupted (str): Corrupted binary string
            
        Returns:
            List[Tuple[int, str, str]]: List of (position, original_bit, corrupted_bit)
            
        Example:
            >>> injector = ErrorInjector()
            >>> errors = injector.highlight_errors('01001000', '11001000')
            >>> errors
            [(0, '0', '1')]
        """
        if len(original) != len(corrupted):
            raise ValueError("Original and corrupted strings must have the same length")
        
        differences = []
        for i, (orig_bit, corr_bit) in enumerate(zip(original, corrupted)):
            if orig_bit != corr_bit:
                differences.append((i, orig_bit, corr_bit))
        
        return differences
    
    def get_error_summary(self) -> Dict:
        """
        Get comprehensive error injection summary.
        
        Returns:
            Dict: Summary of all error injection activities
        """
        return {
            'total_errors_injected': self.error_count,
            'injection_sessions': len(self.error_history),
            'error_history': self.error_history.copy(),
            'last_injection': self.error_history[-1] if self.error_history else None
        }
    
    def clear_error_history(self):
        """Clear error injection history"""
        self.error_history.clear()
        self.error_count = 0
    
    def inject_burst_error(self, data: Dict, block_index: int, start_position: int, burst_length: int) -> Dict:
        """
        Inject a burst error (consecutive bit errors) in a specific block.
        
        This method simulates burst errors that can occur in real network
        transmissions due to interference or signal degradation.
        
        Args:
            data (Dict): Transmission package
            block_index (int): Index of block to corrupt
            start_position (int): Starting position of burst
            burst_length (int): Number of consecutive bits to corrupt
            
        Returns:
            Dict: Data with burst error injected
        """
        if not isinstance(data, dict) or 'data_blocks' not in data:
            raise ValueError("Data must be a dictionary with 'data_blocks' key")
        
        if block_index < 0 or block_index >= len(data['data_blocks']):
            raise ValueError(f"Block index {block_index} is out of range")
        
        block = data['data_blocks'][block_index]
        
        if start_position < 0 or start_position >= len(block):
            raise ValueError(f"Start position {start_position} is out of range")
        
        if burst_length <= 0:
            raise ValueError("Burst length must be positive")
        
        if start_position + burst_length > len(block):
            raise ValueError("Burst extends beyond block boundary")
        
        # Generate error positions for the burst
        error_positions = [(block_index, start_position + i) for i in range(burst_length)]
        
        # Use manual injection for the burst
        corrupted_data = self.inject_manual_error(data, error_positions)
        
        # Update metadata
        corrupted_data.update({
            'error_type': 'burst',
            'burst_block': block_index,
            'burst_start': start_position,
            'burst_length': burst_length
        })
        
        return corrupted_data
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for error history"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_visualization_data(self, original_data: Dict, corrupted_data: Dict) -> Dict:
        """
        Get data formatted for error visualization in the UI.
        
        Args:
            original_data (Dict): Original transmission package
            corrupted_data (Dict): Corrupted transmission package
            
        Returns:
            Dict: Visualization data for UI display
        """
        if not corrupted_data.get('errors_injected', False):
            return {'no_errors': True}
        
        visualization = {
            'error_type': corrupted_data.get('error_type', 'unknown'),
            'error_count': corrupted_data.get('error_count', 0),
            'blocks_comparison': []
        }
        
        # Compare each block
        for i, (orig_block, corr_block) in enumerate(zip(
            original_data['data_blocks'], 
            corrupted_data['data_blocks']
        )):
            block_errors = self.highlight_errors(orig_block, corr_block)
            visualization['blocks_comparison'].append({
                'block_index': i,
                'original': orig_block,
                'corrupted': corr_block,
                'errors': block_errors,
                'has_errors': len(block_errors) > 0
            })
        
        return visualization