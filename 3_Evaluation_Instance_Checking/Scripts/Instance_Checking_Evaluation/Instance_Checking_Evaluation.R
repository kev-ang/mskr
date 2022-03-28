library(dplyr)
library(ggplot2)
library(rstudioapi)
require(tikzDevice)

draw_bar_chart <- function(data) {
  return(
    ggplot(data, aes(y = mean,
                     x = dataset)) +
      geom_bar(position = "dodge", stat = "identity") +
      geom_text(
        aes(label = round(mean)),
        vjust = -0.5,
        position = position_dodge(0.9)
      ) +
      xlab("") +
      ylab("Instance Checking time (seconds)") +
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

draw_bar_chart_detailed <- function(data) {
  return(
    ggplot(data, aes(y = Duration, x = rownames(data))) +
      geom_bar(position = "dodge", stat = "identity") +
      scale_x_discrete(
        labels = c(
          "AssistantProfessor" = "AiP",
          "AssociateProfessor" = "AoP",
          "Course" = "C",
          "Department" = "D",
          "FullProfessor" = "FP",
          "GraduateCourse" = "GC",
          "GraduateStudent" = "GS",
          "Lecturer" = "L",
          "Publication" = "P",
          "ResearchAssistant" = "RA",
          "ResearchGroup" = "RG",
          "TeachingAssistant" = "TA",
          "UndergraduateStudent" = "US",
          "University" = "U"
        )
      ) +
      geom_text(
        aes(label = round(Duration)),
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
root_dir <- gsub("3_Evaluation_Instance_Checking/Scripts/Instance_Checking_Evaluation/Instance_Checking_Evaluation.R", "", file_path)
working_directory <- paste0(root_dir, "5_Evaluation_Results/2_Instance_Checking")
setwd(working_directory)

# Load theraw data as csv file
data <-
  read.csv(paste0(
    working_directory,
    "/Raw_Results/Instance_Checking_Results.csv"
  ),
  sep = ";")

# Set all 0 values to NA so they are not included in the calculations
data[data == 0] <- NA

# Replace all occurrences of '_' with '-'
data$dataset <- gsub('_', '-', data$dataset)

# Replace all occurrences of "LUBM" with ""
colnames(data) <- gsub('LUBM.', '', colnames(data))

# Calculate mean/min/max value for each dataset
data$mean <- rowMeans(data[, 2:length(data)], na.rm = TRUE)
data$min <-
  apply(data[, 2:length(data)], 1, min, na.rm = TRUE)
data$median <-
  apply(data[, 2:length(data)], 1, median, na.rm = TRUE)
data$max <-
  apply(data[, 2:length(data)], 1, max, na.rm = TRUE)


# Draw bar chart overview
tikz('Instance_Checking.tex')
draw_bar_chart(data)
dev.off()

# Draw bar chart for each dataset separately
filter_rows <- c("mean", "min", "median", "max", "dataset")

datasets <-
  c("Univ-100",
    "Univ-1000",
    "Univ-10000")
for (curr_dataset in datasets) {
  tikz(paste0(gsub(
    'Univ-',
    'Instance_Checking_',
    curr_dataset
  ),
  '.tex'))
  relevant_columns <- names(data)[!(names(data) %in% filter_rows)]
  filter(data, dataset == curr_dataset) %>% select(., relevant_columns) %>% t() %>% as.data.frame() %>% `colnames<-`(c("Duration")) %>% draw_bar_chart_detailed() %>% print()
  dev.off()
}
