# 2_Evaluation_Query_Answering

This folder contains a Java implementation to evaluate the query answering reasoning task. Instead of running a
docker container and evaluating SPARQL queries using a REST API, the queries were sent without any HTTP server. Therefore, we implemented the Apache Jena library.

Starting the evaluation requires a configuration file available on the root level of this folder. The configuration file requires:
- "name" - the name of the benchmark
- "timeout" - desired timeout for each query
- "datasets" - list of datasets consisting of:
  - "identifier" - used for the result files
  - "datasetPath" - where to find and from where to load the dataset
- "queries" - queries to be used for the evaluation
  - "identifier" - relevant for the result files
  - "queryPath" - where to find the query
- "rules" - rules for the different formalisms
  - "formalism" - relevant for the result files
  - "rulePath" - where to find the rules

With this rule file, the evaluation can be started using the following command:

```
 java -jar target/MSKR_Jena_Reasoner-1.0-SNAPSHOT.jar configuration.json
```
