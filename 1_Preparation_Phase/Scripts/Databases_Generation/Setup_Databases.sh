#!/bin/bash
# set up databases used by apache fuseki

# Create corresponding folder in the working directory
dataset_working_dir=../../Data/Datasets
database_working_dir=../../../2_Evaluation/Data/Databases

echo "start unzipping existing datasets"

# List all precreated datasets
datasets=( $(file $dataset_working_dir/* | grep ".zip" | cut -d':' -f1) )

# unzip datasets
for dataset in ${datasets[@]}; do
  echo "$dataset"
  unzip $dataset -d $dataset_working_dir/
done

#echo "finish unzipping datasets"

# print time stamp when starting the creation of the databases
echo "start creation of databases"

# get list of datasets
datasets=( $(file $dataset_working_dir/* | grep directory | cut -d':' -f1) )

for dataset in ${datasets[@]}; do
  # Remove ../datasets/ from directory name to create a corresponding folder
  database=${dataset#"${dataset_working_dir}/"}
  mkdir $database_working_dir/${database}
  ./apache-jena-4.3.2/bin/tdb2.tdbloader --loc $database_working_dir/${database} ${dataset}/* ../../Data/Ontology/univ-bench.rdf.xml
  chmod -R 777 $database_working_dir/${database}
  zip -r -m -X $database_working_dir/${database}.zip $database_working_dir/${database}/
  rm -rf ${dataset}/
done

echo "finished creation of databases"
