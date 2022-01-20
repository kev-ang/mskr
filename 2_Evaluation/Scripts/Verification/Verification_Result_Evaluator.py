import collections
import getopt
import os
import sys
import csv
import json
from datetime import datetime


def write_error_report(path, message):
    with open(path + "/error.dataset_modification_log", "a", encoding="utf8") as file:
        file.write(message + "\n")

def load_reports(benchmark_report_folder):
    report = {}
    for dataset in os.listdir(benchmark_report_folder):
        if not os.path.isdir(os.path.join(benchmark_report_folder, dataset)):
            continue
        report[dataset] = {}

        for formalism in os.listdir(os.path.join(benchmark_report_folder, dataset)):
            if not os.path.isdir(os.path.join(benchmark_report_folder, dataset, formalism)):
                continue
            with open(os.path.join(benchmark_report_folder, dataset, formalism, 'results', dataset + '.aggregatedTestCaseResult.jsonld')) as file:
                report[dataset][formalism] = json.load(file)

    return report

def check_validation_results(reports, folder):
    for dataset in reports:
        for formalism in reports[dataset]:
            if reports[dataset][formalism]['testsError'] != 0 or reports[dataset][formalism]['testsFailed'] != 0 :
                write_error_report(folder, 'Errors occured for ' + dataset + ' under ' + formalism + ' which should not be the case.')


def collect_execution_times(reports, csv_output_folder):
    reports = json.loads(json.dumps(reports, sort_keys=True))
    with open(os.path.join(csv_output_folder, 'Constraint_Checking_Results.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Create headline
        headline = ['Dataset']
        isHeadline = True

        for dataset in reports:
                line = [dataset]
                for formalism in reports[dataset]:
                    start = datetime.strptime(reports[dataset][formalism]['startedAtTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    end = datetime.strptime(reports[dataset][formalism]['endedAtTime'], '%Y-%m-%dT%H:%M:%S.%fZ')

                    delta = end - start
                    print(delta)
                    print(delta.total_seconds()/60)
                    line.append(delta.total_seconds()/60)
                    if isHeadline:
                        headline.append(formalism)
                if isHeadline:
                    writer.writerow(headline)
                    isHeadline = False

                writer.writerow(line)


def evaluate_report(benchmark_report_folder, csv_output_folder):
    reports = load_reports(benchmark_report_folder)
    check_validation_results(reports, csv_output_folder)
    collect_execution_times(reports, csv_output_folder)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "r:o:")

    for o, a in opts:
        if o == "-r":
            benchmark_report_folder = a
        elif o == "-o":
            csv_output_folder = a
        else:
            assert False, "unhandled option"

    evaluate_report(benchmark_report_folder, csv_output_folder)
