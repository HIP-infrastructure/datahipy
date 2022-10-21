#!/usr/bin/python3
# -*-coding:Utf-8 -*

import argparse
from bids_utils import get_all_datasets_content
from dataset_handler import DatasetHandler
from participants_handler import ParticipantHandler

dataset_path = '/output'
input_path = '/input'

VALID_COMMANDS = [
    'dataset.create',
    'dataset.get',
    'datasets.get',
    'sub.get',
    'sub.create',
    'sub.edit.clinical',
    'sub.delete',
    'sub.delete.file'
]


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='BIDS dataset handler.')
    parser.add_argument(
        '--command',
        choices=VALID_COMMANDS,
        help="Method to be run."
    )
    parser.add_argument(
        '--input_data',
        help="Input JSON data"
    )
    parser.add_argument(
        '--output_file',
        help="File location after processing"
    )

    cmd_args = parser.parse_args()
    command = cmd_args.command
    input_data = cmd_args.input_data
    output_file = cmd_args.output_file

    dhdl = DatasetHandler(dataset_path=dataset_path)
    phdl = ParticipantHandler(dataset_path=dataset_path, input_path=input_path)

    if command == 'dataset.create':
        dhdl.dataset_create(input_data=input_data)
    if command == 'dataset.get':
        dhdl.dataset_get_content(
            input_data=input_data,
            output_file=output_file
        )
    if command == 'datasets.get':
        get_all_datasets_content(
            datasets_root_dir=dataset_path,  # /output mapped to parent directory of all datasets
            input_data=input_data,
            output_file=output_file
        )
    if command == 'sub.import':
        phdl.sub_import(input_data=input_data)
    if command == 'sub.edit.clinical':
        phdl.sub_edit_clinical(input_data=input_data)
    if command == 'sub.get':
        phdl.sub_get(
            input_data=input_data,
            output_file=output_file
        )
    if command == 'sub.delete':
        phdl.sub_delete(input_data=input_data)
    if command == 'sub.delete.file':
        phdl.sub_delete_file(input_data=input_data)
