# Load required libraries
library(magick)
library(ggplot2)
library(gridExtra)

# Set paths
base_dir <- "D:/CascadeProjects/medical_imaging_analysis"
data_dir <- file.path(base_dir, "data/chest_xray")
output_dir <- file.path(base_dir, "output/r_plots")

# Create output directory if it doesn't exist
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Function to safely load and display images
show_sample_images <- function(class_name, n=4) {
  img_dir <- file.path(data_dir, "train", class_name)
  
  # Check if directory exists
  if (!dir.exists(img_dir)) {
    message("Directory not found: ", img_dir)
    return(NULL)
  }
  
  # Get image files
  img_files <- list.files(img_dir, pattern = "\\.(jpe?g|png|JPEG|JPG|PNG)$", 
                          full.names = TRUE, ignore.case = TRUE)
  
  if (length(img_files) == 0) {
    message("No images found in: ", img_dir)
    return(NULL)
  }
  
  # Limit to requested number of images
  img_files <- head(img_files, n)
  
  # Create and save the plot
  output_file <- file.path(output_dir, paste0("sample_", tolower(class_name), ".png"))
  
  # Create a blank plot as a fallback
  if (length(img_files) == 0) {
    png(output_file, width = 800, height = 600)
    plot(1, type="n", xlab="", ylab="", main=paste("No", class_name, "images found"))
    dev.off()
    return(NULL)
  }
  
  # Try to create image grid
  tryCatch({
    # Read images
    img_list <- lapply(img_files, image_read)
    
    # Combine images
    img_combined <- image_append(image_scale(do.call(c, img_list), "200x200"))
    
    # Save combined image
    image_write(img_combined, path = output_file)
    message("Saved: ", output_file)
  }, error = function(e) {
    message("Error processing images: ", e$message)
    # Create error plot
    png(output_file, width = 800, height = 600)
    plot(1, type="n", xlab="", ylab="", 
         main=paste("Error processing", class_name, "images"))
    text(1, 1, e$message, col="red")
    dev.off()
  })
}

# Show sample images
show_sample_images("NORMAL")
show_sample_images("PNEUMONIA")

# Create class distribution plot
class_counts <- data.frame(
  Class = c("NORMAL", "PNEUMONIA"),
  Count = c(
    length(list.files(file.path(data_dir, "train", "NORMAL"), 
                      pattern = "\\.(jpe?g|png|JPEG|JPG|PNG)$", 
                      ignore.case = TRUE)),
    length(list.files(file.path(data_dir, "train", "PNEUMONIA"),
                      pattern = "\\.(jpe?g|png|JPEG|JPG|PNG)$", 
                      ignore.case = TRUE))
  )
)

if (all(class_counts$Count > 0)) {
  p <- ggplot(class_counts, aes(x = Class, y = Count, fill = Class)) +
    geom_bar(stat = "identity") +
    theme_minimal() +
    labs(title = "Class Distribution in Training Set",
         x = "Class",
         y = "Number of Images") +
    theme(legend.position = "none")
  
  output_plot <- file.path(output_dir, "class_distribution.png")
  ggsave(output_plot, p, width = 8, height = 6)
  message("Saved: ", output_plot)
} else {
  message("Could not create class distribution plot - missing image files")
}

message("Exploratory analysis complete. Check: ", output_dir)