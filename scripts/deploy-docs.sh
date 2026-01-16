#! /bin/bash

set -e

# This script deploys the documentation to the gh-pages branch

uv sync --group docs

# build the docs
uv run mkdocs build

# deploy to gh-pages
uv run mkdocs gh-deploy

uv sync --all-extras