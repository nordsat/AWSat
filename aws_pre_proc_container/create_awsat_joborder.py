#!/usr/bin/env python

"""Create JobOrder files for AWSat preprocessors."""

import argparse
import sys
import xml.etree.ElementTree as ET


GET_STATION_NAME = {"KAN": "Kangerlussuaq",
                    "NRK": "Norrkoping",
                    "OSL": "Oslo",
                    "SOD": "Sodankyla"
                    }

def read_template(fname):
    """Read the template XML."""
    return ET.parse(fname)


def set_station_name(template, station_name):
    """Set the station name in the XML file."""
    root = template.getroot()

    # Change Processing station
    station_elem = root.find('.//Processing_Station')
    if station_elem is not None:
        station_elem.text = station_name


    # Change Processing parameter location
    processing_params = root.findall('.//Processing_Parameter')
    for param in processing_params:
        name_elem = param.find('Name')
        value_elem = param.find('Value')
        if name_elem is not None and name_elem.text == "location":
            value_elem.text = station_name
            break

    return template


def get_raw_file_list(tree):
    """Get the file list element from the XML tree."""
    inputs = tree.findall('.//Input')
    for i in inputs:
        if i.find('.//File_Type').text.startswith('DCS'):
            return i.find('.//List_of_File_Names')
    return None


def set_raw_file_list(template, input_files):
    """Set the file list elements to the file list element."""
    file_list = get_raw_file_list(template)
    attrib = {'count': str(len(input_files))}
    file_list.clear()
    for f in input_files:
        file_name = ET.Element('File_Name')
        file_name.text = f
        file_list.append(file_name)
    file_list.attrib = attrib
    ET.indent(template, space='    ')


def set_l0_files(template, level0_data, level0_nav):
    """Set the the Level0 data and navigation files to the template."""
    input_sections = template.findall(".//Input")
    for i in input_sections:
        file_list = i.find(".//List_of_File_Names")
        file_list.clear()
        file_list.attrib = {'count': '1'}
        file_name = ET.Element('File_Name')
        if i.find(".//File_Type").text == "SRC_AWS_00":
            file_name.text = level0_data
        else:
            file_name.text = level0_nav
        file_list.append(file_name)
    ET.indent(template, space='    ')


def parse_args():
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser(
        description="Create JobOrder files for AWSat.",
        epilog="The dates need to match pattern 'Y%m%d_%H%M%S%f', e.g. 20230818_143618000000",
    )
    parser.add_argument("-t", "--template-file", required=True,
                        dest="template_file", type=str,
                        help="Template for the JobOrder XML.")
    parser.add_argument("-j", "--joborder-file", required=True,
                        dest="joborder_file", type=str,
                        help="Name of the output JobOrder file.")
    parser.add_argument("-0", "--level0-data", dest="level0_data", type=str,
                        help="Level0 data file.")
    parser.add_argument("-n", "--level0-navigation", dest="level0_nav",
                        type=str, help="Level0 navigation file.")
    parser.add_argument("-r", "--raw-files", dest="raw_files", nargs='+',
                        type=str,
                        help="List of raw data files.")
    parser.add_argument("-s", "--station", required=False,
                        dest="station_short_name", type=str,
                        help="ID of the station (e.g. KAN,kan,SOD,sod,NRK,nrk...).")

    args = parser.parse_args()

    raw_missing = args.raw_files is None
    l0_missing = args.level0_data is None or args.level0_nav is None
    if raw_missing and l0_missing:
        print("Need to have either Level0 data and navigation files, or list of raw files.")
        sys.exit(1)

    return args


def main():
    """Create a job order file."""
    args = parse_args()

    template = read_template(args.template_file)
    station_name = None
    station_short_name = args.station_short_name
    if station_short_name:
        station_name = GET_STATION_NAME.get(station_short_name.upper())

    if station_name:
        set_station_name(template, station_name)

    if args.raw_files:
        set_raw_file_list(template, args.raw_files)
    else:
        set_l0_files(template, args.level0_data, args.level0_nav)
    template.write(args.joborder_file, encoding='utf-8', xml_declaration=True)


if __name__ == "__main__":
    main()
