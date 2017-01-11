# This script parses a CSV file containing latitude and longitude coordinates in
# degrees and converts them to WSG-84 decimal coordinates. The transformed coordinates are then
# writen in an output file, in WKT format.
# The paths for the input and output files must be provided as command line arguments

import csv
import os
import sys


def convert_decimal(coordinate):
    # generate the decimal multiplier (if coordinate is S or V, then the
    # decimal representation is negative
    multiplier = 1
    if coordinate.endswith('S') or coordinate.endswith('V'):
        multiplier = -1

    # split coordinate in 3 components and cast them to numbers
    components = coordinate[:-1].split('.')
    degrees = int(components[0])
    minutes = int(components[1])
    seconds = int(components[2])

    # compute decimal coordinate with max 5 decimals
    decimal_coordinate = float("{0:.5f}".format(multiplier * degrees + (minutes / 60) + (seconds / 3600)))

    return decimal_coordinate


def delete_output_file_if_exists(path):
    try:
        os.remove(path)
    except OSError:
        pass


def main():
    #     # open file resources for input
    input_file_path = str(sys.argv[1])
    csv_file_reader = csv.reader(open(input_file_path, "r"))

    # read input one line (row) at a time and store result in an array of tuples
    converted_coordinates = []
    converted_coordinates_index = 1
    for row in csv_file_reader:
        decimal_lat = convert_decimal(row[0])
        decimal_lon = convert_decimal(row[1])
        converted_coordinate = (decimal_lon, decimal_lat)
        converted_coordinates.insert(converted_coordinates_index, converted_coordinate)
        converted_coordinates_index += 1

    # write data to file
    output_file_path = str(sys.argv[2])
    delete_output_file_if_exists(output_file_path)
    output_file = open(output_file_path, "a+")

    output_file.write("POLYGON((")
    for i, val in enumerate(converted_coordinates):
        line_to_append = str(val[0]) + " " + str(val[1])
        # if not last line, append a ',' character
        if i < len(converted_coordinates)-1:
            line_to_append += ","
        output_file.write(line_to_append)
    output_file.write("))")
    output_file.close()

    print("Finished.")


# call main method and execute program
main()
