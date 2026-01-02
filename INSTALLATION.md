# Installation Guide - Antioxidant Activity Prediction

This guide provides detailed step-by-step instructions for installing the Antioxidant Activity prediction software using Conda.

## Prerequisites

Before you begin, make sure you have:
- **Anaconda** or **Miniconda** (recommended)
- **Git** (to clone the repository)
- Operating System: Windows, macOS, or Linux

## Installing Anaconda/Miniconda

If you don't have Anaconda or Miniconda installed yet:

### Option 1: Miniconda (Recommended - lighter)
1. Visit [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. Download the appropriate installer for your operating system
3. Follow the installation instructions

### Option 2: Anaconda (Complete)
1. Visit [https://www.anaconda.com/download](https://www.anaconda.com/download)
2. Download the appropriate installer for your operating system
3. Follow the installation instructions

## Installation Methods

There are **three methods** to set up the environment. Choose the one you prefer:

---

## Method 1: Automatic Installation with environment.yml (Recommended)

This is the fastest and easiest method.

### Step 1: Clone the repository
```bash
git clone https://github.com/juanjosecas/AntioxidantActivity.git
cd AntioxidantActivity
```

Or download the repository as a ZIP from GitHub and extract it.

### Step 2: Create the environment from the environment.yml file
```bash
conda env create -f environment.yml
```

This command will:
- Create an environment named `AntioxidantActivity_DPPH`
- Install Python 3.11
- Automatically install all required dependencies

### Step 3: Activate the environment
```bash
conda activate AntioxidantActivity_DPPH
```

### Step 4: Verify the installation
```bash
python Main.py --help
```

You should see the program's help message.

---

## Method 2: Manual Installation with requirements.txt

If you prefer more control over the installation.

### Step 1: Clone the repository
```bash
git clone https://github.com/juanjosecas/AntioxidantActivity.git
cd AntioxidantActivity
```

### Step 2: Create a Conda environment with Python 3.11
```bash
conda create --name AntioxidantActivity_DPPH python=3.11
```

### Step 3: Activate the environment
```bash
conda activate AntioxidantActivity_DPPH
```

### Step 4: Install dependencies from requirements.txt
```bash
pip install -r requirements.txt
```

### Step 5: Verify the installation
```bash
python Main.py --help
```

---

## Method 3: Step-by-Step Manual Installation

For users who want to install each package individually.

### Step 1: Clone the repository
```bash
git clone https://github.com/juanjosecas/AntioxidantActivity.git
cd AntioxidantActivity
```

### Step 2: Create a Conda environment
```bash
conda create --name AntioxidantActivity_DPPH python=3.11
```

### Step 3: Activate the environment
```bash
conda activate AntioxidantActivity_DPPH
```

### Step 4: Install dependencies one by one
```bash
pip install scikit-learn==1.4.0
pip install xgboost==2.1.3
pip install rdkit==2023.9.4
pip install mordred==1.2.0
pip install pandas==2.2.0
pip install openpyxl
```

### Step 5: Verify the installation
```bash
python Main.py --help
```

---

## Basic Usage

Once installed, you can use the software in the following ways:

### Predict a single molecule
```bash
conda activate AntioxidantActivity_DPPH
python Main.py --smiles "c1ccccc1O"
```

### Predict multiple molecules from an Excel file
```bash
conda activate AntioxidantActivity_DPPH
python Main.py --filename test.xlsx
```

### Summary output (consensus only)
```bash
conda activate AntioxidantActivity_DPPH
python Main.py --filename test.xlsx --summary 1
```

---

## Troubleshooting

### Error: "ModuleNotFoundError"
**Problem**: A Python module cannot be found.

**Solution**:
```bash
# Make sure the environment is activated
conda activate AntioxidantActivity_DPPH

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "FileNotFoundError" for model files
**Problem**: The program cannot find the model files.

**Solution**:
```bash
# Make sure you're in the correct directory
cd /path/to/AntioxidantActivity
python Main.py --smiles "..."
```

### Error: "conda: command not found"
**Problem**: Conda is not installed or not in PATH.

**Solution**:
- Reinstall Anaconda/Miniconda
- On Windows, use "Anaconda Prompt" instead of CMD
- On Linux/macOS, restart your terminal or run: `source ~/.bashrc` (or `~/.zshrc`)

### Error: "invalid smiles!"
**Problem**: The SMILES string is invalid.

**Solution**:
- Verify your SMILES string using online tools like [PubChem](https://pubchem.ncbi.nlm.nih.gov/)
- Make sure to use quotes around the SMILES: `--smiles "your_smiles_here"`

### Error: RDKit installation fails
**Problem**: RDKit is difficult to install with pip on some systems.

**Alternative solution with Conda**:
```bash
conda activate AntioxidantActivity_DPPH
conda install -c conda-forge rdkit=2023.9.4
# Then install the rest with pip
pip install scikit-learn==1.4.0 xgboost==2.1.3 mordred==1.2.0 pandas==2.2.0 openpyxl
```

---

## Environment Management

### Deactivate the environment
```bash
conda deactivate
```

### List all Conda environments
```bash
conda env list
```

### Update packages (with caution)
```bash
conda activate AntioxidantActivity_DPPH
pip install --upgrade scikit-learn xgboost pandas openpyxl
```

**Note**: Updating packages may cause incompatibilities. Use the specified versions to ensure proper functionality.

### Remove the environment (if no longer needed)
```bash
conda deactivate
conda env remove --name AntioxidantActivity_DPPH
```

### Recreate the environment from scratch
```bash
conda env remove --name AntioxidantActivity_DPPH
conda env create -f environment.yml
```

---

## Installation Verification

To verify that everything is installed correctly, run:

```bash
conda activate AntioxidantActivity_DPPH
python -c "import sklearn, xgboost, rdkit, mordred, pandas; print('All dependencies are installed correctly!')"
```

If there are no errors, the installation was successful.

---

## Export Your Environment

If you want to share your environment with others or reproduce it on another machine:

```bash
conda activate AntioxidantActivity_DPPH
conda env export > my_environment.yml
```

Or for requirements.txt:
```bash
pip freeze > my_requirements.txt
```

---

## Additional Information

- **Complete documentation**: See `README.md`
- **OECD QSAR Analysis**: See `OECD_QSAR_ANALYSIS.md`
- **Source code**: See `Main.py` (fully commented)
- **Test data**: See `test.xlsx` (example file)

---

## Support

If you encounter problems during installation:
1. Review this troubleshooting guide
2. Verify you're using Python 3.11
3. Make sure all dependencies are installed
4. Check [GitHub Issues](https://github.com/juanjosecas/AntioxidantActivity/issues)

---

**Ready to use!** Once installation is complete, see README.md for detailed usage examples.
