# Function to check if a package is installed
check_package <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat(sprintf("✗ %s is NOT installed\n", pkg))
    return(FALSE)
  } else {
    cat(sprintf("✓ %s is installed\n", pkg))
    return(TRUE)
  }
}

# Check R version
cat("R Version:", R.version.string, "\n\n")

# List of core packages to check
core_packages <- c(
  "tidyverse", "data.table", "magrittr", 
  "imager", "magick", "ggplot2",
  "rmarkdown", "knitr", "reticulate"
)

# Check each package
cat("Checking core packages...\n")
installed <- sapply(core_packages, check_package)

# Check Bioconductor packages
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  cat("\n✗ BiocManager is NOT installed\n")
} else {
  cat("\n✓ BiocManager is installed\n")
  
  bioconductor_pkgs <- c("EBImage", "rhdf5")
  cat("\nChecking Bioconductor packages...\n")
  sapply(bioconductor_pkgs, check_package)
}

# Check Python integration
cat("\nChecking Python integration...\n")
if (requireNamespace("reticulate", quietly = TRUE)) {
  cat("reticulate version:", as.character(packageVersion("reticulate")), "\n")
  
  # Check if Python is available
  if (reticulate::py_available(initialize = FALSE)) {
    cat("Python is available through reticulate\n")
    cat("Python version:", reticulate::py_config()$version, "\n")
  } else {
    cat("Python is NOT available through reticulate\n")
  }
} else {
  cat("reticulate package is not available\n")
}

# Summary
cat("\n--- Summary ---\n")
cat("Total packages checked:", length(core_packages) + length(bioconductor_pkgs), "\n")
cat("Packages installed:", sum(installed), "\n")
cat("Packages missing:", sum(!installed), "\n")

if (any(!installed)) {
  cat("\nTo install missing packages, run:\n")
  missing_pkgs <- names(installed)[!installed]
  cat("install.packages(c(\"", paste(missing_pkgs, collapse = "\", \""), "\"))\n")
}
