library(ggplot2)
library(reshape2)
library(rstudioapi)
require(tikzDevice)

draw_bar_chart <- function(data) {
  return(
    ggplot(data, aes(
      fill = Var1, y = value, x = Var2
    )) +
      geom_bar(position = "dodge", stat = "identity") +
      xlab("Queries") +
      ylab("Response times (seconds)") +
      labs(fill = "Formalism") +
      scale_fill_grey(start = 0, end = .9) +
      theme_bw() +
      theme(
        axis.text = element_text(size = 12),
        axis.title = element_text(size = 14, face = "bold"),
        legend.title = element_text(size=14, face = "bold"),
        legend.text=element_text(size=14)
      )
  )
}

draw_overview_bar_chart <- function(data) {
  means <- rowMeans(data, na.rm = TRUE)
  mins <- apply(data, 1, FUN = min)
  maxs <- apply(data, 1, FUN = max)
  statistic_frame <-
    data.frame(
      formalism = rownames(data),
      mean = means,
      minimum = mins,
      maximum = maxs
    )
  
  return(
    ggplot(statistic_frame, aes(
      y = mean, x = factor(formalism, level = c('rdfs', 'mskr', 'rdfs-plus', 'owl-2-rl'))
    )) +
      geom_bar(position = "dodge", stat = "identity") +
      geom_text(aes(label = round(mean)), vjust = -0.5) +
      xlab("") +
      ylab("Response times (seconds)") +
      labs(fill = "Formalism") +
      scale_fill_grey(start = 0, end = .9) +
      theme_bw() +
      theme(
        axis.text = element_text(size = 12),
        axis.text.x = element_text(size = 14, face = "bold"),
        axis.title = element_text(size = 14, face = "bold")
      )
  )
}

extract_dataset_identifier <- function(filename) {
  last_slash <- regexpr("/[^/]*$", filename) + 1
  last_dot <- regexpr("\\.[^\\.]*$", filename) - 1
  return(substr(filename, last_slash, last_dot))
}

# Specify and set working directory for this script. Path is based on the location of this file
file_path <- rstudioapi::getActiveDocumentContext()$path
root_dir <- gsub("2_Evaluation_Query_Answering/Scripts/Query_Answering_Evaluation/Query_Answering_Evaluation_Bar_Chart.R", "", file_path)
working_directory <- paste0(root_dir, "5_Evaluation_Results/1_Question_Answering")
setwd(working_directory)

# Specify result files to load
csv_files <-
  c(
    "/Raw_Results/Univ_100.csv",
    "/Raw_Results/Univ_1000.csv",
    "/Raw_Results/Univ_10000.csv"
  )

for (csv_file in csv_files) {
  # Load query results from csv file
  data <-
    read.csv(paste0(working_directory, csv_file),
             sep = ";",
             row.names = 1)
  
  # Set all 0 values to NA so they are not included in the calculations
  data[data == 0] <- NA
  
  # Replace underscore with dash
  row.names(data) <- gsub('_', '-', rownames(data))
  
  # Identified queries with the highest complexity
  slowest_queries <- c("query2")
  medium_queries <- c("query6", "query9", "query14")
  
  # Dataset containing the queries with lower complexity
  fastest_queries <-
    names(data) %in% c(slowest_queries, medium_queries)
  fast_queries_data <- data[!fastest_queries]
  
  # Dataset containing the queries with higher complexity
  slow_queries_data <- data[slowest_queries]
  
  # Dataset containing the queries with medium complexity
  medium_queries_data <- data[medium_queries]
  
  # Draw plot for fast queries
  tikz(paste0(
    gsub('Univ', 'QA', extract_dataset_identifier(csv_file)),
    '_Fast.tex'
  ))
  print(draw_bar_chart(melt(as.matrix(
    fast_queries_data
  ))))
  dev.off()
  
  # Draw plot for medium queries
  tikz(paste0(
    gsub('Univ', 'QA', extract_dataset_identifier(csv_file)),
    '_Medium.tex'
  ))
  print(draw_bar_chart(melt(as.matrix(
    medium_queries_data
  ))))
  dev.off()
  
  # Draw plot for slowest queries
  tikz(paste0(
    gsub('Univ', 'QA', extract_dataset_identifier(csv_file)),
    '_Slow.tex'
  ))
  print(draw_bar_chart(melt(as.matrix(
    slow_queries_data
  ))))
  dev.off()
  
  # Draw plot for the overview
  tikz(paste0(
    gsub('Univ', 'QA', extract_dataset_identifier(csv_file)),
    '_Overview.tex'
  ))
  print(draw_overview_bar_chart(data))
  dev.off()
}
