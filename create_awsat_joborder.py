#!/usr/bin/env python

"""Create JobOrder files for AWSat preprocessors."""

import argparse
import sys
import xml.etree.ElementTree as ET


def read_template(fname):
    """Read the template XML."""
    return ET.parse(fname)


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


def set_l0_files(template, level0_data, level0_nav, level1_dir=None):
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

    if level1_dir:
        output_sections = template.findall(".//Output")
        for o in output_sections:
            file_name = o.find("File_Name")
            if o.find(".//File_Type").text == "RAD_AWS_1B":
                file_name.text = level1_dir

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
    parser.add_argument("-1", "--level1-dir", dest="level1_dir", type=str,
                        help="Level1 data dir.")
    parser.add_argument("-n", "--level0-navigation", dest="level0_nav",
                        type=str, help="Level0 navigation file.")
    parser.add_argument("-r", "--raw-files", dest="raw_files", nargs='+',
                        type=str,
                        help="List of raw data files.")

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
    if args.raw_files:
        set_raw_file_list(template, args.raw_files)
    else:
        set_l0_files(template, args.level0_data, args.level0_nav, args.level1_dir)
    template.write(args.joborder_file)


if __name__ == "__main__":
    main()
