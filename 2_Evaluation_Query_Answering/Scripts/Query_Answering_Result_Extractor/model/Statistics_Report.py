from dataclasses import dataclass, field


@dataclass
class StatisticsDatasetReport:
    minimum: float = field(default_factory=float)
    maximum: float = field(default_factory=float)
    mean: float = field(default_factory=float)
    median: float = field(default_factory=float)
    first_quartile: float = field(default_factory=float)
    third_quartile: float = field(default_factory=float)
    fastest_query: str = field(default_factory=str)
    slowest_query: str = field(default_factory=str)


@dataclass
class StatisticsFormalismReport:
    rdfs: StatisticsDatasetReport = field(default_factory=StatisticsDatasetReport)
    mskr: StatisticsDatasetReport = field(default_factory=StatisticsDatasetReport)
    rdfs_plus: StatisticsDatasetReport = field(default_factory=StatisticsDatasetReport)
    owl_2_rl: StatisticsDatasetReport = field(default_factory=StatisticsDatasetReport)


@dataclass
class StatisticsReport:
    Univ_100: StatisticsFormalismReport = field(default_factory=StatisticsFormalismReport)
    Univ_1000: StatisticsFormalismReport = field(default_factory=StatisticsFormalismReport)
    Univ_10000: StatisticsFormalismReport = field(default_factory=StatisticsFormalismReport)
