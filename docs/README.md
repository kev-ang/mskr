Knowledge graphs are very large semantic nets that integrate data from heterogeneous sources relying on a knowledge representation formalism to describe the stored knowledge. The size of knowledge graphs can quickly grow to a vast amount of facts a reasoning engine must handle. For a performant, in terms of reasoning and constraint checking, knowledge graph, a straightforward knowledge representation formalism that is a simple as possible and as expressive as necessary is required. Typically, knowledge graphs have a relatively simple TBox and a vast ABox. A knowledge representation formalism supporting type hierarchies, property definitions, and value assertions including *sameAs* statements is sufficient for most of the enterprise use cases.

We present a knowledge representation formalism supporting the aforementioned features, called Maximally Simple Knowledge Representation Formalism for schema.org-based knowledge graphs (MSKR). MSKR is derived from RDFS and aligned with the data model of schema.org. Reasoning with MSKR can be implemented using a rule-based engine.

## Abstract Syntax

The informal definition of our Maximally Simple Knowledge Representation Formalism and the work of \[Patel-Schneider, 2014\] are the basis for our abstract syntax. MSKR is a simplification of schema.org and therefore a simplification and adaptation of Patel-Schneider’s definitions is sufficient to describe the abstract syntax of MSKR.

**Definition 1.** First, we define the terms *URI*, *text* and *literal*.

-   **URI** – Uniform Resource Identifier - A *String* with a special syntax that identifies an abstract or physical resource.[^1]\
    An example of a *URI* is: http://schema.org/Thing

-   **text** - represents any finite list of Unicode Symbols.[^2]

-   **Literal** – a pair consisting of
    -   a ***URI***, datatype identifier of the literal

    -   ***text*** string

In the following we give an abstract syntax definition for *regular types*, *enumerated types*, *datatypes* and *global properties*.

**Definition 2.** A regular type is defined as triple $\langle U,S,PR \rangle$,where

-   **U** – URI – identifier of the type

-   **S** – set of URIs – defining the supertypes of the type

-   **PR** – set of property-range pairs – defining the local properties
    of the type

An example for a type definition called *Bed* could be $\langle Thing,\{\},\{\langle image,\{URI\}\rangle,\langle name,\{String\}\rangle \}\rangle$.

**Definition 3.** An enumerated type is defined as tuple $\langle U,E \rangle$, where

-   **U** – URI – identifier of the type

-   **E** – set of URIs – direct instances of the enumerated type

The enumerated type BedType is presented in the following way $\langle BedType, \{SingleBed,DoubleBed\}\rangle$

**Definition 4.** A datatype is defined as $\langle U\rangle$, where

-   **U** – URI – identifier of the datatype

In the following example we will use the following datatypes: *DateTime*, *NaturalNumber*, *Number* and *String*.

**Definition 5.** A definition of a **type** is either a **regular type** definition, **enumerated type** definition or a **datatype** definition. For definitions we differentiate between **type** definition and **property** definition. A definition means to give a definition for its
identifiers.

**Definition 6.** A **type** definition D, is a child of another D’, if D’ is one of the supertypes of D. A type definition D is a descendant of another D’, if
there is a chain of child relationships from D to D’.

**Definition 7.** A property-value pair is defined as tuple $\langle U,V\rangle$, where

-   **U** – URI – identifying the property

-   **V** – a text string, a literal or a URI

**Definition 8.** A property-range pair is defined as tuple $\langle U,R\rangle$, where

-   **U** – URI – identifying the property

-   **R** – set of URIs – defining the range

**Definition 9.** An instance is described as triple $\langle N,T,PV\rangle$, where

-   **N** – URI – identifier of the instance

-   **T** – non-empty set of URIs – identifiers of types of the item

-   **PV** – possibly empty set of property-value pairs

An instance of type Bed is represented in the following way $\langle \{http://example.org/instance/b1\},\{Bed\},\{\langle name, "King Size Bed"\rangle, \langle occupancy, "2"\rangle \}\rangle$.

**Definition 10.** A global property is defined as triple $\langle U,R,D\rangle$, where

-   **U** – URI – identifier of the property

-   **R** – non-empty set of URIs – ranges of the property

-   **D** – non-empty set of URIs – domains for which the property is
    applied to

An example of a global property could be *rating*, that is applied to the domains *Event* and *Hotel*. *Rating* and *String* are possible values for this property. $\langle rating, \{Rating, String\}, \{Event, Hotel\}\rangle$.

**Definition 11.** A MSKR knowledge base is described as sextuple $\langle DT, ET, GP, I, LP, RT\rangle$, where

-   **DT** – set of datatype definitions

-   **ET** – set of enumerated type definitions

-   **GP** – set of global property definitions

-   **I** - set of instances that satisfy the following conditions:
    -   Each URI is the identifier of at most one definition in T, and
        similarly for P. There is at most one definition for any URI in
        T and P.

    -   The descendant relationship for types in T is a strict
        partial order.

    -   For each literal $\langle U,V\rangle$ in the knowledge base
        there is a datatype definition $\langle U\rangle$ in T.

    -   T has a datatype definition for U iff U $<$ datatype in T.

    -   T has an enumerated type definition for U iff U $<$ enumeration
        in T.

    -   T has a regular type definition for U iff U is datatype or
        regular type or U $<$ regular type but not U $<$ enumeration
        in T.

-   **LP** - set of local property definitions

-   **RT** - set of regular type definitions

[^1]: [See RFC 3986 - https://tools.ietf.org/html/rfc3986](See RFC 3986 - https://tools.ietf.org/html/rfc3986)

[^2]: <https://techterms.com/definition/string>



## Formal Semantics

A full-fledged definition of the semantics of schema.org is provided in \[Patel-Schneider, 2014\] . Our definition of the formal semantics is a simplification of the work of Patel-Schneider. In contrast to Patel-Schneider, we do not formalize schema.org but our language for knowledge representation. We simplified the following things:

-   No predefined *regular types* and *datatypes*

-   Distinction between *global* & *local properties*

-   No hierarchy for

    -   *enumerated types*

    -   *datatypes*

    -   *properties*

-   simplified definition of possible *datatype* values

-   we will call an *item* “instance”

-   An *instance* can have only one URI

-   A value in property-value pairs can only be

    -   A regular type instance

    -   An enumeration type instance

    -   A datatype value

The semantics for the Maximally Simple Knowledge Representation formalism is based on interpretations, which provide formal meanings for all URIs. URIs can identify types, properties or resources. In addition, a resource can be identified by an item (see previous section for the definition of an item).

**Definition 12.** An interpretation is an octuple $\langle I_{ET},I_{GP},I_{IET},I_{LP},I_T,I_V\rangle$ where $I_{IET}$ is a set of enumeration type instances; $I_V$ is a set of data values and

-   $I_{ET}:U \rightarrow 2^{(I_{IET})}$

-   $I_{GP}:U \rightarrow 2^{(I_U  x (I_I  x I_V  x I_{IET} )  x I_T)}$

-   $I_{LP}:U \rightarrow 2^{(I_U  x (I_I  x I_V  x I_{IET}))}$

-   $I_T:U \rightarrow 2^{(I_I)}$

where the set of URIs is given by U and the set of instances is represented by I.

$I_{ET}$ maps *enumerated types* into their extensions. $I_{GP}$ maps *global properties* into sets of triples whose first element is a URI,
second element is a data value or URI (representing a *regular type instance* or an *enumeration type instance*) and third element is a set of *regular types* (the domains the global property is applied to). $I_{LP}$ maps *local properties* into sets of pairs whose first element
is a URI, second element is a data value or a URI (representing a *regular type instance* or an *enumeration type instance*). $I_T$ maps
*regular types* into their extensions.

**Definition 13.** An interpretation $\langle I_{ET},I_{GP},I_I,I_{IET},I_{LP},I_T,I_U,I_V\rangle$, satisfies a knowledge base, $\langle K_{DT},K_{ET},K_{GP},K_I,K_{LP},K_T\rangle$ iff

1.  for $\langle U,\{S_1,…,S_n\},PR\rangle$ a regular type definition in $K_T,I_T (U) \subseteq I_T (S_i )$;

2.  for $\langle U,\{E_1,…,E_m\}\rangle$ an enumerated type definition in $K_{ET}$,

    1.  $I_T (U)=\{I_U (e)| e \in E\}$, and

    2.  $\forall e_i \neq e_j \in E; I_U (e_i) \neq I_U(e_j)$

3.  for $\langle U\rangle$ a datatype definition in $K_{DT}$, such that $I_V(U)=$all allowed values of the datatype

4.  for INST=$\langle U,\{T_1,…,T_m\},\{\langle P_1,V_1\rangle,...,\langle P_l,V_l\rangle \}\rangle$, an item $K_I$,

    1.  $I_I(INST)  \subseteq I_T (T_i),1 \leq i \leq m$,

    2.  for $x \in I_I(INST)$, for $1 \leq i \leq l$, there exists $\langle P_i,R\rangle$ a property definition and there exists y such that $\langle x,y\rangle \in I_{LP} (P_i)$ and

        1.  if $V_i$ is a regular type instance then $y \in I_I (V_i)$

        2.  if $V_i$ is an enumerated type instance then
            $y \in I_{IET} (V_i)$

        3.  if $V_i$ is a value of a datatype then $y \in I_V (V_i)$

5.  for each U,for each $\langle x,y\rangle \in  I_{LP}(U)$,

    -   there exists $\langle T,S,PR\rangle$ a regular type definition in $K_T$ such that $U \in PR$ and $y \in I_T(U)$ and

    -   there exists $\langle U,R\rangle$ a local property definition in $K_{LP}$ such that there exists $R'\in R$ with $y \in I_T(R')$

6.  for $GP=\langle U,\{R_1,...,R_m\},\{D_1,...,D_m\}\rangle$ a global
    property definition in $K_{GP}$,
    1.  GP is applied to $\langle I,T,PV\rangle$ an instance definition in $K_I$,iff $I_T(U) \subseteq I_T (D_i)$,for $1 \leq i \leq n$

    2.  there exists $y$ such that $\langle x,y,z\rangle \in I_{GP}(U)$ and $R'_i \in R_i$, for $1 \leq i \leq m$, with $y \in I_T(R'_i)$, for $1 \leq i \leq m$.

In the following we give a textual explanation of the different clauses mentioned in *Definition 1*. The first clause describes the type generalization hierarchy, which means that the extension of a type is a subset of the extension of each of its parent types. The second clause gives a formal semantics for enumeration types. First part of the clause describes that an extension of an enumeration is the set of all enumeration type instances. The second part states that all these instances are different from each other. The third clause defines the extension of a datatype as its set of possible/valid values (according to the XML definition of [datatypes](https://www.w3.org/TR/xmlschema-2/) ). The fourth clause defines all parts of an instance. The first part of the clause states that an instance is in the extension of its types. The second part of this clause gives a definition on the property-value pairs of an instance. In detail, the relationship between instance and the value of the property. We differentiate three different types of values: a *regular type instance*, an *enumerated type instance* (both referenced via URI) or a *datatype* value. Domain and range restrictions for *local properties* are enforced in the fifth clause. For each property, there exists a *regular type* definition that defines the property with its range. This property is then applied to all instances that are in the extension of this *regular type* definition. The value of the property belongs to one of the defined ranges. The sixth clause is about *global properties*. First part of the global properties clause states that a global property is applied to an instance if the type of the instance lies in the domain of the *global property*. The second part of the clause enforces range restrictions for *global properties*. If there is an instance in the domain of a *global property* and the property has a value, then the value of the property belongs to one of the ranges.



## Concrete Syntax

MSKR is aligned with the data model of schema.org, which is derived from RDF-Schema. RDF-Schema itself is an extension of RDF. A language applicable to describe and verify RDF data is SHACL[^1]. As syntax for MSKR, a special notation of SHACL is used to define types, their supertype, and properties. This notation is a shortcut of the standard notation without explicitly mentioning the target class (the focus node of a SHACL shape). Due to this shortcut, a more intuitive definition of types is possible. The special notation of SHACL implicitly defines target classes for SHACL shapes and is defined as follows:

*“If s is a SHACL instance of sh:NodeShape or sh:PropertyShape in a shapes graph SG and s is also a SHACL instance of rdfs:Class in SG then the set of SHACL instances of s in a data graph DG is a target from DG for s in SG.”* - SHACL Specification Implicit Class Targets[^2]

Besides, the MSKR syntax requires the property *rdfs:subClassOf* for each type definition to determine the hierarchy and especially the inheritance of constraints from supertypes. Except for those two requirements, we aim to support all the other SHACL features[^3].

An example using the short notation of SHACL for defining a *Hotel* type is shown in the following Listing:

```SHACL
@prefix schema: <http://schema.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

schema:Hotel
  a rdfs:Class, sh:NodeShape ;
  rdfs:subClassOf schema:Thing;
  sh:property [
    sh:path schema:makesOffer ;
    sh:node schema:Offer ;
    sh:name "Things the hotel offers" ;
  ] ;
  sh:property [
    sh:path schema:name ;
    sh:datatype xsd:string ;
    sh:name "Name of the hotel" ;
  ] .
```


The shape for type *schema:Hotel* is defined as *rdfs:Class* with the relevant constraints for the properties. Additionally, to represent the type hierarchy the property *rdfs:subClassOf* is used. In this listing the *rdfs:subClassOf* property defines that *schema:Hotel* is a subclass of *schema:Thing*.

For the definition of property shapes, there is no such notation defined. Therefore, the property *sh:targetClass* is used to define the domains the global property applies. An example for defining `location` as a global property is given in the following Listing:

    ex:GlobalLocationShape
      a sh:PropertyShape ;
      sh:targetClass schema:Event, schema:Organization ;
      sh:path schema:location ;
      sh:or (
        [ sh:class schema:Place ; ]
        [ sh:class schema:PostalAddress ; ]
        [ sh:datatype xsd:string ; ]
        [ sh:class schema:VirtualLocation ; ]
      ) ;
      sh:name "location of something" .


[^1]: <https://www.w3.org/TR/shacl/>

[^2]: Quoted from: <https://www.w3.org/TR/shacl/#implicit-targetClass>

[^3]: consider the SHACL documentation for a definition of other


## References

[Patel-Schneider, 2014] -  Patel-Schneider, P.F.: Analyzing schema. org. In: International Semantic Web Con-ference. pp. 261–276. Springer (2014)
