from dataclasses import dataclass, field


@dataclass
class QueryResult:
    executionTime: float = field(default_factory=float)
    query: str = field(default_factory=str)
    result: str = field(default_factory=str)


@dataclass
class Queries:
    query1: QueryResult = field(default_factory=QueryResult)
    query2: QueryResult = field(default_factory=QueryResult)
    query3: QueryResult = field(default_factory=QueryResult)
    query4: QueryResult = field(default_factory=QueryResult)
    query5: QueryResult = field(default_factory=QueryResult)
    query6: QueryResult = field(default_factory=QueryResult)
    query7: QueryResult = field(default_factory=QueryResult)
    query8: QueryResult = field(default_factory=QueryResult)
    query9: QueryResult = field(default_factory=QueryResult)
    query10: QueryResult = field(default_factory=QueryResult)
    query11: QueryResult = field(default_factory=QueryResult)
    query12: QueryResult = field(default_factory=QueryResult)
    query13: QueryResult = field(default_factory=QueryResult)
    query13a: QueryResult = field(default_factory=QueryResult)
    query14: QueryResult = field(default_factory=QueryResult)


@dataclass
class DatasetFormalismReport:
    dataset: str = field(default_factory=str)
    formalism: str = field(default_factory=str)
    query_results: Queries = field(default_factory=Queries)


@dataclass
class DatasetReport:
    Univ_100: list[DatasetFormalismReport] = field(default_factory=list)
    Univ_1000: list[DatasetFormalismReport] = field(default_factory=list)
    Univ_10000: list[DatasetFormalismReport] = field(default_factory=list)


@dataclass
class OverallReport:
    rdfs: DatasetReport = field(default_factory=DatasetReport)
    mskr: DatasetReport = field(default_factory=DatasetReport)
    rdfs_plus: DatasetReport = field(default_factory=DatasetReport)
    owl_2_rl: DatasetReport = field(default_factory=DatasetReport)

@dataclass
class AggregatedDatasetReport:
    rdfs: DatasetFormalismReport = field(default_factory=DatasetFormalismReport)
    mskr: DatasetFormalismReport = field(default_factory=DatasetFormalismReport)
    rdfs_plus: DatasetFormalismReport = field(default_factory=DatasetFormalismReport)
    owl_2_rl: DatasetFormalismReport = field(default_factory=DatasetFormalismReport)

@dataclass
class AggregatedOverallReport:
    Univ_100: AggregatedDatasetReport = field(default_factory=AggregatedDatasetReport)
    Univ_1000: AggregatedDatasetReport = field(default_factory=AggregatedDatasetReport)
    Univ_10000: AggregatedDatasetReport = field(default_factory=AggregatedDatasetReport)