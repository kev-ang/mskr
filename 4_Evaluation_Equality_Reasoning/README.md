# 4_Evaluation_Equality_Reasoning

Evaluation equality reasoning based on rules is infeasible due to the proliferation of statements to be inferred.
Therefore, we used GraphDB to evaluate the given reasoning task as it comes with an [efficient implementation](https://graphdb.ontotext.com/documentation/10.0/reasoning.html#same-as-optimization) for
equality reasoning based on `owl:sameAs` links.

We set up different repositories for the formalisms using either the predefined rule sets or a custom rule set for
MSKR (available in `/Data/Rules/mskr.pie`). The configuration for the various repositories is available in `/Data/Configurations/`.
