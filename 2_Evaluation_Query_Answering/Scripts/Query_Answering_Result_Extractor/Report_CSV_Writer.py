import os
import csv

def write_report_to_csv(report, folder):
    for dataset_key in report.__dict__:
        dataset = getattr(report, dataset_key)
        write_dataset_to_csv(folder, dataset_key, dataset)


def write_dataset_to_csv(folder, dataset_key, dataset):
    with open(os.path.join(folder, dataset_key + ".csv"), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Create headline
        headline = ['formalism']
        isHeadline = True

        for formalism_key in dataset.__dict__:
            line = [formalism_key]
            formalism_object = getattr(dataset, formalism_key)
            for query in formalism_object.query_results.__dict__:
                query_object = getattr(formalism_object.query_results, query)
                line.append(query_object.executionTime)
                if isHeadline:
                    headline.append(query)
            if isHeadline:
                writer.writerow(headline)
                isHeadline = False

            writer.writerow(line)
