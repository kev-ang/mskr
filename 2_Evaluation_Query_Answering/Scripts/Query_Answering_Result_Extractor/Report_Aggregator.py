import statistics
from model.Report import *
from utils.Utils import *


@dataclass
class QueryResultCollector:
    executionTime: [float]
    query: str
    result: str


def aggregate_report(report):
    aggregated_report = AggregatedOverallReport()
    for formalism_key in report.__dict__:
        formalism_object = getattr(report, formalism_key)
        for dataset_key in formalism_object.__dict__:
            report_formalism = getattr(report, formalism_key)
            report_formalism_dataset = getattr(report_formalism, dataset_key)
            if len(report_formalism_dataset) > 0:
                aggregated_queries = prepare_run_values(report_formalism_dataset)
                aggregated_dataset = getattr(aggregated_report, dataset_key)
                setattr(aggregated_dataset, formalism_key,
                        DatasetFormalismReport(dataset_key, formalism_key, aggregated_queries))
    return aggregated_report


def prepare_run_values(datasetReport: list[DatasetFormalismReport]):
    collected_values = collect_run_values(datasetReport)
    return aggregate_values(collected_values)


def collect_run_values(datasetReport: list[DatasetFormalismReport]):
    collected_query_results = {}
    for formalism_report in datasetReport:
        for query in formalism_report.query_results:
            if query not in collected_query_results:
                current_query = formalism_report.query_results[query]
                collected_query_results[query] = QueryResultCollector([current_query["executionTime"]],
                                                                      current_query["query"],
                                                                      current_query["result"])
            else:
                existing_query = collected_query_results[query]
                current_query = formalism_report.query_results[query]
                existing_query.executionTime.append(current_query["executionTime"])
                if not compare_result(existing_query.result, current_query["result"]):
                    print(
                        "ERROR! Different results for query " + query + " for formalism " + formalism_report.formalism)
    return collected_query_results


def aggregate_values(collected_query_results):
    aggregated_queries = Queries()
    for query in collected_query_results:
        current_collection = collected_query_results[query]
        mean_value = statistics.fmean(current_collection.executionTime)
        query_attribute = getattr(aggregated_queries, query)
        query_attribute.executionTime = mean_value
        query_attribute.query = current_collection.query
        query_attribute.result = current_collection.result
    return aggregated_queries
