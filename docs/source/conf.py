
# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# [... Full text of the GNU General Public License v3.0 goes here ...]

# Copyright (C) 2025 Kris Kirby

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full list see
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
# Add the project root to the path so Sphinx can find the 'pyhpfec' package
sys.path.insert(0, os.path.abspath('../../')) 


# -- Project information -----------------------------------------------------

project = 'PyHPFEC'
copyright = '2025, [Your Name/Company Name]' # Update this to match your LICENSE files
author = '[Your Name/Company Name]'

# The short X.Y version
version = '1.0'
# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc', # Automatically document Python code
    'sphinx.ext.napoleon', # Support for NumPy and Google style docstrings
    'sphinx.ext.viewcode', # Add links to highlighted source code
    'sphinx.ext.mathjax', # Render math equations (useful for coding theory)
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo' # A modern, responsive theme. Install with: pip install furo

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Ensure the index.rst includes the correct API reference files
autodoc_member_order = 'bysource'

