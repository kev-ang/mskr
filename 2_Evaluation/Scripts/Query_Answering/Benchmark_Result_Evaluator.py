import getopt
import os
import sys
import time
import requests
import json


def evaluate_report(benchmark_report):
    a_dictionary = {}
    a_file = open('/Users/Kevin/Documents/GitHub/Kev_ang/mskr/Benchmark_Temp_Dir/Query_Results/benchmark_results_mskr.json')
    for line in a_file:
        key, value = line.split()
        a_dictionary[key] = value

    print(a_dictionary)


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "r:")

    for o, a in opts:
        if o == "-r":
            benchmark_report = a
        else:
            assert False, "unhandled option"

    evaluate_report(benchmark_report)
