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
            format_func=lambda x: "Text Input" if x == "text" else "Binary Input",
            help="Choose whether to input text (converted to binary) or direct binary data"
        )
    
    with col2:
        if input_type == "text":
            user_input = st.text_input(
                "Enter text data:",
                placeholder="e.g., Hello World",
                help="Enter any text. Each character will be converted to 8-bit ASCII binary.",
                max_chars=50
            )
            
            # Show live preview of binary conversion
            if user_input:
                st.write("**Live Preview:**")
                preview_binary = []
                for char in user_input[:10]:  # Limit preview to first 10 chars
                    binary = format(ord(char), '08b')
                    preview_binary.append(f"{char} → {binary}")
                
                preview_text = " | ".join(preview_binary)
                if len(user_input) > 10:
                    preview_text += " | ..."
                st.code(preview_text, language=None)
        else:
            user_input = st.text_area(
                "Enter binary data:",
                placeholder="e.g., 01001000 01100101 01101100 01101100 01101111",
                help="Enter binary data (0s and 1s). Spaces are allowed and will be removed.",
                height=100
            )
            
            # Show live validation
            if user_input:
                clean_binary = user_input.replace(' ', '').replace('\n', '')
                is_valid = all(bit in '01' for bit in clean_binary)
                
                if is_valid:
                    st.success(f"✅ Valid binary input ({len(clean_binary)} bits)")
                    if len(clean_binary) % 8 != 0:
                        padding_needed = 8 - (len(clean_binary) % 8)
                        st.info(f"ℹ️ Will be padded with {padding_needed} zeros to complete the last block")
                else:
                    st.error("❌ Invalid binary input - only 0s and 1s are allowed")
    
    # Input examples
    with st.expander("💡 Input Examples", expanded=False):
        st.write("**Text Examples:**")
        example_texts = ["Hi", "Test", "ABC123", "Hello World"]
        example_cols = st.columns(len(example_texts))
        
        for i, (col, example) in enumerate(zip(example_cols, example_texts)):
            with col:
                if st.button(f'"{example}"', key=f"text_example_{i}"):
                    st.session_state.example_input = example
                    st.session_state.example_type = "text"
                    st.rerun()
        
        st.write("**Binary Examples:**")
        binary_examples = [
            ("Hi", "0100100001101001"),
            ("AB", "0100000101000010"),
            ("123", "001100010011001000110011")
        ]
        
        for label, binary in binary_examples:
            if st.button(f'{label} → {binary}', key=f"binary_example_{label}"):
                st.session_state.example_input = binary
                st.session_state.example_type = "binary"
                st.rerun()
    
    # Handle example selection
    if hasattr(st.session_state, 'example_input'):
        user_input = st.session_state.example_input
        input_type = st.session_state.example_type
        # Clear the example from session state
        del st.session_state.example_input
        del st.session_state.example_type
    
    # Process input button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        process_button = st.button(
            "🚀 Process Input", 
            type="primary", 
            disabled=not user_input,
            use_container_width=True
        )
    
    if process_button:
        try:
            with st.spinner("Processing input..."):
                # Process the input
                result = st.session_state.sender.process_input(user_input, input_type)
                
                # Show processing results
                st.success("✅ Input processed successfully!")
                
                # Display conversion results in tabs
                tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔢 Conversion Details", "📋 Data Blocks"])
                
                with tab1:
                    # Summary metrics
                    if input_type == "text":
                        conversion_info = result['conversion_info']
                        
                        metric_cols = st.columns(4)
                        with metric_cols[0]:
                            st.metric("Original Text", f'"{conversion_info["original_text"]}"')
                        with metric_cols[1]:
                            st.metric("Characters", conversion_info['character_count'])
                        with metric_cols[2]:
                            st.metric("Total Bits", conversion_info['total_bits'])
                        with metric_cols[3]:
                            st.metric("Data Blocks", len(result['data_blocks']))
                    else:
                        clean_input = user_input.replace(' ', '').replace('\n', '')
                        metric_cols = st.columns(4)
                        with metric_cols[0]:
                            st.metric("Input Type", "Binary")
                        with metric_cols[1]:
                            st.metric("Input Bits", len(clean_input))
                        with metric_cols[2]:
                            st.metric("Processed Bits", sum(len(block) for block in result['data_blocks']))
                        with metric_cols[3]:
                            st.metric("Data Blocks", len(result['data_blocks']))
                
                with tab2:
                    if input_type == "text":
                        # Show character-to-binary conversion table
                        conversion_info = result['conversion_info']
                        st.write("**Character-to-Binary Conversion:**")
                        
                        conversion_data = []
                        for item in conversion_info['conversion_table']:
                            conversion_data.append({
                                'Position': item['position'],
                                'Character': f"'{item['character']}'",
                                'ASCII Code': item['ascii_value'],
                                'Binary (8-bit)': item['binary'],
                                'Decimal Check': int(item['binary'], 2)
                            })
                        
                        st.dataframe(conversion_data, use_container_width=True, hide_index=True)
                        
                        # Show formatted binary string
                        st.write("**Complete Binary String:**")
                        formatted_binary = result['formatted_binary']
                        st.code(formatted_binary, language=None)
                        
                    else:
                        # Show binary processing details
                        st.write("**Binary Processing Details:**")
                        st.write(f"**Original Input:** `{user_input}`")
                        st.write(f"**Cleaned Binary:** `{user_input.replace(' ', '').replace('\\n', '')}`")
                        st.write(f"**Formatted Output:** `{result['formatted_binary']}`")
                        
                        if len(user_input.replace(' ', '').replace('\n', '')) % 8 != 0:
                            st.info("ℹ️ Input was padded with zeros to create complete 8-bit blocks")
                
                with tab3:
                    # Show data blocks table
                    st.write("**Data Blocks for LRC Calculation:**")
                    blocks_data = []
                    for i, block in enumerate(result['data_blocks']):
                        decimal_val = int(block, 2)
                        char_repr = chr(decimal_val) if 32 <= decimal_val <= 126 else '·'
                        
                        blocks_data.append({
                            'Block #': i + 1,
                            'Binary (8-bit)': block,
                            'Decimal Value': decimal_val,
                            'Character': char_repr,
                            'Hex': f"0x{decimal_val:02X}"
                        })
                    
                    st.dataframe(blocks_data, use_container_width=True, hide_index=True)
                    
                    # Show XOR truth table for reference
                    with st.expander("📚 XOR Truth Table Reference"):
                        st.write("LRC calculation uses XOR (Exclusive OR) operations:")
                        truth_table = [
                            {"A": "0", "B": "0", "A ⊕ B": "0"},
                            {"A": "0", "B": "1", "A ⊕ B": "1"},
                            {"A": "1", "B": "0", "A ⊕ B": "1"},
                            {"A": "1", "B": "1", "A ⊕ B": "0"}
                        ]
                        st.dataframe(truth_table, hide_index=True)
                
                # Move to next phase
                st.session_state.current_phase = 'calculate'
                
                # Auto-advance after showing results
                st.balloons()
                st.info("🎉 Ready to calculate LRC! Click the button below to continue.")
                
                if st.button("➡️ Continue to LRC Generation", type="secondary"):
                    st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error processing input: {str(e)}")
            st.write("**Debug Info:**")
            st.write(f"Input: `{user_input}`")
            st.write(f"Type: `{input_type}`")


def show_calculate_phase():
    """Show LRC calculation interface"""
    st.header("🧮 Step 2: LRC Generation")
    
    # Show current data summary
    processing_history = st.session_state.sender.get_processing_history()
    if processing_history:
        latest = processing_history[-1]
        
        # Quick summary of input data
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        with summary_col1:
            st.info(f"**Input:** {latest['input'][:20]}{'...' if len(latest['input']) > 20 else ''}")
        with summary_col2:
            st.info(f"**Type:** {latest['type'].title()}")
        with summary_col3:
            blocks_count = len(latest['result']['data_blocks'])
            st.info(f"**Blocks:** {blocks_count}")
    
    # Check if LRC has been calculated
    current_package = st.session_state.sender.get_current_package()
    if not current_package:
        st.write("📋 Ready to generate LRC from your processed data.")
        
        # Show what will happen
        with st.expander("🔍 What happens during LRC calculation?", expanded=True):
            st.write("""
            **LRC (Longitudinal Redundancy Check) Calculation Process:**
            
            1. **Initialize:** Start with LRC = 00000000
            2. **XOR Operations:** For each data block, perform: LRC = LRC ⊕ Block
            3. **Result:** Final LRC byte serves as error detection code
            4. **Transmission:** LRC is sent along with data blocks
            5. **Verification:** Receiver recalculates LRC to detect errors
            """)
        
        # Generate LRC button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔢 Generate LRC", type="primary", use_container_width=True):
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
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "📋 Data Blocks", "🔢 LRC Steps", "📚 Educational"])
        
        with tab1:
            # Summary metrics
            st.subheader("📊 Transmission Package Summary")
            
            metric_cols = st.columns(5)
            with metric_cols[0]:
                st.metric("Input Type", viz_data['summary_stats']['Input Type'])
            with metric_cols[1]:
                st.metric("Total Blocks", viz_data['summary_stats']['Total Blocks'])
            with metric_cols[2]:
                st.metric("Total Bits", viz_data['summary_stats']['Total Bits'])
            with metric_cols[3]:
                st.metric("LRC Byte", viz_data['summary_stats']['LRC Byte'])
            with metric_cols[4]:
                st.metric("LRC Decimal", viz_data['summary_stats']['LRC Decimal'])
            
            # Package metadata
            st.subheader("📦 Package Information")
            metadata_cols = st.columns(2)
            
            with metadata_cols[0]:
                for key, value in list(viz_data['package_metadata'].items())[:2]:
                    st.write(f"**{key}:** {value}")
            
            with metadata_cols[1]:
                for key, value in list(viz_data['package_metadata'].items())[2:]:
                    st.write(f"**{key}:** {value}")
        
        with tab2:
            # Data blocks table with enhanced information
            st.subheader("📋 Data Blocks")
            st.dataframe(viz_data['data_blocks_table'], use_container_width=True, hide_index=True)
            
            # Visual representation
            st.subheader("🎨 Visual Block Representation")
            blocks = viz_data['data_blocks_table']
            
            # Create visual blocks
            visual_cols = st.columns(min(len(blocks), 8))  # Max 8 columns
            for i, (col, block) in enumerate(zip(visual_cols, blocks)):
                with col:
                    st.markdown(f"""
                    <div style='border: 2px solid #1f77b4; border-radius: 5px; padding: 10px; text-align: center; margin: 5px;'>
                        <strong>Block {i+1}</strong><br>
                        <code>{block['Binary']}</code><br>
                        <small>'{block['Character']}'</small><br>
                        <small>Dec: {block['Decimal']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                if i >= 7:  # Show max 8 blocks visually
                    break
            
            if len(blocks) > 8:
                st.write(f"... and {len(blocks) - 8} more blocks")
        
        with tab3:
            # LRC calculation steps
            st.subheader("🔢 LRC Calculation Steps")
            
            if viz_data['lrc_calculation_steps']:
                # Show step-by-step calculation
                st.dataframe(viz_data['lrc_calculation_steps'], use_container_width=True, hide_index=True)
                
                # Show visual step-by-step process
                st.subheader("👁️ Visual Step Process")
                
                steps = viz_data['lrc_calculation_steps']
                for i, step in enumerate(steps):
                    step_col1, step_col2, step_col3 = st.columns([1, 2, 1])
                    
                    with step_col1:
                        st.write(f"**Step {step['Step']}**")
                    
                    with step_col2:
                        if 'XOR' in step['Operation']:
                            st.code(step['Operation'], language=None)
                        else:
                            st.write(step['Operation'])
                    
                    with step_col3:
                        st.code(step['Result'], language=None)
                    
                    if i < len(steps) - 1:  # Don't show arrow after last step
                        st.markdown("⬇️", help="Next step")
                
                # Final result highlight
                final_lrc = viz_data['summary_stats']['LRC Byte']
                st.success(f"🎯 **Final LRC Result: {final_lrc}** (Decimal: {int(final_lrc, 2)})")
            
        with tab4:
            # Educational content
            st.subheader("📚 Educational Notes")
            for i, note in enumerate(viz_data['educational_notes'], 1):
                st.write(f"{i}. {note}")
            
            # Additional educational content
            st.subheader("🧠 Key Concepts")
            
            concept_tabs = st.tabs(["XOR Properties", "Error Detection", "Limitations"])
            
            with concept_tabs[0]:
                st.write("""
                **XOR (Exclusive OR) Properties:**
                - **Commutative:** A ⊕ B = B ⊕ A
                - **Associative:** (A ⊕ B) ⊕ C = A ⊕ (B ⊕ C)
                - **Identity:** A ⊕ 0 = A
                - **Self-inverse:** A ⊕ A = 0
                
                These properties make XOR ideal for error detection calculations.
                """)
            
            with concept_tabs[1]:
                st.write("""
                **How LRC Detects Errors:**
                - Single-bit errors: Always detected
                - Two-bit errors in same position: Always detected
                - Odd number of bit errors: Always detected
                - Some even number of bit errors: May not be detected
                
                LRC provides good error detection for common transmission errors.
                """)
            
            with concept_tabs[2]:
                st.write("""
                **LRC Limitations:**
                - Cannot detect all even-number bit errors
                - Cannot correct errors (only detect)
                - Burst errors spanning multiple blocks may not be detected
                - More sophisticated codes (like CRC) provide better detection
                
                Despite limitations, LRC is simple and effective for many applications.
                """)
        
        # Navigation buttons
        st.divider()
        nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
        
        with nav_col1:
            if st.button("⬅️ Back to Input", type="secondary"):
                st.session_state.current_phase = 'input'
                st.rerun()
        
        with nav_col3:
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