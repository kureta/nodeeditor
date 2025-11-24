#!/usr/bin/env python3
"""
Test script for QtNodes Python bindings

This script performs basic import and instantiation tests to verify
that the bindings are working correctly.
"""

import sys
import traceback

def test_imports():
    """Test that all major classes can be imported"""
    print("Testing imports...")
    
    try:
        from QtNodes import (
            # Enums
            NodeRole,
            PortType,
            ConnectionPolicy,
            
            # Core types
            ConnectionId,
            NodeDataType,
            NodeValidationState,
            
            # Abstract classes
            AbstractGraphModel,
            NodeData,
            
            # Model classes
            NodeDelegateModel,
            NodeDelegateModelRegistry,
            DataFlowGraphModel,
            
            # Graphics classes
            BasicGraphicsScene,
            DataFlowGraphicsScene,
            GraphicsView,
            
            # Style classes
            NodeStyle,
            ConnectionStyle,
            GraphicsViewStyle,
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False


def test_enum_values():
    """Test that enums have correct values"""
    print("\nTesting enum values...")
    
    try:
        from QtNodes import PortType, ConnectionPolicy, NodeRole
        
        # Test PortType
        assert hasattr(PortType, 'In')
        assert hasattr(PortType, 'Out')
        assert hasattr(PortType, 'None')
        
        # Test ConnectionPolicy
        assert hasattr(ConnectionPolicy, 'One')
        assert hasattr(ConnectionPolicy, 'Many')
        
        # Test NodeRole
        assert hasattr(NodeRole, 'Type')
        assert hasattr(NodeRole, 'Position')
        assert hasattr(NodeRole, 'Caption')
        
        print("✓ Enum values correct")
        return True
    except (ImportError, AssertionError) as e:
        print(f"✗ Enum test failed: {e}")
        traceback.print_exc()
        return False


def test_basic_instantiation():
    """Test that basic classes can be instantiated"""
    print("\nTesting basic instantiation...")
    
    try:
        from QtNodes import (
            NodeDelegateModelRegistry,
            NodeDataType,
            ConnectionId,
        )
        
        # Test registry creation
        registry = NodeDelegateModelRegistry()
        print("  ✓ NodeDelegateModelRegistry created")
        
        # Test NodeDataType creation
        dtype = NodeDataType()
        print("  ✓ NodeDataType created")
        
        # Test ConnectionId creation
        conn_id = ConnectionId()
        print("  ✓ ConnectionId created")
        
        print("✓ Basic instantiation successful")
        return True
    except Exception as e:
        print(f"✗ Instantiation test failed: {e}")
        traceback.print_exc()
        return False


def test_with_qt():
    """Test integration with Qt (requires display)"""
    print("\nTesting Qt integration...")
    
    try:
        from PySide6.QtWidgets import QApplication
        from QtNodes import (
            DataFlowGraphModel,
            DataFlowGraphicsScene,
            GraphicsView,
            NodeDelegateModelRegistry,
        )
        
        # Create QApplication (required for Qt widgets)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create registry and model
        registry = NodeDelegateModelRegistry()
        model = DataFlowGraphModel(registry)
        print("  ✓ DataFlowGraphModel created")
        
        # Create scene
        scene = DataFlowGraphicsScene(model)
        print("  ✓ DataFlowGraphicsScene created")
        
        # Create view (but don't show it)
        view = GraphicsView(scene)
        print("  ✓ GraphicsView created")
        
        print("✓ Qt integration successful")
        return True
    except Exception as e:
        print(f"✗ Qt integration test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("QtNodes Python Bindings Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Enum values", test_enum_values()))
    results.append(("Basic instantiation", test_basic_instantiation()))
    results.append(("Qt integration", test_with_qt()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
