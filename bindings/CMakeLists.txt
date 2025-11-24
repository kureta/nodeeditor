cmake_minimum_required(VERSION 3.18)

project(QtNodesPython)

# Find required packages
if(USE_QT6)
    find_package(Qt6 REQUIRED COMPONENTS Core Widgets Gui OpenGL)
    set(QT_VERSION_MAJOR 6)
else()
    find_package(Qt5 REQUIRED COMPONENTS Core Widgets Gui OpenGL)
    set(QT_VERSION_MAJOR 5)
endif()

# Find PySide6 (or PySide2 if Qt5 is used)
if(QT_VERSION_MAJOR EQUAL 6)
    find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
    find_package(PySide6 REQUIRED)
    find_package(Shiboken6 REQUIRED)
    
    set(PYSIDE_INCLUDE_DIR ${PySide6_INCLUDE_DIRS})
    set(PYSIDE_LIBRARY ${PySide6_LIBRARIES})
    set(SHIBOKEN_INCLUDE_DIR ${Shiboken6_INCLUDE_DIRS})
    set(SHIBOKEN_LIBRARY ${Shiboken6_LIBRARIES})
    set(SHIBOKEN_GENERATOR Shiboken6::shiboken6)
    set(PYSIDE_TYPESYSTEMS ${PySide6_TYPESYSTEMS})
    set(PYTHON_MODULE_NAME "QtNodes")
else()
    find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
    find_package(PySide2 REQUIRED)
    find_package(Shiboken2 REQUIRED)
    
    set(PYSIDE_INCLUDE_DIR ${PySide2_INCLUDE_DIRS})
    set(PYSIDE_LIBRARY ${PySide2_LIBRARIES})
    set(SHIBOKEN_INCLUDE_DIR ${Shiboken2_INCLUDE_DIRS})
    set(SHIBOKEN_LIBRARY ${Shiboken2_LIBRARIES})
    set(SHIBOKEN_GENERATOR Shiboken2::shiboken2)
    set(PYSIDE_TYPESYSTEMS ${PySide2_TYPESYSTEMS})
    set(PYTHON_MODULE_NAME "QtNodes")
endif()

# Fallback for PYSIDE_TYPESYSTEMS if not set by find_package
if(NOT PYSIDE_TYPESYSTEMS)
    # Try to get it from shiboken module
    execute_process(
        COMMAND ${Python3_EXECUTABLE} -c "import PySide6; import os; print(os.path.join(os.path.dirname(PySide6.__file__), 'typesystems'))"
        OUTPUT_VARIABLE PYSIDE_TYPESYSTEMS
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
    )
    if(NOT PYSIDE_TYPESYSTEMS OR NOT EXISTS "${PYSIDE_TYPESYSTEMS}")
        execute_process(
            COMMAND ${Python3_EXECUTABLE} -c "import PySide2; import os; print(os.path.join(os.path.dirname(PySide2.__file__), 'typesystems'))"
            OUTPUT_VARIABLE PYSIDE_TYPESYSTEMS
            OUTPUT_STRIP_TRAILING_WHITESPACE
            ERROR_QUIET
        )
    endif()
endif()

message(STATUS "PySide typesystems directory: ${PYSIDE_TYPESYSTEMS}")

# Set up paths
set(WRAPPED_HEADER ${CMAKE_CURRENT_SOURCE_DIR}/bindings.h)
set(TYPESYSTEM_FILE ${CMAKE_CURRENT_SOURCE_DIR}/typesystem_qtnodes.xml)

# Get QtNodes include directories
get_target_property(QTNODES_INCLUDE_DIRS QtNodes INTERFACE_INCLUDE_DIRECTORIES)

# Prepare include directories for shiboken
set(SHIBOKEN_INCLUDE_DIRS
    ${QTNODES_INCLUDE_DIRS}
    ${PYSIDE_INCLUDE_DIR}
    ${SHIBOKEN_INCLUDE_DIR}
    ${Qt${QT_VERSION_MAJOR}Core_INCLUDE_DIRS}
    ${Qt${QT_VERSION_MAJOR}Widgets_INCLUDE_DIRS}
    ${Qt${QT_VERSION_MAJOR}Gui_INCLUDE_DIRS}
    ${Python3_INCLUDE_DIRS}
)

# Convert include directories to compiler flags
set(SHIBOKEN_INCLUDE_FLAGS "")
foreach(dir ${SHIBOKEN_INCLUDE_DIRS})
    list(APPEND SHIBOKEN_INCLUDE_FLAGS "-I${dir}")
endforeach()

# Set output directory for generated bindings
set(GENERATED_SOURCES_DIR ${CMAKE_CURRENT_BINARY_DIR}/QtNodes)

# Create the output directory
file(MAKE_DIRECTORY ${GENERATED_SOURCES_DIR})

# Run shiboken to generate bindings
add_custom_command(
    OUTPUT
        ${GENERATED_SOURCES_DIR}/qtnodes_module_wrapper.cpp
        ${GENERATED_SOURCES_DIR}/qtnodes_python.h
    COMMAND ${SHIBOKEN_GENERATOR}
        --generator-set=shiboken
        --enable-parent-ctor-heuristic
        --enable-return-value-heuristic
        --use-isnull-as-nb_nonzero
        --avoid-protected-hack
        ${SHIBOKEN_INCLUDE_FLAGS}
        --typesystem-paths=${PYSIDE_TYPESYSTEMS}
        --output-directory=${CMAKE_CURRENT_BINARY_DIR}
        ${TYPESYSTEM_FILE}
        ${WRAPPED_HEADER}
    DEPENDS
        ${WRAPPED_HEADER}
        ${TYPESYSTEM_FILE}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Generating Python bindings for QtNodes..."
)

# Collect all generated source files
file(GLOB GENERATED_SOURCES ${GENERATED_SOURCES_DIR}/*.cpp)

# If no sources are generated yet (first run), use a placeholder
if(NOT GENERATED_SOURCES)
    set(GENERATED_SOURCES ${GENERATED_SOURCES_DIR}/qtnodes_module_wrapper.cpp)
endif()

# Create the Python module
add_library(QtNodes_python MODULE
    ${GENERATED_SOURCES}
)

# Set the module name
set_target_properties(QtNodes_python PROPERTIES
    OUTPUT_NAME "${PYTHON_MODULE_NAME}"
    PREFIX ""
    SUFFIX "${Python3_SOABI}.so"
)

# Include directories for the module
target_include_directories(QtNodes_python PRIVATE
    ${QTNODES_INCLUDE_DIRS}
    ${PYSIDE_INCLUDE_DIR}
    ${SHIBOKEN_INCLUDE_DIR}
    ${Python3_INCLUDE_DIRS}
    ${GENERATED_SOURCES_DIR}
)

# Link libraries
target_link_libraries(QtNodes_python PRIVATE
    QtNodes
    ${SHIBOKEN_LIBRARY}
    ${PYSIDE_LIBRARY}
    Qt${QT_VERSION_MAJOR}::Core
    Qt${QT_VERSION_MAJOR}::Widgets
    Qt${QT_VERSION_MAJOR}::Gui
    ${Python3_LIBRARIES}
)

# Install the Python module
install(TARGETS QtNodes_python
    LIBRARY DESTINATION ${Python3_SITELIB}
)

# Create a Python package structure
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/__init__.py.in
    ${CMAKE_CURRENT_BINARY_DIR}/__init__.py
    @ONLY
)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/__init__.py
    DESTINATION ${Python3_SITELIB}/QtNodes
)
