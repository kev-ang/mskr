# 1_Preparation_Phase

In the preparation phase the datasets used for evaluating the knowledge representation formalisms `RDFS`, `MSKR`
, `RDFS-Plus`, and `OWL-2-RL`are generated. All the other parts as the ontology, queries, rules, and shapes are fix. In
this folder you find two scripts distributed into the folders:

- Dataset_Generator
- Dataset_Modifer

## Dataset_Generator

The `Dataset_Generator` folder contains a JAR-file of the LUBM Benchmark used to generate datasets of different sizes.
The LUBM generator for this evaluation was executed with the following command:

```
java -jar LUBM_Data_Generator.jar -univ $size -onto http://swat.cse.lehigh.edu/onto/univ-bench.owl
```

As `$size` we used the three values 5, 10, and 50. The LUBM generator generates various files starting with `University`
and ending with `.owl`. For those files to be used by the evaluation scripts, the dataset needs to be zipped and added
to the corresponding folder in `2_Evaluation` -> `Data` -> `Datasets`. As a naming convention for those zip files we
recommend: `Dataset_Univ_$size.zip`. It is important to stick to this convention as the evaluation scripts use parts of
the dataset names for creating configurations and so on.

**IMPORTANT**: The JAR is created based on the java source files from http://swat.cse.lehigh.edu/projects/lubm/

## Dataset_Modifier

The `Dataset_Generator` generates datasets without `owl:sameAs`-links. Introducing `sameAs`-links requires the
modification of the given datasets. Therefore, we imported the datasets into different repositories in a GraphDB
instance. The names of those repositories is hardcoded within the `repositories` variable. The url of the GraphDB
instance is hardcoded as `graph_db_url`. Besides, based on the URIs used within the queries of the LUBM benchmark we
hardcoded a map consisting of the found URIs and their corresponding type. Based on those definitions, the python script
enriches the given datasets. Therefore, the script randomly selects other instances of the same type and
introduces `sameAs` links with the URIs occuring in the queries as source and the randomly selected URIs of the
instances as target. Afterward, those datasets can be exported from GraphDB into a JSON-LD file for example. For larger
files it might be necessary to split them into smaller files. Then, those files are zipped using the same naming
convention as for the `Data_Generator`. Those files can then be added to the folder in `2_Evaluation` -> `Data`
-> `Datasets` as well.

Everything is hardcoded within the python script. For the execution, use the following command:
```
python3 main.py
```

The logs will show what was introduced. 