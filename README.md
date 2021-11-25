# MSKR
Knowledge graphs are very large semantic nets that integrate data from heterogeneous sources relying on a knowledge representation formalism to describe the stored knowledge. The size of knowledge graphs can quickly grow to a vast amount of facts a reasoning engine must handle. For a performant, in terms of reasoning and constraint checking, knowledge graph, a straightforward knowledge representation formalism that is a simple as possible and as expressive as necessary is required. Typically, knowledge graphs have a relatively simple TBox and a vast ABox. A knowledge representation formalism supporting type hierarchies, property definitions, and value assertions including *sameAs* statements is sufficient for most of the enterprise use cases.

Therefore, we present a knowledge representation formalism supporting the aforementioned features, called Maximally Simple Knowledge Representation Formalism for schema.org-based knowledge graphs (MSKR). MSKR is derived from RDFS and aligned with the data model of schema.org. Reasoning with MSKR can be implemented using a rule-based engine.



## How to run the benchmark

Within the git repository is a filed called "config" that allows to configure certain parameters of the benchmark:

- **working_dir** - temp directory for storing all the files that are used for the benchmark execution
- **java_max_ram** - max RAM the Apache Jena Fuseki server is allowed to use
- **dataset_sizes** - comma separated list of numbers. For each number a corresponding dataset is generated. The number represents the number of universities included in the dataset
  - 5 -> 5 Universities -> ~600,000 triples
  - 10 -> 10 Universities -> ~1,300,000 triples
  - 50 -> 50 Universities -> ~6,900,000 triples
- **formalism_list** - list of formalisms that should be used for benchmarking. **Caution**: Every formalism needs a corresponding rules file in the `Rules` folder.

After specifying the configuration of the Benchmark we can start the execution. Therefore, the shell-script `Execute_Benchmark.sh` is executed. This script does the following:

1. Create the *working_dir* as specified in the configuration file
2. Create the different datasets as specified by the *dataset_sizes* configuration
3. Each of those datasets is then loaded into an Apache Fuseki Jena TDB2 database
4. Fuseki configurations for the different formalisms and all databases is generated
5. Execution of the **query_answering** part of the benchmark 
6. Execution of the **constraint_checking** part of the benchmark
7. Finally, the results are copied to a `Result` folder which lies outside of the *working_dir*
   1. The `working_dir` can be deleted afterwards if not needed



After the benchmark execution, the `Result` folder contains the results for **query_answering** and **constraint_checking**. The results include the average response time for the queries for the different formalisms on the different datasets. For constraint checking, the results contain the total execution time for the shapes on the different datasets for the different formalisms.



## Git Structure

In this section we are going to describe the structure of the git repository. Besides, the we explain what is contained in the specific folders and how to execute the scripts.

Currently, this repository contains the following folders:

- Bash_Utilities
- Datasets
- Jena_Fuseki



### Bash_Utilities

Currently contains a single bash script only. This bash script allows to print the current time stamp on the console. This method is mainly used for logging.



### Constraint_Checking

Contains a SHACL2SPARQL implementation in python. This script applies the given SHACL shapes on the datasets and measures the total execution time.



### Databases

Contains the TDB2 databases used by Jena Fuseki containing the relevant benchmark data. The script within this folder has a dependency to the **Datasets** script. The **Datasets** script **must** be executed before the database script is executable. Otherwise, the relevant data for creating the databases is missing.

**Dependencies:**

- Datasets need to be created before



### Datasets

Contains the LUBM Data Generator and a script creating datasets of different sizes. The script is configured to create datasets including 10, 100, and 1000 universities. The output of the script are folders for each dataset.



### Fuseki_Configurations

Contains a script for generating the configuration files for the given databases and given knowledge representation formalisms. So far, we consider the knowledge representation formalisms:

- RDFS
- RDFS Plus
- MSKR

**Dependencies:**

- Databases need to be created before



### Jena_Fuseki

Apache Jena Fuseki is a SPARQL server. It can run as a operating system service, as a Java web application (WAR file), and as a standalone server.

Fuseki comes in in two forms, a single system “webapp”, combined with a UI for admin and query, and as “main”, a server suitable to run as part of a larger deployment, including [with Docker](https://jena.apache.org/documentation/fuseki2/fuseki-main.html#docker) or running embedded. Both forms use the same core protocol engine and [same configuration file format](https://jena.apache.org/documentation/fuseki2/fuseki-configuration.html).

Fuseki provides the SPARQL 1.1 [protocols for query and update](http://www.w3.org/TR/sparql11-protocol/) as well as the [SPARQL Graph Store protocol](http://www.w3.org/TR/sparql11-http-rdf-update/).

Fuseki is tightly integrated with [TDB](https://jena.apache.org/documentation/tdb/index.html) to provide a robust, transactional persistent storage layer, and incorporates [Jena text query](https://jena.apache.org/documentation/query/text-query.html).



**Build Docker Container:**

    docker-compose build --build-arg JENA_VERSION=4.2.0

**Run Docker Container:**

    docker-compose run --rm --service-ports -e JAVA_OPTIONS="-Xmx5096m -Xms1048m" fuseki --conf /fuseki/configs/<config>.ttl



### Ontology

This folder contains the ontology file of the LUBM benchmark.



### Queries

Contains the 14 queries provided by the LUBM benchmark dataset.



### Query_Answering

Script and python implementations for running the LUBM-SPARQL queries against the different datasets. Time between sending the SPARQL query and receiving the result is measured.



### Rules

Contains the rule files for the supported knowledge representation formalisms.



### Shapes

SHACL shapes that are used for the constraint checking task.



## Dataset

As benchmark dataset we rely on the *Lehigh University Benchmark (LUBM)* - http://swat.cse.lehigh.edu/projects/lubm/.

*"The Lehigh University Benchmark is developed to facilitate the evaluation of Semantic Web repositories in a standard and systematic way. The benchmark is intended to evaluate the performance of those repositories with respect to extensional queries over a large data set that commits to a single realistic ontology. It consists of a university domain ontology, customizable and repeatable synthetic data, a set of test queries, and several performance metrics."*



For our benchmark we created three datasets of different sizes:

| No. of universities | No. of triples |
| ------------------- | -------------- |
| 5                   | ~600,000       |
| 10                  | ~1,300,000     |
| 50                  | ~6,900,000     |



## Queries

Queries used for the benchmark are the ones coming with the LUBM dataset. The LUBM dataset brings 14 queries:

```SPARQL
# Query1
# This query bears large input and high selectivity. It queries about just one class and
# one property and does not assume any hierarchy information or inference.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X	
WHERE
{?X rdf:type ub:GraduateStudent .
  ?X ub:takesCourse
http://www.Department0.University0.edu/GraduateCourse0}

# Query2
# This query increases in complexity: 3 classes and 3 properties are involved. Additionally, 
# there is a triangular pattern of relationships between the objects involved.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X, ?Y, ?Z
WHERE
{?X rdf:type ub:GraduateStudent .
  ?Y rdf:type ub:University .
  ?Z rdf:type ub:Department .
  ?X ub:memberOf ?Z .
  ?Z ub:subOrganizationOf ?Y .
  ?X ub:undergraduateDegreeFrom ?Y}

# Query3
# This query is similar to Query 1 but class Publication has a wide hierarchy.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X
WHERE
{?X rdf:type ub:Publication .
  ?X ub:publicationAuthor 
        http://www.Department0.University0.edu/AssistantProfessor0}

# Query4
# This query has small input and high selectivity. It assumes subClassOf relationship 
# between Professor and its subclasses. Class Professor has a wide hierarchy. Another 
# feature is that it queries about multiple properties of a single class.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X, ?Y1, ?Y2, ?Y3
WHERE
{?X rdf:type ub:Professor .
  ?X ub:worksFor <http://www.Department0.University0.edu> .
  ?X ub:name ?Y1 .
  ?X ub:emailAddress ?Y2 .
  ?X ub:telephone ?Y3}

# Query5
# This query assumes subClassOf relationship between Person and its subclasses
# and subPropertyOf relationship between memberOf and its subproperties.
# Moreover, class Person features a deep and wide hierarchy.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X
WHERE
{?X rdf:type ub:Person .
  ?X ub:memberOf <http://www.Department0.University0.edu>}


# Query6
# This query queries about only one class. But it assumes both the explicit
# subClassOf relationship between UndergraduateStudent and Student and the
# implicit one between GraduateStudent and Student. In addition, it has large
# input and low selectivity.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X WHERE {?X rdf:type ub:Student}


# Query7
# This query is similar to Query 6 in terms of class Student but it increases in the
# number of classes and properties and its selectivity is high.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X, ?Y
WHERE 
{?X rdf:type ub:Student .
  ?Y rdf:type ub:Course .
  ?X ub:takesCourse ?Y .
  <http://www.Department0.University0.edu/AssociateProfessor0>,   
  	ub:teacherOf, ?Y}


# Query8
# This query is further more complex than Query 7 by including one more property.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X, ?Y, ?Z
WHERE
{?X rdf:type ub:Student .
  ?Y rdf:type ub:Department .
  ?X ub:memberOf ?Y .
  ?Y ub:subOrganizationOf <http://www.University0.edu> .
  ?X ub:emailAddress ?Z}


# Query9
# Besides the aforementioned features of class Student and the wide hierarchy of
# class Faculty, like Query 2, this query is characterized by the most classes and
# properties in the query set and there is a triangular pattern of relationships.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X, ?Y, ?Z
WHERE
{?X rdf:type ub:Student .
  ?Y rdf:type ub:Faculty .
  ?Z rdf:type ub:Course .
  ?X ub:advisor ?Y .
  ?Y ub:teacherOf ?Z .
  ?X ub:takesCourse ?Z}


# Query10
# This query differs from Query 6, 7, 8 and 9 in that it only requires the
# (implicit) subClassOf relationship between GraduateStudent and Student, i.e., 
#subClassOf rela-tionship between UndergraduateStudent and Student does not add
# to the results.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X
WHERE
{?X rdf:type ub:Student .
  ?X ub:takesCourse
<http://www.Department0.University0.edu/GraduateCourse0>}


# Query11
# Query 11, 12 and 13 are intended to verify the presence of certain OWL reasoning
# capabilities in the system. In this query, property subOrganizationOf is defined
# as transitive. Since in the benchmark data, instances of ResearchGroup are stated
# as a sub-organization of a Department individual and the later suborganization of 
# a University individual, inference about the subOrgnizationOf relationship between
# instances of ResearchGroup and University is required to answer this query. 
# Additionally, its input is small.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X
WHERE
{?X rdf:type ub:ResearchGroup .
  ?X ub:subOrganizationOf <http://www.University0.edu>}


# Query12
# The benchmark data do not produce any instances of class Chair. Instead, each
# Department individual is linked to the chair professor of that department by 
# property headOf. Hence this query requires realization, i.e., inference that
# that professor is an instance of class Chair because he or she is the head of a
# department. Input of this query is small as well.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X, ?Y
WHERE
{?X rdf:type ub:Chair .
  ?Y rdf:type ub:Department .
  ?X ub:worksFor ?Y .
  ?Y ub:subOrganizationOf <http://www.University0.edu>}


# Query13
# Property hasAlumnus is defined in the benchmark ontology as the inverse of
# property degreeFrom, which has three subproperties: undergraduateDegreeFrom, 
# mastersDegreeFrom, and doctoralDegreeFrom. The benchmark data state a person as
# an alumnus of a university using one of these three subproperties instead of
# hasAlumnus. Therefore, this query assumes subPropertyOf relationships between 
# degreeFrom and its subproperties, and also requires inference about inverseOf.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X
WHERE
{?X rdf:type ub:Person .
  <http://www.University0.edu> ub:hasAlumnus ?X}


# Query14
# This query is the simplest in the test set. This query represents those with large input and low selectivity and does not assume any hierarchy information or inference.
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ub: <http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl#>
SELECT ?X
WHERE {?X rdf:type ub:UndergraduateStudent}
```



## Ontology

Taken from https://franz.com/agraph/allegrograph3.3/agraph3.3_bench_lubm.lhtml:

Because the LUBM benchmark was designed to test some aspects of OWL reasoning that (by design) are beyond the strength of the RDFS++ reasoner, we added the single triple:

- ub:GraduateStudent rdfs:subClassOf ub:Student



```xml
<?xml version="1.0" encoding="UTF-8" ?>
<rdf:RDF
  xmlns = "http://swat.cse.lehigh.edu/onto/univ-bench.owl#"
  xml:base = "http://swat.cse.lehigh.edu/onto/univ-bench.owl"
  xmlns:rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  xmlns:owl="http://www.w3.org/2002/07/owl#"
>

<owl:Ontology rdf:about="">
  <rdfs:comment>An university ontology for benchmark tests</rdfs:comment>
  <rdfs:label>Univ-bench Ontology</rdfs:label>
  <owl:versionInfo>univ-bench-ontology-owl, ver April 1, 2004</owl:versionInfo>
</owl:Ontology>

<owl:Class rdf:ID="AdministrativeStaff">
  <rdfs:label>administrative staff worker</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Employee" />
</owl:Class>

<owl:Class rdf:ID="Article">
  <rdfs:label>article</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Publication" />
</owl:Class>

<owl:Class rdf:ID="AssistantProfessor">
  <rdfs:label>assistant professor</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Professor" />
</owl:Class>

<owl:Class rdf:ID="AssociateProfessor">
  <rdfs:label>associate professor</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Professor" />
</owl:Class>

<owl:Class rdf:ID="Book">
  <rdfs:label>book</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Publication" />
</owl:Class>

<owl:Class rdf:ID="Chair">
  <rdfs:label>chair</rdfs:label>
  <owl:intersectionOf rdf:parseType="Collection">
  <owl:Class rdf:about="#Person" />
  <owl:Restriction>
  <owl:onProperty rdf:resource="#headOf" />
  <owl:someValuesFrom>
  <owl:Class rdf:about="#Department" />
  </owl:someValuesFrom>
  </owl:Restriction>
  </owl:intersectionOf>
  <rdfs:subClassOf rdf:resource="#Professor" />
</owl:Class>

<owl:Class rdf:ID="ClericalStaff">
  <rdfs:label>clerical staff worker</rdfs:label>
  <rdfs:subClassOf rdf:resource="#AdministrativeStaff" />
</owl:Class>

<owl:Class rdf:ID="College">
  <rdfs:label>school</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Organization" />
</owl:Class>

<owl:Class rdf:ID="ConferencePaper">
  <rdfs:label>conference paper</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Article" />
</owl:Class>

<owl:Class rdf:ID="Course">
  <rdfs:label>teaching course</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Work" />
</owl:Class>

<owl:Class rdf:ID="Dean">
  <rdfs:label>dean</rdfs:label>
  <owl:intersectionOf rdf:parseType="Collection">
  <owl:Restriction>
  <owl:onProperty rdf:resource="#headOf" />
  <owl:someValuesFrom>
  <owl:Class rdf:about="#College" />
  </owl:someValuesFrom>
  </owl:Restriction>
  </owl:intersectionOf>
  <rdfs:subClassOf rdf:resource="#Professor" />
</owl:Class>

<owl:Class rdf:ID="Department">
  <rdfs:label>university department</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Organization" />
</owl:Class>

<owl:Class rdf:ID="Director">
  <rdfs:label>director</rdfs:label>
  <owl:intersectionOf rdf:parseType="Collection">
  <owl:Class rdf:about="#Person" />
  <owl:Restriction>
  <owl:onProperty rdf:resource="#headOf" />
  <owl:someValuesFrom>
  <owl:Class rdf:about="#Program" />
  </owl:someValuesFrom>
  </owl:Restriction>
  </owl:intersectionOf>
</owl:Class>

<owl:Class rdf:ID="Employee">
  <rdfs:label>Employee</rdfs:label>
  <owl:intersectionOf rdf:parseType="Collection">
  <owl:Class rdf:about="#Person" />
  <owl:Restriction>
  <owl:onProperty rdf:resource="#worksFor" />
  <owl:someValuesFrom>
  <owl:Class rdf:about="#Organization" />
  </owl:someValuesFrom>
  </owl:Restriction>
  </owl:intersectionOf>
</owl:Class>

<owl:Class rdf:ID="Faculty">
  <rdfs:label>faculty member</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Employee" />
</owl:Class>

<owl:Class rdf:ID="FullProfessor">
  <rdfs:label>full professor</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Professor" />
</owl:Class>

<owl:Class rdf:ID="GraduateCourse">
  <rdfs:label>Graduate Level Courses</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Course" />
</owl:Class>

<owl:Class rdf:ID="GraduateStudent">
  <rdfs:label>graduate student</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Person" />
  <rdfs:subClassOf rdf:resource="#Student" />
  <rdfs:subClassOf>
  <owl:Restriction>
  <owl:onProperty rdf:resource="#takesCourse" />
  <owl:someValuesFrom>
  <owl:Class rdf:about="#GraduateCourse" />
  </owl:someValuesFrom>
  </owl:Restriction>
  </rdfs:subClassOf>
</owl:Class>

<owl:Class rdf:ID="Institute">
  <rdfs:label>institute</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Organization" />
</owl:Class>

<owl:Class rdf:ID="JournalArticle">
  <rdfs:label>journal article</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Article" />
</owl:Class>

<owl:Class rdf:ID="Lecturer">
  <rdfs:label>lecturer</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Faculty" />
</owl:Class>

<owl:Class rdf:ID="Manual">
  <rdfs:label>manual</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Publication" />
</owl:Class>

<owl:Class rdf:ID="Organization">
  <rdfs:label>organization</rdfs:label>
</owl:Class>

<owl:Class rdf:ID="Person">
  <rdfs:label>person</rdfs:label>
</owl:Class>

<owl:Class rdf:ID="PostDoc">
  <rdfs:label>post doctorate</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Faculty" />
</owl:Class>

<owl:Class rdf:ID="Professor">
  <rdfs:label>professor</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Faculty" />
</owl:Class>

<owl:Class rdf:ID="Program">
  <rdfs:label>program</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Organization" />
</owl:Class>

<owl:Class rdf:ID="Publication">
  <rdfs:label>publication</rdfs:label>
</owl:Class>

<owl:Class rdf:ID="Research">
  <rdfs:label>research work</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Work" />
</owl:Class>

<owl:Class rdf:ID="ResearchAssistant">
  <rdfs:label>university research assistant</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Person" />
  <rdfs:subClassOf>
  <owl:Restriction>
  <owl:onProperty rdf:resource="#worksFor" />
  <owl:someValuesFrom>
  <owl:Class rdf:about="#ResearchGroup" />
  </owl:someValuesFrom>
  </owl:Restriction>
  </rdfs:subClassOf>
</owl:Class>

<owl:Class rdf:ID="ResearchGroup">
  <rdfs:label>research group</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Organization" />
</owl:Class>

<owl:Class rdf:ID="Schedule">
  <rdfs:label>schedule</rdfs:label>
</owl:Class>

<owl:Class rdf:ID="Software">
  <rdfs:label>software program</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Publication" />
</owl:Class>

<owl:Class rdf:ID="Specification">
  <rdfs:label>published specification</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Publication" />
</owl:Class>

<owl:Class rdf:ID="Student">
  <rdfs:label>student</rdfs:label>
  <owl:intersectionOf rdf:parseType="Collection">
  <owl:Class rdf:about="#Person" />
  <owl:Restriction>
  <owl:onProperty rdf:resource="#takesCourse" />
  <owl:someValuesFrom>
  <owl:Class rdf:about="#Course" />
  </owl:someValuesFrom>
  </owl:Restriction>
  </owl:intersectionOf>
</owl:Class>

<owl:Class rdf:ID="SystemsStaff">
  <rdfs:label>systems staff worker</rdfs:label>
  <rdfs:subClassOf rdf:resource="#AdministrativeStaff" />
</owl:Class>

<owl:Class rdf:ID="TeachingAssistant">
  <rdfs:label>university teaching assistant</rdfs:label>
  <owl:intersectionOf rdf:parseType="Collection">
  <owl:Class rdf:about="#Person" />
  <owl:Restriction>
  <owl:onProperty rdf:resource="#teachingAssistantOf" />
  <owl:someValuesFrom>
  <owl:Class rdf:about="#Course" />
  </owl:someValuesFrom>
  </owl:Restriction>
  </owl:intersectionOf>
</owl:Class>

<owl:Class rdf:ID="TechnicalReport">
  <rdfs:label>technical report</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Article" />
</owl:Class>

<owl:Class rdf:ID="UndergraduateStudent">
  <rdfs:label>undergraduate student</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Student" />
</owl:Class>

<owl:Class rdf:ID="University">
  <rdfs:label>university</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Organization" />
</owl:Class>

<owl:Class rdf:ID="UnofficialPublication">
  <rdfs:label>unnoficial publication</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Publication" />
</owl:Class>

<owl:Class rdf:ID="VisitingProfessor">
  <rdfs:label>visiting professor</rdfs:label>
  <rdfs:subClassOf rdf:resource="#Professor" />
</owl:Class>

<owl:Class rdf:ID="Work">
  <rdfs:label>Work</rdfs:label>
</owl:Class>

<owl:ObjectProperty rdf:ID="advisor">
  <rdfs:label>is being advised by</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
  <rdfs:range rdf:resource="#Professor" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="affiliatedOrganizationOf">
  <rdfs:label>is affiliated with</rdfs:label>
  <rdfs:domain rdf:resource="#Organization" />
  <rdfs:range rdf:resource="#Organization" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="affiliateOf">
  <rdfs:label>is affiliated with</rdfs:label>
  <rdfs:domain rdf:resource="#Organization" />
  <rdfs:range rdf:resource="#Person" />
</owl:ObjectProperty>

<owl:DatatypeProperty rdf:ID="age">
  <rdfs:label>is age</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
</owl:DatatypeProperty>

<owl:ObjectProperty rdf:ID="degreeFrom">
  <rdfs:label>has a degree from</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
  <rdfs:range rdf:resource="#University" />
  <owl:inverseOf rdf:resource="#hasAlumnus"/>
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="doctoralDegreeFrom">
  <rdfs:label>has a doctoral degree from</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
  <rdfs:range rdf:resource="#University" />
  <rdfs:subPropertyOf rdf:resource="#degreeFrom" />
</owl:ObjectProperty>

<owl:DatatypeProperty rdf:ID="emailAddress">
  <rdfs:label>can be reached at</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
</owl:DatatypeProperty>

<owl:ObjectProperty rdf:ID="hasAlumnus">
  <rdfs:label>has as an alumnus</rdfs:label>
  <rdfs:domain rdf:resource="#University" />
  <rdfs:range rdf:resource="#Person" />
  <owl:inverseOf rdf:resource="#degreeFrom"/>
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="headOf">
  <rdfs:label>is the head of</rdfs:label>
  <rdfs:subPropertyOf rdf:resource="#worksFor"/>
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="listedCourse">
  <rdfs:label>lists as a course</rdfs:label>
  <rdfs:domain rdf:resource="#Schedule" />
  <rdfs:range rdf:resource="#Course" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="mastersDegreeFrom">
  <rdfs:label>has a masters degree from</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
  <rdfs:range rdf:resource="#University" />
  <rdfs:subPropertyOf rdf:resource="#degreeFrom"/>
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="member">
  <rdfs:label>has as a member</rdfs:label>
  <rdfs:domain rdf:resource="#Organization" />
  <rdfs:range rdf:resource="#Person" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="memberOf">
<rdfs:label>member of</rdfs:label>
<owl:inverseOf rdf:resource="#member" />
</owl:ObjectProperty>

<owl:DatatypeProperty rdf:ID="name">
<rdfs:label>name</rdfs:label>
</owl:DatatypeProperty>

<owl:DatatypeProperty rdf:ID="officeNumber">
  <rdfs:label>office room No.</rdfs:label>
</owl:DatatypeProperty>

<owl:ObjectProperty rdf:ID="orgPublication">
  <rdfs:label>publishes</rdfs:label>
  <rdfs:domain rdf:resource="#Organization" />
  <rdfs:range rdf:resource="#Publication" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="publicationAuthor">
  <rdfs:label>was written by</rdfs:label>
  <rdfs:domain rdf:resource="#Publication" />
  <rdfs:range rdf:resource="#Person" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="publicationDate">
  <rdfs:label>was written on</rdfs:label>
  <rdfs:domain rdf:resource="#Publication" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="publicationResearch">
  <rdfs:label>is about</rdfs:label>
  <rdfs:domain rdf:resource="#Publication" />
  <rdfs:range rdf:resource="#Research" />
</owl:ObjectProperty>

<owl:DatatypeProperty rdf:ID="researchInterest">
  <rdfs:label>is researching</rdfs:label>
</owl:DatatypeProperty>

<owl:ObjectProperty rdf:ID="researchProject">
  <rdfs:label>has as a research project</rdfs:label>
  <rdfs:domain rdf:resource="#ResearchGroup" />
  <rdfs:range rdf:resource="#Research" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="softwareDocumentation">
  <rdfs:label>is documented in</rdfs:label>
  <rdfs:domain rdf:resource="#Software" />
  <rdfs:range rdf:resource="#Publication" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="softwareVersion">
  <rdfs:label>is version</rdfs:label>
  <rdfs:domain rdf:resource="#Software" />
</owl:ObjectProperty>

<owl:TransitiveProperty rdf:ID="subOrganizationOf">
  <rdfs:label>is part of</rdfs:label>
  <rdfs:domain rdf:resource="#Organization" />
  <rdfs:range rdf:resource="#Organization" />
</owl:TransitiveProperty>

<owl:ObjectProperty rdf:ID="takesCourse">
  <rdfs:label>is taking</rdfs:label>
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="teacherOf">
  <rdfs:label>teaches</rdfs:label>
  <rdfs:domain rdf:resource="#Faculty" />
  <rdfs:range rdf:resource="#Course" />
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="teachingAssistantOf">
  <rdfs:label>is a teaching assistant for</rdfs:label>
  <rdfs:domain rdf:resource="#TeachingAssistant" />
  <rdfs:range rdf:resource="#Course" />
</owl:ObjectProperty>

<owl:DatatypeProperty rdf:ID="telephone">
  <rdfs:label>telephone number</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
</owl:DatatypeProperty>

<owl:ObjectProperty rdf:ID="tenured">
  <rdfs:label>is tenured:</rdfs:label>
  <rdfs:domain rdf:resource="#Professor" />
</owl:ObjectProperty>

<owl:DatatypeProperty rdf:ID="title">
  <rdfs:label>title</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
</owl:DatatypeProperty>

<owl:ObjectProperty rdf:ID="undergraduateDegreeFrom">
  <rdfs:label>has an undergraduate degree from</rdfs:label>
  <rdfs:domain rdf:resource="#Person" />
  <rdfs:range rdf:resource="#University" />
  <rdfs:subPropertyOf rdf:resource="#degreeFrom"/>
</owl:ObjectProperty>

<owl:ObjectProperty rdf:ID="worksFor">
  <rdfs:label>Works For</rdfs:label>
  <rdfs:subPropertyOf rdf:resource="#memberOf" />
</owl:ObjectProperty>

</rdf:RDF>
```

