#!/bin/bash
# set up databases used by apache fuseki

source ./Bash_Utilities/timestamp.sh
source ./config

# Switch to configurations folder
cd Fuseki_Configurations

# Create corresponding folder in the working directory
database_working_dir=../$working_dir/Databases
configuration_working_dir=../$working_dir/Configurations
mkdir $configuration_working_dir

# print time stamp when starting the creation of the databases
echo "$(timestamp)  start creation of fuseki configurations"

# get list of datasets
datasets=( $(file $database_working_dir/* | grep directory | cut -d':' -f1) )

# list of formalisms
IFS=',' #setting comma as delimiter
read -a formalisms <<<"$formalism_list" #reading str as an array as tokens separated by IFS

for formalism in ${formalisms[@]}; do
  for dataset in ${datasets[@]}; do
    # databases and rules are mounted into the docker container
    # databases: /fuseki/databases
    # rules: /fuseki/rules

    # Remove ../datasets/ from directory name to create a corresponding folder
    datasetName=${dataset#"$database_working_dir/"}
    python Configuration_Generator.py -t ./Template.ttl -d /fuseki/databases/${datasetName} -r /fuseki/rules/${formalism}.rules  -n $configuration_working_dir/Configuration_${datasetName}_${formalism}.ttl
  done
done

echo "$(timestamp)  finished creation of fuseki configurations"
