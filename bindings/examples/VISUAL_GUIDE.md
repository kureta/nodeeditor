# QtNodes Python Calculator - Visual Guide

## Application Screenshot Description

When you run `python3 bindings/examples/calculator.py`, you'll see:

### Main Window

```
┌─────────────────────────────────────────────────────────────┐
│ [*]QtNodes Calculator - Python                              │
├─────────────────────────────────────────────────────────────┤
│ File                                                         │
│   Save Scene (Ctrl+S)                                        │
│   Load Scene (Ctrl+O)                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐                                         │
│  │ Number Source  │                                         │
│  │ ┌────────────┐ │                                         │
│  │ │    5.0     │ ○─────┐                                  │
│  │ └────────────┘ │      │                                  │
│  └────────────────┘      │    ┌──────────────┐             │
│                          └────○ Addition      │             │
│  ┌────────────────┐           │              ○────┐        │
│  │ Number Source  │           └──────────────┘     │        │
│  │ ┌────────────┐ │      ┌───○                    │        │
│  │ │    3.0     │ ○──────┘                         │        │
│  │ └────────────┘ │                                │        │
│  └────────────────┘          ┌──────────────────┐  │        │
│                               │ Result Display   │  │        │
│                          ┌───○                   │  │        │
│                          │    │      8           │  │        │
│                          │    └──────────────────┘  │        │
│                          │                          │        │
│  ┌────────────────┐      │    ┌──────────────┐    │        │
│  │ Number Source  │      │    │ Multiplication│    │        │
│  │ ┌────────────┐ │      │    │              ○────┘        │
│  │ │    2.0     │ ○──────┴───○              │              │
│  │ └────────────┘ │           └──────────────┘             │
│  └────────────────┘                  │                      │
│                                      │                      │
│                               ┌──────┘                      │
│                               │    ┌──────────────────┐    │
│                               │    │ Result Display   │    │
│                               └───○                   │    │
│                                    │      16          │    │
│                                    └──────────────────┘    │
│                                                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Node Types Visualization

#### Number Source Node
```
┌──────────────────┐
│ Number Source    │  ← Title (caption)
│ ┌──────────────┐ │
│ │   5.0        │ │  ← Editable text field
│ └──────────────┘ │
│                 ○│  ← Output port (right side)
└──────────────────┘
```

#### Math Operation Node (e.g., Addition)
```
┌──────────────────┐
│○                 │  ← Input port 1 (left side)
│  Addition        │  ← Title (caption)
│○                ○│  ← Input port 2 (left) & Output port (right)
└──────────────────┘
```

#### Result Display Node
```
┌──────────────────┐
│○ Result Display  │  ← Input port (left side)
│                  │
│      8.0         │  ← Computed result (label)
│                  │
└──────────────────┘
```

### Context Menu (Right-Click)

When you right-click on empty space:
```
┌─────────────────┐
│ Sources         ▶│──┬─────────────────────┐
│ Operators       ▶│  │ Number Source       │
│ Displays        ▶│  └─────────────────────┘
└─────────────────┘
```

Operators submenu:
```
┌─────────────────┐
│ Addition        │
│ Subtraction     │
│ Multiplication  │
│ Division        │
└─────────────────┘
```

### Connection Visuals

Connections are drawn as curved lines (Bezier curves):
- **Black** when connected and normal
- **Gray** when being created
- **Deep Sky Blue** when selected or hovered
- **Line Width**: 3.0 pixels
- **Port Diameter**: 10.0 pixels

### Interactive Features

1. **Adding Nodes**: Right-click → Select category → Select node type
2. **Connecting**: Drag from output port (○) to input port (○)
3. **Editing Numbers**: Click in the text field of Number Source nodes
4. **Moving Nodes**: Drag node by its title bar
5. **Selecting**: Click to select, Ctrl+Click for multiple selection
6. **Deleting**: Select and press Delete key
7. **Saving**: Ctrl+S or File → Save Scene
8. **Loading**: Ctrl+O or File → Load Scene

### Real-Time Computation

As you type in a Number Source:
1. Value updates immediately
2. Signal propagates to connected nodes
3. Math operations recompute
4. Display nodes update automatically

Example flow:
```
[Type "5"] → [Emit signal] → [Addition receives] → [Computes 5+3=8] 
→ [Emit result] → [Display updates to "8"]
```

### Color Scheme

- **Node Background**: Light gray
- **Node Border**: Dark gray
- **Selected Node**: Blue highlight
- **Connection Lines**: Black (normal), Deep Sky Blue (selected/hover)
- **Port Circles**: Dark gray outline, light fill
- **Text**: Black on white/light gray background

### Window Features

- **Title**: Shows "[*]" when scene is modified (unsaved changes)
- **Resizable**: Can be resized like any standard window
- **Menu Bar**: Standard File menu with keyboard shortcuts
- **Status**: Window title updates to show modified state

## Example Calculation Session

### Step 1: Create Number Sources
Add three Number Source nodes and set them to 5, 3, and 2.

### Step 2: Add Addition
Add an Addition node and connect:
- Number Source (5) → Addition input 1
- Number Source (3) → Addition input 2

Result: Addition outputs 8

### Step 3: Add Multiplication
Add a Multiplication node and connect:
- Addition output → Multiplication input 1
- Number Source (2) → Multiplication input 2

Result: Multiplication outputs 16

### Step 4: Add Displays
Add two Result Display nodes:
- Connect Addition output → Display 1 (shows "8")
- Connect Multiplication output → Display 2 (shows "16")

### Final Graph
```
    5 ──┐
        ├─→ Addition (8) ──┐
    3 ──┘                  ├─→ Multiplication (16) ──→ Display (16)
                           │
    2 ─────────────────────┘
            ↓
         Display (8)
```

## Console Output

When the application starts, you'll see:
```
============================================================
QtNodes Calculator - Python Example
============================================================

Available nodes:
  Sources:
    - Number Source: Input numbers
  Operators:
    - Addition, Subtraction, Multiplication, Division
  Displays:
    - Result Display: Show results

Usage:
  - Right-click in empty space to add nodes
  - Drag from output ports to input ports to connect
  - Type numbers in Number Source nodes
  - Results appear automatically in Display nodes
  - Save/Load scenes with Ctrl+S / Ctrl+O
============================================================
```

## Tips

1. **Validation**: Number Source only accepts valid decimal numbers
2. **Division by Zero**: Returns "inf" when dividing by zero
3. **Missing Inputs**: Operation nodes show no output until both inputs are connected
4. **Live Update**: All results update in real-time as you change input values
5. **Save Format**: Scenes are saved as JSON files
6. **Multiple Displays**: Connect one output to multiple display nodes
7. **Chain Operations**: Create complex expressions by chaining operations

## Performance

- **Instant Updates**: Sub-millisecond propagation for typical graphs
- **Efficient**: Only recomputes affected nodes when inputs change
- **Scalable**: Can handle hundreds of nodes without lag
- **Memory**: Minimal overhead, shared data between connections

## Keyboard Shortcuts

- **Ctrl+S**: Save scene
- **Ctrl+O**: Load scene  
- **Delete**: Delete selected nodes/connections
- **Ctrl+D**: Duplicate selected nodes (if implemented)
- **Ctrl+Z/Ctrl+Y**: Undo/Redo (if implemented)
- **Mouse Wheel**: Zoom in/out (if implemented)
- **Middle Mouse Drag**: Pan view (if implemented)
