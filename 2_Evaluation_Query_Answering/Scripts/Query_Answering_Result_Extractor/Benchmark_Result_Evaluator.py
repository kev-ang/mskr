import getopt
import sys
from Benchmark_Result_Parser import *
from Report_Aggregator import *
from Formalism_Comparator import *
from Report_CSV_Writer import *


def evaluate_report(benchmark_report_folder, run_folders, csv_output_folder):
    """
    Overall method handling the evaluation of the benchmark results.
    :param benchmark_report_folder: path to the root folder containing the benchmark results.
    :param run_folders: list of subfolders within the benchmark_report_folder containing the benchmark results.
    :param csv_output_folder: folder that should contain the results of the evaluation
    """
    # Load all benchmark results into a single report
    print("Loading reports...")
    report = parse_benchmark_results(benchmark_report_folder, run_folders)
    # Aggregate the runs into a single report
    print("Aggregating reports from different runs...")
    aggregated_report = aggregate_report(report)
    # Check whether different formalisms deliver the same result
    print("Check results for each query of the different formalisms...")
    check_query_results(aggregated_report)
    # Write statistics report into separate files for each dataset
    print("Write statistics report to separate csv files...")
    write_report_to_csv(aggregated_report, csv_output_folder)

    print("DONE!")


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "r:o:f:")

    for o, a in opts:
        if o == "-r":
            benchmark_report_folder = a
        elif o == "-o":
            csv_output_file = a
        elif o == "-f":
            run_folders = a
        else:
            assert False, "unhandled option"

    evaluate_report(benchmark_report_folder, split_run_folders_string(run_folders), csv_output_file)
