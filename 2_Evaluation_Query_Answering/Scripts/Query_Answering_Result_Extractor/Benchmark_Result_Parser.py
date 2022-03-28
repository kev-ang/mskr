import json
import os
from model.Report import DatasetFormalismReport, OverallReport
from utils.Utils import *


def parse_benchmark_results(benchmark_report_directory, run_directories):
    overall_report = OverallReport()
    # Determine formalisms based on the given folders
    for run_folder in run_directories:
        sub_folders = []
        for dir, sub_dirs, files in os.walk(os.path.join(benchmark_report_directory, run_folder)):
            sub_folders.extend(sub_dirs)

        for formalism in sub_folders:
            for dir, sub_dirs, files in os.walk(os.path.join(benchmark_report_directory, run_folder, formalism)):
                for file in files:
                    if file.startswith("Univ") and file.endswith(".json"):
                        print("Loading " + os.path.join(run_folder, formalism, file) + " ...")
                        with open(os.path.join(benchmark_report_directory, run_folder, formalism, file)) as f:
                            report_dict = json.load(f)
                            report_object = DatasetFormalismReport(**report_dict)
                            report_formalism = getattr(overall_report, formalism.replace("-", "_"))
                            report_dataset = getattr(report_formalism, extract_dataset_from(file))
                            report_dataset.append(report_object)
    return overall_report
