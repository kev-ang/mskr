import getopt
import os
import sys
import csv
import json

def write_error_report(path, message):
    with open(path + "/error.log", "a", encoding="utf8") as file:
        file.write(message + "\n")

def load_reports(benchmark_report_folder):
    reports = {}
    sub_folders = []
    # Determine formalisms based on the given folders
    for dir, sub_dirs, files in os.walk(benchmark_report_folder):
        sub_folders.extend(sub_dirs)

    # Load all reports for the formalisms
    formalism_files = []
    for formalism in sub_folders:
        for dir, sub_dirs, files in os.walk(benchmark_report_folder + '/' + formalism):
            for file in files:
                f = open(benchmark_report_folder + '/' + formalism + '/' + file)
                report = json.load(f)
                if report["dataset"] not in reports:
                    reports[report["dataset"]] = [report]
                else:
                    reports[report["dataset"]].append(report)

    return reports

def compare_results(reports, folder):
    # Group all formalisms based on the query and dataset
    queries = {}
    for dataset in reports:
        results_per_dataset = {}
        formalisms = reports[dataset]
        for formalism in formalisms:
            query_entry = {}
            query_entry["formalism"] = formalism["formalism"]
            for query in formalism["query_results"]:
                query_entry["results"] = formalism["query_results"][query]["result"]
                if (query + "_" + dataset) in queries:
                    queries[(query + "_" + dataset)].append(query_entry)
                else:
                    queries[(query + "_" + dataset)] = [query_entry]

    # Compare the results per query
    for query in queries:
        formalisms = queries[query]
        base_result = formalisms[0]["results"]
        for i in range(1, len(formalisms)):
            to_compare = formalisms[i]["results"]
            equal = json.dumps(base_result, sort_keys=True) ==  json.dumps(to_compare,sort_keys=True)
            if not equal:
                write_error_report(folder, "Results for query " + query + " differs for the different formalisms!")

def calculate_mean_duration(reports):
    timing_report = {}
    for report in reports:
        formalism_report = {}
        for formalism in reports[report]:
            query_results = formalism["query_results"]
            totalCount = 0
            for query in query_results:
                totalCount = totalCount + float(query_results[query]["executionTime"])
            mean = totalCount / len(query_results)
            formalism_report[formalism["formalism"]] = mean

        timing_report[report] = formalism_report

    return timing_report

def write_to_csv(timing_report, csv_output_file):
    with open(csv_output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        sorted_json = json.dumps(timing_report, sort_keys=True)
        # Create headline
        headline = ['dataset']
        isHeadline = True

        for dataset in timing_report:
            line = [dataset]
            for formalism in timing_report[dataset]:
                line.append(timing_report[dataset][formalism])
                if isHeadline:
                    headline.append(formalism)
            if isHeadline:
                writer.writerow(headline)
                isHeadline = False

            writer.writerow(line)


def evaluate_report(benchmark_report_folder, csv_output_file):
    reports = load_reports(benchmark_report_folder)
    compare_results(reports, benchmark_report_folder)
    timing_report = calculate_mean_duration(reports)
    write_to_csv(timing_report, csv_output_file)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "r:o:")

    for o, a in opts:
        if o == "-r":
            benchmark_report_folder = a
        elif o == "-o":
            csv_output_file = a
        else:
            assert False, "unhandled option"

    evaluate_report(benchmark_report_folder, csv_output_file)
