# A Maximally Simple Knowledge Representation Formalism (MSKR)

Knowledge graphs are very large semantic nets that integrate data from heterogeneous sources relying on a knowledge
representation formalism to describe the stored knowledge. The size of knowledge graphs can quickly grow to a vast
amount of facts a reasoning engine must handle. For performant reasoning and constraint checking over a knowledge graph,
a straightforward knowledge representation formalism that is as simple as possible and as expressive as necessary is
required. Typically, knowledge graphs have a relatively simple TBox and a vast ABox. A knowledge representation
formalism supporting type hierarchies, property definitions, and value assertions including \textit{sameAs} statements
is sufficient for most of the enterprise use cases

For a detailed description of MSKR, please consider the paper **!!!TODO paper needs to be published!!!**.

**This git repository contains all the code, data (links to the datasets can be found within this README), and scripts
required to reproduce the evaluation presented in the paper above.**

## Structure of the git repository

On this page, we give a brief overview of the structure of the git repository. Each of those folders contains it's
own `README.md` file presenting detailed information on the content of those folders. The repository consists of
the following folders:

- 0_Data:
  - Contains the ontology, queries, rules, and shapes used throughout the benchmark.
- 1_Preparation_Phase
    - Contains scripts for producing the data used for testing. Those scripts can be used to generate new test data, e.g. if larger datasets are
      needed. For reproducibility, we provide the used datasets on external storage (links can be found in the README in folder `0_Data`).
- 2_Evaluation_Query_Answering
  - Provides a java implementation of the Jena reasoning engine used to evaluate the query answering reasoning task.
- 3_Evaluation_Instance_Checking
  - Provides a README that links to the implementation of the verification tool that was used for the evaluation.
- 4_Evaluation_Equality_Reasoning
    - We manually evaluated the performance of MSKR in comparison to the other formalisms on GraphDB. Additional
      datasets containing `sameAs` links are included within this folder. Those datasets were produced using the
      scripts from the `1_Preparation_Phase` (links are provided in the README in folder `0_Data`).
- 5_Evaluation_Results
    - Results produced by the different scripts used to generate the tables in the paper are kept within this folder.
- docs
  - Files required for GitHub pages.

For detailed information on the evaluation, consider the MSKR paper.