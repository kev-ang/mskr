import statistics
from model.Report import *
from utils.Utils import *


@dataclass
class QueryResultCollector:
    executionTime: [float]
    query: str
    result: str


def aggregate_report(report):
    aggregated_report = VerificationReport()
    for dataset_key in report.__dict__:
        dataset = getattr(report, dataset_key)
        if len(dataset) > 0:
            grouped_values = group_domain_specifications(dataset)
            setattr(aggregated_report, dataset_key, aggregate_values(grouped_values))
    return aggregated_report


def group_domain_specifications(dataset):
    grouped_domainspecifications = {}
    for domain_specification in dataset:
        if not domain_specification.domain_specification in grouped_domainspecifications:
            grouped_domainspecifications[domain_specification.domain_specification] = []
        grouped_domainspecifications[domain_specification.domain_specification].append(domain_specification)
    return grouped_domainspecifications


def aggregate_values(grouped_domain_specifications):
    aggregated_domain_specifications = []
    for domain_specification in grouped_domain_specifications:
        values = grouped_domain_specifications[domain_specification]
        number_errors = values[0].number_errors
        duration_values = []
        for value in values:
            if value.number_errors != number_errors:
                raise ValueError("Number of errors between different runs not equal!")
            duration_values.append(value.duration)
        mean = statistics.fmean(duration_values)
        aggregated_domain_specifications.append(DomainSpecificationReport(domain_specification, mean, number_errors))
    return aggregated_domain_specifications
