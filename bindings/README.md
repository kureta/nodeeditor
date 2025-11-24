# QtNodes Python Bindings

This directory contains Python bindings for the QtNodes library using PySide6 and Shiboken6.

## Overview

The Python bindings allow you to use QtNodes from Python, providing access to all major classes and functionality of the library. The bindings are generated using Shiboken6, the binding generator used by the PySide6 project.

## Prerequisites

To build the Python bindings, you need:

- Python 3.8 or later
- PySide6 (for Qt6 builds) or PySide2 (for Qt5 builds)
- Shiboken6 (for Qt6) or Shiboken2 (for Qt5)
- CMake 3.18 or later
- The QtNodes library built with `BUILD_SHARED_LIBS=ON`

### Installing PySide6 and Shiboken6

```bash
pip install PySide6 shiboken6 shiboken6-generator
```

For Qt5 builds:
```bash
pip install PySide2 shiboken2 shiboken2-generator
```

## Building the Bindings

### With Qt6 (recommended)

```bash
mkdir build
cd build
cmake .. -DUSE_QT6=ON -DBUILD_PYTHON_BINDINGS=ON -DBUILD_SHARED_LIBS=ON
cmake --build .
```

### With Qt5

```bash
mkdir build
cd build
cmake .. -DUSE_QT6=OFF -DBUILD_PYTHON_BINDINGS=ON -DBUILD_SHARED_LIBS=ON
cmake --build .
```

## Installation

After building, install the bindings:

```bash
cmake --install .
```

Or manually copy the generated module to your Python site-packages directory.

## Usage Example

```python
import sys
from PySide6.QtWidgets import QApplication
from QtNodes import (
    DataFlowGraphModel,
    GraphicsView,
    DataFlowGraphicsScene,
    NodeDelegateModel,
    NodeDelegateModelRegistry
)

# Create your custom node model by inheriting from NodeDelegateModel
class MyNodeModel(NodeDelegateModel):
    def __init__(self):
        super().__init__()
    
    def name(self):
        return "MyNode"
    
    def caption(self):
        return "My Node"
    
    def nPorts(self, portType):
        return 1
    
    def dataType(self, portType, portIndex):
        from QtNodes import NodeDataType
        return NodeDataType()

# Create application
app = QApplication(sys.argv)

# Create registry and register node models
registry = NodeDelegateModelRegistry()
registry.registerModel(MyNodeModel, "MyNode")

# Create graph model
model = DataFlowGraphModel(registry)

# Create scene and view
scene = DataFlowGraphicsScene(model)
view = GraphicsView(scene)
view.setWindowTitle("QtNodes Python Example")
view.resize(800, 600)
view.show()

sys.exit(app.exec())
```

## File Structure

- `bindings.h` - Main header file that includes all public QtNodes headers
- `typesystem_qtnodes.xml` - Shiboken typesystem file describing the bindings
- `CMakeLists.txt` - CMake build configuration for the bindings
- `__init__.py.in` - Python package initialization template

## Customization

### Adding New Classes

To expose additional QtNodes classes to Python:

1. Add the class to `bindings.h` if not already included
2. Add the corresponding type to `typesystem_qtnodes.xml`:
   - Use `<object-type>` for QObject-derived classes
   - Use `<value-type>` for value types (structs, simple classes)
   - Use `<enum-type>` for enumerations

### Handling Special Cases

The typesystem file can include special directives for handling:
- Template classes
- Smart pointers
- Reference parameters
- Ownership transfer
- Custom conversions

See the [Shiboken documentation](https://doc.qt.io/qtforpython/shiboken6/) for more details.

## Troubleshooting

### Module import errors

If you get import errors, make sure:
- The QtNodes shared library is in your library path (LD_LIBRARY_PATH on Linux, PATH on Windows)
- The Python module is in your Python path or installed in site-packages

### Build errors

- Ensure PySide6 and Shiboken6 are properly installed
- Check that Qt6 (or Qt5) is found by CMake
- Verify that QtNodes is built as a shared library

### Runtime errors

- Check Qt version compatibility between QtNodes and PySide6
- Ensure all dependencies are available at runtime

## Contributing

When adding new features to QtNodes that should be exposed to Python:

1. Update `bindings.h` to include new headers
2. Update `typesystem_qtnodes.xml` with new types
3. Test the bindings with a simple Python script
4. Update this README with any new usage patterns

## License

The Python bindings follow the same license as QtNodes (see LICENSE.rst in the root directory).
