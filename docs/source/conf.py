# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import subprocess
import sys
import pyfian

# ---------------------------------------------------------------------------
# Make the project-level notebooks/ directory accessible inside the Sphinx
# source tree by creating a junction (Windows) or symlink (Unix/macOS) at
# docs/source/notebooks -> <project_root>/notebooks.
# The link is transient (ignored by git) and is recreated automatically.
# ---------------------------------------------------------------------------
_source_dir = os.path.dirname(os.path.abspath(__file__))
_notebooks_link = os.path.join(_source_dir, "notebooks")
# Using absolute paths to ensure reliability across different build environments
_notebooks_target = os.path.abspath(os.path.join(_source_dir, "..", "..", "notebooks"))

if not os.path.exists(_notebooks_link):
    if sys.platform == "win32":
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", _notebooks_link, _notebooks_target],
            check=True,
        )
    else:
        os.symlink(_notebooks_target, _notebooks_link)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Python Financial Analyst"
copyright = "2025, Pablo Orazi/Panteleymon Semka"
author = "Pablo Orazi/Panteleymon Semka"
release = pyfian.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "myst_nb",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
]

mathjax3_config = {
    "tex": {
        "inlineMath": [["$", "$"], ["\\(", "\\)"]],
        "displayMath": [["$$", "$$"], ["\\[", "\\]"]],
    }
}
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
]

# Combined exclude_patterns to prevent the second definition from overwriting the first
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- AutoAPI configuration ---------------------------------------------------
autoapi_dirs = ["../../src/pyfian"]
autodoc_inherit_docstrings = True
autoapi_keep_files = True
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    # "imported-members" excluded: avoids naming conflicts between imported symbols
    # and submodule names (e.g., function irr vs module pyfian.time_value.irr)
]

# -- Napoleon & Autodoc settings ---------------------------------------------
napoleon_use_ivar = True
autosummary_generate = False
napoleon_custom_sections = [("Methods", "notes")]

autodoc_default_options = {
    "members": True,
}

templates_path = ["_templates"]

# -- Warning Suppression -----------------------------------------------------
suppress_warnings = [
    "py.duplicate_object",  # Napoleon Attributes section + autoapi introspection both document attrs
    "ref.python",  # re-exported symbols appear under two qualified names
    "myst.xref_missing",  # README links to project root files not in Sphinx source tree
    "docutils",  # RST formatting issues in math-heavy docstrings
]

nb_execution_mode = "cache"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]