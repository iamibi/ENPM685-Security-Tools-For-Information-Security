#!/usr/bin/env python3

# Homework - 4

# Author       : Syed Mohammad Ibrahim
# Created At   : 03/12/2022
# UID Number   : 118428369
# Email        : iamibi@umd.edu
# Course       : ENPM685
# Section      : 0101

# Imports
import csv


def read_csv_file(filename: str):
    try:
        with open(filename, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            return list(csv_reader)
    except Exception as ex:
        print(f"Something went wrong while trying to read {filename}", str(ex))
        raise


def write_csv_file(filename: str, field_names: tuple, data: list):
    try:
        with open(filename, mode="w") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)

            # Write headers
            csv_writer.writeheader()

            # Write each entry in the data
            for row in data:
                csv_writer.writerow(row)

    except Exception as ex:
        print(f"Something went wrong while trying to write to {filename}", str(ex))
        raise


def get_remaining(ad_list: list, edr_list: list):
    # Collect the hostnames list to and edr
    hostnames_edr = [edr["Hostname"] for edr in edr_list]

    # Calculate the data on the systems remaining
    edr_enrolled = 0
    remaining = 0
    list_remaining = []
    for ad in ad_list:
        if ad["Hostname"] in hostnames_edr:
            edr_enrolled += 1
        else:
            remaining += 1
            list_remaining.append(ad)

    return (list_remaining, edr_enrolled, remaining)


# Filenames
edr_csv_file = "edr.csv"
ad_csv_file = "ad.csv"
remaining_csv_file = "remaining.csv"

# Read the files
edr_csv_list = read_csv_file(edr_csv_file)
ad_csv_list = read_csv_file(ad_csv_file)

# Get the remaining data
remaining_data, edr_enrolled, remaining_count = get_remaining(ad_csv_list, edr_csv_list)

# Header fields
fields = ("Hostname", "Operating System", "Build")

# Write the data to a file
write_csv_file(remaining_csv_file, fields, remaining_data)

# Print the output for verification
print("Output of remaining systems to install EDR on written to remaining.csv\n")
print(f"Systems enrolled in EDR: {edr_enrolled}")
print(f"Systems needing to be enrolled in EDR: {remaining_count}")
