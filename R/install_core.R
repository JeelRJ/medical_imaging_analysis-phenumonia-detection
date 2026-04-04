# Install core R packages
install.packages(c(
  # Data manipulation
  'tidyverse',    # Includes dplyr, ggplot2, tidyr, etc.
  'data.table',   # Fast data manipulation
  'magrittr',     # Pipe operator
  
  # Image processing
  'imager',       # Image processing based on CImg
  'magick',       # Advanced image processing
  'imagerExtra',  # Additional image processing functions
  
  # Visualization
  'ggplot2',      # Advanced plotting
  'plotly',       # Interactive plots
  'RColorBrewer', # Color palettes
  'viridis',      # Color-blind friendly palettes
  
  # Reporting
  'rmarkdown',    # Dynamic documents
  'knitr',        # Report generation
  'officer',      # MS Office documents
  'flextable',    # Formatted tables
  
  # Development
  'devtools',     # Package development
  'testthat',     # Unit testing
  'roxygen2',     # Documentation
  'usethis'       # Project setup
), dependencies = TRUE)

# Install Bioconductor packages
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c(
  'EBImage',     # Image processing and analysis
  'rhdf5',       # HDF5 interface
  'EBImage'      # Image processing
))

# Install GitHub packages if needed
github_pkgs <- c(
  # Add any GitHub packages here if needed
)

if (length(github_pkgs) > 0) {
  if (!requireNamespace("remotes", quietly = TRUE)) {
    install.packages("remotes")
  }
  remotes::install_github(github_pkgs)
}

# Install IRkernel for Jupyter
if (!"IRkernel" %in% installed.packages()) {
  install.packages("IRkernel")
  IRkernel::installspec(name = 'ir', displayname = 'R (Medical Imaging)')
}

# Verify installations
cat("\nVerifying package installations...\n")
required_pkgs <- c(
  'tidyverse', 'data.table', 'magrittr', 'imager', 'magick', 
  'imagerExtra', 'ggplot2', 'plotly', 'rmarkdown', 'knitr',
  'EBImage', 'rhdf5'
)

missing_pkgs <- required_pkgs[!sapply(required_pkgs, requireNamespace, quietly = TRUE)]
if (length(missing_pkgs) == 0) {
  cat("All required R packages are installed successfully!\n")
} else {
  cat("The following packages could not be installed:\n")
  print(missing_pkgs)
  cat("Please install them manually.\n")
}

# Install reticulate for Python integration
if (!"reticulate" %in% installed.packages()) {
  install.packages("reticulate")
  # Configure reticulate to use the Python virtual environment
  reticulate::use_virtualenv("../venv")
}
