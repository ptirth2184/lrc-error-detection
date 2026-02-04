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
from datetime import datetime

# Add the current directory to Python path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.sender_module import SenderModule
from modules.receiver_module import ReceiverModule
from modules.transmission_simulator import TransmissionSimulator
from modules.error_injector import ErrorInjector


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'sender' not in st.session_state:
        st.session_state.sender = SenderModule()
    
    if 'receiver' not in st.session_state:
        st.session_state.receiver = ReceiverModule()
    
    if 'simulator' not in st.session_state:
        st.session_state.simulator = TransmissionSimulator()
    
    if 'injector' not in st.session_state:
        st.session_state.injector = ErrorInjector()
    
    if 'current_phase' not in st.session_state:
        st.session_state.current_phase = 'input'
    
    if 'transmission_package' not in st.session_state:
        st.session_state.transmission_package = None
    
    if 'received_package' not in st.session_state:
        st.session_state.received_package = None
    
    if 'verification_result' not in st.session_state:
        st.session_state.verification_result = None


def create_sidebar():
    """Create educational sidebar with LRC information"""
    with st.sidebar:
        st.header("📚 About LRC")
        
        st.markdown("""
        **Longitudinal Redundancy Check (LRC)** is an error detection method that:
        
        - Divides data into fixed-size blocks
        - Computes a parity byte using XOR operations
        - Detects single-bit and some multi-bit errors
        - Provides simple but effective error detection
        """)
        
        st.subheader("🎯 Learning Objectives")
        st.markdown("""
        - Understand binary data representation
        - Learn XOR-based parity calculation
        - Observe error detection capabilities
        - Explore transmission simulation
        """)
        
        st.subheader("🔄 Workflow Phases")
        phases = {
            'input': '1️⃣ Data Input',
            'calculate': '2️⃣ LRC Generation',
            'transmit': '3️⃣ Transmission',
            'verify': '4️⃣ Verification'
        }
        
        for phase_key, phase_name in phases.items():
            if st.session_state.current_phase == phase_key:
                st.markdown(f"**{phase_name}** ← Current")
            else:
                st.markdown(phase_name)
        
        st.divider()
        
        # Reset button
        if st.button("🔄 Reset Application", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def create_progress_indicator():
    """Create progress indicator for the workflow"""
    phases = ['Input', 'Generate LRC', 'Transmit', 'Verify']
    phase_mapping = {
        'input': 0,
        'calculate': 1,
        'transmit': 2,
        'verify': 3
    }
    
    current_step = phase_mapping.get(st.session_state.current_phase, 0)
    
    # Create progress bar
    progress = (current_step + 1) / len(phases)
    st.progress(progress, text=f"Step {current_step + 1} of {len(phases)}: {phases[current_step]}")
    
    # Create step indicators
    cols = st.columns(len(phases))
    for i, (col, phase) in enumerate(zip(cols, phases)):
        with col:
            if i <= current_step:
                st.markdown(f"✅ **{phase}**")
            else:
                st.markdown(f"⏳ {phase}")


def show_educational_info():
    """Show educational information about the current phase"""
    phase_info = {
        'input': {
            'title': '📝 Data Input Phase',
            'description': 'Enter your data (text or binary) to begin the LRC demonstration.',
            'tips': [
                'Text input will be converted to 8-bit ASCII binary',
                'Binary input should contain only 0s and 1s',
                'Each character becomes one 8-bit data block'
            ]
        },
        'calculate': {
            'title': '🧮 LRC Calculation Phase',
            'description': 'Generate the LRC parity byte using XOR operations.',
            'tips': [
                'LRC is calculated by XORing all data blocks',
                'Each step of the calculation is shown',
                'The result is an 8-bit parity byte'
            ]
        },
        'transmit': {
            'title': '📡 Transmission Phase',
            'description': 'Simulate data transmission over a network.',
            'tips': [
                'Data blocks and LRC are transmitted together',
                'Errors can be injected to simulate transmission problems',
                'Real networks can introduce various types of errors'
            ]
        },
        'verify': {
            'title': '🔍 Verification Phase',
            'description': 'Verify data integrity using LRC error detection.',
            'tips': [
                'Receiver recalculates LRC from received data',
                'Compares calculated vs received LRC',
                'Detects errors if LRC values differ'
            ]
        }
    }
    
    info = phase_info.get(st.session_state.current_phase, phase_info['input'])
    
    with st.expander(f"ℹ️ {info['title']}", expanded=False):
        st.write(info['description'])
        st.write("**Tips:**")
        for tip in info['tips']:
            st.write(f"• {tip}")


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="LRC Error Detection System",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Create sidebar
    create_sidebar()
    
    # Main header
    st.title("🔍 LRC Error Detection System")
    st.markdown("""
    ### Educational Tool for Computer Networks
    
    This interactive application demonstrates **Longitudinal Redundancy Check (LRC)** 
    for error detection in data transmission. Learn how LRC works through hands-on 
    experimentation with data encoding, transmission simulation, and error detection.
    """)
    
    # Progress indicator
    create_progress_indicator()
    
    # Educational information
    show_educational_info()
    
    st.divider()
    
    # Main content area based on current phase
    if st.session_state.current_phase == 'input':
        show_input_phase()
    elif st.session_state.current_phase == 'calculate':
        show_calculate_phase()
    elif st.session_state.current_phase == 'transmit':
        show_transmit_phase()
    elif st.session_state.current_phase == 'verify':
        show_verify_phase()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
    LRC Error Detection System - Educational Tool for Computer Networks<br>
    Built with Streamlit • Python • Educational Purpose
    </div>
    """, unsafe_allow_html=True)


def show_input_phase():
    """Show data input interface"""
    st.header("📝 Step 1: Data Input")
    
    # Input type selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        input_type = st.radio(
            "Select input type:",
            ["text", "binary"],
            format_func=lambda x: "Text Input" if x == "text" else "Binary Input"
        )
    
    with col2:
        if input_type == "text":
            user_input = st.text_input(
                "Enter text data:",
                placeholder="e.g., Hello World",
                help="Enter any text. Each character will be converted to 8-bit binary."
            )
        else:
            user_input = st.text_area(
                "Enter binary data:",
                placeholder="e.g., 01001000 01100101 01101100 01101100 01101111",
                help="Enter binary data (0s and 1s). Spaces are allowed and will be removed."
            )
    
    # Process input button
    if st.button("🚀 Process Input", type="primary", disabled=not user_input):
        try:
            with st.spinner("Processing input..."):
                # Process the input
                result = st.session_state.sender.process_input(user_input, input_type)
                
                # Show processing results
                st.success("✅ Input processed successfully!")
                
                # Display conversion results
                st.subheader("📊 Conversion Results")
                
                if input_type == "text":
                    # Show character-to-binary conversion
                    conversion_info = result['conversion_info']
                    
                    st.write(f"**Original Text:** {conversion_info['original_text']}")
                    st.write(f"**Character Count:** {conversion_info['character_count']}")
                    st.write(f"**Total Bits:** {conversion_info['total_bits']}")
                    
                    # Show conversion table
                    st.write("**Character-to-Binary Conversion:**")
                    conversion_data = []
                    for item in conversion_info['conversion_table']:
                        conversion_data.append({
                            'Position': item['position'],
                            'Character': item['character'],
                            'ASCII': item['ascii_value'],
                            'Binary': item['binary']
                        })
                    st.dataframe(conversion_data, use_container_width=True)
                
                else:
                    # Show binary processing results
                    st.write(f"**Original Binary:** {user_input}")
                    st.write(f"**Processed Blocks:** {len(result['data_blocks'])}")
                    st.write(f"**Total Bits:** {sum(len(block) for block in result['data_blocks'])}")
                
                # Show data blocks
                st.write("**Data Blocks:**")
                blocks_data = []
                for i, block in enumerate(result['data_blocks']):
                    blocks_data.append({
                        'Block': f"Block {i + 1}",
                        'Binary': block,
                        'Decimal': int(block, 2),
                        'Character': chr(int(block, 2)) if 32 <= int(block, 2) <= 126 else '·'
                    })
                st.dataframe(blocks_data, use_container_width=True)
                
                # Move to next phase
                st.session_state.current_phase = 'calculate'
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error processing input: {str(e)}")


def show_calculate_phase():
    """Show LRC calculation interface"""
    st.header("🧮 Step 2: LRC Generation")
    
    # Show current data
    current_package = st.session_state.sender.get_current_package()
    if not current_package:
        st.info("📋 Ready to generate LRC from your processed data.")
        
        if st.button("🔢 Generate LRC", type="primary"):
            try:
                with st.spinner("Calculating LRC..."):
                    # Generate transmission package
                    package = st.session_state.sender.generate_transmission_package()
                    st.session_state.transmission_package = package
                    
                    st.success("✅ LRC calculated successfully!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error calculating LRC: {str(e)}")
    else:
        # Show LRC calculation results
        st.success("✅ LRC has been calculated!")
        
        # Get visualization data
        viz_data = st.session_state.sender.get_visualization_data()
        
        # Show summary
        st.subheader("📊 Summary")
        summary_cols = st.columns(4)
        with summary_cols[0]:
            st.metric("Input Type", viz_data['summary_stats']['Input Type'])
        with summary_cols[1]:
            st.metric("Total Blocks", viz_data['summary_stats']['Total Blocks'])
        with summary_cols[2]:
            st.metric("Total Bits", viz_data['summary_stats']['Total Bits'])
        with summary_cols[3]:
            st.metric("LRC Byte", viz_data['summary_stats']['LRC Byte'])
        
        # Show data blocks
        st.subheader("📋 Data Blocks")
        st.dataframe(viz_data['data_blocks_table'], use_container_width=True)
        
        # Show LRC calculation steps
        st.subheader("🔢 LRC Calculation Steps")
        if viz_data['lrc_calculation_steps']:
            st.dataframe(viz_data['lrc_calculation_steps'], use_container_width=True)
        
        # Educational notes
        st.subheader("📚 Educational Notes")
        for note in viz_data['educational_notes']:
            st.write(f"• {note}")
        
        # Next phase button
        if st.button("📡 Proceed to Transmission", type="primary"):
            st.session_state.current_phase = 'transmit'
            st.rerun()


def show_transmit_phase():
    """Show transmission simulation interface"""
    st.header("📡 Step 3: Transmission Simulation")
    st.write("Placeholder for transmission interface - to be implemented in next task")


def show_verify_phase():
    """Show verification interface"""
    st.header("🔍 Step 4: Data Verification")
    st.write("Placeholder for verification interface - to be implemented in next task")


if __name__ == "__main__":
    main()