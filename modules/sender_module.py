"""
Sender Module for LRC Error Detection System

This module orchestrates data preparation and LRC generation at the sender side.
It integrates DataConverter and LRCCalculator components to provide a complete
sender-side implementation for the LRC error detection demonstration.

Educational Purpose:
- Demonstrates the sender's role in error detection systems
- Shows how data is prepared for transmission
- Integrates multiple components into a cohesive sender workflow
"""

from typing import Dict, List, Optional
from datetime import datetime
import copy

from .data_converter import DataConverter
from .lrc_calculator import LRCCalculator


class SenderModule:
    """
    Orchestrates data preparation and LRC generation at the sender side.
    
    This class provides a high-level interface for the sender's operations,
    integrating data conversion, LRC calculation, and transmission package
    preparation into a unified workflow.
    """
    
    def __init__(self, data_converter: Optional[DataConverter] = None, 
                 lrc_calculator: Optional[LRCCalculator] = None):
        """
        Initialize the Sender Module with required components.
        
        Args:
            data_converter (DataConverter, optional): Data conversion component
            lrc_calculator (LRCCalculator, optional): LRC calculation component
        """
        self.data_converter = data_converter or DataConverter()
        self.lrc_calculator = lrc_calculator or LRCCalculator()
        self.processing_history = []
        self.current_package = None
    
    def process_input(self, user_input: str, input_type: str) -> Dict:
        """
        Process user input and prepare it for LRC calculation.
        
        This method handles both text and binary input types, converting them
        to the appropriate format for LRC processing and providing detailed
        information about the conversion process.
        
        Args:
            user_input (str): User's input data (text or binary)
            input_type (str): Type of input ('text' or 'binary')
            
        Returns:
            Dict: Processing result with converted data and metadata
            
        Example:
            >>> sender = SenderModule()
            >>> result = sender.process_input("Hello", "text")
            >>> print(result['data_blocks'])
            ['01001000', '01100101', '01101100', '01101100', '01101111']
        """
        if not user_input:
            raise ValueError("Input cannot be empty")
        
        if input_type not in ['text', 'binary']:
            raise ValueError("Input type must be 'text' or 'binary'")
        
        processing_start = datetime.now()
        
        try:
            if input_type == 'text':
                # Process text input
                result = self._process_text_input(user_input)
            else:
                # Process binary input
                result = self._process_binary_input(user_input)
            
            # Add processing metadata
            result.update({
                'original_input': user_input,
                'input_type': input_type,
                'processing_time': processing_start,
                'processing_status': 'SUCCESS',
                'sender_id': len(self.processing_history) + 1
            })
            
            # Store in processing history
            self.processing_history.append({
                'input': user_input,
                'type': input_type,
                'timestamp': processing_start,
                'result': copy.deepcopy(result)
            })
            
            return result
            
        except Exception as e:
            # Handle processing errors
            error_result = {
                'original_input': user_input,
                'input_type': input_type,
                'processing_time': processing_start,
                'processing_status': 'ERROR',
                'error_message': str(e),
                'data_blocks': [],
                'binary_representation': []
            }
            
            self.processing_history.append({
                'input': user_input,
                'type': input_type,
                'timestamp': processing_start,
                'error': str(e)
            })
            
            raise ValueError(f"Input processing failed: {str(e)}")
    
    def generate_transmission_package(self) -> Dict:
        """
        Generate complete transmission package with LRC calculation.
        
        This method takes the processed input data and generates a complete
        transmission package including data blocks, LRC byte, and all
        necessary metadata for transmission and educational display.
        
        Returns:
            Dict: Complete transmission package ready for transmission
            
        Raises:
            ValueError: If no data has been processed yet
            
        Example:
            >>> sender = SenderModule()
            >>> sender.process_input("Hi", "text")
            >>> package = sender.generate_transmission_package()
            >>> print(package['lrc_byte'])
            '00101101'
        """
        if not self.processing_history:
            raise ValueError("No input data has been processed. Call process_input() first.")
        
        # Get the most recent processing result
        latest_processing = self.processing_history[-1]
        
        if 'error' in latest_processing:
            raise ValueError("Cannot generate package from failed processing")
        
        processed_data = latest_processing['result']
        data_blocks = processed_data['data_blocks']
        
        # Calculate LRC
        lrc_byte, calculation_steps = self.lrc_calculator.calculate_lrc(data_blocks)
        
        # Create comprehensive transmission package
        transmission_package = {
            # Core data
            'data_blocks': data_blocks,
            'lrc_byte': lrc_byte,
            'original_input': processed_data['original_input'],
            'input_type': processed_data['input_type'],
            
            # Processing information
            'binary_representation': processed_data['binary_representation'],
            'conversion_info': processed_data.get('conversion_info', {}),
            'block_size': len(data_blocks[0]) if data_blocks else 8,
            'total_blocks': len(data_blocks),
            'total_bits': sum(len(block) for block in data_blocks),
            
            # LRC calculation details
            'lrc_calculation_steps': calculation_steps,
            'calculation_summary': self.lrc_calculator.format_calculation_steps(calculation_steps),
            
            # Metadata
            'package_id': len(self.processing_history),
            'creation_time': datetime.now(),
            'sender_module_version': '1.0',
            'ready_for_transmission': True
        }
        
        # Store current package
        self.current_package = copy.deepcopy(transmission_package)
        
        return transmission_package
    
    def get_visualization_data(self) -> Dict:
        """
        Get data formatted for UI display and visualization.
        
        This method provides comprehensive data formatted specifically
        for the Streamlit user interface, including tables, charts,
        and educational explanations.
        
        Returns:
            Dict: Visualization data for UI display
            
        Example:
            >>> sender = SenderModule()
            >>> sender.process_input("Test", "text")
            >>> sender.generate_transmission_package()
            >>> viz_data = sender.get_visualization_data()
        """
        if not self.current_package:
            return {'error': 'No transmission package available. Generate package first.'}
        
        package = self.current_package
        
        # Prepare data blocks table
        blocks_table = []
        for i, block in enumerate(package['data_blocks']):
            blocks_table.append({
                'Block': f"Block {i + 1}",
                'Binary': block,
                'Decimal': int(block, 2),
                'Character': chr(int(block, 2)) if 32 <= int(block, 2) <= 126 else '·'
            })
        
        # Prepare LRC calculation visualization
        lrc_steps = []
        for step in package['lrc_calculation_steps']:
            if step['operation'] == 'XOR':
                lrc_steps.append({
                    'Step': step['step_number'],
                    'Operation': f"{step['operand1']} ⊕ {step['operand2']}",
                    'Result': step['result'],
                    'Description': step['description']
                })
        
        # Prepare summary statistics
        summary_stats = {
            'Input Type': package['input_type'].title(),
            'Original Input': package['original_input'],
            'Total Characters': len(package['original_input']) if package['input_type'] == 'text' else 'N/A',
            'Total Blocks': package['total_blocks'],
            'Total Bits': package['total_bits'],
            'LRC Byte': package['lrc_byte'],
            'LRC Decimal': int(package['lrc_byte'], 2)
        }
        
        return {
            'package_ready': True,
            'summary_stats': summary_stats,
            'data_blocks_table': blocks_table,
            'lrc_calculation_steps': lrc_steps,
            'binary_representation': package['binary_representation'],
            'conversion_info': package.get('conversion_info', {}),
            'educational_notes': self._get_educational_notes(package),
            'package_metadata': {
                'Package ID': package['package_id'],
                'Creation Time': package['creation_time'].strftime('%H:%M:%S'),
                'Block Size': f"{package['block_size']} bits",
                'Ready for Transmission': package['ready_for_transmission']
            }
        }
    
    def get_processing_history(self) -> List[Dict]:
        """
        Get history of all input processing operations.
        
        Returns:
            List[Dict]: List of processing history entries
        """
        return copy.deepcopy(self.processing_history)
    
    def clear_history(self):
        """Clear processing history and current package"""
        self.processing_history.clear()
        self.current_package = None
    
    def get_current_package(self) -> Optional[Dict]:
        """
        Get the current transmission package.
        
        Returns:
            Dict or None: Current transmission package if available
        """
        return copy.deepcopy(self.current_package) if self.current_package else None
    
    def _process_text_input(self, text: str) -> Dict:
        """
        Process text input through the data conversion pipeline.
        
        Args:
            text (str): Text input to process
            
        Returns:
            Dict: Processing result with binary data and conversion info
        """
        # Convert text to binary
        binary_list = self.data_converter.text_to_binary(text)
        
        # Get detailed conversion information
        conversion_info = self.data_converter.get_conversion_info(text)
        
        # Format binary representation for display
        formatted_binary = self.data_converter.format_binary_display(binary_list)
        
        return {
            'data_blocks': binary_list,
            'binary_representation': binary_list,
            'formatted_binary': formatted_binary,
            'conversion_info': conversion_info,
            'processing_method': 'text_to_binary'
        }
    
    def _process_binary_input(self, binary_str: str) -> Dict:
        """
        Process binary input through validation and block division.
        
        Args:
            binary_str (str): Binary string input to process
            
        Returns:
            Dict: Processing result with validated binary blocks
        """
        # Validate binary input
        if not self.data_converter.validate_binary(binary_str.replace(' ', '')):
            raise ValueError("Invalid binary input: contains non-binary characters")
        
        # Convert to blocks
        data_blocks = self.data_converter.binary_to_blocks(binary_str, 8)
        
        # Format for display
        formatted_binary = self.data_converter.format_binary_display(data_blocks)
        
        return {
            'data_blocks': data_blocks,
            'binary_representation': data_blocks,
            'formatted_binary': formatted_binary,
            'conversion_info': {
                'original_input': binary_str,
                'total_bits': len(binary_str.replace(' ', '')),
                'block_count': len(data_blocks),
                'processing_method': 'binary_validation_and_blocking'
            },
            'processing_method': 'binary_to_blocks'
        }
    
    def _get_educational_notes(self, package: Dict) -> List[str]:
        """
        Generate educational notes for the current package.
        
        Args:
            package (Dict): Transmission package
            
        Returns:
            List[str]: List of educational notes
        """
        notes = []
        
        if package['input_type'] == 'text':
            notes.append(f"Each character in '{package['original_input']}' is converted to its 8-bit ASCII binary representation.")
            notes.append(f"Total of {package['total_blocks']} blocks were created, each containing 8 bits.")
        else:
            notes.append(f"Binary input was validated and divided into {package['total_blocks']} blocks of 8 bits each.")
        
        notes.append(f"LRC (Longitudinal Redundancy Check) is calculated by XORing all data blocks together.")
        notes.append(f"The final LRC byte '{package['lrc_byte']}' will be used at the receiver to detect transmission errors.")
        notes.append(f"If any bit changes during transmission, the recalculated LRC will differ from the transmitted LRC.")
        
        return notes