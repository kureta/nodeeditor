# QtNodes Python Examples

This directory contains example applications demonstrating the use of QtNodes Python bindings.

## Calculator Example

`calculator.py` - A fully functional calculator application using node-based data flow.

### Features

- **Number Source Nodes**: Input decimal numbers with validation
- **Math Operation Nodes**: Addition, subtraction, multiplication, and division
- **Display Nodes**: Show computation results
- **Data Flow**: Automatic result propagation through the node graph
- **Save/Load**: Save and load node graphs as JSON files

### Running the Example

Make sure QtNodes Python bindings are installed first:

```bash
# Build and install the bindings
cd /path/to/nodeeditor
mkdir build && cd build
cmake .. -DBUILD_PYTHON_BINDINGS=ON -DUSE_QT6=ON -DBUILD_SHARED_LIBS=ON
cmake --build .
cmake --install .
```

Then run the calculator:

```bash
python3 bindings/examples/calculator.py
```

### Usage

1. **Add Nodes**: Right-click in empty space to open the context menu
2. **Connect Nodes**: Drag from an output port (right side) to an input port (left side)
3. **Enter Numbers**: Click on Number Source nodes and type values
4. **View Results**: Results appear automatically in Display nodes
5. **Save/Load**: Use Ctrl+S to save and Ctrl+O to load scenes

### Example Calculations

You can create various calculations:

**Simple Addition:**
```
[Number: 5] → [Addition] → [Display: 12]
[Number: 7] →     ↑
```

**Complex Expression: (5 + 3) * 2**
```
[Number: 5] → [Addition] → [Multiplication] → [Display: 16]
[Number: 3] →     ↑              ↑
[Number: 2] ──────────────────→
```

**Multiple Operations:**
```
[Number: 10] → [Subtraction] → [Display: 5]
[Number: 5]  →       ↑
               
[Number: 6]  → [Division] → [Display: 3]
[Number: 2]  →     ↑
```

### Node Types

#### Sources
- **Number Source**: Editable text input for decimal numbers

#### Operators
- **Addition**: Adds two numbers
- **Subtraction**: Subtracts second input from first
- **Multiplication**: Multiplies two numbers
- **Division**: Divides first input by second (returns inf for division by zero)

#### Displays
- **Result Display**: Shows the computed result

### Code Structure

The calculator example demonstrates several key concepts:

1. **Custom Data Types**: `DecimalData` class extends `NodeData` to transfer decimal values
2. **Node Models**: Each node type extends `NodeDelegateModel`
3. **Port Configuration**: Nodes define input/output ports via `nPorts()` and `dataType()`
4. **Data Processing**: Math nodes compute results when inputs change
5. **Embedded Widgets**: Nodes can contain Qt widgets (QLineEdit, QLabel)
6. **Signal Handling**: Nodes emit signals when data changes

### Screenshot

When you run the application, you'll see:
- A node editor canvas
- Context menu for adding nodes (right-click)
- Nodes with input/output ports
- Connections showing data flow
- Live result updates as you change values

### Customization

You can extend the calculator by:

1. **Adding new operations**: Create classes extending `MathOperationModel`
2. **Adding new functions**: sqrt, power, trigonometric functions, etc.
3. **Adding constants**: Nodes that output fixed values like π or e
4. **Adding memory**: Store and recall values
5. **Adding history**: Track previous calculations

Example of adding a square root operation:

```python
class SquareRootModel(NodeDelegateModel):
    def __init__(self):
        super().__init__()
        self._number: Optional[DecimalData] = None
        self._result: Optional[DecimalData] = None
    
    def caption(self) -> str:
        return "Square Root"
    
    def name(self) -> str:
        return "SquareRoot"
    
    def nPorts(self, port_type: PortType) -> int:
        return 1  # 1 input, 1 output
    
    def dataType(self, port_type: PortType, port_index: PortIndex) -> NodeDataType:
        return DecimalData().type()
    
    def outData(self, port_index: PortIndex):
        return self._result
    
    def setInData(self, data, port_index: PortIndex):
        self._number = data
        if self._number:
            import math
            value = self._number.number()
            if value >= 0:
                self._result = DecimalData(math.sqrt(value))
            else:
                self._result = DecimalData(float('nan'))
        else:
            self._result = None
        self.dataUpdated.emit(0)

# Register it
registry.registerModel(SquareRootModel, "Operators")
```

## Future Examples

Planned examples:
- **Image Processing**: Load, filter, and display images
- **Text Processing**: String manipulation and text analysis
- **Data Visualization**: Plot data using matplotlib integration
- **State Machine**: Visual state machine editor

## Contributing

To add new examples:

1. Create a new Python file in this directory
2. Follow the pattern established in `calculator.py`
3. Add documentation in this README
4. Test with both Qt5 and Qt6 if possible
5. Submit a pull request

## Troubleshooting

**Import Error:**
```
ImportError: No module named 'QtNodes'
```
Solution: Install the QtNodes bindings (see above)

**Qt Application Error:**
```
QWidget: Must construct a QApplication before a QWidget
```
Solution: Make sure you create QApplication before any widgets

**Module Suffix Error:**
```
ImportError: ... .so/.pyd not found
```
Solution: Check that the bindings were built for your platform and Python version

## References

- [QtNodes Documentation](https://qtnodes.readthedocs.io/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Python Bindings README](../README.md)
