library(dplyr)
library(ggplot2)
library(rstudioapi)
require(tikzDevice)

draw_bar_chart <- function(data) {
  return(
    ggplot(data, aes(
      fill = Dataset,
      y = mean,
      x = factor(Formalism, level = c('rdfs', 'mskr', 'rdfs-plus', 'owl-2-rl'))
    )) +
      geom_bar(position = "dodge", stat = "identity") +
      geom_text(
        aes(label = round(mean)),
        vjust = -0.5,
        position = position_dodge(0.9)
      ) +
      xlab("") +
      ylab("Loading time (seconds)") +
      labs(fill = "Dataset") +
      scale_fill_grey(start = 0, end = .9) +
      theme_bw() +
      theme(
        axis.text = element_text(size = 12, face = "bold"),
        axis.title = element_text(size = 14, face = "bold"),
        legend.title = element_text(size=14, face = "bold"),
        legend.text=element_text(size=14)
      )
  )
}

# Specify and set working directory for this script. Path is based on the location of this file
file_path <- rstudioapi::getActiveDocumentContext()$path
root_dir <- gsub("4_Evaluation_GraphDB/Scripts/Loading_Time_Evaluation/Loading_Time_Evaluation.R", "", file_path)
working_directory <- paste0(root_dir, "5_Evaluation_Results/3_Equality_Reasoning")
setwd(working_directory)

# Load the GraphDB loading times as csv file
data <-
  read.csv(paste0(working_directory, "/Raw_Results/GraphDB_Loading_Times.csv"),
           sep = ";")

# Set all 0 values to NA so they are not included in the calculations
data[data == 0] <- NA

# Replace all occurences of '_' with '-'
data$Dataset <- gsub('_', '-', data$Dataset)

# Convert rows containing numbers into numeric values
data <-
  data %>% mutate(Run.1 = as.numeric(Run.1)) %>% mutate(Run.2 = as.numeric(Run.2)) %>% mutate(Run.3 = as.numeric(Run.3))

# Calculate mean value for each run for each formalism and dataset
data$mean <-
  apply(data[, c("Run.1", "Run.2", "Run.3")], 1, mean, na.rm = TRUE)

# Define available datasets
datasets <-
  c("Univ-100",
    "Univ-1000",
    "Univ-10000")

# Select columns required for the loading time bar chart
for (dataset in datasets) {
  tikz(paste0(gsub('Univ-',
                   'GraphDB_Loading_Times_',
                   dataset),
              '.tex'))
  print(filter(data, Dataset == dataset |
                 Dataset == paste0(dataset, "-sameAs")) %>% draw_bar_chart())
  dev.off()
}
