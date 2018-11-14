import os
import json
from datetime import datetime
import csv

files_path = '/Users/kebba/Desktop/Precor-EE_AWS_Files/precor-ee-bucket1'
# files_path = '/Users/kebba/Desktop/Precor-EE_AWS_Files/precor-ee-bucket_main'

device_id = os.listdir(files_path)
# device_id = ['esp32_1C8BA4', 'esp32_1C9D24']

# TODO make dictionary to rettrieve the amount of files in the each folder and make sure it matches with the total scanned later on
# device_id = ['esp32_1C8BA4', 'esp32_1C8BC0', 'esp32_1C8C44', 'esp32_1C8F1C', 'esp32_1C8F6C',
#              'esp32_1C8F14', 'esp32_1C8F30', 'esp32_1C8F44', 'esp32_1C9B2C', 'esp32_1C9CDC',
#              'esp32_1C9CFC', 'esp32_1C9D0C', 'esp32_1C9D20', 'esp32_1C9D24', 'esp32_1C9D44',
#              'esp32_1C9D50', 'esp32_1C86EC', 'esp32_1C88E8', 'esp32_1C888C', 'esp32_1C8684',
#              'esp32_1C8988', 'esp32_1C9294', 'esp32_1CA2E0', 'esp32_1CA3A8', 'esp32_1CA124'
#              ]


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
    if (len(device_id) - 1) == 25:
        return True
    return False


if __name__ == '__main__':

    # Check to see if there is a folder for all 25 devices
    if all_reported():
        print('Folder downloaded for all devices')
    else:
        print('One or more folders missing')

    total_timestamp_diff = 0
    total_uptime_diff = 0

    # Recursive directory traversing
    for dirpath, dirs, files in os.walk(files_path):
        # create empty list to store the uptime and timestamp
        uptime = []
        timestamp = []
        file_count = 0
        for filename in files:

            with open(os.path.join(dirpath, filename)) as json_file:
                json_text = json.load(json_file)
                uptime.append(int(json_text["uptime"]))

                timestamp.append(get_timestamp(filename))
                file_count += 1
        uptime.sort()
        timestamp.sort()

        if len(files) != 0:
            print('-' * 30)
            print(f'{os.path.basename(dirpath)} Data starts')
            # my_dict = dict(zip(timestamp, uptime))
            # print(my_dict)

            # Calculate the difference in timestamp and in uptime, and then compare
            timestamp_diff = timestamp[-1] - timestamp[0]
            uptime_diff = round(uptime[-1] - uptime[0])

            first_timestamp_diff = timestamp[-1] - timestamp[49]
            first_uptime_diff = round(uptime[-1] - uptime[49])

            total_timestamp_diff += timestamp_diff
            total_uptime_diff += uptime_diff

            with open(f'{os.path.basename(dirpath)}.csv', 'w', newline='') as f:
                thewriter = csv.writer(f)
                thewriter.writerow(['Device ID', 'Timestamp Differece',
                                    'Uptime Difference', 'First 100 Timestamp Differece', 'First 100 Uptime Difference'])
                thewriter.writerow([f'{os.path.basename(dirpath)}', timestamp_diff,
                                    uptime_diff, first_timestamp_diff, first_uptime_diff])

            print(f'{file_count} files counted')
            print(f'Timestamp delta is {timestamp_diff} seconds')
            print(f'Uptime delta is {uptime_diff} seconds')

            print(
                f'Timestamp delta (first 100 ignored)is {first_timestamp_diff} seconds')
            print(
                f'Uptime delta (first 100 ignored) is {first_uptime_diff} seconds')

            print(f'{os.path.basename(dirpath)} Data end')
            print('-' * 30)
            print('\n' * 3)

    print(f'Total timestamp difference {total_timestamp_diff}')
    print(f'Total uptime difference {total_uptime_diff}')
    pecentage = ((total_uptime_diff - total_timestamp_diff) /
                 total_uptime_diff) * 100
    print(f'Pecentage loss {pecentage}%')
