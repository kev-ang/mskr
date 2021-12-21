#!/bin/bash
# Run the benchmark over all databases using the given configurations

source ./Bash_Utilities/timestamp.sh
source ./config

# print time stamp when starting the creation of the databases
echo "$(timestamp)  start execution of benchmarks"

# Setup working directory for benchmarks
mkdir $working_dir

# Create all relevant datasets
./Datasets/Setup_Datasets.sh

# Create databases used for apache fuseki
./Databases/Setup_Databases.sh

# Create fuseki configurations for all formalisms and databases
./Fuseki_Configurations/Setup_Configurations.sh

# Execute the benchmark on query answering
./Query_Answering/Run_Query_Answering.sh

# Execute the benchmark on constraint checking
./Constraint_Checking/Run_Constraint_Checking.sh

# Copy results to result folder
# Copy query results
mkdir -p ./Results/Queries
cp ./$working_dir/Query_Results/error.log ./Results/Queries
cp ./$working_dir/Query_Results/*.csv ./Results/Queries

# Copy constraint results
mkdir -p ./Results/Constraints
cp ./$working_dir/Constraint_Checking_Results/error.log ./Results/Constraints
cp ./$working_dir/Constraint_Checking_Results/*.csv ./Results/Constraints

echo "$(timestamp)  finished execution of benchmarks"
