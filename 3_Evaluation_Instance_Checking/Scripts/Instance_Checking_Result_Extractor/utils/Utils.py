import json

def extract_dataset_from(file_name):
    if file_name:
        return file_name.replace(".json", "")
    return file_name


def split_run_folders_string(run_folders):
    """
    The benchmark was done in three runs. This method splits a string of given folders (one for each run) into a list containing each folder separately.
    :param run_folders: string representing all the folders that contain results
    :return: list consisting of an entry for each directory
    """
    if run_folders:
        return run_folders.split(";")
    return run_folders

def compare_result(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
