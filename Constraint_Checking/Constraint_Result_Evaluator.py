import collections
import getopt
import os
import sys
import csv
import json

def write_error_report(path, message):
    with open(path + "/error.log", "a", encoding="utf8") as file:
        file.write(message + "\n")

def readlast(f, sep, fixed=True):
    """Read the last segment from a file-like object.

    :param f: File to read last line from.
    :type  f: file-like object
    :param sep: Segment separator (delimiter).
    :type  sep: bytes, str
    :param fixed: Treat data in ``f`` as a chain of fixed size blocks.
    :type  fixed: bool
    :returns: Last line of file.
    :rtype  : bytes, str
    """
    bs = len(sep)
    step = bs if fixed else 1
    if not bs:
        raise ValueError("Zero-length separator.")
    try:
        o = f.seek(0, os.SEEK_END)
        o = f.seek(o-bs-step)      # - Ignore trailing delimiter 'sep'.
        while f.read(bs) != sep:   # - Until reaching 'sep': Read data, seek past
            o = f.seek(o-step)     # read data *and* the data to read next.
    except (OSError, ValueError):  # - Beginning of file reached.
        f.seek(0)
    return f.read()[:-1]


def validation_time(path):
    """Reads the stats file at the given path and reports the runtime in milliseconds.

    :param path: path of the stats file
    :type: str
    :return: runtime in milliseconds
    :rtype: int
    """
    with open(path + "/stats.txt", "r", encoding="utf8") as file:
        last_line = readlast(file, "\n", False)
#        print(path, last_line)
        if not last_line:
            return -1
        return int(last_line)

def read_files(filename):
    with open(filename, "r", encoding="utf8") as file:
        content = file.read()
        return content.split("\n")

def load_reports(benchmark_report_folder):
    report = {}
    for dataset in os.listdir(benchmark_report_folder):
        if not os.path.isdir(os.path.join(benchmark_report_folder, dataset)):
            continue
        report[dataset] = {}

        for schema in os.listdir(os.path.join(benchmark_report_folder, dataset)):
            if not os.path.isdir(os.path.join(benchmark_report_folder, dataset, schema)):
                continue
            report[dataset][schema] = {}

            for formalism in os.listdir(os.path.join(benchmark_report_folder, dataset, schema)):
                if not os.path.isdir(os.path.join(benchmark_report_folder, dataset, schema, formalism)):
                    continue
                report[dataset][schema][formalism] = {}

                val_time = validation_time(os.path.join(benchmark_report_folder, dataset, schema, formalism))
                valid_targets = read_files(os.path.join(benchmark_report_folder, dataset, schema, formalism, "targets_valid.log"))
                invalid_targets = read_files(os.path.join(benchmark_report_folder, dataset, schema, formalism, "targets_violated.log"))
                report[dataset][schema][formalism]["validation_time"] = val_time
                report[dataset][schema][formalism]["valid_targets"] = valid_targets
                report[dataset][schema][formalism]["invalid_targets"] = invalid_targets

    return report

def check_validation_results(reports, folder):
    for dataset in reports:
        for schema in reports[dataset]:
            base_case_valid_targets = ''
            base_case_invalid_targets = ''
            for formalism in reports[dataset][schema]:
                if not base_case_valid_targets and not base_case_invalid_targets:
                    base_case_valid_targets = reports[dataset][schema][formalism]["valid_targets"]
                    base_case_valid_targets.sort()
                    base_case_invalid_targets = reports[dataset][schema][formalism]["invalid_targets"]
                    base_case_invalid_targets.sort()
                else:
                    to_compare_valid_targets = reports[dataset][schema][formalism]["valid_targets"]
                    to_compare_valid_targets.sort()
                    to_compare_invalid_target = reports[dataset][schema][formalism]["invalid_targets"]
                    to_compare_invalid_target.sort()
                    valids_equal = base_case_valid_targets == to_compare_valid_targets
                    invalids_equal = base_case_invalid_targets == to_compare_invalid_target

                    if not valids_equal or not invalids_equal:
                        write_error_report(folder, "Result are not the same for " + dataset + " -> " + schema)

def collect_execution_times(reports, csv_output_folder):
    reports = json.loads(json.dumps(reports, sort_keys=True))
    for dataset in reports:
        with open(os.path.join(csv_output_folder, dataset) + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # Create headline
            headline = ['Shapes']
            isHeadline = True

            for shape in reports[dataset]:
                line = [shape]
                for formalism in reports[dataset][shape]:
                    line.append(reports[dataset][shape][formalism]['validation_time'])
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
