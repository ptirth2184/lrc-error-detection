"""
LRC Error Detection System - Main Streamlit Application

This educational web application demonstrates Longitudinal Redundancy Check (LRC)
for error detection in data transmission. Students can input data, observe LRC
calculation, simulate transmission with error injection, and verify error detection.

Usage: streamlit run app.py
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="LRC Error Detection System",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔍 LRC Error Detection System")
    st.markdown("""
    ### Educational Tool for Computer Networks
    
    This interactive application demonstrates **Longitudinal Redundancy Check (LRC)** 
    for error detection in data transmission. Learn how LRC works through hands-on 
    experimentation with data encoding, transmission simulation, and error detection.
    
    **Getting Started:**
    1. Enter your data (text or binary)
    2. Generate LRC checksum
    3. Simulate transmission
    4. Inject errors (optional)
    5. Verify data integrity
    """)
    
    # Placeholder for main application logic
    st.info("🚧 Application modules are being implemented. Please check back soon!")
    
    # Educational sidebar
    with st.sidebar:
        st.header("📚 About LRC")
        st.markdown("""
        **Longitudinal Redundancy Check (LRC)** is an error detection method that:
        
        - Divides data into fixed-size blocks
        - Computes a parity byte using XOR operations
        - Detects single-bit and some multi-bit errors
        - Provides simple but effective error detection
        
        **Learning Objectives:**
        - Understand binary data representation
        - Learn XOR-based parity calculation
        - Observe error detection capabilities
        - Explore transmission simulation
        """)

if __name__ == "__main__":
    main()