#ifndef QTNODES_BINDINGS_H
#define QTNODES_BINDINGS_H

// Include all public QtNodes headers for binding generation

// Core definitions
#include <QtNodes/internal/Definitions.hpp>
#include <QtNodes/internal/Export.hpp>

// Base classes
#include <QtNodes/internal/NodeData.hpp>
#include <QtNodes/internal/Serializable.hpp>
#include <QtNodes/internal/AbstractGraphModel.hpp>
#include <QtNodes/internal/AbstractNodeGeometry.hpp>
#include <QtNodes/internal/AbstractNodePainter.hpp>
#include <QtNodes/internal/AbstractConnectionPainter.hpp>

// Model classes
#include <QtNodes/internal/NodeDelegateModel.hpp>
#include <QtNodes/internal/NodeDelegateModelRegistry.hpp>
#include <QtNodes/internal/DataFlowGraphModel.hpp>

// Graphics scene and view
#include <QtNodes/internal/BasicGraphicsScene.hpp>
#include <QtNodes/internal/DataFlowGraphicsScene.hpp>
#include <QtNodes/internal/GraphicsView.hpp>
#include <QtNodes/internal/NodeGraphicsObject.hpp>
#include <QtNodes/internal/ConnectionGraphicsObject.hpp>

// Style classes
#include <QtNodes/internal/NodeStyle.hpp>
#include <QtNodes/internal/ConnectionStyle.hpp>
#include <QtNodes/internal/GraphicsViewStyle.hpp>
#include <QtNodes/internal/StyleCollection.hpp>

// Geometry implementations
#include <QtNodes/internal/DefaultHorizontalNodeGeometry.hpp>
#include <QtNodes/internal/DefaultVerticalNodeGeometry.hpp>

// Painter implementations
#include <QtNodes/internal/DefaultNodePainter.hpp>
#include <QtNodes/internal/DefaultConnectionPainter.hpp>

// State classes
#include <QtNodes/internal/NodeState.hpp>
#include <QtNodes/internal/ConnectionState.hpp>

// Undo system
#include <QtNodes/internal/UndoCommands.hpp>

// Utilities
#include <QtNodes/internal/NodeConnectionInteraction.hpp>
#include <QtNodes/internal/ConnectionIdUtils.hpp>
#include <QtNodes/internal/locateNode.hpp>

#endif // QTNODES_BINDINGS_H
