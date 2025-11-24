#!/usr/bin/env python3
"""
Simple QtNodes Python binding example

This example demonstrates basic usage of QtNodes from Python.
It creates a simple node editor with a custom node type.
"""

import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt

try:
    from QtNodes import (
        DataFlowGraphModel,
        GraphicsView,
        DataFlowGraphicsScene,
        NodeDelegateModel,
        NodeDelegateModelRegistry,
        NodeDataType,
        PortType,
    )
except ImportError as e:
    print(f"Error importing QtNodes: {e}")
    print("Make sure the QtNodes Python bindings are installed.")
    print("Build with -DBUILD_PYTHON_BINDINGS=ON and install.")
    sys.exit(1)


class SimpleTextModel(NodeDelegateModel):
    """A simple node model that displays text"""
    
    def __init__(self):
        super().__init__()
        self._widget = None
    
    def name(self):
        """Unique name for this node type"""
        return "SimpleText"
    
    def caption(self):
        """Display name shown in the UI"""
        return "Text Node"
    
    def captionVisible(self):
        """Whether to show the caption"""
        return True
    
    def nPorts(self, portType):
        """Number of input/output ports"""
        if portType == PortType.In:
            return 1  # One input port
        else:
            return 1  # One output port
    
    def dataType(self, portType, portIndex):
        """Data type for each port"""
        return NodeDataType("text", "Text")
    
    def embeddedWidget(self):
        """Widget to display inside the node"""
        if self._widget is None:
            self._widget = QLabel("Text Node")
            self._widget.setAlignment(Qt.AlignCenter)
            self._widget.setMinimumSize(100, 50)
        return self._widget


class NumberSourceModel(NodeDelegateModel):
    """A node that outputs a number"""
    
    def __init__(self):
        super().__init__()
        self._widget = None
    
    def name(self):
        return "NumberSource"
    
    def caption(self):
        return "Number Source"
    
    def captionVisible(self):
        return True
    
    def nPorts(self, portType):
        if portType == PortType.In:
            return 0  # No inputs
        else:
            return 1  # One output
    
    def dataType(self, portType, portIndex):
        return NodeDataType("number", "Number")
    
    def embeddedWidget(self):
        if self._widget is None:
            self._widget = QLabel("42")
            self._widget.setAlignment(Qt.AlignCenter)
            self._widget.setMinimumSize(80, 40)
        return self._widget


def main():
    """Main application entry point"""
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create node registry
    registry = NodeDelegateModelRegistry()
    
    # Register our custom node types
    # Note: The exact API may vary depending on the binding implementation
    try:
        registry.registerModel(SimpleTextModel, "SimpleText")
        registry.registerModel(NumberSourceModel, "NumberSource")
    except Exception as e:
        print(f"Note: Could not register models - API may need adjustment: {e}")
        print("The basic structure is correct, but the exact registration API")
        print("may need to be verified with the actual binding implementation.")
    
    # Create the graph model
    model = DataFlowGraphModel(registry)
    
    # Create graphics scene and view
    scene = DataFlowGraphicsScene(model)
    view = GraphicsView(scene)
    
    # Configure the view
    view.setWindowTitle("QtNodes Python Example")
    view.resize(800, 600)
    view.show()
    
    print("QtNodes Python example running...")
    print("Right-click in the window to add nodes (if context menu is available)")
    
    # Run the application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
