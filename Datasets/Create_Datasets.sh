#!/bin/bash
# set up datasets required for the creation of the corresponding databases

source ./Bash_Utilities/timestamp.sh
source ./config

# Switch to datasets folder
cd Datasets

# Create corresponding folder in the working directory
dataset_working_dir=../$working_dir/Datasets
mkdir $dataset_working_dir

# print time stamp when starting the creation of the datasets
echo "$(timestamp)  start creation of datasets"


# set consisting of the number of universities a dataset should have
IFS=',' #setting comma as delimiter
read -a datasetSizes <<<"$dataset_sizes" #reading str as an array as tokens separated by IFS

# create small dataset consisting of the given number of universities
for size in ${datasetSizes[@]}; do
  echo "$size"
  java -jar LUBM_Data_Generator.jar -univ $size -onto http://swat.cse.lehigh.edu/onto/univ-bench.owl
  mkdir $dataset_working_dir/Dataset_Univ_$size
  mv University*.owl $dataset_working_dir/Dataset_Univ_$size/
  sleep 1s
done

# remove the log file created by the LUBM data LUBM_Data_Generator
#rm log.txt

echo "$(timestamp)  finished creation of datasets"
