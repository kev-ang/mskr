# 3_Evaluation_Instance_Checking

For evaluating the instance checking reasoning task, we used a verifier
called ["VeriGraph"](https://github.com/semantifyit/VeriGraph). Based on given SHACL shapes, VeriGraph accesses SPARQL
endpoints to retrieve the required instances. Those instances are then verified, and a verification report is generated. 

The shapes used for this task can be found in `0_data/Shapes/`.

A description of using VeriGraph is available in the respective git repository.
