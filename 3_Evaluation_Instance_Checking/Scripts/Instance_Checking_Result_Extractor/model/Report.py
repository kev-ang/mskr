from dataclasses import dataclass, field


@dataclass
class DomainSpecificationReport:
    domain_specification: str = field(default_factory=str)
    duration: float = field(default_factory=float)
    number_errors: int = field(default_factory=int)


@dataclass
class VerificationReport:
    Univ_100: list[DomainSpecificationReport] = field(default_factory=list)
    Univ_1000: list[DomainSpecificationReport] = field(default_factory=list)
    Univ_10000: list[DomainSpecificationReport] = field(default_factory=list)
