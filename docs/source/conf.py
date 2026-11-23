import sys
import tomllib
from pathlib import Path

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# -- Project information -----------------------------------------------------
project = 'Python Code Validator'
# noinspection PyShadowingBuiltins
copyright = '2025, Ivan Kovach (@Qu1nel)'
author = 'Ivan Kovach (@Qu1nel)'
repository_root = Path(__file__).resolve().parents[2]
with (repository_root / 'pyproject.toml').open('rb') as metadata:
    release = tomllib.load(metadata)['project']['version']

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
    'sphinx_design',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# -- Path setup --------------------------------------------------------------


sys.path.insert(0, str(repository_root / 'src'))
