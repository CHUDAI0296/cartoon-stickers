#!/bin/bash

# Install Elixir dependencies
mix deps.get --only prod

# Compile assets
mix assets.deploy

# Generate static files
mix phx.digest

# Copy static files to public directory for Vercel
mkdir -p public
cp -r priv/static/* public/

echo "Build completed!"