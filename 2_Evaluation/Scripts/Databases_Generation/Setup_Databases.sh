#!/bin/bash
# set up databases used by apache fuseki

source ./Scripts/Bash_Utilities/timestamp.sh
source ./config

# Switch to datasets folder
cd Scripts/Databases_Generation

# Create corresponding folder in the working directory
dataset_working_dir=../../$working_dir/Datasets
database_working_dir=../../$working_dir/Databases
mkdir $database_working_dir

# print time stamp when starting the creation of the databases
echo "$(timestamp)  start creation of databases"

# get list of datasets
datasets=( $(file $dataset_working_dir/* | grep directory | cut -d':' -f1) )

for dataset in ${datasets[@]}; do
  # Remove ../datasets/ from directory name to create a corresponding folder
  database=${dataset#"${dataset_working_dir}/"}
  mkdir $database_working_dir/${database}
  ./apache-jena-4.2.0/bin/tdb2.tdbloader --loc $database_working_dir/${database} ${dataset}/* ../../Data/Ontology/univ-bench.rdf.xml
  chmod -R 777 $database_working_dir/${database}
done

echo "$(timestamp)  finished creation of databases"
