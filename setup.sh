#!/bin/bash

# Setup script for Antioxidant Activity Prediction
# This script automates the environment setup process

set -e  # Exit on error

echo "=========================================="
echo "Antioxidant Activity - Environment Setup"
echo "=========================================="
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "ERROR: conda could not be found"
    echo "Please install Anaconda or Miniconda first:"
    echo "  - Miniconda: https://docs.conda.io/en/latest/miniconda.html"
    echo "  - Anaconda: https://www.anaconda.com/download"
    exit 1
fi

echo "✓ Conda found: $(conda --version)"
echo ""

# Environment name
ENV_NAME="AntioxidantActivity_DPPH"

# Check if environment already exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "⚠ Environment '${ENV_NAME}' already exists."
    read -p "Do you want to remove it and recreate? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing environment..."
        conda env remove --name ${ENV_NAME} -y
    else
        echo "Aborting setup. You can activate the existing environment with:"
        echo "  conda activate ${ENV_NAME}"
        exit 0
    fi
fi

# Create environment
echo "Creating conda environment '${ENV_NAME}'..."
if [ -f "environment.yml" ]; then
    echo "Using environment.yml..."
    conda env create -f environment.yml
else
    echo "environment.yml not found, creating environment manually..."
    conda create --name ${ENV_NAME} python=3.11 -y
    
    # Activate and install dependencies
    eval "$(conda shell.bash hook)"
    conda activate ${ENV_NAME}
    
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
    else
        echo "requirements.txt not found, installing dependencies manually..."
        pip install scikit-learn==1.4.0 xgboost==2.1.3 rdkit==2023.9.4 mordred==1.2.0 pandas==2.2.0 openpyxl
    fi
fi

echo ""
echo "=========================================="
echo "✓ Setup completed successfully!"
echo "=========================================="
echo ""
echo "To use the software:"
echo "  1. Activate the environment:"
echo "     conda activate ${ENV_NAME}"
echo ""
echo "  2. Run a prediction:"
echo "     python Main.py --smiles \"c1ccccc1O\""
echo ""
echo "  3. Or process a file:"
echo "     python Main.py --filename test.xlsx"
echo ""
echo "For more information, see README.md or INSTALLATION.md"
echo ""
