# Antioxidant Activity Prediction: QSAR Model for DPPH Assay

## Overview

This software provides **in silico prediction of antioxidant activity** for small organic molecules (< 1000 Da) using machine learning-based QSAR (Quantitative Structure-Activity Relationship) models. The tool predicts the half-maximal inhibitory concentration (IC50) in the DPPH (2,2-diphenyl-1-picrylhydrazyl) radical scavenging assay, a widely used method for assessing antioxidant capacity.

### Key Features
- 🎯 **Ensemble prediction**: Combines three machine learning algorithms (Extra Trees, XGBoost, Gradient Boosting) for robust predictions
- 📊 **Uncertainty quantification**: Provides confidence estimates through model variance
- 🔍 **Applicability domain assessment**: Identifies whether predictions are reliable for your molecule
- ⚡ **Fast predictions**: Processes single molecules or batches from Excel files
- 📈 **Multiple output units**: Results in both molar (-log IC50) and practical (mg/L) concentration units

### Target Audience
- Researchers screening natural products or synthetic compounds for antioxidant activity
- Medicinal chemists designing molecules with radical scavenging properties
- Food scientists evaluating potential preservatives or nutraceuticals
- Computational toxicologists assessing oxidative stress-related properties

---

## Scientific Background

**Antioxidant Activity**: The ability of a molecule to scavenge free radicals and prevent oxidative damage, which is relevant to aging, inflammation, and various diseases.

**DPPH Assay**: A colorimetric assay measuring the reduction of the DPPH radical (purple) to DPPH-H (yellow) by antioxidant compounds. The IC50 value represents the concentration needed to reduce 50% of DPPH radicals after 30 minutes.

**Output Interpretation**:
- **Lower IC50 values** = **Higher antioxidant activity** (less compound needed for radical scavenging)
- **-log(IC50)** in molar units provides a normalized scale (higher values = more potent)
- **IC50 in mg/L** provides practical concentration units for experimental design

---

## Installation

> 📚 **Detailed Installation Guides Available:**
> - 🇬🇧 **English**: See [INSTALLATION.md](INSTALLATION.md) for comprehensive installation instructions
> - 🇪🇸 **Español**: Ver [INSTALACION.md](INSTALACION.md) para instrucciones detalladas de instalación

### Quick Start (3 methods available)

**Method 1: Automatic Setup (Recommended)**
```bash
git clone https://github.com/juanjosecas/AntioxidantActivity.git
cd AntioxidantActivity
conda env create -f environment.yml
conda activate AntioxidantActivity_DPPH
```

**Method 2: Using Setup Scripts**
- **Linux/macOS**: `./setup.sh`
- **Windows**: `setup.bat` (run in Anaconda Prompt)

**Method 3: Manual Installation**
```bash
git clone https://github.com/juanjosecas/AntioxidantActivity.git
cd AntioxidantActivity
conda create --name AntioxidantActivity_DPPH python=3.11
conda activate AntioxidantActivity_DPPH
pip install -r requirements.txt
```

### Prerequisites
- **Python 3.11** (recommended for compatibility)
- **Anaconda** or **Miniconda** (for environment management)
- **Excel files** (.xlsx) for batch mode (optional)

### Verify Installation
```bash
conda activate AntioxidantActivity_DPPH
python Main.py --help
```

You should see the help message with usage instructions.

---

## Usage

### Before You Start
- Ensure you're in the `AntioxidantActivity` directory
- Activate the conda environment: `conda activate AntioxidantActivity_DPPH`
- Prepare your molecules as SMILES strings (see examples below)

### Input Format

**SMILES Notation**: Simplified Molecular Input Line Entry System
- Examples: 
  - Benzene: `c1ccccc1`
  - Phenethylamine: `c1ccccc1CCN`
  - Quercetin: `O=c1c(O)c(-c2ccc(O)c(O)c2)oc2cc(O)cc(O)c12`

**Excel File Format** (for batch mode):
- Must contain a column named **`SMILES`** (case-sensitive)
- Additional columns are preserved in the output
- Example file: `test.xlsx` (included in repository)

---

### Command-Line Interface

#### General Syntax
```bash
python Main.py [--smiles SMILES | --filename FILE] [--summary 1]
```

#### Option 1: Single Molecule Prediction
```bash
python Main.py --smiles "SMILES_STRING"
```

**Example**:
```bash
python Main.py --smiles "c1ccccc1O"
```
Predicts antioxidant activity of phenol.

#### Option 2: Batch Prediction from File
```bash
python Main.py --filename INPUT_FILE.xlsx
```

**Example**:
```bash
python Main.py --filename test.xlsx
```
Processes all molecules in the file.

#### Optional: Summary Output Mode
```bash
python Main.py --smiles "SMILES_STRING" --summary 1
```

**Effect**:
- Default (no `--summary` or `--summary None`): Outputs all individual model predictions
- `--summary 1`: Outputs only consensus prediction, uncertainty, and applicability domain (simplified)

---

### Usage Examples

#### Example 1: Predict Activity for Vitamin C
```bash
python Main.py --smiles "OC[C@H](O)[C@H]1OC(=O)C(O)=C1O"
```

#### Example 2: Batch Process Multiple Molecules
```bash
python Main.py --filename test.xlsx
```

#### Example 3: Get Summary Output Only
```bash
python Main.py --filename test.xlsx --summary 1
```

#### Example 4: Screen Natural Product Library
```bash
# Create an Excel file with SMILES column
python Main.py --filename natural_products.xlsx --summary 1
```

---

## Output Files

### Full Output (default)
**Filename**: `Predictions_DD_MM_YYYY.xlsx`

**Columns**:
- `SMILES`: Input molecular structure
- `Predictions_ETR [-log(IC50) M]`: Extra Trees model prediction (molar units)
- `Predictions_ETR [mg/L]`: Extra Trees model prediction (mg/L)
- `Predictions_XGB [-log(IC50) M]`: XGBoost model prediction (molar units)
- `Predictions_XGB [mg/L]`: XGBoost model prediction (mg/L)
- `Predictions_GB [-log(IC50) M]`: Gradient Boosting model prediction (molar units)
- `Predictions_GB [mg/L]`: Gradient Boosting model prediction (mg/L)
- `Consensus [-log(IC50) M]`: Mean prediction across all models (molar units)
- `Consensus [mg/L]`: Mean prediction across all models (mg/L)
- `Interval [-log(IC50) M]`: Standard deviation (uncertainty) in molar units
- `Interval [mg/L]`: Standard deviation (uncertainty) in mg/L
- `Consensus AND Uncertanty [mg/L]`: Formatted as "mean ± std"
- `Applicability Domain`: 1 = reliable prediction, 0 = outside training data range (use with caution)

### Summary Output (`--summary 1`)
**Filename**: `Summary_predictions_DD_MM_YYYY.xlsx`

**Columns**:
- `SMILES`: Input molecular structure
- `Consensus AND Uncertanty [mg/L]`: Predicted IC50 with uncertainty (mean ± std)
- `Applicability Domain`: Reliability indicator (1 = reliable, 0 = caution)

---

## Interpreting Results

### Understanding Predictions

1. **IC50 Values**:
   - **Lower values** = **More potent antioxidant** (e.g., IC50 = 10 mg/L is better than 100 mg/L)
   - Typical ranges:
     - Strong antioxidants: < 50 mg/L
     - Moderate antioxidants: 50-200 mg/L
     - Weak antioxidants: > 200 mg/L

2. **Uncertainty (Interval)**:
   - Represents disagreement between the three models
   - **Low uncertainty** (small std): High confidence, models agree
   - **High uncertainty** (large std): Lower confidence, models disagree
   - If uncertainty > 30% of predicted value, interpret with caution

3. **Applicability Domain**:
   - **AD = 1**: Molecule is within the training data chemical space → prediction is reliable
   - **AD = 0**: Molecule is outside training data → prediction may be unreliable
   - **Always check AD before trusting predictions!**

### Example Interpretation

```
SMILES: c1ccc(O)cc1
Consensus: 150.5 ± 12.3 mg/L
Applicability Domain: 1
```

**Interpretation**: The predicted IC50 for this compound is ~150 mg/L (moderate antioxidant activity). The low uncertainty (±12.3 mg/L, ~8% of predicted value) indicates high confidence. AD = 1 confirms the prediction is reliable. This compound would require approximately 150 mg/L to scavenge 50% of DPPH radicals.

---

## Model Information

### Algorithm
- **Ensemble of three machine learning models**:
  1. **Extra Trees Regressor**: Uses extremely randomized decision trees
  2. **XGBoost Regressor**: Gradient boosting with regularization
  3. **Gradient Boosting Regressor**: Sequential ensemble of decision trees

- **Consensus prediction**: Arithmetic mean of three models (reduces bias)
- **Uncertainty**: Standard deviation across models (quantifies confidence)

### Features
- **Molecular descriptors**: >1800 2D structural and physicochemical descriptors (Mordred library)
- **Preprocessing**: Feature selection, imputation, and scaling for optimal performance

### Training Data
- **Endpoint**: DPPH radical scavenging IC50 at 30 minutes
- **Dataset**: Expert-curated antioxidant molecules (< 1000 Da)

### Validation
- Ensemble approach reduces overfitting and improves generalization
- Applicability domain ensures predictions are within training data scope
- See `OECD_QSAR_ANALYSIS.md` for detailed OECD validation analysis

---

## Limitations and Considerations

### Important Notes

1. **In Silico Predictions**: These are computational predictions. Always validate important results experimentally.

2. **Applicability Domain**: Predictions outside the AD (AD = 0) may be unreliable. Use with caution and consider experimental validation.

3. **Molecular Size**: Model is trained on small molecules (< 1000 Da). Performance on larger molecules is not validated.

4. **Assay Specificity**: Predictions are specific to the DPPH assay at 30 minutes. Other antioxidant assays (ABTS, FRAP, ORAC) may give different results.

5. **Chemical Diversity**: Model performs best on drug-like organic molecules. Performance on exotic chemistries (organometallics, highly charged species) is uncertain.

6. **Not for Regulatory Decisions**: While the model follows OECD principles, additional documentation and validation are required for regulatory submissions.

### When to Use Experimental Validation
- When AD = 0 (outside applicability domain)
- When uncertainty is high (> 30% of predicted value)
- For lead compounds in drug development
- For regulatory or safety-critical applications

---

## Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'pandas'`
- **Solution**: Ensure you've activated the conda environment:
  ```bash
  conda activate AntioxidantActivity_DPPH
  ```

**Problem**: `FileNotFoundError` for model files
- **Solution**: Ensure you're running the script from the `AntioxidantActivity` directory:
  ```bash
  cd /path/to/AntioxidantActivity
  python Main.py --smiles "..."
  ```

**Problem**: `KeyError: 'SMILES'` when processing Excel file
- **Solution**: Your Excel file must have a column named exactly `SMILES` (case-sensitive). Rename the column if needed.

**Problem**: `invalid smiles!` error
- **Solution**: Verify your SMILES string is correct using online tools like [PubChem Sketcher](https://pubchem.ncbi.nlm.nih.gov/edit3/index.html) or [ChemSpider](http://www.chemspider.com/).

**Problem**: Predictions look unreasonable
- **Solution**: Check the Applicability Domain value. If AD = 0, the molecule may be too different from training data.

---

## Citation

If you use this software in your research, please cite:

```
[Citation to be added - please contact the authors]
```

---

## License

[License information to be added]

---

## Contact and Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/juanjosecas/AntioxidantActivity/issues)
- **Authors**: [Contact information to be added]

---

## Additional Resources

### Related Documentation
- `OECD_QSAR_ANALYSIS.md`: Detailed analysis of model quality and OECD compliance
- `Main.py`: Fully commented source code explaining the prediction workflow

### External Resources
- [RDKit Documentation](https://www.rdkit.org/docs/)
- [Mordred: Molecular Descriptor Calculator](https://github.com/mordred-descriptor/mordred)
- [OECD QSAR Toolbox](https://www.oecd.org/chemicalsafety/risk-assessment/oecd-qsar-toolbox.htm)
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/): Convert molecular names to SMILES

### Example Antioxidants to Test
- **Vitamin E** (α-tocopherol): `CC1=C(C)C2=C(CCC(C)(CCCC(C)CCCC(C)CCCC(C)C)O2)C(C)=C1O`
- **Resveratrol**: `Oc1ccc(cc1)C=Cc1cc(O)cc(O)c1`
- **Gallic acid**: `OC(=O)c1cc(O)c(O)c(O)c1`
- **Catechin**: `Oc1cc(O)c2c(c1)O[C@H](c1ccc(O)c(O)c1)[C@H](O)C2`

---

## Version History

### Version 1.1 (Current)
- Added comprehensive code comments
- Created OECD QSAR analysis document
- Improved README with detailed usage instructions
- Enhanced output to include SMILES in summary mode

### Version 1.0
- Initial release
- Ensemble QSAR model for DPPH antioxidant activity prediction
- Applicability domain assessment
- Command-line interface

---

## Acknowledgments

This work builds upon:
- **RDKit**: Open-source cheminformatics toolkit
- **Mordred**: Comprehensive molecular descriptor calculator
- **Scikit-learn, XGBoost**: Machine learning libraries
- **OECD QSAR Framework**: Principles for model validation

---

**Note**: This is a research tool. Always validate computational predictions with experimental data for critical applications.
 
