# Guía de Instalación - Antioxidant Activity Prediction

Esta guía proporciona instrucciones detalladas paso a paso para instalar el software de predicción de actividad antioxidante utilizando Conda.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:
- **Anaconda** o **Miniconda** (recomendado)
- **Git** (para clonar el repositorio)
- Sistema operativo: Windows, macOS o Linux

## Instalación de Anaconda/Miniconda

Si aún no tienes Anaconda o Miniconda instalado:

### Opción 1: Miniconda (Recomendado - más ligero)
1. Visita [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. Descarga el instalador apropiado para tu sistema operativo
3. Sigue las instrucciones de instalación

### Opción 2: Anaconda (Completo)
1. Visita [https://www.anaconda.com/download](https://www.anaconda.com/download)
2. Descarga el instalador apropiado para tu sistema operativo
3. Sigue las instrucciones de instalación

## Métodos de Instalación

Hay **tres métodos** para configurar el entorno. Elige el que prefieras:

---

## Método 1: Instalación Automática con environment.yml (Recomendado)

Este es el método más rápido y sencillo.

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/juanjosecas/AntioxidantActivity.git
cd AntioxidantActivity
```

O descarga el repositorio como ZIP desde GitHub y descomprímelo.

### Paso 2: Crear el entorno desde el archivo environment.yml
```bash
conda env create -f environment.yml
```

Este comando:
- Crea un entorno llamado `AntioxidantActivity_DPPH`
- Instala Python 3.11
- Instala todas las dependencias necesarias automáticamente

### Paso 3: Activar el entorno
```bash
conda activate AntioxidantActivity_DPPH
```

### Paso 4: Verificar la instalación
```bash
python Main.py --help
```

Deberías ver el mensaje de ayuda del programa.

---

## Método 2: Instalación Manual con requirements.txt

Si prefieres más control sobre la instalación.

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/juanjosecas/AntioxidantActivity.git
cd AntioxidantActivity
```

### Paso 2: Crear un entorno Conda con Python 3.11
```bash
conda create --name AntioxidantActivity_DPPH python=3.11
```

### Paso 3: Activar el entorno
```bash
conda activate AntioxidantActivity_DPPH
```

### Paso 4: Instalar las dependencias desde requirements.txt
```bash
pip install -r requirements.txt
```

### Paso 5: Verificar la instalación
```bash
python Main.py --help
```

---

## Método 3: Instalación Manual Paso a Paso

Para usuarios que quieren instalar cada paquete individualmente.

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/juanjosecas/AntioxidantActivity.git
cd AntioxidantActivity
```

### Paso 2: Crear un entorno Conda
```bash
conda create --name AntioxidantActivity_DPPH python=3.11
```

### Paso 3: Activar el entorno
```bash
conda activate AntioxidantActivity_DPPH
```

### Paso 4: Instalar las dependencias una por una
```bash
pip install scikit-learn==1.4.0
pip install xgboost==2.1.3
pip install rdkit==2023.9.4
pip install mordred==1.2.0
pip install pandas==2.2.0
pip install openpyxl
```

### Paso 5: Verificar la instalación
```bash
python Main.py --help
```

---

## Uso Básico

Una vez instalado, puedes usar el software de las siguientes maneras:

### Predicción de una molécula individual
```bash
conda activate AntioxidantActivity_DPPH
python Main.py --smiles "c1ccccc1O"
```

### Predicción de múltiples moléculas desde un archivo Excel
```bash
conda activate AntioxidantActivity_DPPH
python Main.py --filename test.xlsx
```

### Salida resumida (solo consenso)
```bash
conda activate AntioxidantActivity_DPPH
python Main.py --filename test.xlsx --summary 1
```

---

## Solución de Problemas

### Error: "ModuleNotFoundError"
**Problema**: No se encuentra un módulo de Python.

**Solución**:
```bash
# Asegúrate de que el entorno esté activado
conda activate AntioxidantActivity_DPPH

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "FileNotFoundError" para archivos del modelo
**Problema**: El programa no encuentra los archivos del modelo.

**Solución**:
```bash
# Asegúrate de estar en el directorio correcto
cd /ruta/a/AntioxidantActivity
python Main.py --smiles "..."
```

### Error: "conda: command not found"
**Problema**: Conda no está instalado o no está en el PATH.

**Solución**:
- Reinstala Anaconda/Miniconda
- En Windows, usa "Anaconda Prompt" en lugar de CMD
- En Linux/macOS, reinicia tu terminal o ejecuta: `source ~/.bashrc` (o `~/.zshrc`)

### Error: "invalid smiles!"
**Problema**: La cadena SMILES no es válida.

**Solución**:
- Verifica tu cadena SMILES usando herramientas en línea como [PubChem](https://pubchem.ncbi.nlm.nih.gov/)
- Asegúrate de usar comillas alrededor del SMILES: `--smiles "tu_smiles_aqui"`

### Error: Instalación de RDKit falla
**Problema**: RDKit es difícil de instalar con pip en algunos sistemas.

**Solución alternativa con Conda**:
```bash
conda activate AntioxidantActivity_DPPH
conda install -c conda-forge rdkit=2023.9.4
# Luego instala el resto con pip
pip install scikit-learn==1.4.0 xgboost==2.1.3 mordred==1.2.0 pandas==2.2.0 openpyxl
```

---

## Gestión del Entorno

### Desactivar el entorno
```bash
conda deactivate
```

### Listar todos los entornos Conda
```bash
conda env list
```

### Actualizar paquetes (con precaución)
```bash
conda activate AntioxidantActivity_DPPH
pip install --upgrade scikit-learn xgboost pandas openpyxl
```

**Nota**: Actualizar paquetes puede causar incompatibilidades. Usa las versiones especificadas para garantizar el funcionamiento correcto.

### Eliminar el entorno (si ya no lo necesitas)
```bash
conda deactivate
conda env remove --name AntioxidantActivity_DPPH
```

### Recrear el entorno desde cero
```bash
conda env remove --name AntioxidantActivity_DPPH
conda env create -f environment.yml
```

---

## Verificación de la Instalación

Para verificar que todo está instalado correctamente, ejecuta:

```bash
conda activate AntioxidantActivity_DPPH
python -c "import sklearn, xgboost, rdkit, mordred, pandas; print('Todas las dependencias están instaladas correctamente!')"
```

Si no hay errores, la instalación fue exitosa.

---

## Exportar tu Entorno

Si deseas compartir tu entorno con otros o reproducirlo en otra máquina:

```bash
conda activate AntioxidantActivity_DPPH
conda env export > my_environment.yml
```

O para requirements.txt:
```bash
pip freeze > my_requirements.txt
```

---

## Información Adicional

- **Documentación completa**: Ver `README.md`
- **Análisis QSAR OECD**: Ver `OECD_QSAR_ANALYSIS.md`
- **Código fuente**: Ver `Main.py` (totalmente comentado)
- **Datos de prueba**: Ver `test.xlsx` (archivo de ejemplo)

---

## Soporte

Si encuentras problemas durante la instalación:
1. Revisa esta guía de solución de problemas
2. Verifica que estás usando Python 3.11
3. Asegúrate de que todas las dependencias están instaladas
4. Consulta los [Issues de GitHub](https://github.com/juanjosecas/AntioxidantActivity/issues)

---

**¡Listo para usar!** Una vez completada la instalación, consulta el README.md para ejemplos de uso detallados.
