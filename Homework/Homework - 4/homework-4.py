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


def write_csv_file(filename: str, field_names: tuple, data: dict):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)

            # Write headers
            csv_writer.writeheader()

            # Write each entry in the data
            for key in data.keys():
                csv_writer.writerow(data[key])
    except Exception as ex:
        print(f"Something went wrong while trying to write to {filename}", str(ex))
        raise


def get_remaining(ad_list: list, edr_list: list):
    # Collect the hostnames list of edr
    hostnames_edr = [edr["Hostname"] for edr in edr_list]

    # Collect the data on remaining hostname's
    # Only count a hostname once.
    hostnames_ad = {}
    edr_enrolled_set = set()
    for ad in ad_list:
        ad_hostname = ad["Hostname"]

        # Check whether the hostname is already added to the dictionary or not
        if ad_hostname not in hostnames_ad:
            # Check whether the current hostname is present in hostname_edr list
            # If present, add it to the set of edr_enrolled_set to remove duplicates
            # Else add the object to the dictionary with key as ad_hostname
            if ad_hostname in hostnames_edr:
                edr_enrolled_set.add(ad_hostname)
            else:
                hostnames_ad[ad_hostname] = ad

    # Return the hostnames_ad dictionary which contains the remaining
    # hostnames that are yet to enroll, already enrolled hostnames count
    return hostnames_ad, len(edr_enrolled_set)


# Filenames
edr_csv_file = "edr.csv"
ad_csv_file = "ad.csv"
remaining_csv_file = "remaining.csv"

# Read the files
edr_csv_list = read_csv_file(edr_csv_file)
ad_csv_list = read_csv_file(ad_csv_file)

# Get the remaining data
remaining_data, edr_enrolled = get_remaining(ad_csv_list, edr_csv_list)

# Header fields
fields = ("Hostname", "Operating System", "Build")

# Write the data to a file
write_csv_file(remaining_csv_file, fields, remaining_data)

# Print the output for verification
print("Output of remaining systems to install EDR on written to remaining.csv\n")
print(f"Systems enrolled in EDR: {edr_enrolled}")
print(f"Systems needing to be enrolled in EDR: {len(remaining_data)}")
