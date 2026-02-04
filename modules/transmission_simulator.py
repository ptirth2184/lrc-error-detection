"""
Transmission Simulator Module for LRC Error Detection System

This module simulates network transmission with data integrity preservation
and provides educational visualization of the transmission process.

Educational Purpose:
- Demonstrates how data is transmitted over networks
- Shows the concept of data integrity during transmission
- Provides realistic simulation with transmission logs
"""

from typing import Dict, List
import time
import copy
from datetime import datetime


class TransmissionSimulator:
    """
    Simulates network transmission with data integrity preservation.
    
    This class provides methods to simulate sending data over a network,
    maintaining data integrity during normal transmission, and tracking
    transmission events for educational display.
    """
    
    def __init__(self):
        """Initialize the Transmission Simulator"""
        self.transmission_log = []
        self.transmission_count = 0
    
    def transmit_data(self, transmission_package: Dict) -> Dict:
        """
        Simulate network transmission with data integrity preservation.
        
        This method simulates sending a transmission package over a network,
        preserving all data during normal transmission and providing
        educational visualization of the process.
        
        Args:
            transmission_package (Dict): Package containing data blocks and LRC
            
        Returns:
            Dict: Received transmission package with transmission metadata
            
        Example:
            >>> simulator = TransmissionSimulator()
            >>> package = {
            ...     'data_blocks': ['01001000', '01100101'],
            ...     'lrc_byte': '00101101',
            ...     'original_input': 'He'
            ... }
            >>> received = simulator.transmit_data(package)
        """
        if not transmission_package:
            raise ValueError("Transmission package cannot be empty")
        
        # Validate required fields
        required_fields = ['data_blocks', 'lrc_byte']
        for field in required_fields:
            if field not in transmission_package:
                raise ValueError(f"Missing required field: {field}")
        
        self.transmission_count += 1
        transmission_start = datetime.now()
        
        # Log transmission start
        self._log_event("TRANSMISSION_START", f"Starting transmission #{self.transmission_count}")
        
        # Simulate transmission delay (for educational effect)
        self._simulate_transmission_delay()
        
        # Create received package (deep copy to preserve original)
        received_package = copy.deepcopy(transmission_package)
        
        # Add transmission metadata
        received_package.update({
            'transmission_id': self.transmission_count,
            'transmission_time': transmission_start,
            'received_time': datetime.now(),
            'transmission_status': 'SUCCESS',
            'errors_injected': False,
            'error_positions': [],
            'transmission_log_entry': len(self.transmission_log)
        })
        
        # Log successful transmission
        self._log_event("TRANSMISSION_SUCCESS", 
                       f"Data transmitted successfully. Blocks: {len(received_package['data_blocks'])}, LRC: {received_package['lrc_byte']}")
        
        # Log data integrity
        self._log_event("DATA_INTEGRITY", "All data blocks and LRC preserved during transmission")
        
        return received_package
    
    def get_transmission_log(self) -> List[str]:
        """
        Get transmission log for educational visualization.
        
        Returns:
            List[str]: List of transmission log entries
        """
        return self.transmission_log.copy()
    
    def clear_transmission_log(self):
        """Clear the transmission log"""
        self.transmission_log.clear()
        self.transmission_count = 0
    
    def get_transmission_statistics(self) -> Dict:
        """
        Get transmission statistics for educational display.
        
        Returns:
            Dict: Statistics about transmissions performed
        """
        return {
            'total_transmissions': self.transmission_count,
            'log_entries': len(self.transmission_log),
            'last_transmission': self.transmission_log[-1] if self.transmission_log else None
        }
    
    def simulate_network_conditions(self, package: Dict, 
                                  latency_ms: int = 100, 
                                  bandwidth_kbps: int = 1000) -> Dict:
        """
        Simulate realistic network conditions during transmission.
        
        This method adds realistic network simulation including latency
        and bandwidth considerations for educational purposes.
        
        Args:
            package (Dict): Transmission package
            latency_ms (int): Network latency in milliseconds
            bandwidth_kbps (int): Network bandwidth in kbps
            
        Returns:
            Dict: Package with network simulation metadata
        """
        # Calculate transmission time based on data size and bandwidth
        data_size_bits = 0
        if 'data_blocks' in package:
            data_size_bits = sum(len(block) for block in package['data_blocks'])
        if 'lrc_byte' in package:
            data_size_bits += len(package['lrc_byte'])
        
        # Calculate transmission time (simplified)
        transmission_time_ms = (data_size_bits / bandwidth_kbps) + latency_ms
        
        # Log network conditions
        self._log_event("NETWORK_CONDITIONS", 
                       f"Simulating network: {latency_ms}ms latency, {bandwidth_kbps}kbps bandwidth")
        self._log_event("TRANSMISSION_TIME", 
                       f"Estimated transmission time: {transmission_time_ms:.2f}ms for {data_size_bits} bits")
        
        # Simulate the calculated transmission time
        time.sleep(transmission_time_ms / 1000.0)  # Convert to seconds
        
        # Add network metadata to package
        enhanced_package = copy.deepcopy(package)
        enhanced_package.update({
            'network_latency_ms': latency_ms,
            'network_bandwidth_kbps': bandwidth_kbps,
            'data_size_bits': data_size_bits,
            'transmission_time_ms': transmission_time_ms
        })
        
        return enhanced_package
    
    def validate_transmission_package(self, package: Dict) -> bool:
        """
        Validate that a transmission package has all required components.
        
        Args:
            package (Dict): Package to validate
            
        Returns:
            bool: True if package is valid, False otherwise
        """
        if not isinstance(package, dict):
            return False
        
        # Check required fields
        required_fields = ['data_blocks', 'lrc_byte']
        for field in required_fields:
            if field not in package:
                return False
        
        # Validate data blocks
        if not isinstance(package['data_blocks'], list):
            return False
        
        if not package['data_blocks']:  # Empty list
            return False
        
        # Validate each data block is binary string
        for block in package['data_blocks']:
            if not isinstance(block, str):
                return False
            if not all(bit in '01' for bit in block):
                return False
        
        # Validate LRC byte
        lrc_byte = package['lrc_byte']
        if not isinstance(lrc_byte, str):
            return False
        if not all(bit in '01' for bit in lrc_byte):
            return False
        
        return True
    
    def _simulate_transmission_delay(self):
        """Simulate realistic transmission delay for educational effect"""
        # Small delay to simulate network transmission
        time.sleep(0.1)  # 100ms delay
    
    def _log_event(self, event_type: str, message: str):
        """
        Log a transmission event with timestamp.
        
        Args:
            event_type (str): Type of event
            message (str): Event message
        """
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Include milliseconds
        log_entry = f"[{timestamp}] {event_type}: {message}"
        self.transmission_log.append(log_entry)
    
    def get_transmission_visualization_data(self, package: Dict) -> Dict:
        """
        Get data formatted for transmission visualization in the UI.
        
        Args:
            package (Dict): Transmission package
            
        Returns:
            Dict: Visualization data for UI display
        """
        if not self.validate_transmission_package(package):
            return {'error': 'Invalid transmission package'}
        
        return {
            'sender_data': {
                'data_blocks': package['data_blocks'],
                'lrc_byte': package['lrc_byte'],
                'total_bits': sum(len(block) for block in package['data_blocks']) + len(package['lrc_byte']),
                'block_count': len(package['data_blocks'])
            },
            'transmission_info': {
                'transmission_id': getattr(package, 'transmission_id', 'N/A'),
                'status': 'READY_TO_TRANSMIT',
                'timestamp': datetime.now().isoformat()
            },
            'network_path': [
                {'node': 'Sender', 'status': 'ready'},
                {'node': 'Network', 'status': 'waiting'},
                {'node': 'Receiver', 'status': 'waiting'}
            ]
        }