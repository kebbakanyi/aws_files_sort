import os
import json
from datetime import datetime
import csv

files_path = '/Users/kebba/Desktop/Precor-EE_AWS_Files/precor-ee-bucket1'
# files_path = '/Users/kebba/Desktop/Precor-EE_AWS_Files/precor-ee-bucket_main'

device_id = os.listdir(files_path)


def get_timestamp(filename):

    (name, ext) = os.path.splitext(filename)
    utc_timestamp = name[:-3]

    # subtract 28800 seconds (8 hours) to convert to pacific time
    pacific_timestamp = (int(utc_timestamp) - 28800)

    return pacific_timestamp


def readable_time(pacific_timestamp):
    # change to readable time format
    for time in pacific_timestamp:
        print(datetime.utcfromtimestamp(
            pacific_timestamp).strftime('%Y-%m-%d %H:%M:%S'))


def all_reported():
    if len(device_id) == 25:
        return True
    return False


def check_list(shifted_one, shifted_two):

    error_count = 0
    seconds_skipped = 0
    for ls_one, ls_two in zip(shifted_one, shifted_two):
        if ls_one - ls_two > 1:
            # print(ls_one, ls_two)
            error_count += 1
            seconds = ls_one - ls_two
            seconds_skipped += seconds

    return error_count, seconds_skipped


if __name__ == '__main__':

    # Check to see if there is a folder for all 25 devices
    if all_reported():
        print('Folder downloaded for all devices')
    else:
        print('One or more folders missing')

    with open('header.csv', 'w', newline='') as fi:
        thewriter = csv.writer(fi)
        thewriter.writerow(
            ['Device Id', 'Skip count', 'Seconds skiped', 'Total seconds'])

    # Recursive directory traversing
    for dirpath, dirs, files in os.walk(files_path):
        # create empty list to store the uptime and timestamp
        uptime = []
        file_count = 0

        # open each json file and extract the uptime data and append to a list
        for filename in files:
            with open(os.path.join(dirpath, filename)) as json_file:
                json_text = json.load(json_file)
                uptime.append(int(json_text["uptime"]))
                file_count += 1
        uptime.sort()

        if len(files) != 0:
            print('-' * 30)
            print(f'{os.path.basename(dirpath)} Data starts')

            shifted_uptime_one = uptime[1:]
            shifted_uptime_two = uptime[: -2]

            hundred_excluded_one = uptime[100:]
            hundred_excluded_two = uptime[99:-2]

            # for i, j in zip(shifted_uptime_one, shifted_uptime_two):
            #     print(i, j)
            # print('\n' * 2)

            errors, seconds = check_list(
                shifted_uptime_one, shifted_uptime_two)

            errors_2, seconds_2 = check_list(
                hundred_excluded_one, hundred_excluded_two)

            print(f'There were {errors} errors and {seconds} seconds missing')
            print(
                f'There were {errors_2} errors and {seconds_2} seconds missing after excluding the first 100')
            print(f'Total of {file_count} files')

            with open(f'{os.path.basename(dirpath)}.csv', 'w', newline='') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(
                    [f'{os.path.basename(dirpath)}', f'{errors}', f'{seconds}', f'{file_count}'])

            print(f'{os.path.basename(dirpath)} Data end')
            print('-' * 30)
            print('\n' * 3)
