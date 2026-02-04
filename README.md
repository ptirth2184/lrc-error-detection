# LRC Error Detection System

An interactive educational web application that demonstrates **Longitudinal Redundancy Check (LRC)** for error detection in data transmission. Built for Computer Networks students to understand how error detection works through hands-on experimentation.

## 🎯 Overview

This Streamlit-based application provides a complete simulation of the LRC error detection process, from data input through transmission simulation to error verification. Students can experiment with different types of data, inject various error patterns, and observe how LRC detects transmission errors.

## ✨ Features

### 📝 Data Input & Processing
- **Text Input**: Convert ASCII text to 8-bit binary representation
- **Binary Input**: Direct binary data input with validation
- **Live Preview**: Real-time conversion and validation feedback
- **Example Data**: Quick-start examples for both text and binary input

### 🧮 LRC Calculation
- **Step-by-Step Visualization**: See each XOR operation in the LRC calculation
- **Educational Explanations**: Understand the mathematical process behind LRC
- **Visual Block Representation**: Clear display of data blocks and parity bytes
- **Interactive Learning**: XOR truth tables and concept explanations

### 📡 Transmission Simulation
- **Normal Transmission**: Simulate error-free data transmission
- **Manual Error Injection**: Select specific bits to corrupt
- **Random Error Injection**: Configurable error rates for realistic simulation
- **Burst Error Simulation**: Consecutive bit errors (interference simulation)
- **Transmission Logging**: Complete log of all transmission events

### 🔍 Error Detection & Verification
- **LRC Verification**: Recalculate and compare LRC values
- **Visual Error Highlighting**: See exactly which bits were corrupted
- **Comprehensive Analysis**: Detailed breakdown of error patterns
- **Educational Insights**: Learn about LRC capabilities and limitations
- **Results Export**: Download verification reports

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd lrc-error-detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The application will automatically open in your default browser
   - If not, navigate to `http://localhost:8501`

## 📚 How to Use

### Step 1: Data Input
1. Choose input type (Text or Binary)
2. Enter your data or use provided examples
3. Click "Process Input" to convert and validate

### Step 2: LRC Generation
1. Review your processed data blocks
2. Click "Generate LRC" to calculate the parity byte
3. Explore the step-by-step calculation process

### Step 3: Transmission Simulation
1. Choose transmission type:
   - **Normal**: Error-free transmission
   - **Manual Errors**: Select specific bits to corrupt
   - **Random Errors**: Set error rate percentage
   - **Burst Errors**: Simulate interference patterns
2. Click "Transmit" to send data with or without errors

### Step 4: Verification
1. Click "Verify Data Integrity" to check for errors
2. Explore detailed results across multiple tabs:
   - Summary of verification results
   - Data comparison (original vs received)
   - LRC verification details
   - Error analysis and educational content
   - Recommendations for further learning

## 🏗️ Project Structure

```
lrc-error-detection/
├── app.py                          # Main Streamlit application
├── modules/                        # Core application modules
│   ├── data_converter.py          # Text/binary conversion utilities
│   ├── lrc_calculator.py          # LRC calculation engine
│   ├── sender_module.py           # Sender-side operations
│   ├── receiver_module.py         # Receiver-side operations
│   ├── transmission_simulator.py  # Network transmission simulation
│   └── error_injector.py          # Error injection utilities
├── tests/                          # Comprehensive test suite
│   ├── property/                   # Property-based tests
│   ├── integration/                # Integration tests
│   └── conftest.py                # Test configuration
├── requirements.txt                # Python dependencies
└── README.md                      # This file
```

## 🧪 Testing

The project includes comprehensive testing with property-based tests to ensure correctness:

```bash
# Run all tests
python -m pytest tests/ -v

# Run property-based tests only
python -m pytest tests/property/ -v

# Run integration tests
python -m pytest tests/integration/ -v
```

## 📖 Educational Content

### Learning Objectives
- Understand binary data representation in computer networks
- Learn XOR-based parity calculation methods
- Observe error detection capabilities and limitations
- Explore realistic network transmission scenarios
- Gain hands-on experience with error detection codes

### Key Concepts Covered
- **ASCII to Binary Conversion**: How text becomes binary data
- **XOR Operations**: Mathematical foundation of LRC
- **Parity Calculation**: Step-by-step LRC generation
- **Error Detection**: How LRC identifies transmission errors
- **Network Simulation**: Realistic transmission scenarios
- **Error Patterns**: Single-bit, multi-bit, and burst errors

### LRC Capabilities & Limitations
- ✅ **Detects**: Single-bit errors, odd-number bit errors
- ✅ **Simple**: Easy to understand and implement
- ❌ **Limitations**: Some even-number bit errors may go undetected
- ❌ **No Correction**: Can only detect, not correct errors

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Hypothesis**: Property-based testing
- **Pytest**: Testing framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations

### Architecture Highlights
- **Modular Design**: Separate concerns for maintainability
- **Property-Based Testing**: Ensures correctness across input ranges
- **Educational Focus**: Every component includes learning materials
- **Interactive UI**: Streamlit-based responsive interface
- **Comprehensive Logging**: Track all operations for debugging

## 🎓 For Educators

This tool is designed for Computer Networks courses and can be used for:

- **Classroom Demonstrations**: Live error detection examples
- **Lab Exercises**: Hands-on student experimentation
- **Assignment Projects**: Extend functionality or analyze results
- **Concept Reinforcement**: Visual learning of abstract concepts

### Suggested Exercises
1. Compare LRC detection rates for different error patterns
2. Analyze why certain error combinations go undetected
3. Experiment with different block sizes (code modification)
4. Research and compare with other error detection methods

## 🤝 Contributing

This is an educational project. Contributions that enhance learning value are welcome:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is created for educational purposes. Feel free to use and modify for learning and teaching.

## 🙋‍♂️ Support

For questions or issues:
1. Check the educational explanations within the app
2. Review the comprehensive test suite for examples
3. Examine the modular code structure for implementation details

## 🔗 Related Topics

To deepen your understanding of error detection and correction:
- Cyclic Redundancy Check (CRC)
- Hamming Codes
- Reed-Solomon Codes
- Forward Error Correction (FEC)
- Network Protocol Error Handling

---

**Built with ❤️ for Computer Networks Education**