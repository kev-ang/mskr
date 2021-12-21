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
echo "$(timestamp)  start setup of datasets"

# List all precreated datasets
datasets=( $(file ./* | grep ".zip" | cut -d':' -f1) )

# unzip datasets
for dataset in ${datasets[@]}; do
  unzip $dataset -d $dataset_working_dir/
done

echo "$(timestamp)  finished setup of datasets"
