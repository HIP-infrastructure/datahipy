# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Command line interface for bids_tools."""

import argparse
from bids_tools import __version__, __release_date__
from bids_tools.bids.utils import get_all_datasets_content
from bids_tools.handlers.dataset import DatasetHandler
from bids_tools.handlers.participants import ParticipantHandler

VALID_COMMANDS = [
    "dataset.create",
    "dataset.get",
    "datasets.get",
    "sub.get",
    "sub.import",
    "sub.edit.clinical",
    "sub.delete",
    "sub.delete.file",
]


def get_parser():
    """Get parser object for command line interface."""
    parser = argparse.ArgumentParser(description="BIDS dataset handler.")
    parser.add_argument("--command", choices=VALID_COMMANDS, help="Method to be run.")
    parser.add_argument("--input_data", help="Input JSON data")
    parser.add_argument("--output_file", help="File location after processing")
    parser.add_argument("--dataset_path", help="Path to the dataset", default="/output")
    parser.add_argument(
        "--input_path",
        help="Path to the input data (e.g. input_data.json)",
        default="/input",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="bids_tools version {} \n(release date: {})".format(
            __version__, __release_date__
        ),
    )
    return parser


def main():
    parser = get_parser()

    cmd_args = parser.parse_args()
    command = cmd_args.command
    input_data = cmd_args.input_data
    output_file = cmd_args.output_file
    dataset_path = cmd_args.dataset_path
    input_path = cmd_args.input_path

    dhdl = DatasetHandler(dataset_path=dataset_path)
    phdl = ParticipantHandler(dataset_path=dataset_path, input_path=input_path)

    if command == "dataset.create":
        return dhdl.dataset_create(input_data=input_data)
    if command == "dataset.get":
        dhdl.dataset_get_content(input_data=input_data, output_file=output_file)
    if command == "datasets.get":
        return get_all_datasets_content(
            input_data=input_data,
            output_file=output_file,
        )
    if command == "sub.import":
        return phdl.sub_import(input_data=input_data)
    if command == "sub.edit.clinical":
        return phdl.sub_edit_clinical(input_data=input_data)
    if command == "sub.get":
        return phdl.sub_get(input_data=input_data, output_file=output_file)
    if command == "sub.delete":
        return phdl.sub_delete(input_data=input_data)
    if command == "sub.delete.file":
        return phdl.sub_delete_file(input_data=input_data)


if __name__ == "__main__":
    main()
