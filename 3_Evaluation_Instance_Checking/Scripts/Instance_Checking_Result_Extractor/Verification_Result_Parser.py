import json
import os
from model.Report import *
from utils.Utils import *


def parse_verification_results(benchmark_report_directory, run_directories):
    overall_report = VerificationReport()
    # Determine formalisms based on the given folders
    for run_folder in run_directories:
        sub_folders = []
        for dir, sub_dirs, files in os.walk(os.path.join(benchmark_report_directory, run_folder)):
            sub_folders.extend(sub_dirs)

        for dataset in sub_folders:
            for dir, sub_dirs, files in os.walk(os.path.join(benchmark_report_directory, run_folder, dataset)):
                for file in files:
                    if file.startswith("LUBM") and file.endswith(".txt"):
                        with open(os.path.join(benchmark_report_directory, run_folder, dataset, file)) as f:
                            report_dict = json.load(f)
                            getattr(overall_report, dataset).append(DomainSpecificationReport(
                                report_dict["Verification settings"]["Used Domain Specification"],
                                report_dict["Statistics"]["Total duration (Seconds)"],
                                report_dict["Statistics"]["Number of errors found"]))
    return overall_report
