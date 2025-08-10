#!/usr/bin/env python3
"""File operation utilities."""

import os
from typing import Dict, Any


def save_project_file(filename: str, content: str, project_dir: str = "generated_project"):
    """Save a file to the project directory."""
    os.makedirs(project_dir, exist_ok=True)
    filepath = os.path.join(project_dir, filename)
    
    # Create subdirectories if needed
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def read_project_file(filename: str, project_dir: str = "generated_project") -> str:
    """Read a file from the project directory."""
    filepath = os.path.join(project_dir, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def file_exists(filename: str, project_dir: str = "generated_project") -> bool:
    """Check if a file exists in the project directory."""
    filepath = os.path.join(project_dir, filename)
    return os.path.exists(filepath)


def list_project_files(project_dir: str = "generated_project") -> list:
    """List all files in the project directory."""
    if not os.path.exists(project_dir):
        return []
    
    files = []
    for root, dirs, filenames in os.walk(project_dir):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), project_dir)
            files.append(rel_path)
    return files


def create_directory(dir_path: str, project_dir: str = "generated_project"):
    """Create a directory in the project."""
    full_path = os.path.join(project_dir, dir_path)
    os.makedirs(full_path, exist_ok=True)