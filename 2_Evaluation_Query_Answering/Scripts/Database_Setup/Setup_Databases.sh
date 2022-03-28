#!/bin/bash
# set up datasets required for the creation of the corresponding databases

source ./Scripts/Bash_Utilities/timestamp.sh
source ./config

# Switch to datasets folder
cd Data/Databases

# Create corresponding folder in the working directory
database_working_dir=../../$working_dir/Databases
mkdir $database_working_dir

# print time stamp when starting the creation of the datasets
echo "$(timestamp)  start setup of databases"

# List all precreated datasets
databases=( $(file ./* | grep ".zip" | cut -d':' -f1) )

# unzip datasets
for database in ${databases[@]}; do
  unzip $database -d $database_working_dir/
done

echo "$(timestamp)  finished setup of databases"
