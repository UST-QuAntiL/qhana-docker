# -- Path setup --------------------------------------------------------------

import subprocess
import sys
from collections import ChainMap
from json import load
from os import environ
from pathlib import Path
from shutil import copyfile
from typing import Any, Dict, Mapping, Optional, Tuple, Union, cast

from dotenv import dotenv_values
from tomli import load as parse

ON_READTHEDOCS = environ.get("READTHEDOCS") == "True"

# Define the canonical URL if you are using a custom domain on Read the Docs
html_baseurl = environ.get("READTHEDOCS_CANONICAL_URL", "")

# Tell Jinja2 templates the build is running on Read the Docs
if environ.get("READTHEDOCS", "") == "True":
    if "html_context" not in globals():
        html_context = {}
    html_context["READTHEDOCS"] = True

# -- Project information -----------------------------------------------------

current_path = Path(".").absolute()

project_root: Path
pyproject_path: Path

if current_path.name == "docs":
    project_root = current_path.parent
    pyproject_path = current_path / Path("../pyproject.toml")
else:
    project_root = current_path
    pyproject_path = current_path / Path("pyproject.toml")


# insert project root to allow autodoc to find and import modules
sys.path.insert(0, str(project_root))

flask_environ = cast(
    Mapping[str, str], ChainMap(dotenv_values(project_root / Path(".flaskenv")), environ)
)

pyproject_toml: Any

with pyproject_path.open(mode="rb") as pyproject:
    pyproject_toml = parse(pyproject)

package_config = pyproject_toml["tool"]["poetry"]
sphinx_config = pyproject_toml["tool"].get("sphinx")

project = str(package_config.get("name"))
author = ", ".join(package_config.get("authors"))
copyright_year = sphinx_config.get("copyright-year", 2020)
copyright = f"{copyright_year}, {author}"
version = str(package_config.get("version"))
release = str(sphinx_config.get("release", version))

if sphinx_config.get("html-baseurl", None):
    html_baseurl = sphinx_config.get("html-baseurl", None)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

autosectionlabel_prefix_document = False
autosectionlabel_maxdepth = None

intersphinx_mapping: Optional[
    Dict[str, Tuple[str, Union[Optional[str], Tuple[str]]]]
] = None
intersphinx_timeout = 30

source_suffix = {
    ".rst": "restructuredtext",
}

graphviz_dot = "dot"
graphviz_dot_args = []
graphviz_output_format = "png"

todo_include_todos = not ON_READTHEDOCS
todo_emit_warnings = not ON_READTHEDOCS
todo_link_only = False

python_use_unqualified_type_names = sphinx_config.get("python_use_unqualified_type_names", False)

# enable sphinx autodoc
if sphinx_config.get("enable-autodoc", False):
    extensions.append("sphinx.ext.autodoc")

# enable sphinx autosectionlabel
if sphinx_config.get("enable-autosectionlabel", False):
    extensions.append("sphinx.ext.autosectionlabel")
    config = sphinx_config.get("autosectionlabel", None)
    if config:
        autosectionlabel_prefix_document = config.get("prefix-document", False)
        autosectionlabel_maxdepth = config.get("maxdepth", None)

# enable intersphinx
if sphinx_config.get("intersphinx-mapping", None):
    extensions.append("sphinx.ext.intersphinx")
    mapping = sphinx_config.get("intersphinx-mapping", None)
    intersphinx_mapping = {
        key: (val[0], val[1] if len(val) > 1 and val[1] else None)
        for key, val in mapping.items()
    }

myst_enable_extensions = []

# enable markdown parsing
if sphinx_config.get("enable-markdown", False):
    extensions.append("myst_parser")
    print("MARKDOWN ENABLED")

    source_suffix[".txt"] = "markdown"
    source_suffix[".md"] = "markdown"


# enable sphinx githubpages
if sphinx_config.get("enable-githubpages", False):
    extensions.append("sphinx.ext.githubpages")

# enable sphinx graphviz
if sphinx_config.get("enable-graphviz", False):
    extensions.append("sphinx.ext.graphviz")
    config = sphinx_config.get("graphviz", None)
    if config:
        graphviz_dot = config.get("dot", "dot")
        graphviz_dot_args = config.get("dot-args", [])
        graphviz_output_format = config.get("output-format", "png")

# enable sphinx napoleon
if sphinx_config.get("enable-napoleon", False):
    extensions.append("sphinx.ext.napoleon")

# enable sphinx todo
if sphinx_config.get("enable-todo", False):
    extensions.append("sphinx.ext.todo")
    config = sphinx_config.get("todo", None)
    if config:
        todo_include_todos = config.get("include-todos", False)
        todo_emit_warnings = config.get("emit-warnings", False)
        todo_link_only = config.get("link-only", False)
    if ON_READTHEDOCS:
        todo_include_todos = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

if ON_READTHEDOCS:
    html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Further extension options -----------------------------------------------

# myst markdown parsing
_myst_options = sphinx_config.get("myst", {})
allowed_md_extensions = {
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
}

_heading_achors = _myst_options.get("heading_anchors", None)
if _heading_achors and isinstance(_heading_achors, int) and _heading_achors > 0:
    myst_heading_anchors = _heading_achors


_md_extensions = _myst_options.get("extensions", None)
if _md_extensions and isinstance(_md_extensions, list):
    myst_enable_extensions = [x for x in _md_extensions if x in allowed_md_extensions]
    unknown_md_extensions = [x for x in _md_extensions if x not in allowed_md_extensions]
    if unknown_md_extensions:
        print("Unknown Markdown extensions:", unknown_md_extensions)

_md_substitutions = _myst_options.get("substitutions", None)
if _md_substitutions and isinstance(_md_substitutions, dict):
    myst_substitutions = _md_substitutions


# -- Extra Files -------------------------------------------------------------


if sphinx_config.get("include-changelog"):
    changelog = project_root / Path("CHANGELOG.md")
    dest = project_root / Path("docs/changelog.md")
    copyfile(changelog, dest)

if sphinx_config.get("include-readme"):
    readme = project_root / Path("readme.md")
    dest = project_root / Path("docs/readme.md")
    copyfile(readme, dest)

