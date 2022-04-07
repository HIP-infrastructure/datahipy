#!/usr/bin/python3
# -*-coding:Utf-8 -*

import argparse
from database_handler import DatabaseHandler
from participants_handler import ParticipantHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BIDS database handler.')
    parser.add_argument('--command', help="Method to be run, db.create, db.get, sub.get, sub.create, sub.remove")
    parser.add_argument('--input_data', help="Input JSON data")
    parser.add_argument('--database_path', help="BIDS database input/output folder")
    parser.add_argument('--output_file', help="File location after processing")

    cmd_args = parser.parse_args()
    command = cmd_args.command
    input_data = cmd_args.input_data
    database_path = cmd_args.database_path
    output_file = cmd_args.output_file

    dhdl = DatabaseHandler()
    phdl = ParticipantHandler()

    if command == 'db.create':
        dhdl.db_create(input_data=input_data,
                       database_path=database_path)
    if command == 'db.get':
        dhdl.db_get(input_data=input_data,
                    output_file=output_file)
    if command == 'sub.import':
        phdl.sub_import(input_data=input_data,
                        database_path=database_path)
    if command == 'sub.get':
        phdl.sub_get(input_data=input_data,
                     database_path=database_path,
                     output_file=output_file)
    if command == 'sub.delete':
        phdl.sub_delete(input_data=input_data,
                        database_path=database_path)
    if command == 'sub.delete.file':
        phdl.sub_delete_file(input_data=input_data,
                             database_path=database_path)
