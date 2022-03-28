from utils.Utils import *


def check_query_results(report):
    queries_per_dataset = group_query_results_by_dataset(report)
    compare_query_results(queries_per_dataset)


def group_query_results_by_dataset(report):
    queries_per_dataset = {}
    for formalism in report.__dict__:
        dataset_reports = getattr(report, formalism)
        for dataset in dataset_reports.__dict__:
            dataset_report = getattr(dataset_reports, dataset)
            dataset_report_query_results = dataset_report.query_results
            if dataset_report_query_results:
                for query in dataset_report_query_results.__dict__:
                    query_object = getattr(dataset_report.query_results, query)
                    query_entry = {}
                    query_entry["formalism"] = formalism
                    query_entry["results"] = query_object.result
                    query_identifier = query + "_" + dataset
                    if query_identifier in queries_per_dataset:
                        queries_per_dataset[query_identifier].append(query_entry)
                    else:
                        queries_per_dataset[query_identifier] = [query_entry]
    return queries_per_dataset


def compare_query_results(queries_per_dataset):
    for query in queries_per_dataset:
        query_results = queries_per_dataset[query]
        base_formalism, base_element = select_first_non_empty_result(query_results)
        if not base_element:
            print("ERROR: No formalism delivered result for query " + query + "!")
        else:
            for query_result in query_results:
                if not query_result["results"]:
                    print("Formalism " + query_result["formalism"] + " did not deliver a result for query " + query)
                elif not compare_result(base_element, query_result["results"]):
                    print("ERROR: Query results for query " + query + " for formalism " + query_result[
                        "formalism"] + " are not matching the results of " + base_formalism)


def select_first_non_empty_result(query_results):
    for query_result in query_results:
        if query_result["results"]:
            return query_result["formalism"], query_result["results"]

    return "", ""
