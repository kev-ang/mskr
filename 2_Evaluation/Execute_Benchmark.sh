#!/bin/bash
# Run the benchmark over all databases using the given configurations

source ./Scripts/Bash_Utilities/timestamp.sh
source ./config

# print time stamp when starting the creation of the databases
echo "$(timestamp)  start execution of benchmarks"

# Setup working directory for benchmarks
mkdir $working_dir

# Unzip all relevant datasets
./Scripts/Dataset_Setup/Setup_Datasets.sh

# Create databases used for apache fuseki
./Scripts/Databases_Generation/Setup_Databases.sh

# Create fuseki configurations for all formalisms and databases
./Scripts/Configuration_Generation/Setup_Configurations.sh

# Execute the benchmark on query answering
./Scripts/Query_Answering/Run_Query_Answering.sh

# Execute the benchmark on verification
./Scripts/Verification/Run_Verification.sh

# Copy results to result folder
# Copy query results
mkdir -p ./Results/Queries
cp ../$working_dir/Query_Results/error.log ./Results/Queries
cp ../$working_dir/Query_Results/*.csv ./Results/Queries

# Copy constraint results
mkdir -p ./Results/Constraints
cp ../$working_dir/Constraint_Checking_Results/error.log ./Results/Constraints
cp ../$working_dir/Constraint_Checking_Results/*.csv ./Results/Constraints

echo "$(timestamp)  finished execution of benchmarks"
