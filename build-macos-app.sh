#!/bin/sh

# Clean build and dist directories if they exist

if [ -d "build" ]; then
    echo "Removing build directory..."
    rm -r build
fi

if [ -d "dist" ]; then
    echo "Removing dist directory..."
    rm -r dist
fi

# Build the app

echo "Building app..."

python setup.py py2app

echo "Done building app, you can find it in the dist folder."
