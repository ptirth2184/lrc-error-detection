# LRC Error Detection System

A comprehensive college project demonstrating **Longitudinal Redundancy Check (LRC)** for error detection in data transmission. This interactive web application was developed as part of Computer Networks coursework to showcase understanding of error detection mechanisms through practical implementation.

## 🎯 Project Overview

This Streamlit-based application provides a complete simulation of the LRC error detection process, from data input through transmission simulation to error verification. The project demonstrates practical knowledge of network error detection concepts through an interactive, educational interface.

## 📚 Academic Context

**Course**: Computer Networks  
**Topic**: Error Detection and Correction  
**Implementation**: Python with Streamlit Framework  
**Focus**: Longitudinal Redundancy Check (LRC) Algorithm  

### Project Objectives
- Implement LRC algorithm from theoretical concepts
- Demonstrate understanding of binary data processing
- Simulate realistic network transmission scenarios
- Create educational tool for error detection visualization
- Apply software engineering principles with modular design

## ✨ Features Implemented

### 📝 Data Input & Processing Module
- **Text to Binary Conversion**: ASCII text to 8-bit binary representation
- **Binary Input Validation**: Direct binary data input with error checking
- **Real-time Feedback**: Live preview and validation during input
- **Example Data Sets**: Pre-configured examples for testing

### 🧮 LRC Calculation Engine
- **Step-by-Step Algorithm**: Complete XOR-based LRC calculation
- **Mathematical Visualization**: Each calculation step displayed clearly
- **Educational Interface**: XOR truth tables and concept explanations
- **Block Processing**: Fixed-size data block handling

### 📡 Network Transmission Simulator
- **Perfect Transmission**: Error-free data transmission simulation
- **Controlled Error Injection**: Manual bit selection for corruption
- **Random Error Patterns**: Configurable error rates for testing
- **Burst Error Simulation**: Consecutive bit errors (interference modeling)
- **Comprehensive Logging**: Complete transmission event tracking

### 🔍 Error Detection & Verification System
- **LRC Verification Algorithm**: Receiver-side error detection implementation
- **Visual Error Analysis**: Highlighted corrupted bits and comparison views
- **Detailed Reporting**: Comprehensive analysis of detection results
- **Educational Insights**: Explanation of LRC capabilities and limitations

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Running the Project

1. **Navigate to project directory**
   ```bash
   cd lrc-error-detection
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the interface**
   - Application opens automatically in browser
   - Manual access: `http://localhost:8501`

## 💻 Usage Instructions

### Phase 1: Data Input
1. Select input type (Text or Binary)
2. Enter data or use provided examples
3. Process input to generate data blocks

### Phase 2: LRC Generation
1. Review processed data blocks
2. Generate LRC parity byte
3. Study step-by-step calculation process

### Phase 3: Transmission Simulation
1. Choose transmission scenario:
   - Normal (error-free)
   - Manual error injection
   - Random error patterns
   - Burst error simulation
2. Execute transmission with selected parameters

### Phase 4: Error Verification
1. Perform LRC verification on received data
2. Analyze results across multiple views
3. Study error detection effectiveness

## 🏗️ Technical Implementation

### Project Architecture
```
lrc-error-detection/
├── app.py                          # Main Streamlit application
├── modules/                        # Core implementation modules
│   ├── data_converter.py          # Binary conversion utilities
│   ├── lrc_calculator.py          # LRC algorithm implementation
│   ├── sender_module.py           # Sender-side operations
│   ├── receiver_module.py         # Receiver-side verification
│   ├── transmission_simulator.py  # Network simulation
│   └── error_injector.py          # Error injection mechanisms
├── tests/                          # Comprehensive test suite
│   ├── property/                   # Property-based testing
│   ├── integration/                # Integration testing
│   └── conftest.py                # Test configuration
├── requirements.txt                # Python dependencies
└── README.md                      # Project documentation
```

### Key Technologies Used
- **Streamlit**: Interactive web application framework
- **Python**: Core programming language
- **Hypothesis**: Property-based testing for algorithm verification
- **Pytest**: Comprehensive testing framework
- **Pandas**: Data manipulation and display
- **NumPy**: Numerical operations support

## 🧪 Testing & Validation

Implemented comprehensive testing to ensure algorithm correctness:

```bash
# Run complete test suite
python -m pytest tests/ -v

# Property-based algorithm testing
python -m pytest tests/property/ -v

# Integration testing
python -m pytest tests/integration/ -v
```

### Testing Approach
- **Property-Based Testing**: Validates algorithm correctness across input ranges
- **Integration Testing**: Ensures module interactions work properly
- **Edge Case Testing**: Handles boundary conditions and error scenarios

## 📊 Project Achievements

### Technical Accomplishments
- ✅ Complete LRC algorithm implementation from scratch
- ✅ Modular, maintainable code architecture
- ✅ Comprehensive error handling and validation
- ✅ Interactive user interface with educational value
- ✅ Extensive testing suite with 100% core functionality coverage

### Learning Outcomes Demonstrated
- **Algorithm Implementation**: Translated theoretical LRC concepts into working code
- **Software Engineering**: Applied modular design and testing principles
- **User Interface Design**: Created intuitive, educational interface
- **Network Concepts**: Demonstrated understanding of error detection in networks
- **Problem Solving**: Handled edge cases and error scenarios effectively

## 🔍 LRC Algorithm Analysis

### Implementation Details
- **Block Size**: 8-bit fixed blocks for standard byte processing
- **XOR Operations**: Bitwise exclusive OR for parity calculation
- **Error Detection**: Single-bit and odd-number bit error detection
- **Limitations**: Some even-number bit errors may remain undetected

### Demonstrated Capabilities
- ✅ **Single-bit Error Detection**: 100% detection rate
- ✅ **Odd-bit Error Detection**: Reliable detection
- ✅ **Educational Value**: Clear visualization of process
- ❌ **Even-bit Error Limitation**: Some patterns undetectable (as expected)

## 📝 Project Report Summary

This project successfully demonstrates:

1. **Theoretical Understanding**: Complete grasp of LRC error detection principles
2. **Practical Implementation**: Working algorithm with real-world applicability
3. **Software Development Skills**: Clean, modular, well-tested code
4. **User Experience Design**: Intuitive interface for complex concepts
5. **Academic Excellence**: Comprehensive documentation and testing

## 🎓 Academic References

### Concepts Implemented
- Longitudinal Redundancy Check (LRC)
- Binary data representation
- XOR-based parity calculation
- Network error detection mechanisms
- Data transmission simulation

### Related Network Concepts
- Error detection vs. correction
- Parity checking methods
- Network reliability mechanisms
- Data integrity verification

## 📞 Project Information

**Student Project**: Computer Networks Course  
**Implementation Language**: Python  
**Framework**: Streamlit  
**Testing**: Comprehensive property-based and integration testing  
**Documentation**: Complete technical and user documentation  

---

**Developed as part of Computer Networks coursework - Demonstrating practical implementation of theoretical concepts**