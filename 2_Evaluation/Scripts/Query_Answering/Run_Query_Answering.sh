#!/bin/bash
# Run the benchmark over all databases using the given configurations

source ./Scripts/Bash_Utilities/timestamp.sh
source ./config

# Switch to benchmark folder
cd Scripts/Query_Answering

# Create corresponding folder in the working directory
configuration_working_dir=../../$working_dir/Configurations
query_working_dir=../../$working_dir/Query_Results
mkdir $query_working_dir

# print time stamp when starting the creation of the databases
echo "$(timestamp)  start execution of queries"

# get list of configurations
configurations=($configuration_working_dir/Configuration*.ttl)

# Build docker container before executing the benchmarks
export WORKING_DIR=../../$working_dir
docker-compose -f ../../Jena_Fuseki_Docker/docker-compose.yaml build --build-arg JENA_VERSION=4.2.0

for configuration in ${configurations[@]}; do
  configname=${configuration##*/}
  echo "$(timestamp) executing queries using config: ${configname}"
  # start docker container
  docker-compose -f ../../Jena_Fuseki_Docker/docker-compose.yaml run -d --rm --service-ports -e JAVA_OPTIONS="-Xmx$java_max_ram -Xms1048m" fuseki --conf /fuseki/configs/${configname}

  echo "$(timestamp) start waiting"
  sleep 10
  echo "$(timestamp) end waiting"

  echo "$(timestamp) server up and running"

  # Remove all unnecessary parts of the config name to retrieve the formalism
  formalism=${configname#"Configuration_Dataset_"}
  formalism=${formalism%".ttl"}
  formalism=${formalism##*"_"}

  # Remove all unnecessary parts of the config name to retrieve the dataset
  dataset=${configname#"Configuration_Dataset_"}
  dataset=${dataset%"_"*}

  python3 Query_Executor.py -e http://localhost:3030/dataset/query -q ../../Data/Queries/ -f ${formalism} -d ${dataset} -o $query_working_dir
  docker-compose -f ../../Jena_Fuseki_Docker/docker-compose.yaml down
done

# Evaluate results
python3 Query_Result_Evaluator.py -r $query_working_dir -o $query_working_dir/Query_Results.csv

echo "$(timestamp)  finished execution of queries"
