# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'R-testbench'
copyright = '2020, Alexandre Quenon'
author = 'Alexandre Quenon'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings.
extensions = [
	'recommonmark',
	'sphinx_rtd_theme'
]

# The file extensions of source files.
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The “master” document, that contains the root toctree directive
master_doc = 'index'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for internationalization ----------------------------------------



# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
	# Toc options
	'collapse_navigation': True,
	'sticky_navigation': True,
	'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
	# Appearance options
	'display_version': True,
	'logo_only': False,
	'prev_next_buttons_location': 'both',
	'style_external_links': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

