#! /bin/bash

set -e

# This script deploys the documentation to the gh-pages branch

# build the docs
uv run mkdocs build

# deploy to gh-pages
uv run mkdocs gh-deploy
