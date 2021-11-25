import getopt
import os
import sys
import time
import requests
import json


def execute(sparql_endpoint, sparql_query_folder, formalism, dataset, output_path):
    sparql_queries = load_queries(sparql_query_folder)
    sparql_results = run_queries(sparql_endpoint, sparql_queries)

    dataset_config_object = {}
    dataset_config_object["formalism"] = formalism
    dataset_config_object["dataset"] = dataset
    dataset_config_object["query_results"] = sparql_results

    filename = output_path + '/' + formalism + '/' + dataset + '.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a') as out:
        out.write(json.dumps(dataset_config_object, indent=4, sort_keys=True, default=str))
        out.close


def load_queries(query_folder):
    queries = {}
    sparql_files = [os.path.join(query_folder, f) for f in os.listdir(query_folder) if
                    os.path.isfile(os.path.join(query_folder, f)) and f.endswith(".sparql")]
    for file in sparql_files:
        with open(file) as file_reader:
            query_name = file.split(os.sep)[-1].replace(".sparql", "")
            queries[query_name] = ''.join(file_reader.readlines())

    return queries


def run_queries(endpoint, queries):
    results = {}
    for query_number in queries:
        query_entry = {}
        query = queries[query_number]
        print('Executing query: ' + query_number)
        start_time = time.monotonic()
        result = requests.get(endpoint, params={'query': query})
        end_time = time.monotonic()
        query_entry["query"] = query
        query_entry["result"] = result.text
        query_entry["executionTime"] = end_time - start_time
        results[query_number] = query_entry
    return results


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "d:e:f:o:q:")

    for o, a in opts:
        if o == "-e":
            sparql_endpoint = a
        elif o == "-q":
            sparql_query_folder = a
        elif o == "-f":
            formalism = a
        elif o == "-d":
            dataset = a
        elif o == "-o":
            output_path = a
        else:
            assert False, "unhandled option"

    execute(sparql_endpoint, sparql_query_folder, formalism, dataset, output_path)
