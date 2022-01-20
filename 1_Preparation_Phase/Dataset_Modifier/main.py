import random

from SPARQLWrapper import SPARQLWrapper, JSON

graph_db_url = ""

repositories = ['Univ_5', 'Univ_10', 'Univ_50']

relevant_ontology_types = ['Department', 'University', 'GraduateCourse', 'AssociateProfessor',
                           'AssistantProfessor']

used_uris_per_type = {'University': 'http://www.University0.edu',
                      'Department': 'http://www.Department0.University0.edu',
                      'GraduateCourse': 'http://www.Department0.University0.edu/GraduateCourse0',
                      'AssociateProfessor': 'http://www.Department0.University0.edu/AssociateProfessor0',
                      'AssistantProfessor': 'http://www.Department0.University0.edu/AssistantProfessor0'}


def add_same_as_links(sparqlWrapper, origin, targets):
    sparqlWrapper.setMethod('PUT')

    print('Targets:')
    same_as_triples = []
    for target in targets:
        print(target)
        same_as_triples.append('<' + origin + '> owl:sameAs <' + target + '>.')

    inner_query_part = '\n'.join(same_as_triples)


    sparqlWrapper.setQuery(f"""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        INSERT DATA {{
            {inner_query_part}
        }}
    """)

    results = sparqlWrapper.query()
    print(results.response.read())


def enrich_instances_of_type(sparqlWrapper, type):
    queryString = 'SELECT * WHERE { ?s a <http://swat.cse.lehigh.edu/onto/univ-bench.owl#' + type + '>. }'
    sparqlWrapper.setQuery(queryString)
    sparqlWrapper.setReturnFormat(JSON)
    results = sparqlWrapper.query().convert()

    instances = []
    for result in results["results"]["bindings"]:
        instances.append(result["s"]["value"])

    if used_uris_per_type[type] in instances:
        instances.remove(used_uris_per_type[type])

    n = random.randrange(1, min(len(instances) - 1, 15000))
    print('Selecting ' + str(n) + '/' + str(len(instances)) + ' instances for type ' + type)
    selected_instances = random.sample(instances, n)
    add_same_as_links(sparqlWrapper, used_uris_per_type[type], selected_instances)


if __name__ == '__main__':
    for repository in repositories:
        print('Repository: ' + repository)
        sparqlWrapper = SPARQLWrapper(graph_db_url + repository, graph_db_url + repository + '/statements')
        for relevant_ontology_type in relevant_ontology_types:
            print('Type: ' + relevant_ontology_type)
            enrich_instances_of_type(sparqlWrapper, relevant_ontology_type)
