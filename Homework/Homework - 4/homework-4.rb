#!/usr/bin/env ruby

# The program was written in ruby 3.1.1 with YJIT compiler
# Read more about ruby 3.1.x https://www.ruby-lang.org/en/news/2021/12/25/ruby-3-1-0-released/

# Imports
require 'csv'

def read_csv_file(filename)
	# Read the CSV file and convert it to an array of hashes
	return CSV.open(filename, headers: :first_row).map(&:to_h)
rescue => error
	puts("Something went wrong while trying to read #{filename}\n#{error.message}")
	raise
end

def write_csv_file(filename, fields, data)
	CSV.open(filename, "wb", headers: true) do |csv|
		csv << fields
		data.each do |hash|
			csv << hash
		end
	end
rescue => error
	puts("Something went wrong while trying to write to #{filename}\n#{error.message}")
	raise
end

def get_remaining(ad_list, edr_list)
	# Collect the hostnames list to and edr
    hostnames_edr = edr_list.map { |edr| edr["Hostname"] }
	
	# Calculate the data on the systems remaining
    edr_enrolled = 0
    remaining = 0
	arr_remaining = []
	
	ad_list.each do |ad|
		if hostnames_edr.include?(ad["Hostname"])
			edr_enrolled += 1
		else
			remaining += 1
			arr_remaining << ad
		end
	end
	
	# Return the values
	[arr_remaining, edr_enrolled, remaining]
end

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
fields = ["Hostname", "Operating System", "Build"].freeze

# Write the data to a file
write_csv_file(remaining_csv_file, fields, remaining_data)

# Print the output for verification
puts("Output of remaining systems to install EDR on written to remaining.csv\n")
puts("Systems enrolled in EDR: #{edr_enrolled}")
puts("Systems needing to be enrolled in EDR: #{remaining_count}")
