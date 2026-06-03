# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = "SysSim"
copyright = "2025, SysSim Contributors"
author = "SysSim Contributors"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "docs/superpowers/**", ".docsenv"]

# Treat the documented modules as the default domain for :func:/:class: refs.
default_role = "py:obj"
primary_domain = "py"
add_module_names = False

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_title = "SysSim"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "_static/logo.svg"
html_favicon = "_static/logo.svg"

html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#5b4ee5",
        "color-brand-content": "#5b4ee5",
    },
    "dark_css_variables": {
        "color-brand-primary": "#9d92ff",
        "color-brand-content": "#9d92ff",
    },
    "source_repository": "https://github.com/AISysSim/SysSim/",
    "source_branch": "main",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/AISysSim/SysSim",
            "html": "",
            "class": "fa-brands fa-github",
        },
    ],
}

pygments_style = "friendly"
pygments_dark_style = "monokai"
