"""
Property-based tests for verification functionality.

These tests verify universal properties that should hold for all valid inputs
to the SenderModule and ReceiverModule classes, ensuring correctness of the
complete sender-receiver workflow.
"""

import pytest
from hypothesis import given, strategies as st, assume
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.sender_module import SenderModule
from modules.receiver_module import ReceiverModule
from modules.lrc_calculator import LRCCalculator
from modules.error_injector import ErrorInjector


class TestVerificationProperties:
    """Property-based tests for sender-receiver verification workflow"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.sender = SenderModule()
        self.receiver = ReceiverModule()
        self.injector = ErrorInjector()
    
    # Feature: lrc-error-detection, Property 7: LRC Verification Accuracy
    @given(
        st.text(min_size=1, max_size=20).filter(lambda x: all(ord(c) < 128 for c in x)),
        st.sampled_from(['text', 'binary'])
    )
    def test_lrc_verification_accuracy_property(self, user_input, input_type):
        """
        **Property 7: LRC Verification Accuracy**
        For any received data blocks and LRC byte, the verification process should 
        detect an error if and only if the recalculated LRC differs from the received LRC byte.
        **Validates: Requirements 5.1, 5.2**
        """
        # Convert text input to binary if needed
        if input_type == 'binary':
            # Convert text to binary for testing
            binary_input = ''.join(format(ord(c), '08b') for c in user_input)
            test_input = binary_input
        else:
            test_input = user_input
        
        # Sender workflow
        sender_result = self.sender.process_input(test_input, input_type)
        transmission_package = self.sender.generate_transmission_package()
        
        # Receiver workflow with correct data
        processed_data = self.receiver.process_received_data(transmission_package)
        is_valid, error_message, error_report = self.receiver.detect_errors()
        
        # Property: Verification should pass for uncorrupted data
        assert is_valid == True
        assert "No Error Detected" in error_message
        assert error_report['is_valid'] == True
        assert error_report['received_lrc'] == error_report['calculated_lrc']
        
        # Test with corrupted data (if possible)
        if transmission_package['data_blocks']:
            # Create corrupted version
            corrupted_package = self.injector.inject_manual_error(
                transmission_package, 
                [(0, 0)]  # Corrupt first bit of first block
            )
            
            # Clear receiver history for new test
            self.receiver.clear_history()
            
            # Receiver workflow with corrupted data
            processed_corrupted = self.receiver.process_received_data(corrupted_package)
            is_valid_corrupted, error_message_corrupted, error_report_corrupted = self.receiver.detect_errors()
            
            # Property: Verification should fail for corrupted data
            assert is_valid_corrupted == False
            assert "Error Detected" in error_message_corrupted
            assert error_report_corrupted['is_valid'] == False
            assert error_report_corrupted['received_lrc'] != error_report_corrupted['calculated_lrc']
    
    # Feature: lrc-error-detection, Property 8: Error Detection Message Correctness
    @given(
        st.lists(st.text(alphabet='01', min_size=8, max_size=8), min_size=1, max_size=5),
        st.text(alphabet='01', min_size=8, max_size=8)
    )
    def test_error_detection_message_correctness_property(self, data_blocks, lrc_byte):
        """
        **Property 8: Error Detection Message Correctness**
        For any LRC verification result, the system should display "No Error Detected" 
        when LRC values match and "Error Detected" when they differ, along with both 
        LRC values for comparison.
        **Validates: Requirements 5.3, 5.4, 5.5**
        """
        # Create transmission package
        package = {
            'data_blocks': data_blocks,
            'lrc_byte': lrc_byte,
            'original_input': 'test'
        }
        
        # Test with correct LRC
        calculator = LRCCalculator()
        correct_lrc, _ = calculator.calculate_lrc(data_blocks)
        correct_package = package.copy()
        correct_package['lrc_byte'] = correct_lrc
        
        # Receiver workflow with correct LRC
        processed_correct = self.receiver.process_received_data(correct_package)
        is_valid_correct, message_correct, report_correct = self.receiver.detect_errors()
        
        # Property: Correct LRC should produce "No Error Detected" message
        assert is_valid_correct == True
        assert "No Error Detected" in message_correct
        assert report_correct['received_lrc'] == report_correct['calculated_lrc']
        
        # Clear receiver for next test
        self.receiver.clear_history()
        
        # Test with incorrect LRC (if different from correct)
        if lrc_byte != correct_lrc:
            incorrect_package = package.copy()
            incorrect_package['lrc_byte'] = lrc_byte
            
            # Receiver workflow with incorrect LRC
            processed_incorrect = self.receiver.process_received_data(incorrect_package)
            is_valid_incorrect, message_incorrect, report_incorrect = self.receiver.detect_errors()
            
            # Property: Incorrect LRC should produce "Error Detected" message
            assert is_valid_incorrect == False
            assert "Error Detected" in message_incorrect
            assert report_incorrect['received_lrc'] != report_incorrect['calculated_lrc']
            
            # Property: Message should contain both LRC values
            assert report_incorrect['received_lrc'] in message_incorrect
            assert report_incorrect['calculated_lrc'] in message_incorrect
    
    @given(
        st.text(min_size=1, max_size=10).filter(lambda x: all(ord(c) < 128 for c in x))
    )
    def test_sender_receiver_integration_property(self, text_input):
        """
        Property test for complete sender-receiver integration.
        The complete workflow should preserve data integrity without errors.
        """
        # Sender workflow
        sender_result = self.sender.process_input(text_input, 'text')
        transmission_package = self.sender.generate_transmission_package()
        
        # Property: Sender should produce valid transmission package
        assert 'data_blocks' in transmission_package
        assert 'lrc_byte' in transmission_package
        assert transmission_package['ready_for_transmission'] == True
        assert len(transmission_package['data_blocks']) == len(text_input)
        
        # Receiver workflow
        processed_data = self.receiver.process_received_data(transmission_package)
        is_valid, error_message, error_report = self.receiver.detect_errors()
        
        # Property: Receiver should successfully verify uncorrupted data
        assert is_valid == True
        assert processed_data['block_count'] == len(text_input)
        assert processed_data['original_input'] == text_input
        
        # Property: Comparison report should be generated successfully
        comparison_report = self.receiver.generate_comparison_report()
        assert comparison_report['verification_successful'] == True
        assert comparison_report['summary']['Transmission Status'] == 'SUCCESS'
        assert len(comparison_report['data_comparison']) == len(text_input)
    
    @given(
        st.lists(st.text(alphabet='01', min_size=8, max_size=8), min_size=1, max_size=3)
    )
    def test_receiver_input_validation_property(self, data_blocks):
        """
        Property test for receiver input validation.
        Invalid packages should be rejected with appropriate errors.
        """
        # Valid package should be accepted
        valid_package = {
            'data_blocks': data_blocks,
            'lrc_byte': '00000000'
        }
        
        processed = self.receiver.process_received_data(valid_package)
        assert processed['processing_status'] == 'SUCCESS'
        
        # Clear receiver for next tests
        self.receiver.clear_history()
        
        # Invalid packages should be rejected
        invalid_packages = [
            {},  # Empty package
            {'data_blocks': data_blocks},  # Missing LRC
            {'lrc_byte': '00000000'},  # Missing data blocks
            {'data_blocks': [], 'lrc_byte': '00000000'},  # Empty data blocks
            {'data_blocks': ['invalid'], 'lrc_byte': '00000000'},  # Non-binary data
            {'data_blocks': data_blocks, 'lrc_byte': 'invalid'},  # Non-binary LRC
        ]
        
        for invalid_package in invalid_packages:
            with pytest.raises(ValueError):
                self.receiver.process_received_data(invalid_package)
    
    def test_verification_history_property(self):
        """
        Property test for verification history tracking.
        History should accurately track all verification operations.
        """
        initial_history = self.receiver.get_verification_history()
        initial_count = len(initial_history)
        
        # Perform multiple verifications
        packages = [
            {
                'data_blocks': ['01010101', '10101010'],
                'lrc_byte': '11111111',
                'original_input': 'test1'
            },
            {
                'data_blocks': ['11110000'],
                'lrc_byte': '11110000',
                'original_input': 'test2'
            }
        ]
        
        for i, package in enumerate(packages):
            self.receiver.process_received_data(package)
            self.receiver.detect_errors()
            
            # Property: History should grow with each verification
            current_history = self.receiver.get_verification_history()
            assert len(current_history) == initial_count + i + 1
            
            # Property: Latest entry should match current package
            latest_entry = current_history[-1]
            assert latest_entry['received_package']['original_input'] == package['original_input']
            assert latest_entry['processed_data']['original_input'] == package['original_input']
    
    @given(
        st.text(min_size=1, max_size=5).filter(lambda x: all(ord(c) < 128 for c in x))
    )
    def test_error_injection_detection_property(self, text_input):
        """
        Property test for error injection and detection workflow.
        Injected errors should be reliably detected by the receiver.
        """
        # Create transmission package
        self.sender.process_input(text_input, 'text')
        original_package = self.sender.generate_transmission_package()
        
        # Test without errors first
        self.receiver.process_received_data(original_package)
        is_valid_clean, _, _ = self.receiver.detect_errors()
        assert is_valid_clean == True
        
        # Clear receiver for error test
        self.receiver.clear_history()
        
        # Inject error and test detection
        if original_package['data_blocks']:
            corrupted_package = self.injector.inject_manual_error(
                original_package,
                [(0, 0)]  # Corrupt first bit
            )
            
            self.receiver.process_received_data(corrupted_package)
            is_valid_corrupted, error_msg, error_report = self.receiver.detect_errors()
            
            # Property: Error should be detected
            assert is_valid_corrupted == False
            assert "Error Detected" in error_msg
            assert error_report['is_valid'] == False
            
            # Property: Comparison report should reflect error
            comparison_report = self.receiver.generate_comparison_report()
            assert comparison_report['summary']['Transmission Status'] == 'ERROR DETECTED'
            assert comparison_report['summary']['LRC Match'] == 'NO'
    
    def test_educational_content_generation_property(self):
        """
        Property test for educational content generation.
        Educational explanations should be available for all operations.
        """
        # Create test scenario
        self.sender.process_input("Test", 'text')
        package = self.sender.generate_transmission_package()
        
        # Test sender visualization data
        sender_viz = self.sender.get_visualization_data()
        assert 'educational_notes' in sender_viz
        assert len(sender_viz['educational_notes']) > 0
        assert any('LRC' in note for note in sender_viz['educational_notes'])
        
        # Test receiver comparison report
        self.receiver.process_received_data(package)
        self.receiver.detect_errors()
        comparison_report = self.receiver.generate_comparison_report()
        
        # Property: Educational explanations should be present
        assert 'educational_explanations' in comparison_report
        assert len(comparison_report['educational_explanations']) > 0
        assert 'recommendations' in comparison_report
        assert len(comparison_report['recommendations']) > 0
        
        # Property: Explanations should contain relevant educational content
        explanations_text = ' '.join(comparison_report['educational_explanations'])
        assert 'LRC' in explanations_text
        assert 'receiver' in explanations_text.lower() or 'verification' in explanations_text.lower()
    
    def test_module_state_management_property(self):
        """
        Property test for module state management.
        Modules should properly manage their internal state and history.
        """
        # Test sender state management
        initial_sender_history = len(self.sender.get_processing_history())
        
        self.sender.process_input("Test1", 'text')
        assert len(self.sender.get_processing_history()) == initial_sender_history + 1
        assert self.sender.get_current_package() is None  # No package generated yet
        
        self.sender.generate_transmission_package()
        assert self.sender.get_current_package() is not None
        
        # Test receiver state management
        initial_receiver_history = len(self.receiver.get_verification_history())
        
        package = self.sender.get_current_package()
        self.receiver.process_received_data(package)
        assert len(self.receiver.get_verification_history()) == initial_receiver_history + 1
        
        # Test state clearing
        self.sender.clear_history()
        assert len(self.sender.get_processing_history()) == 0
        assert self.sender.get_current_package() is None
        
        self.receiver.clear_history()
        assert len(self.receiver.get_verification_history()) == 0