# 1_Preparation_Phase

In the preparation phase, the datasets used for evaluating the knowledge representation formalisms `RDFS`, `MSKR`
, `RDFS-Plus`, and `OWL-2-RL`are generated. All the other parts as the ontology, queries, rules, and shapes are fixed. In
this folder, you find scripts distributed into the folders:

- Database_Generator
- Dataset_Generator
- Dataset_Modifer

## Database_Generator

The `Database_Generator` loads existing datasets into a database. For this evaluation Apache Jena and its persistent
storage called [TDB2](https://jena.apache.org/documentation/tdb2/) is used. This folder contains a script that unzips
existing datasets and loads them into corresponding databases. Use the following command if you want to load a
particular dataset into a database:

```
./apache-jena-4.3.2/bin/tdb2.tdbloader --loc $database_working_dir/${database} ${dataset}/*
```

## Dataset_Generator

The `Dataset_Generator` folder contains a JAR file of the LUBM Benchmark used to generate datasets of different sizes.
The LUBM generator for this evaluation was executed with the following command:

```
java -jar LUBM_Data_Generator.jar -univ $size -onto http://swat.cse.lehigh.edu/onto/univ-bench.owl
```

As `$size`, we used the three values 100, 1000, and 10000. The LUBM generator generates various files starting
with `University`
and ending with `.owl`.

**IMPORTANT**: The JAR is created based on the java source files from http://swat.cse.lehigh.edu/projects/lubm/

## Dataset_Modifier

The `Dataset_Generator` generates datasets without `sameAs`-links. Introducing `sameAs`-links requires the
modification of the given datasets. Therefore, we imported the datasets into different repositories in a GraphDB
instance. The names of those repositories are hardcoded within the `repositories` variable. The URL of the GraphDB
instance is hardcoded as `graph_db_url`. Besides, based on the URIs used within the queries of the LUBM benchmark, we
hardcoded a map consisting of the found URIs and their corresponding type. Based on those definitions, the python script
enriches the given datasets. The script randomly selects other instances of the same type. Then, `sameAs` links with the URIs occurring in the queries as the source, and the randomly selected URIs of the
instances as the target are introduced. Afterward, those datasets can be exported from GraphDB into a JSON-LD file, for example. It might be necessary to split larger files into smaller ones.

Everything is hardcoded within the python script. For the execution, use the following command:

```
python3 main.py
```

The logs will show what was introduced.