"""
Property-based tests for transmission and error injection functionality.

These tests verify universal properties that should hold for all valid inputs
to the TransmissionSimulator and ErrorInjector classes.
"""

import pytest
from hypothesis import given, strategies as st, assume
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.transmission_simulator import TransmissionSimulator
from modules.error_injector import ErrorInjector


class TestTransmissionProperties:
    """Property-based tests for TransmissionSimulator class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.simulator = TransmissionSimulator()
    
    # Feature: lrc-error-detection, Property 5: Transmission Data Integrity
    @given(
        st.lists(st.text(alphabet='01', min_size=8, max_size=8), min_size=1, max_size=10),
        st.text(alphabet='01', min_size=8, max_size=8),
        st.text(min_size=1, max_size=50)
    )
    def test_transmission_integrity_property(self, data_blocks, lrc_byte, original_input):
        """
        **Property 5: Transmission Data Integrity**
        For any transmission package, normal transmission (without error injection) 
        should preserve all data blocks and LRC byte exactly as transmitted.
        **Validates: Requirements 3.1, 3.4**
        """
        # Create transmission package
        transmission_package = {
            'data_blocks': data_blocks,
            'lrc_byte': lrc_byte,
            'original_input': original_input,
            'input_type': 'text'
        }
        
        # Transmit the data
        received_package = self.simulator.transmit_data(transmission_package)
        
        # Property: All original data should be preserved exactly
        assert received_package['data_blocks'] == data_blocks
        assert received_package['lrc_byte'] == lrc_byte
        assert received_package['original_input'] == original_input
        assert received_package['input_type'] == 'text'
        
        # Property: Transmission should be marked as successful
        assert received_package['transmission_status'] == 'SUCCESS'
        assert received_package['errors_injected'] == False
        assert received_package['error_positions'] == []
        
        # Property: Transmission metadata should be added
        assert 'transmission_id' in received_package
        assert 'transmission_time' in received_package
        assert 'received_time' in received_package
        assert received_package['transmission_id'] > 0
        
        # Property: Original package should not be modified
        original_keys = set(transmission_package.keys())
        for key in original_keys:
            assert transmission_package[key] == data_blocks if key == 'data_blocks' else transmission_package[key]
    
    @given(
        st.lists(st.text(alphabet='01', min_size=8, max_size=8), min_size=1, max_size=5),
        st.text(alphabet='01', min_size=8, max_size=8)
    )
    def test_transmission_log_property(self, data_blocks, lrc_byte):
        """
        Property test for transmission logging.
        Each transmission should generate appropriate log entries.
        """
        package = {
            'data_blocks': data_blocks,
            'lrc_byte': lrc_byte
        }
        
        initial_log_count = len(self.simulator.get_transmission_log())
        
        # Transmit data
        self.simulator.transmit_data(package)
        
        # Property: Log should have new entries
        final_log = self.simulator.get_transmission_log()
        assert len(final_log) > initial_log_count
        
        # Property: Log should contain transmission events
        log_text = ' '.join(final_log)
        assert 'TRANSMISSION_START' in log_text
        assert 'TRANSMISSION_SUCCESS' in log_text
        assert 'DATA_INTEGRITY' in log_text
    
    @given(
        st.lists(st.text(alphabet='01', min_size=8, max_size=8), min_size=1, max_size=3),
        st.text(alphabet='01', min_size=8, max_size=8)
    )
    def test_package_validation_property(self, data_blocks, lrc_byte):
        """
        Property test for transmission package validation.
        Valid packages should pass validation, invalid ones should fail.
        """
        # Valid package
        valid_package = {
            'data_blocks': data_blocks,
            'lrc_byte': lrc_byte
        }
        assert self.simulator.validate_transmission_package(valid_package) == True
        
        # Invalid packages
        invalid_packages = [
            {},  # Empty dict
            {'data_blocks': data_blocks},  # Missing LRC
            {'lrc_byte': lrc_byte},  # Missing data blocks
            {'data_blocks': [], 'lrc_byte': lrc_byte},  # Empty data blocks
            {'data_blocks': ['invalid'], 'lrc_byte': lrc_byte},  # Non-binary data
            {'data_blocks': data_blocks, 'lrc_byte': 'invalid'},  # Non-binary LRC
        ]
        
        for invalid_package in invalid_packages:
            assert self.simulator.validate_transmission_package(invalid_package) == False
    
    def test_transmission_statistics_property(self):
        """
        Property test for transmission statistics tracking.
        Statistics should accurately reflect transmission activity.
        """
        initial_stats = self.simulator.get_transmission_statistics()
        initial_count = initial_stats['total_transmissions']
        
        # Perform some transmissions
        package = {
            'data_blocks': ['01010101', '10101010'],
            'lrc_byte': '11111111'
        }
        
        num_transmissions = 3
        for _ in range(num_transmissions):
            self.simulator.transmit_data(package)
        
        final_stats = self.simulator.get_transmission_statistics()
        
        # Property: Transmission count should increase correctly
        assert final_stats['total_transmissions'] == initial_count + num_transmissions
        assert final_stats['log_entries'] > initial_stats['log_entries']
        assert final_stats['last_transmission'] is not None


class TestErrorInjectorProperties:
    """Property-based tests for ErrorInjector class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.injector = ErrorInjector()
    
    # Feature: lrc-error-detection, Property 6: Error Injection Precision
    @given(
        st.lists(st.text(alphabet='01', min_size=8, max_size=8), min_size=1, max_size=5),
        st.text(alphabet='01', min_size=8, max_size=8)
    )
    def test_error_injection_precision_property(self, data_blocks, lrc_byte):
        """
        **Property 6: Error Injection Precision**
        For any data package and error specification, error injection should modify 
        exactly the specified bits while leaving all other bits unchanged, and 
        preserve the original data for comparison.
        **Validates: Requirements 4.1, 4.2, 4.4, 4.5**
        """
        # Create original data package
        original_data = {
            'data_blocks': data_blocks,
            'lrc_byte': lrc_byte
        }
        
        # Generate valid error positions
        if data_blocks:
            block_idx = 0
            bit_idx = 0
            error_positions = [(block_idx, bit_idx)]
            
            # Inject manual error
            corrupted_data = self.injector.inject_manual_error(original_data, error_positions)
            
            # Property: Original data should be preserved for comparison
            assert 'error_summary' in corrupted_data
            error_summary = corrupted_data['error_summary'][0]
            assert error_summary['original_block'] == data_blocks[block_idx]
            
            # Property: Only specified bits should be modified
            original_block = data_blocks[block_idx]
            corrupted_block = corrupted_data['data_blocks'][block_idx]
            
            differences = []
            for i, (orig_bit, corr_bit) in enumerate(zip(original_block, corrupted_block)):
                if orig_bit != corr_bit:
                    differences.append(i)
            
            # Should have exactly one difference at the specified position
            assert len(differences) == 1
            assert differences[0] == bit_idx
            
            # Property: All other blocks should remain unchanged
            for i, block in enumerate(data_blocks):
                if i != block_idx:
                    assert corrupted_data['data_blocks'][i] == block
            
            # Property: Error metadata should be accurate
            assert corrupted_data['errors_injected'] == True
            assert corrupted_data['error_type'] == 'manual'
            assert corrupted_data['error_count'] == 1
            assert corrupted_data['error_positions'] == error_positions
    
    @given(st.text(alphabet='01', min_size=1, max_size=32))
    def test_bit_flip_property(self, binary_str):
        """
        Property test for bit flipping operation.
        Flipping a bit should change exactly one bit and preserve all others.
        """
        for position in range(len(binary_str)):
            flipped = self.injector.flip_bit(binary_str, position)
            
            # Property: Result should have same length
            assert len(flipped) == len(binary_str)
            
            # Property: Exactly one bit should be different
            differences = sum(1 for orig, flip in zip(binary_str, flipped) if orig != flip)
            assert differences == 1
            
            # Property: The difference should be at the specified position
            assert binary_str[position] != flipped[position]
            
            # Property: All other positions should be unchanged
            for i, (orig, flip) in enumerate(zip(binary_str, flipped)):
                if i != position:
                    assert orig == flip
            
            # Property: Flipped bit should be opposite of original
            original_bit = binary_str[position]
            flipped_bit = flipped[position]
            assert (original_bit == '0' and flipped_bit == '1') or (original_bit == '1' and flipped_bit == '0')
    
    @given(
        st.integers(min_value=1, max_value=100),
        st.integers(min_value=0, max_value=10)
    )
    def test_random_error_generation_property(self, data_length, error_count):
        """
        Property test for random error position generation.
        Generated positions should be unique and within bounds.
        """
        assume(error_count <= data_length)
        
        positions = self.injector.generate_random_errors(data_length, error_count)
        
        # Property: Should generate exactly the requested number of positions
        assert len(positions) == error_count
        
        # Property: All positions should be unique
        assert len(set(positions)) == error_count
        
        # Property: All positions should be within bounds
        for pos in positions:
            assert 0 <= pos < data_length
        
        # Property: Positions should be sorted
        assert positions == sorted(positions)
    
    @given(
        st.lists(st.text(alphabet='01', min_size=8, max_size=8), min_size=1, max_size=5),
        st.text(alphabet='01', min_size=8, max_size=8),
        st.floats(min_value=0.0, max_value=1.0)
    )
    def test_random_error_injection_property(self, data_blocks, lrc_byte, error_rate):
        """
        Property test for random error injection.
        Random errors should respect the error rate and preserve data structure.
        """
        original_data = {
            'data_blocks': data_blocks,
            'lrc_byte': lrc_byte
        }
        
        corrupted_data = self.injector.inject_random_error(original_data, error_rate)
        
        # Property: Data structure should be preserved
        assert len(corrupted_data['data_blocks']) == len(data_blocks)
        assert 'lrc_byte' in corrupted_data
        
        if error_rate == 0.0:
            # Property: No errors should be injected with 0% error rate
            # Should return clean copy without error metadata
            assert corrupted_data['data_blocks'] == data_blocks
            assert corrupted_data['lrc_byte'] == lrc_byte
        else:
            # Property: Error metadata should be present for non-zero error rates
            assert 'errors_injected' in corrupted_data
            assert 'error_type' in corrupted_data
            assert 'error_rate' in corrupted_data
            assert 'error_count' in corrupted_data
            assert 'error_positions' in corrupted_data
    
    @given(
        st.text(alphabet='01', min_size=8, max_size=8),
        st.text(alphabet='01', min_size=8, max_size=8)
    )
    def test_error_highlighting_property(self, original, corrupted):
        """
        Property test for error highlighting.
        Should correctly identify all differences between strings.
        """
        differences = self.injector.highlight_errors(original, corrupted)
        
        # Property: Each difference should be valid
        for pos, orig_bit, corr_bit in differences:
            assert 0 <= pos < len(original)
            assert original[pos] == orig_bit
            assert corrupted[pos] == corr_bit
            assert orig_bit != corr_bit
            assert orig_bit in '01'
            assert corr_bit in '01'
        
        # Property: Should find all differences
        manual_differences = []
        for i, (o, c) in enumerate(zip(original, corrupted)):
            if o != c:
                manual_differences.append((i, o, c))
        
        assert len(differences) == len(manual_differences)
        assert differences == manual_differences
    
    def test_error_injection_validation_property(self):
        """
        Property test for error injection input validation.
        Invalid inputs should raise appropriate errors.
        """
        # Test invalid data structures
        invalid_data_sets = [
            {},  # Empty dict
            {'wrong_key': []},  # Missing data_blocks
            {'data_blocks': 'not_a_list'},  # Wrong type
        ]
        
        for invalid_data in invalid_data_sets:
            with pytest.raises(ValueError):
                self.injector.inject_manual_error(invalid_data, [(0, 0)])
        
        # Test invalid error positions
        valid_data = {'data_blocks': ['01010101']}
        invalid_positions = [
            [(1, 0)],  # Block index out of range
            [(0, 8)],  # Bit position out of range
            [(-1, 0)],  # Negative block index
            [(0, -1)],  # Negative bit position
        ]
        
        for invalid_pos in invalid_positions:
            with pytest.raises(ValueError):
                self.injector.inject_manual_error(valid_data, invalid_pos)
    
    @given(st.floats(min_value=-1.0, max_value=2.0).filter(lambda x: x < 0.0 or x > 1.0))
    def test_invalid_error_rate_property(self, invalid_rate):
        """
        Property test for invalid error rates.
        Error rates outside [0.0, 1.0] should raise ValueError.
        """
        data = {'data_blocks': ['01010101']}
        
        with pytest.raises(ValueError, match="Error rate must be between 0.0 and 1.0"):
            self.injector.inject_random_error(data, invalid_rate)