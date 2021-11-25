#!/bin/bash
# Run the benchmark over all databases using the given configurations

source ./Bash_Utilities/timestamp.sh
source ./Bash_Utilities/wait_until_endpoint_available.sh
source ./config

# Switch to benchmark folder
cd Constraint_Checking

# Create corresponding folder in the working directory
configuration_working_dir=../$working_dir/Configurations
shapes_dir=../Shapes
constraint_working_dir=../$working_dir/Constraint_Checking_Results
mkdir $constraint_working_dir

# print time stamp when starting the creation of the databases
echo "$(timestamp)  start execution of constraint checking"

# get list of configurations
#configurations=($configuration_working_dir/Configuration*.ttl)

# get list of shapes
shapes=($shapes_dir/*)

# Build docker container before executing the benchmarks
export WORKING_DIR=../$working_dir
docker-compose -f ../Jena_Fuseki/docker-compose.yaml build --build-arg JENA_VERSION=4.2.0

for configuration in ${configurations[@]}; do
  configname=${configuration##*/}
  echo "$(timestamp) starting server with config: ${configname}"
  # start docker container
  docker-compose -f ../Jena_Fuseki/docker-compose.yaml run -d --rm --service-ports -e JAVA_OPTIONS="-Xmx$java_max_ram -Xms1048m" fuseki --conf /fuseki/configs/${configname}

  sleep 10

  for shape in ${shapes[@]}; do
    echo "$(timestamp) executing constraints from folder: ${shape}"

    # Remove all unnecessary parts of the config name to retrieve the formalism
    formalism=${configname#"Configuration_Dataset_"}
    formalism=${formalism%".ttl"}
    formalism=${formalism##*"_"}

    # Remove all unnecessary parts of the config name to retrieve the dataset
    dataset=${configname#"Configuration_Dataset_"}
    dataset=${dataset%"_"*}

    # Remove all unnecessary parts of the shapes directory to retrieve the current shape set
    schema_specific_output_folder=${shape#$shapes_dir/}

    python3 Constraint_Checking.py -d $shape http://localhost:3030/dataset/query $constraint_working_dir/${dataset}/${schema_specific_output_folder}/${formalism}/
  done

  docker-compose -f ../Jena_Fuseki/docker-compose.yaml down
done

# Evaluate results
python3 Constraint_Result_Evaluator.py -r $constraint_working_dir -o $constraint_working_dir

echo "$(timestamp)  finished execution of constraint checking"
