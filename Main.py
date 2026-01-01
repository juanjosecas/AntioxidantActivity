"""
Antioxidant Activity QSAR Prediction Model

This script implements a consensus QSAR (Quantitative Structure-Activity Relationship) model
for predicting antioxidant activity (DPPH 30min assay) of small molecules. The model uses
an ensemble of three machine learning algorithms and includes applicability domain assessment.

The script follows OECD principles for QSAR validation by providing:
- Defined endpoint (DPPH IC50)
- Unambiguous algorithm (ensemble of ExtraTrees, XGBoost, GradientBoosting)
- Applicability domain assessment
- Uncertainty quantification through consensus predictions
"""

import pandas as pd
import pickle
import os
from mordred import Calculator, descriptors, error

from rdkit import Chem
from rdkit.Chem.Descriptors import MolWt
import numpy as np
import argparse
import sys
from datetime import datetime


def mordred_calculator(dataset: pd.DataFrame):
    """
    Calculate molecular descriptors using the Mordred library.
    
    This function computes a comprehensive set of 2D molecular descriptors (>1800 descriptors)
    that characterize the structural, topological, and physicochemical properties of molecules.
    These descriptors are used as features for the QSAR machine learning models.
    
    Args:
        dataset (pd.DataFrame): Input dataset with a "SMILES" column containing molecular structures
                               in SMILES notation (Simplified Molecular Input Line Entry System)

    Returns:
        pd.DataFrame: The original dataset concatenated with all calculated molecular descriptors.
                     Error values from descriptor calculation are replaced with NaN for robustness.
    """
    # Convert SMILES strings to RDKit molecule objects for descriptor calculation
    mols = [Chem.MolFromSmiles(smi) for smi in dataset['SMILES']]
    
    # Initialize Mordred calculator with all 2D descriptors (ignore_3D=True excludes 3D conformers)
    calc = Calculator(descriptors, ignore_3D=True)
    
    # Calculate descriptors and return as pandas DataFrame
    df = calc.pandas(mols)
    
    # Combine original dataset with calculated descriptors
    df = pd.concat([dataset, df], axis=1)

    # Replace any calculation errors or missing values with NaN for downstream processing
    df = df.applymap(lambda x: np.nan if isinstance(x, error.Error) or isinstance(x, error.Missing) else x)
    return df

def check_smiles(smiles):
    """
    Validate SMILES string format.
    
    This function attempts to parse a SMILES string to verify it represents a valid molecular structure.
    If invalid, the program exits with an error message to prevent processing of malformed input.
    
    Args:
        smiles (str): SMILES notation string to validate
        
    Raises:
        SystemExit: If SMILES is invalid, exits with code 1
    """
    try:
        Chem.MolFromSmiles(smiles)
    except:
        print(f"{smiles}: invalid smiles!")
        sys.exit(1)

def pipeline_model_importer():
    """
    Load pre-trained models, preprocessing pipeline, and applicability domain classifier.
    
    This function loads all necessary components for the QSAR prediction:
    - Three ensemble regression models (Extra Trees, XGBoost, Gradient Boosting)
    - Feature preprocessing pipeline (handles feature selection, scaling, and transformation)
    - Applicability Domain (AD) classifier to assess prediction reliability
    
    The ensemble approach improves prediction robustness by combining multiple algorithms,
    each with different learning biases and strengths.
    
    Returns:
        tuple: (model1, model2, model3, pipeline, ad)
            - model1: Extra Trees Regressor - ensemble of randomized decision trees
            - model2: XGBoost Regressor - gradient boosting with extreme gradient optimization
            - model3: Gradient Boosting Regressor - sequential ensemble of decision trees
            - pipeline: Preprocessing pipeline for feature transformation
            - ad: Applicability Domain classifier for reliability assessment
    """
    # Load Extra Trees Regressor model
    # Extra Trees uses fully random splits, reducing variance and overfitting
    with open(os.path.join(os.getcwd(), 'models', 'alldata_model_Antioxidant_DPPH30MIN_extra_trees_regressor.pkl'), 'rb') as f:
        model1 = pickle.load(f)

    # Load XGBoost Regressor model
    # XGBoost optimizes a regularized objective function and uses advanced gradient boosting
    with open(os.path.join(os.getcwd(),'models', 'alldata_model_Antioxidant_DPPH30MIN_xgb_regressor.pkl'), 'rb') as f:
        model2 = pickle.load(f)
    
    # Load Gradient Boosting Regressor model
    # Sequential ensemble that builds trees to correct errors of previous trees
    with open(os.path.join(os.getcwd(),'models', 'alldata_model_Antioxidant_DPPH30MIN_gradient_boosting_regressor.pkl'), 'rb') as f:
        model3 = pickle.load(f)

    # Load preprocessing pipeline
    # Handles feature selection, imputation, scaling to ensure consistent data transformation
    with open(os.path.join(os.getcwd(), 'pipeline_and_AD', 'pipeline_Antioxidant_DPPH30MIN.pkl'), 'rb') as f:
        pipeline = pickle.load(f)

    # Load Applicability Domain classifier
    # Determines if query molecules are within the chemical space covered by training data
    # Predictions for molecules outside AD should be interpreted with caution
    with open(os.path.join(os.getcwd(), 'pipeline_and_AD', 'AD_clf.pkl'), 'rb') as f:
        ad = pickle.load(f)
        
    return model1, model2, model3, pipeline, ad

def files_importer():
    """
    Parse command-line arguments to handle input (single SMILES or batch file).
    
    This function configures the argument parser for two mutually exclusive input modes:
    - Single molecule mode: User provides one SMILES string directly
    - Batch mode: User provides an Excel file (.xlsx) with multiple molecules
    
    Returns:
        tuple: (input_value, summary)
            - input_value (str): Either a SMILES string or filename path
            - summary (str or None): Flag indicating output format preference
    """
    parser = argparse.ArgumentParser(description='Antioxidant assesment')
    
    # Create mutually exclusive group: user must provide either SMILES or filename, but not both
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--smiles', required=False, help='Specify target SMILES')
    group.add_argument('--filename', required=False, help='Specify xlsx file with molecules to predict')
    
    # Optional flag to control output detail level
    parser.add_argument('--summary', default=None, help='Specify if you want prediction from all models or only the consensus (default: summary=None) ones')
    
    args = parser.parse_args()
    
    # Extract the input value (either SMILES string or filename)
    input_value = args.smiles
    if input_value is None:
        input_value = args.filename
        
    print(f"Input value: {input_value}")
    return input_value, args.summary


if __name__ == '__main__':
    # ============================================================================
    # MAIN EXECUTION PIPELINE
    # ============================================================================
    # This section orchestrates the complete workflow:
    # 1. Input parsing (SMILES or batch file)
    # 2. Molecular descriptor calculation
    # 3. Data preprocessing
    # 4. Ensemble model predictions (3 models)
    # 5. Consensus prediction and uncertainty estimation
    # 6. Applicability domain assessment
    # 7. Results export
    
    print("Antioxidant Model:\nExtra trees model to predict IC50 (log(ug/ml))")
    
    # Parse command-line arguments to get input and output preferences
    input_value, summary = files_importer()
    
    # ============================================================================
    # STEP 1: INPUT DATA PREPARATION
    # ============================================================================
    # Handle two input modes:
    # - Single SMILES string: create DataFrame with one row
    # - Excel file: read multiple molecules from file
    if ".xlsx" not in input_value: 
        df = pd.DataFrame([input_value], columns=['SMILES'])
    else:
        df = pd.read_excel(input_value)
    
    # ============================================================================
    # STEP 2: LOAD PRE-TRAINED MODELS AND PIPELINE
    # ============================================================================
    # Import the trained models, preprocessing pipeline, and AD classifier
    model1, model2, model3, pipeline, ad = pipeline_model_importer()
    
    # ============================================================================
    # STEP 3: CALCULATE MOLECULAR DESCRIPTORS
    # ============================================================================
    # Compute >1800 2D molecular descriptors using Mordred
    # These descriptors encode structural and physicochemical properties
    print("Molecular descriptors calculation....\n")
    data = mordred_calculator(df)
    
    # ============================================================================
    # STEP 4: PREPROCESS DESCRIPTORS
    # ============================================================================
    # Apply preprocessing pipeline: feature selection, imputation, scaling
    # Ensures data is in the same format as training data
    print("MDs tranformation...\n")
    data_input = pd.DataFrame(pipeline.transform(data.loc[:, pipeline.feature_names_in_]), 
                              columns=pipeline.feature_names_in_)
    
    # ============================================================================
    # STEP 5: GENERATE PREDICTIONS FROM ENSEMBLE MODELS
    # ============================================================================
    print("Model Assessment...")
    
    # Calculate molecular weight for unit conversion (M to mg/L)
    mw_calc = [MolWt(Chem.MolFromSmiles(smi)) for smi in df['SMILES']]
    
    # --- Extra Trees Regressor Predictions ---
    # Predicts -log(IC50) in molar units
    df['Predictions_ETR [-log(IC50) M]'] = model1.predict(data_input.loc[:, model1.feature_names_in_])
    # Convert from -log(IC50) M to mg/L: IC50 = 10^(-log(IC50)) * MW * 1000
    df['Predictions_ETR [mg/L]'] = [(10**-(c))*mw_*1000 for c, mw_ in zip(df['Predictions_ETR [-log(IC50) M]'], mw_calc)]

    # --- XGBoost Regressor Predictions ---
    df['Predictions_XGB [-log(IC50) M]'] = model2.predict(data_input.loc[:, model2.feature_names_in_])
    df['Predictions_XGB [mg/L]'] = [(10**-(c))*mw_*1000 for c, mw_ in zip(df['Predictions_XGB [-log(IC50) M]'], mw_calc)]

    # --- Gradient Boosting Regressor Predictions ---
    df['Predictions_GB [-log(IC50) M]'] = model3.predict(data_input.loc[:, model3.feature_names_in_])
    df['Predictions_GB [mg/L]'] = [(10**-(c))*mw_*1000 for c, mw_ in zip(df['Predictions_GB [-log(IC50) M]'], mw_calc)]

    # ============================================================================
    # STEP 6: CONSENSUS PREDICTION AND UNCERTAINTY QUANTIFICATION
    # ============================================================================
    # Consensus prediction: mean of the three model predictions
    # This ensemble approach reduces model-specific biases and improves robustness
    df['Consensus [-log(IC50) M]'] = [np.mean([y1, y2, y3]) for y1, y2, y3 in zip(df['Predictions_ETR [-log(IC50) M]'], df['Predictions_XGB [-log(IC50) M]'], df['Predictions_GB [-log(IC50) M]'])]
    
    # Uncertainty interval: standard deviation across the three models
    # Higher std indicates greater disagreement between models, suggesting lower confidence
    df['Interval [-log(IC50) M]'] = [np.std([y1, y2, y3]) for y1, y2, y3 in zip(df['Predictions_ETR [-log(IC50) M]'], df['Predictions_XGB [-log(IC50) M]'], df['Predictions_GB [-log(IC50) M]'])]
    
    # Consensus and uncertainty in mg/L units
    df['Consensus [mg/L]'] = [np.mean([y1, y2, y3]) for y1, y2, y3 in zip(df['Predictions_ETR [mg/L]'], df['Predictions_XGB [mg/L]'], df['Predictions_GB [mg/L]'])]
    df['Interval [mg/L]'] = [np.std([y1, y2, y3]) for y1, y2, y3 in zip(df['Predictions_ETR [mg/L]'], df['Predictions_XGB [mg/L]'], df['Predictions_GB [mg/L]'])]

    # Round all numeric values to 3 decimal places for cleaner output
    df = round(df, 3)
    
    # Format consensus with uncertainty as "mean ± std" for easier interpretation
    df['Consensus AND Uncertanty [mg/L]'] = [f"{str(y)} \u00B1 {i}" for y, i in zip(df['Consensus [mg/L]'], df['Interval [mg/L]'])] 
    
    # ============================================================================
    # STEP 7: APPLICABILITY DOMAIN ASSESSMENT
    # ============================================================================
    # Classify whether molecules fall within the applicability domain
    # 1 = within AD (reliable prediction), 0 = outside AD (use with caution)
    df['Applicability Domain'] = ad.predict(data_input.loc[:, model2.feature_names_in_])
    
    # ============================================================================
    # STEP 8: EXPORT RESULTS
    # ============================================================================
    # Generate timestamp for unique output filenames
    current_date = datetime.now().strftime("%d_%m_%Y")
    
    # Export results based on summary flag:
    # - summary=True: only consensus and AD (simplified output)
    # - summary=False/None: all predictions and detailed information
    if summary:
        df.loc[:, ['SMILES', 'Consensus AND Uncertanty [mg/L]', 'Applicability Domain']].to_excel(f'Summary_predictions_{current_date}.xlsx')
        print(df.loc[:, ['SMILES', 'Consensus AND Uncertanty [mg/L]', 'Applicability Domain']])
    else:
        df.to_excel(f'Predictions_{current_date}.xlsx')
        print(df)
    
    
    
    
        
        

        