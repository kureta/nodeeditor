#!/usr/bin/env python3
"""
QtNodes Calculator Example - Python Implementation

This example demonstrates a fully functional calculator application using QtNodes Python bindings.
It recreates the C++ calculator example with Python, showing:
- Custom NodeData types (DecimalData)
- Number source nodes with editable widgets
- Math operation nodes (addition, subtraction, multiplication, division)
- Display nodes to show results
- Data flow between nodes
"""

import sys
from typing import Optional

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QMenuBar,
    QMenu,
)
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QDoubleValidator, QAction, QKeySequence

try:
    from QtNodes import (
        NodeData,
        NodeDataType,
        NodeDelegateModel,
        NodeDelegateModelRegistry,
        DataFlowGraphModel,
        DataFlowGraphicsScene,
        GraphicsView,
        ConnectionStyle,
        PortType,
        PortIndex,
    )
except ImportError as e:
    print(f"Error: QtNodes Python bindings not found: {e}")
    print("Please build and install the bindings first.")
    print("See bindings/README.md for instructions.")
    sys.exit(1)


# ============================================================================
# Data Classes
# ============================================================================

class DecimalData(NodeData):
    """
    Custom data type representing a decimal number.
    This is transferred between nodes in the graph.
    """
    
    def __init__(self, number: float = 0.0):
        super().__init__()
        self._number = number
    
    def type(self) -> NodeDataType:
        """Return the data type identifier"""
        return NodeDataType("decimal", "Decimal")
    
    def number(self) -> float:
        """Get the number value"""
        return self._number
    
    def number_as_text(self) -> str:
        """Get the number as formatted text"""
        return f"{self._number:.6f}".rstrip('0').rstrip('.')


# ============================================================================
# Node Models
# ============================================================================

class NumberSourceModel(NodeDelegateModel):
    """
    Number source node that allows user input.
    Has no inputs and one output.
    """
    
    def __init__(self):
        super().__init__()
        self._line_edit: Optional[QLineEdit] = None
        self._number = DecimalData(0.0)
    
    def caption(self) -> str:
        return "Number Source"
    
    def name(self) -> str:
        return "NumberSource"
    
    def nPorts(self, port_type: PortType) -> int:
        """Number of ports: 0 inputs, 1 output"""
        if port_type == PortType.In:
            return 0
        return 1
    
    def dataType(self, port_type: PortType, port_index: PortIndex) -> NodeDataType:
        return DecimalData().type()
    
    def outData(self, port_index: PortIndex):
        """Return the current number data"""
        return self._number
    
    def embeddedWidget(self) -> QWidget:
        """Return the embedded line edit widget"""
        if not self._line_edit:
            self._line_edit = QLineEdit()
            self._line_edit.setValidator(QDoubleValidator())
            self._line_edit.setMaximumSize(self._line_edit.sizeHint())
            self._line_edit.setText(str(self._number.number()))
            self._line_edit.textChanged.connect(self._on_text_edited)
        return self._line_edit
    
    def _on_text_edited(self, text: str):
        """Handle text changes in the line edit"""
        try:
            number = float(text) if text else 0.0
            self._number = DecimalData(number)
            self.dataUpdated.emit(0)
        except ValueError:
            self.dataInvalidated.emit(0)
    
    def set_number(self, n: float):
        """Set the number programmatically"""
        self._number = DecimalData(n)
        self.dataUpdated.emit(0)
        if self._line_edit:
            self._line_edit.setText(str(n))


class NumberDisplayModel(NodeDelegateModel):
    """
    Display node that shows the result.
    Has one input and no outputs.
    """
    
    def __init__(self):
        super().__init__()
        self._label: Optional[QLabel] = None
        self._number_data: Optional[DecimalData] = None
    
    def caption(self) -> str:
        return "Result Display"
    
    def name(self) -> str:
        return "NumberDisplay"
    
    def nPorts(self, port_type: PortType) -> int:
        """Number of ports: 1 input, 0 outputs"""
        if port_type == PortType.In:
            return 1
        return 0
    
    def dataType(self, port_type: PortType, port_index: PortIndex) -> NodeDataType:
        return DecimalData().type()
    
    def outData(self, port_index: PortIndex):
        """No output data"""
        return None
    
    def setInData(self, data, port_index: PortIndex):
        """Receive input data and update display"""
        self._number_data = data
        
        if not self._label:
            return
        
        if self._number_data and isinstance(self._number_data, DecimalData):
            self._label.setText(self._number_data.number_as_text())
        else:
            self._label.clear()
        
        self._label.adjustSize()
    
    def embeddedWidget(self) -> QWidget:
        """Return the embedded label widget"""
        if not self._label:
            self._label = QLabel("0")
            self._label.setMargin(3)
            self._label.setAlignment(Qt.AlignCenter)
        return self._label
    
    def number(self) -> float:
        """Get the displayed number"""
        if self._number_data:
            return self._number_data.number()
        return 0.0


class MathOperationModel(NodeDelegateModel):
    """
    Base class for math operations.
    Has 2 inputs and 1 output.
    """
    
    def __init__(self):
        super().__init__()
        self._number1: Optional[DecimalData] = None
        self._number2: Optional[DecimalData] = None
        self._result: Optional[DecimalData] = None
    
    def nPorts(self, port_type: PortType) -> int:
        """Number of ports: 2 inputs, 1 output"""
        if port_type == PortType.In:
            return 2
        return 1
    
    def dataType(self, port_type: PortType, port_index: PortIndex) -> NodeDataType:
        return DecimalData().type()
    
    def outData(self, port_index: PortIndex):
        """Return the computation result"""
        return self._result
    
    def setInData(self, data, port_index: PortIndex):
        """Receive input data and compute result"""
        if port_index == 0:
            self._number1 = data
        else:
            self._number2 = data
        
        self._compute()
    
    def _compute(self):
        """Compute the result - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement _compute()")


class AdditionModel(MathOperationModel):
    """Addition operation: output = input1 + input2"""
    
    def caption(self) -> str:
        return "Addition"
    
    def name(self) -> str:
        return "Addition"
    
    def _compute(self):
        if self._number1 and self._number2:
            result = self._number1.number() + self._number2.number()
            self._result = DecimalData(result)
        else:
            self._result = None
        
        self.dataUpdated.emit(0)


class SubtractionModel(MathOperationModel):
    """Subtraction operation: output = input1 - input2"""
    
    def caption(self) -> str:
        return "Subtraction"
    
    def name(self) -> str:
        return "Subtraction"
    
    def _compute(self):
        if self._number1 and self._number2:
            result = self._number1.number() - self._number2.number()
            self._result = DecimalData(result)
        else:
            self._result = None
        
        self.dataUpdated.emit(0)


class MultiplicationModel(MathOperationModel):
    """Multiplication operation: output = input1 * input2"""
    
    def caption(self) -> str:
        return "Multiplication"
    
    def name(self) -> str:
        return "Multiplication"
    
    def _compute(self):
        if self._number1 and self._number2:
            result = self._number1.number() * self._number2.number()
            self._result = DecimalData(result)
        else:
            self._result = None
        
        self.dataUpdated.emit(0)


class DivisionModel(MathOperationModel):
    """Division operation: output = input1 / input2"""
    
    def caption(self) -> str:
        return "Division"
    
    def name(self) -> str:
        return "Division"
    
    def _compute(self):
        if self._number1 and self._number2:
            n2 = self._number2.number()
            if n2 != 0:
                result = self._number1.number() / n2
                self._result = DecimalData(result)
            else:
                self._result = DecimalData(float('inf'))
        else:
            self._result = None
        
        self.dataUpdated.emit(0)


# ============================================================================
# Application Setup
# ============================================================================

def register_data_models() -> NodeDelegateModelRegistry:
    """Register all available node models"""
    registry = NodeDelegateModelRegistry()
    
    # Register source nodes
    registry.registerModel(NumberSourceModel, "Sources")
    
    # Register display nodes
    registry.registerModel(NumberDisplayModel, "Displays")
    
    # Register operator nodes
    registry.registerModel(AdditionModel, "Operators")
    registry.registerModel(SubtractionModel, "Operators")
    registry.registerModel(MultiplicationModel, "Operators")
    registry.registerModel(DivisionModel, "Operators")
    
    return registry


def set_connection_style():
    """Set custom connection style"""
    style_json = """
    {
        "ConnectionStyle": {
            "ConstructionColor": "gray",
            "NormalColor": "black",
            "SelectedColor": "gray",
            "SelectedHaloColor": "deepskyblue",
            "HoveredColor": "deepskyblue",
            "LineWidth": 3.0,
            "ConstructionLineWidth": 2.0,
            "PointDiameter": 10.0,
            "UseDataDefinedColors": true
        }
    }
    """
    ConnectionStyle.setConnectionStyle(style_json)


# ============================================================================
# Main Application
# ============================================================================

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set custom style
    set_connection_style()
    
    # Register node models
    registry = register_data_models()
    
    # Create main widget
    main_widget = QWidget()
    main_widget.setWindowTitle("[*]QtNodes Calculator - Python")
    
    # Create menu bar
    menu_bar = QMenuBar()
    file_menu = menu_bar.addMenu("File")
    
    save_action = QAction("Save Scene", main_widget)
    save_action.setShortcut(QKeySequence.Save)
    file_menu.addAction(save_action)
    
    load_action = QAction("Load Scene", main_widget)
    load_action.setShortcut(QKeySequence.Open)
    file_menu.addAction(load_action)
    
    # Create layout
    layout = QVBoxLayout(main_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    
    # Create data flow model
    data_flow_model = DataFlowGraphModel(registry)
    
    # Create scene and view
    layout.addWidget(menu_bar)
    scene = DataFlowGraphicsScene(data_flow_model, main_widget)
    view = GraphicsView(scene)
    layout.addWidget(view)
    
    # Connect signals
    save_action.triggered.connect(lambda: scene.save() and main_widget.setWindowModified(False))
    load_action.triggered.connect(scene.load)
    scene.sceneLoaded.connect(view.centerScene)
    scene.modified.connect(lambda: main_widget.setWindowModified(True))
    
    # Show window
    main_widget.resize(800, 600)
    
    # Center window on screen
    screen_geometry = app.primaryScreen().availableGeometry()
    window_geometry = main_widget.frameGeometry()
    window_geometry.moveCenter(screen_geometry.center())
    main_widget.move(window_geometry.topLeft())
    
    main_widget.show()
    
    print("=" * 60)
    print("QtNodes Calculator - Python Example")
    print("=" * 60)
    print("\nAvailable nodes:")
    print("  Sources:")
    print("    - Number Source: Input numbers")
    print("  Operators:")
    print("    - Addition, Subtraction, Multiplication, Division")
    print("  Displays:")
    print("    - Result Display: Show results")
    print("\nUsage:")
    print("  - Right-click in empty space to add nodes")
    print("  - Drag from output ports to input ports to connect")
    print("  - Type numbers in Number Source nodes")
    print("  - Results appear automatically in Display nodes")
    print("  - Save/Load scenes with Ctrl+S / Ctrl+O")
    print("=" * 60)
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
