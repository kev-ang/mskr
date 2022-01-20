# 2_Evaluation

This folder contains all the scripts and data that were used for the automatic evaluation of MSKR. The folder is
splitted into:

- Data
- Jena_Fuseki_Docker
- Scripts

Besides, on the top-level it contains a `config` file and an `Execute_Benchmark.sh`script.

**IMPORTANT**: Do not rename or move folders. The scripts use the names and structure of the given git repository.

## Config-File

The `config` file contains three variables:

- `working_dir` - specifying the directory used to store all files created during the evaluation.
- `java_max_ram` - specifying the memory limit for Apache Jena Fuseki
- `formalism_list` - specifying the formalisms to evaluate

## Execute_Benchmark.sh

This script is used to run the whole evaluation. The following steps are executed:

1. Set up the `working_dir` based on the value given in the `config` file. Default value is `Benchmark_Temp_Dir`,
   implying a folder to be created within this folder.
2. Unzip given datasets from `Data/Datasets/` into the `$working_dir/Datasets` folder
3. Create a TDB 2 database for each dataset
4. Create Apache Jena Fuseki configurations for each formalism and each dataset
5. Execute evaluation for the reasoning task `query answering & subsumption`
6. Execute evaluation for the reasoning task `verification`
7. Copy the results for both evaluations into a `Results` folder that is created on the same level as this file.

## Data

This folder contains all the `Datasets`, the `Ontology`, `Queries`, `Rules`, and `Shapes` necessary for the evaluation.

## Jena_Fuseki_Docker

Contains all relevant files for creating an Apache Jena Fuseki docker container used for hosting the test data.

## Scripts

Scripts used for the evaluation.