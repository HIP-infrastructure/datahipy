# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Command line interface for datahipy."""

import argparse
from datahipy import __version__, __release_date__
from datahipy.bids.dataset import get_all_datasets_content
from datahipy.handlers.dataset import DatasetHandler
from datahipy.handlers.participants import ParticipantHandler
from datahipy.handlers.project import create_project, import_subject, import_document
from datahipy.utils.versioning import create_tag, get_tags, checkout_tag

VALID_COMMANDS = [
    "dataset.create",
    "dataset.get",
    "dataset.create_tag",
    "dataset.get_tags",
    "dataset.checkout_tag",
    "datasets.get",
    "sub.get",
    "sub.import",
    "sub.edit.clinical",
    "sub.delete",
    "sub.delete.file",
    "project.create",
    "project.sub.import",
    "project.doc.import",
    "project.create_tag",
    "project.get_tags",
    "project.checkout_tag",
]


def get_parser():
    """Get parser object for command line interface."""
    parser = argparse.ArgumentParser(description="DataHIPy command line interface.")
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
        version="datahipy version {} \n(release date: {})".format(
            __version__, __release_date__
        ),
    )
    return parser


def main():
    """Run the command line interface."""
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
    if command == "dataset.create_tag":
        return create_tag(input_data=input_data)
    if command == "dataset.get_tags":
        return get_tags(input_data=input_data, output_file=output_file)
    if command == "dataset.checkout_tag":
        return checkout_tag(input_data=input_data)
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
    if command == "project.create":
        create_project(input_data=input_data, output_file=output_file)
    if command == "project.sub.import":
        import_subject(input_data=input_data, output_file=output_file)
    if command == "project.doc.import":
        import_document(input_data=input_data)
    if command == "project.create_tag":
        return create_tag(input_data=input_data)
    if command == "project.get_tags":
        return get_tags(input_data=input_data, output_file=output_file)
    if command == "project.checkout_tag":
        return checkout_tag(input_data=input_data)


if __name__ == "__main__":
    main()
