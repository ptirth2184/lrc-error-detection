"""
Test configuration and fixtures for LRC Error Detection System tests.

This module provides common test fixtures and configuration for unit tests,
property-based tests, and integration tests.
"""

import pytest
import sys
import os

# Add the parent directory to Python path for module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_text_data():
    """Fixture providing sample text data for testing"""
    return "Hello"

@pytest.fixture
def sample_binary_data():
    """Fixture providing sample binary data for testing"""
    return "0100100001100101011011000110110001101111"

@pytest.fixture
def sample_data_blocks():
    """Fixture providing sample data blocks for LRC testing"""
    return [
        "01001000",  # H
        "01100101",  # e
        "01101100",  # l
        "01101100",  # l
        "01101111"   # o
    ]

@pytest.fixture
def expected_lrc():
    """Fixture providing expected LRC for sample data blocks"""
    # XOR of all sample_data_blocks
    return "00000100"