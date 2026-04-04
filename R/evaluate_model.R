# Load required libraries
library(ggplot2)
library(pROC)

# Set up output directory
output_dir <- file.path("..", "output", "r_plots")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Simulate model evaluation
set.seed(42)
n <- 1000
true_labels <- sample(0:1, n, replace = TRUE, prob = c(0.3, 0.7))
predicted_probs <- ifelse(
  true_labels == 1,
  rbeta(sum(true_labels == 1), 8, 2),
  rbeta(sum(true_labels == 0), 2, 8)
)

# Create ROC curve
roc_obj <- roc(true_labels, predicted_probs)
png(file.path(output_dir, "roc_curve.png"), width = 800, height = 600)
plot(roc_obj, main = "ROC Curve", col = "blue", lwd = 2)
abline(a = 0, b = 1, lty = 2, col = "red")
dev.off()

# Create probability density plot
df <- data.frame(
  Probability = predicted_probs,
  True_Label = factor(true_labels, labels = c("NORMAL", "PNEUMONIA"))
)

p <- ggplot(df, aes(x = Probability, fill = True_Label)) +
  geom_density(alpha = 0.5) +
  theme_minimal() +
  labs(title = "Predicted Probability Distributions by Class",
       x = "Predicted Probability of PNEUMONIA",
       y = "Density") +
  scale_fill_manual(values = c("blue", "red"))

ggsave(file.path(output_dir, "probability_distributions.png"), p, width = 8, height = 6)

# Calculate metrics
predicted_labels <- ifelse(predicted_probs > 0.5, 1, 0)
metrics <- data.frame(
  Metric = c("Accuracy", "Sensitivity", "Specificity", "AUC"),
  Value = c(
    mean(predicted_labels == true_labels),
    sum(predicted_labels == 1 & true_labels == 1) / sum(true_labels == 1),
    sum(predicted_labels == 0 & true_labels == 0) / sum(true_labels == 0),
    auc(roc_obj)
  )
)

# Save metrics to CSV
write.csv(metrics, file.path(output_dir, "model_metrics.csv"), row.names = FALSE)

message("Evaluation complete. Check output/r_plots/ for visualizations.")

