"""
Receiver Module for LRC Error Detection System

This module handles error detection and verification at the receiver side.
It integrates LRCCalculator to provide comprehensive error detection
and reporting capabilities for the LRC error detection demonstration.

Educational Purpose:
- Demonstrates the receiver's role in error detection systems
- Shows how received data is verified for integrity
- Provides detailed error analysis and reporting
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import copy

from .lrc_calculator import LRCCalculator


class ReceiverModule:
    """
    Handles error detection and verification at the receiver side.
    
    This class provides a high-level interface for the receiver's operations,
    including data verification, error detection, and comprehensive reporting
    of transmission integrity.
    """
    
    def __init__(self, lrc_calculator: Optional[LRCCalculator] = None):
        """
        Initialize the Receiver Module with required components.
        
        Args:
            lrc_calculator (LRCCalculator, optional): LRC calculation component
        """
        self.lrc_calculator = lrc_calculator or LRCCalculator()
        self.verification_history = []
        self.current_verification = None
    
    def process_received_data(self, received_package: Dict) -> Dict:
        """
        Process received transmission package and extract verification data.
        
        This method takes a received transmission package and prepares it
        for error detection verification, extracting data blocks and LRC
        information needed for integrity checking.
        
        Args:
            received_package (Dict): Received transmission package
            
        Returns:
            Dict: Processed data ready for verification
            
        Example:
            >>> receiver = ReceiverModule()
            >>> package = {
            ...     'data_blocks': ['01001000', '01100101'],
            ...     'lrc_byte': '00101101',
            ...     'original_input': 'He'
            ... }
            >>> processed = receiver.process_received_data(package)
        """
        if not isinstance(received_package, dict):
            raise ValueError("Received package must be a dictionary")
        
        # Validate required fields
        required_fields = ['data_blocks', 'lrc_byte']
        for field in required_fields:
            if field not in received_package:
                raise ValueError(f"Missing required field in received package: {field}")
        
        # Validate data blocks
        data_blocks = received_package['data_blocks']
        if not isinstance(data_blocks, list) or not data_blocks:
            raise ValueError("Data blocks must be a non-empty list")
        
        # Validate each data block
        for i, block in enumerate(data_blocks):
            if not isinstance(block, str):
                raise ValueError(f"Data block {i} must be a string")
            if not all(bit in '01' for bit in block):
                raise ValueError(f"Data block {i} contains non-binary characters")
        
        # Validate LRC byte
        lrc_byte = received_package['lrc_byte']
        if not isinstance(lrc_byte, str):
            raise ValueError("LRC byte must be a string")
        if not all(bit in '01' for bit in lrc_byte):
            raise ValueError("LRC byte contains non-binary characters")
        
        processing_time = datetime.now()
        
        # Extract and organize received data
        processed_data = {
            'received_data_blocks': data_blocks,
            'received_lrc_byte': lrc_byte,
            'original_input': received_package.get('original_input', 'Unknown'),
            'input_type': received_package.get('input_type', 'Unknown'),
            'transmission_id': received_package.get('transmission_id', 'Unknown'),
            'block_count': len(data_blocks),
            'total_bits': sum(len(block) for block in data_blocks),
            'processing_time': processing_time,
            'processing_status': 'SUCCESS',
            'receiver_id': len(self.verification_history) + 1,
            'errors_detected_in_transmission': received_package.get('errors_injected', False),
            'transmission_error_positions': received_package.get('error_positions', [])
        }
        
        # Store in verification history
        self.verification_history.append({
            'received_package': copy.deepcopy(received_package),
            'processed_data': processed_data,
            'timestamp': processing_time
        })
        
        return processed_data
    
    def detect_errors(self) -> Tuple[bool, str, Dict]:
        """
        Perform error detection on the most recently processed data.
        
        This method recalculates the LRC from received data blocks and
        compares it with the received LRC to detect transmission errors.
        
        Returns:
            Tuple[bool, str, Dict]: (is_valid, error_message, detailed_report)
            
        Raises:
            ValueError: If no data has been processed yet
            
        Example:
            >>> receiver = ReceiverModule()
            >>> receiver.process_received_data(package)
            >>> is_valid, message, report = receiver.detect_errors()
        """
        if not self.verification_history:
            raise ValueError("No data has been processed. Call process_received_data() first.")
        
        # Get the most recent processed data
        latest_data = self.verification_history[-1] if self.verification_history else None
        if not latest_data or 'error' in latest_data:
            raise ValueError("Cannot perform error detection on failed processing")
        
        processed_data = latest_data['processed_data']
        
        # Perform LRC verification
        is_valid, calculated_lrc, verification_steps = self.lrc_calculator.verify_lrc(
            processed_data['received_data_blocks'],
            processed_data['received_lrc_byte']
        )
        
        # Create detailed error report
        error_report = self._create_error_report(
            processed_data, is_valid, calculated_lrc, verification_steps
        )
        
        # Generate appropriate message
        if is_valid:
            error_message = "No Error Detected - Data transmission was successful"
        else:
            error_message = f"Error Detected - LRC mismatch (Expected: {calculated_lrc}, Received: {processed_data['received_lrc_byte']})"
        
        # Store current verification
        self.current_verification = {
            'is_valid': is_valid,
            'error_message': error_message,
            'error_report': error_report,
            'verification_time': datetime.now()
        }
        
        return is_valid, error_message, error_report
    
    def generate_comparison_report(self) -> Dict:
        """
        Generate comprehensive comparison report for educational display.
        
        This method creates a detailed report comparing transmitted vs
        received data, showing LRC calculations, and providing educational
        explanations of the error detection process.
        
        Returns:
            Dict: Comprehensive comparison report
            
        Example:
            >>> receiver = ReceiverModule()
            >>> receiver.process_received_data(package)
            >>> receiver.detect_errors()
            >>> report = receiver.generate_comparison_report()
        """
        if not self.current_verification:
            raise ValueError("No error detection has been performed. Call detect_errors() first.")
        
        verification = self.current_verification
        error_report = verification['error_report']
        
        # Create comparison tables
        data_comparison = self._create_data_comparison_table(error_report)
        lrc_comparison = self._create_lrc_comparison_table(error_report)
        verification_steps = self._format_verification_steps(error_report['verification_steps'])
        
        # Generate educational explanations
        explanations = self._generate_educational_explanations(error_report)
        
        # Create summary statistics
        summary = {
            'Transmission Status': 'SUCCESS' if verification['is_valid'] else 'ERROR DETECTED',
            'Data Blocks Received': error_report['block_count'],
            'Total Bits Received': error_report['total_bits'],
            'Received LRC': error_report['received_lrc'],
            'Calculated LRC': error_report['calculated_lrc'],
            'LRC Match': 'YES' if verification['is_valid'] else 'NO',
            'Error Detection Result': verification['error_message']
        }
        
        return {
            'verification_successful': True,
            'summary': summary,
            'data_comparison': data_comparison,
            'lrc_comparison': lrc_comparison,
            'verification_steps': verification_steps,
            'educational_explanations': explanations,
            'error_analysis': self._analyze_error_patterns(error_report),
            'recommendations': self._generate_recommendations(error_report),
            'report_metadata': {
                'Report ID': error_report['verification_id'],
                'Verification Time': verification['verification_time'].strftime('%H:%M:%S'),
                'Receiver Module Version': '1.0'
            }
        }
    
    def get_verification_history(self) -> List[Dict]:
        """
        Get history of all verification operations.
        
        Returns:
            List[Dict]: List of verification history entries
        """
        return copy.deepcopy(self.verification_history)
    
    def clear_history(self):
        """Clear verification history and current verification"""
        self.verification_history.clear()
        self.current_verification = None
    
    def _create_error_report(self, processed_data: Dict, is_valid: bool, 
                           calculated_lrc: str, verification_steps: List[Dict]) -> Dict:
        """
        Create detailed error report from verification results.
        
        Args:
            processed_data (Dict): Processed received data
            is_valid (bool): Whether verification passed
            calculated_lrc (str): Recalculated LRC
            verification_steps (List[Dict]): LRC verification steps
            
        Returns:
            Dict: Detailed error report
        """
        return {
            'verification_id': len(self.verification_history) + 1,
            'is_valid': is_valid,
            'received_data_blocks': processed_data['received_data_blocks'],
            'received_lrc': processed_data['received_lrc_byte'],
            'calculated_lrc': calculated_lrc,
            'block_count': processed_data['block_count'],
            'total_bits': processed_data['total_bits'],
            'original_input': processed_data['original_input'],
            'input_type': processed_data['input_type'],
            'verification_steps': verification_steps,
            'transmission_errors_known': processed_data['errors_detected_in_transmission'],
            'known_error_positions': processed_data['transmission_error_positions'],
            'verification_time': datetime.now()
        }
    
    def _create_data_comparison_table(self, error_report: Dict) -> List[Dict]:
        """Create data comparison table for visualization"""
        comparison_table = []
        
        for i, block in enumerate(error_report['received_data_blocks']):
            comparison_table.append({
                'Block': f"Block {i + 1}",
                'Received Data': block,
                'Decimal Value': int(block, 2),
                'Character': chr(int(block, 2)) if 32 <= int(block, 2) <= 126 else '·',
                'Status': 'OK'  # Could be enhanced to show specific block errors
            })
        
        return comparison_table
    
    def _create_lrc_comparison_table(self, error_report: Dict) -> Dict:
        """Create LRC comparison table for visualization"""
        return {
            'Received LRC': {
                'Binary': error_report['received_lrc'],
                'Decimal': int(error_report['received_lrc'], 2),
                'Source': 'Transmitted with data'
            },
            'Calculated LRC': {
                'Binary': error_report['calculated_lrc'],
                'Decimal': int(error_report['calculated_lrc'], 2),
                'Source': 'Recalculated from received data'
            },
            'Match': error_report['is_valid'],
            'Difference': 'None' if error_report['is_valid'] else 'LRC values differ'
        }
    
    def _format_verification_steps(self, verification_steps: List[Dict]) -> List[Dict]:
        """Format verification steps for display"""
        formatted_steps = []
        
        for step in verification_steps:
            if step['operation'] in ['XOR', 'COMPARE']:
                formatted_steps.append({
                    'Step': step['step_number'],
                    'Operation': step['operation'],
                    'Description': step['description'],
                    'Result': step['result']
                })
        
        return formatted_steps
    
    def _generate_educational_explanations(self, error_report: Dict) -> List[str]:
        """Generate educational explanations for the verification process"""
        explanations = []
        
        explanations.append("The receiver recalculates the LRC using the same method as the sender.")
        explanations.append(f"Received {error_report['block_count']} data blocks totaling {error_report['total_bits']} bits.")
        
        if error_report['is_valid']:
            explanations.append("✅ LRC verification PASSED - No transmission errors detected.")
            explanations.append("The recalculated LRC matches the received LRC, indicating data integrity.")
        else:
            explanations.append("❌ LRC verification FAILED - Transmission errors detected.")
            explanations.append("The recalculated LRC differs from the received LRC, indicating data corruption.")
            explanations.append("This demonstrates how LRC can detect single-bit and some multi-bit errors.")
        
        if error_report['transmission_errors_known']:
            explanations.append(f"Note: Errors were intentionally injected at positions {error_report['known_error_positions']} for demonstration.")
        
        return explanations
    
    def _analyze_error_patterns(self, error_report: Dict) -> Dict:
        """Analyze error patterns for educational insights"""
        analysis = {
            'error_detected': not error_report['is_valid'],
            'lrc_effectiveness': 'Demonstrated' if not error_report['is_valid'] else 'Not applicable',
            'error_type': 'Unknown'
        }
        
        if error_report['transmission_errors_known']:
            error_count = len(error_report['known_error_positions'])
            if error_count == 1:
                analysis['error_type'] = 'Single-bit error'
            elif error_count > 1:
                analysis['error_type'] = 'Multi-bit error'
            
            analysis['injected_errors'] = error_count
            analysis['detection_success'] = not error_report['is_valid']
        
        return analysis
    
    def _generate_recommendations(self, error_report: Dict) -> List[str]:
        """Generate recommendations based on verification results"""
        recommendations = []
        
        if error_report['is_valid']:
            recommendations.append("Data transmission was successful. No further action needed.")
            recommendations.append("The LRC error detection method worked as expected.")
        else:
            recommendations.append("Transmission errors detected. Data should be retransmitted.")
            recommendations.append("Consider investigating the transmission channel for sources of interference.")
            recommendations.append("LRC successfully detected the error, demonstrating its effectiveness.")
        
        recommendations.append("Try injecting different types of errors to see LRC's detection capabilities.")
        recommendations.append("Experiment with multiple bit errors to understand LRC's limitations.")
        
        return recommendations