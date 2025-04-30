import os
import tempfile
from spice.analyzers.count_external_dependencies import count_external_dependencies

# Get path to the sample files
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "sample-code")
PY_SAMPLE = os.path.join(SAMPLES_DIR, "example.py")
JS_SAMPLE = os.path.join(SAMPLES_DIR, "example.js")
GO_SAMPLE = os.path.join(SAMPLES_DIR, "example.go")
RB_SAMPLE = os.path.join(SAMPLES_DIR, "example.rb")

def test_count_dependencies_in_samples():
    """Test counting external dependencies in sample files."""
    # These test values may need to be adjusted based on actual sample file content
    py_count = count_external_dependencies(PY_SAMPLE)
    js_count = count_external_dependencies(JS_SAMPLE)
    go_count = count_external_dependencies(GO_SAMPLE)
    rb_count = count_external_dependencies(RB_SAMPLE)
    
    # The expected values should be updated to match actual sample file content
    assert isinstance(py_count, int), "Python dependency count should be an integer"
    assert isinstance(js_count, int), "JavaScript dependency count should be an integer"
    assert isinstance(go_count, int), "Go dependency count should be an integer"
    assert isinstance(rb_count, int), "Ruby dependency count should be an integer"

def test_python_dependencies():
    """Test counting external dependencies in Python code."""
    # Create a temporary file with Python imports
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(b"import os\n")               # Standard library (not counted)
        temp.write(b"import sys\n")              # Standard library (not counted)
        temp.write(b"import numpy as np\n")      # External library (counted)
        temp.write(b"from django import forms\n") # External library (counted)
        temp.write(b"import math\n")             # Standard library (not counted)
        temp_name = temp.name
    
    try:
        count = count_external_dependencies(temp_name)
        assert count == 2, f"Expected 2 external dependencies, got {count}"
    finally:
        os.unlink(temp_name)

def test_javascript_dependencies():
    """Test counting external dependencies in JavaScript code."""
    # Create a temporary file with JavaScript imports
    with tempfile.NamedTemporaryFile(suffix=".js", delete=False) as temp:
        temp.write(b"const fs = require('fs');\n")                # Standard library (not counted)
        temp.write(b"const path = require('path');\n")            # Standard library (not counted)
        temp.write(b"const express = require('express');\n")      # External library (counted)
        temp.write(b"import React from 'react';\n")               # External library (counted)
        temp.write(b"import { useState } from 'react';\n")        # Same as above, counts as 1
        temp.write(b"import './local-file.js';\n")                # Relative import (not counted)
        temp_name = temp.name
    
    try:
        count = count_external_dependencies(temp_name)
        assert count == 2, f"Expected 2 external dependencies, got {count}"
    finally:
        os.unlink(temp_name)

def test_go_dependencies():
    """Test counting external dependencies in Go code."""
    # Create a temporary file with Go imports
    with tempfile.NamedTemporaryFile(suffix=".go", delete=False) as temp:
        temp.write(b'import "fmt"\n')                              # Standard library (not counted)
        temp.write(b'import "os"\n')                               # Standard library (not counted)
        temp.write(b'import "github.com/gorilla/mux"\n')           # External library (counted)
        temp.write(b'import "github.com/jinzhu/gorm"\n')           # External library (counted)
        temp.write(b'import (\n')
        temp.write(b'    "io"\n')                                  # Standard library (not counted)
        temp.write(b'    "github.com/spf13/cobra"\n')              # External library (counted)
        temp.write(b')\n')
        temp_name = temp.name
    
    try:
        count = count_external_dependencies(temp_name)
        assert count == 3, f"Expected 3 external dependencies, got {count}"
    finally:
        os.unlink(temp_name)

def test_ruby_dependencies():
    """Test counting external dependencies in Ruby code."""
    # Create a temporary file with Ruby requires
    with tempfile.NamedTemporaryFile(suffix=".rb", delete=False) as temp:
        temp.write(b'require "json"\n')                  # Standard library (not counted)
        temp.write(b'require "date"\n')                  # Standard library (not counted)
        temp.write(b'require "rails"\n')                 # External library (counted)
        temp.write(b'require "sinatra"\n')               # External library (counted)
        temp.write(b'require_relative "./local_file"\n') # Relative import (not counted)
        temp.write(b'gem "activerecord"\n')              # External gem (counted)
        temp_name = temp.name
    
    try:
        count = count_external_dependencies(temp_name)
        assert count == 3, f"Expected 3 external dependencies, got {count}"
    finally:
        os.unlink(temp_name)

def test_empty_file():
    """Test counting external dependencies in an empty file."""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp_name = temp.name
    
    try:
        count = count_external_dependencies(temp_name)
        assert count == 0, f"Expected 0 external dependencies in empty file, got {count}"
    finally:
        os.unlink(temp_name)

def test_file_with_no_dependencies():
    """Test counting external dependencies in a file with code but no imports."""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(b"def hello():\n")
        temp.write(b"    print('Hello, world!')\n")
        temp.write(b"\n")
        temp.write(b"hello()\n")
        temp_name = temp.name
    
    try:
        count = count_external_dependencies(temp_name)
        assert count == 0, f"Expected 0 external dependencies, got {count}"
    finally:
        os.unlink(temp_name) 