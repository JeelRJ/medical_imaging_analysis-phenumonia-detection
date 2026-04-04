# Medical Imaging Analysis with R and Python

This project demonstrates medical X-ray analysis using both R and Python, serving as a MATLAB alternative. The project showcases:

1. Data loading and preprocessing in both languages
2. Image processing and feature extraction
3. Machine learning model training and evaluation
4. Interoperability between R and Python
5. Visualization and reporting

## Project Structure

```
medical_imaging_analysis/
├── data/                   # Raw and processed data
├── models/                 # Trained models
├── notebooks/              # Jupyter/R Markdown notebooks
├── output/                 # Analysis outputs and visualizations
├── R/                     # R scripts and functions
│   ├── src/               # Core R source files
│   └── tests/             # R test files
└── Python/                # Python scripts and modules
    ├── src/               # Core Python modules
    └── tests/             # Python test files
```

## Setup Instructions

### Prerequisites

1. Install R (≥ 4.0.0) from [CRAN](https://cran.r-project.org/)
2. Install Python (≥ 3.8) from [python.org](https://www.python.org/downloads/)
3. Install RStudio (recommended) from [rstudio.com](https://www.rstudio.com/products/rstudio/download/)
4. Install Jupyter Lab (recommended) via `pip install jupyterlab`

### Python Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # On Windows

# Install Python dependencies
pip install -r requirements.txt

# Install Python kernel for Jupyter
python -m ipykernel install --user --name=medical_imaging --display-name="Python (Medical Imaging)"
```

### R Environment Setup

```r
# Install required R packages
source("R/install_packages.R")

# Install R kernel for Jupyter
install.packages('IRkernel')
IRkernel::installspec(name = 'ir', displayname = 'R (Medical Imaging)')
```

## Usage

1. **Data Preparation**
   - Place your medical images in the `data/raw/` directory
   - Run preprocessing scripts in `Python/src/preprocessing.py` or `R/src/preprocessing.R`

2. **Analysis**
   - Use the Jupyter notebooks in `notebooks/` for interactive analysis
   - Or run the scripts directly:
     ```
     python Python/src/analyze.py
     Rscript R/src/analyze.R
     ```

3. **Interoperability**
   - Use `reticulate` in R to call Python functions
   - Use `rpy2` in Python to call R functions
   - Example notebooks are provided in `notebooks/interop/`

## Example Workflow

1. **Data Loading and Preprocessing**
   ```r
   # R
   source("R/src/load_data.R")
   xray_data <- load_xray_data("data/raw/")
   processed_data <- preprocess_images(xray_data)
   ```

   ```python
   # Python
   from src.preprocessing import load_xray_data, preprocess_images
   
   xray_data = load_xray_data("data/raw/")
   processed_data = preprocess_images(xray_data)
   ```

2. **Feature Extraction**
   - Both R and Python implementations are provided for common image processing tasks

3. **Model Training**
   - Train models using either language
   - Save models in a format that can be loaded by both languages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
