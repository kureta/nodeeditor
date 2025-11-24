# Building QtNodes Python Bindings

This document provides detailed instructions for building QtNodes Python bindings.

## Quick Start

### Prerequisites

1. Install Qt6 (or Qt5)
2. Install Python 3.8+
3. Install PySide6 and Shiboken6:
   ```bash
   pip install PySide6 shiboken6 shiboken6-generator
   ```

### Build Steps

```bash
# Clone the repository
git clone https://github.com/paceholder/nodeeditor.git
cd nodeeditor

# Create build directory
mkdir build && cd build

# Configure with Python bindings enabled
cmake .. \
    -DUSE_QT6=ON \
    -DBUILD_PYTHON_BINDINGS=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_TESTING=OFF

# Build
cmake --build . -j$(nproc)

# Install (optional)
sudo cmake --install .
```

## Platform-Specific Instructions

### Linux (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    qt6-base-dev \
    libqt6opengl6-dev \
    python3-dev \
    python3-pip

# Install Python dependencies
pip3 install PySide6 shiboken6 shiboken6-generator

# Build
mkdir build && cd build
cmake .. -DUSE_QT6=ON -DBUILD_PYTHON_BINDINGS=ON -DBUILD_SHARED_LIBS=ON
cmake --build . -j$(nproc)
```

### macOS

```bash
# Install dependencies using Homebrew
brew install qt@6 cmake python@3.11

# Install Python dependencies
pip3 install PySide6 shiboken6 shiboken6-generator

# Build
mkdir build && cd build
cmake .. \
    -DUSE_QT6=ON \
    -DBUILD_PYTHON_BINDINGS=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_PREFIX_PATH="$(brew --prefix qt@6)"
cmake --build . -j$(sysctl -n hw.ncpu)
```

### Windows

```batch
REM Install Qt6 from https://www.qt.io/download
REM Install Python from https://www.python.org/downloads/

REM Install Python dependencies
pip install PySide6 shiboken6 shiboken6-generator

REM Build (adjust Qt path as needed)
mkdir build
cd build
cmake .. ^
    -DUSE_QT6=ON ^
    -DBUILD_PYTHON_BINDINGS=ON ^
    -DBUILD_SHARED_LIBS=ON ^
    -DCMAKE_PREFIX_PATH="C:\Qt\6.7.0\msvc2019_64"
cmake --build . --config Release
```

## Installation

### System-wide Installation

```bash
cd build
sudo cmake --install .
```

### User Installation

To install for the current user only:

```bash
cd build
cmake --install . --prefix ~/.local
```

Make sure `~/.local/lib/python3.x/site-packages` is in your Python path.

### Development Installation

For development, you can use the bindings directly from the build directory by adding it to your PYTHONPATH:

```bash
export PYTHONPATH="/path/to/nodeeditor/build/bindings:$PYTHONPATH"
export LD_LIBRARY_PATH="/path/to/nodeeditor/build/lib:$LD_LIBRARY_PATH"
```

## Using pip (Alternative)

You can also build and install using pip:

```bash
# From the repository root
pip install .

# Or for development (editable install)
pip install -e .
```

## Verification

Test that the bindings work:

```python
python3 -c "from QtNodes import DataFlowGraphModel; print('QtNodes imported successfully')"
```

Run the example:

```bash
python3 bindings/example.py
```

## Troubleshooting

### "No module named 'PySide6'"

Install PySide6:
```bash
pip install PySide6
```

### "shiboken6 not found"

Install shiboken6-generator:
```bash
pip install shiboken6-generator
```

### "Could not find a package configuration file provided by 'PySide6'"

Make sure PySide6 is installed and CMake can find it. You may need to set the CMAKE_PREFIX_PATH:
```bash
export CMAKE_PREFIX_PATH=$(python3 -c "import PySide6; import os; print(os.path.dirname(PySide6.__file__))")
```

### "libQtNodes.so: cannot open shared object file"

Add the library path to LD_LIBRARY_PATH (Linux) or DYLD_LIBRARY_PATH (macOS):
```bash
export LD_LIBRARY_PATH="/path/to/nodeeditor/build/lib:$LD_LIBRARY_PATH"
```

On Windows, add the library directory to your PATH.

### Shiboken generation errors

Check that:
1. All required headers are included in `bindings/bindings.h`
2. The typesystem file `bindings/typesystem_qtnodes.xml` is valid XML
3. Qt includes are properly found by CMake

Enable verbose output:
```bash
cmake .. -DUSE_QT6=ON -DBUILD_PYTHON_BINDINGS=ON --trace-expand
```

## Advanced Configuration

### Building with Qt5

```bash
cmake .. -DUSE_QT6=OFF -DBUILD_PYTHON_BINDINGS=ON -DBUILD_SHARED_LIBS=ON
pip install PySide2 shiboken2 shiboken2-generator
```

### Custom Python Interpreter

```bash
cmake .. \
    -DUSE_QT6=ON \
    -DBUILD_PYTHON_BINDINGS=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DPython3_EXECUTABLE=/path/to/python
```

### Debug Build

```bash
cmake .. \
    -DUSE_QT6=ON \
    -DBUILD_PYTHON_BINDINGS=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Debug
```

## Contributing

When modifying the bindings:

1. Update `bindings/bindings.h` if adding new headers
2. Update `bindings/typesystem_qtnodes.xml` if adding new classes
3. Test the changes with the example script
4. Update documentation as needed

See `bindings/README.md` for more details on the binding structure.
