# List of required R packages
required_pkgs <- c(
  # Data manipulation
  "tidyverse",    # Includes dplyr, ggplot2, tidyr, etc.
  "data.table",   # Fast data manipulation
  "magrittr",     # Pipe operator
  
  # Image processing
  "EBImage",      # Image processing and analysis
  "imager",       # Image processing based on CImg
  "magick",       # Advanced image processing
  "oro.dicom",    # DICOM image reading
  "oro.nifti",    # NIfTI format support
  
  # Machine learning
  "caret",        # Classification and regression training
  "randomForest", # Random forest implementation
  "e1071",        # SVM and other ML algorithms
  "keras",        # Deep learning
  "tensorflow",   # TensorFlow interface
  "reticulate",   # Python-R integration
  
  # Visualization
  "ggplot2",      # Advanced plotting
  "plotly",       # Interactive plots
  "RColorBrewer", # Color palettes
  "viridis",      # Color-blind friendly palettes
  
  # Reporting
  "rmarkdown",    # Dynamic documents
  "knitr",        # Report generation
  "officer",      # MS Office documents
  "flextable",    # Formatted tables
  
  # Development
  "devtools",     # Package development
  "testthat",     # Unit testing
  "roxygen2",     # Documentation
  "usethis"       # Project setup
)

# Function to install missing packages
install_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
  }
}

# Install missing packages
invisible(sapply(required_pkgs, install_missing))

# Install Bioconductor packages if needed
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}

bioc_pkgs <- c("EBImage", "rhdf5", "EBImage")
for (pkg in bioc_pkgs) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    BiocManager::install(pkg)
  }
}

# Install GitHub packages if needed
github_pkgs <- c("")
if (length(github_pkgs) > 0 && nzchar(github_pkgs[1])) {
  if (!requireNamespace("remotes", quietly = TRUE)) {
    install.packages("remotes")
  }
  remotes::install_github(github_pkgs)
}

# Verify installations
cat("\nVerifying package installations...\n")
missing_pkgs <- required_pkgs[!sapply(required_pkgs, requireNamespace, quietly = TRUE)]
if (length(missing_pkgs) == 0) {
  cat("All required R packages are installed successfully!\n")
} else {
  cat("The following packages could not be installed:")
  print(missing_pkgs)
  cat("Please install them manually.\n")
}

# Install IRkernel for Jupyter
if (!"IRkernel" %in% installed.packages()) {
  install.packages("IRkernel")
  IRkernel::installspec(name = 'ir', displayname = 'R (Medical Imaging)')
}
