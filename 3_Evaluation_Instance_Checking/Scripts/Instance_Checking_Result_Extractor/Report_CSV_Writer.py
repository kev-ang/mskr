import os
import csv

def group_duration_by_domain_specification(statistics_report):
    grouped_durations = {}
    grouped_durations["Univ_100"] = {}
    grouped_durations["Univ_1000"] = {}
    grouped_durations["Univ_10000"] = {}
    for dataset_key in statistics_report.__dict__:
        domain_specifications = getattr(statistics_report, dataset_key)
        if domain_specifications:
            for domain_specification in domain_specifications:
                grouped_durations[dataset_key][domain_specification.domain_specification] = domain_specification.duration

    # Sort domain specifications
    grouped_durations["Univ_100"] = dict(sorted(grouped_durations["Univ_100"].items()))
    grouped_durations["Univ_1000"] = dict(sorted(grouped_durations["Univ_1000"].items()))
    grouped_durations["Univ_10000"] = dict(sorted(grouped_durations["Univ_10000"].items()))
    return grouped_durations


def write_report_to_csv(statistics_report, folder):
    grouped_durations = group_duration_by_domain_specification(statistics_report)
    with open(os.path.join(folder, "Instance_Checking_Results.csv"), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Create headline
        headline = ['dataset']
        isHeadline = True

        for dataset_key in grouped_durations:
            line = [dataset_key]
            if grouped_durations[dataset_key]:
                for domain_specification in grouped_durations[dataset_key]:
                    duration = grouped_durations[dataset_key][domain_specification]
                    line.append(duration)
                    if isHeadline:
                        headline.append(domain_specification)
                if isHeadline:
                    writer.writerow(headline)
                    isHeadline = False

                writer.writerow(line)
