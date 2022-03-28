#!/bin/bash
# Run the benchmark over all databases using the given configurations

source ./Scripts/Bash_Utilities/timestamp.sh
source ./config

# Switch to benchmark folder
cd Scripts/Verification

# Create corresponding folder in the working directory
configuration_working_dir=../../$working_dir/Configurations
shapes_dir=../Data/Shapes
constraint_working_dir=../../$working_dir/Constraint_Checking_Results
mkdir $constraint_working_dir

# print time stamp when starting the creation of the databases
echo "$(timestamp)  start execution of constraint checking"

# get list of configurations
configurations=($configuration_working_dir/Configuration*.ttl)

# Build docker container before executing the benchmarks
export WORKING_DIR=../$working_dir
docker-compose -f ../../Jena_Fuseki_Docker/docker-compose.yaml build --build-arg JENA_VERSION=4.2.0

for configuration in ${configurations[@]}; do
  configname=${configuration##*/}
  echo "$(timestamp) starting server with config: ${configname}"
  # start docker container
  docker-compose -f ../../Jena_Fuseki_Docker/docker-compose.yaml run -d --rm --service-ports -e JAVA_OPTIONS="-Xmx$java_max_ram -Xms1048m" fuseki --conf /fuseki/configs/${configname}

  sleep 10

  # Remove all unnecessary parts of the config name to retrieve the formalism
  formalism=${configname#"Configuration_Dataset_"}
  formalism=${formalism%".ttl"}
  formalism=${formalism##*"_"}

  # Remove all unnecessary parts of the config name to retrieve the dataset
  dataset=${configname#"Configuration_Dataset_"}
  dataset=${dataset%"_"*}

  mkdir -p $constraint_working_dir/${dataset}/${formalism}/
  java -jar rdfunit.jar -d ${dataset} -e http://localhost:3030/dataset/query -s ../../Data/Shapes/All_Shapes.ttl -f $constraint_working_dir/${dataset}/${formalism}/ -o json-ld -T 0

  docker-compose -f ../../Jena_Fuseki_Docker/docker-compose.yaml down
  rm -rf cache/
done

# Evaluate results
python3 Constraint_Result_Evaluator.py -r $constraint_working_dir -o $constraint_working_dir

echo "$(timestamp)  finished execution of constraint checking"
