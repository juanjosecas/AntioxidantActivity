@echo off
REM Setup script for Antioxidant Activity Prediction
REM This script automates the environment setup process

echo ==========================================
echo Antioxidant Activity - Environment Setup
echo ==========================================
echo.

REM Check if conda is available
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: conda could not be found
    echo Please install Anaconda or Miniconda first:
    echo   - Miniconda: https://docs.conda.io/en/latest/miniconda.html
    echo   - Anaconda: https://www.anaconda.com/download
    echo.
    echo If you just installed conda, restart your terminal or use Anaconda Prompt
    pause
    exit /b 1
)

conda --version
echo.

REM Environment name
set ENV_NAME=AntioxidantActivity_DPPH

REM Check if environment already exists
conda env list | findstr /C:"%ENV_NAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo WARNING: Environment '%ENV_NAME%' already exists.
    set /p REMOVE="Do you want to remove it and recreate? (y/n): "
    if /i "%REMOVE%"=="y" (
        echo Removing existing environment...
        call conda env remove --name %ENV_NAME% -y
    ) else (
        echo Aborting setup. You can activate the existing environment with:
        echo   conda activate %ENV_NAME%
        pause
        exit /b 0
    )
)

REM Create environment
echo Creating conda environment '%ENV_NAME%'...
if exist "environment.yml" (
    echo Using environment.yml...
    call conda env create -f environment.yml
) else (
    echo environment.yml not found, creating environment manually...
    call conda create --name %ENV_NAME% python=3.11 -y
    
    REM Activate and install dependencies
    call conda activate %ENV_NAME%
    
    if exist "requirements.txt" (
        echo Installing dependencies from requirements.txt...
        pip install -r requirements.txt
    ) else (
        echo requirements.txt not found, installing dependencies manually...
        pip install scikit-learn==1.4.0 xgboost==2.1.3 rdkit==2023.9.4 mordred==1.2.0 pandas==2.2.0 openpyxl
    )
)

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo To use the software:
echo   1. Activate the environment:
echo      conda activate %ENV_NAME%
echo.
echo   2. Run a prediction:
echo      python Main.py --smiles "c1ccccc1O"
echo.
echo   3. Or process a file:
echo      python Main.py --filename test.xlsx
echo.
echo For more information, see README.md or INSTALLATION.md
echo.
pause
