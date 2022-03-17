#!/usr/bin/python3
# -*-coding:Utf-8 -*

import argparse
import database_handler
import participants_handler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BIDS database handler.')
    parser.add_argument(
        '--command', help="Method to be run, db.create, db.get, sub.get, sub.create, sub.remove")
    parser.add_argument('--input_data', help="Input JSON data")
    parser.add_argument('--database_path', help="BIDS database input/output folder")
    parser.add_argument('--output_file', help="File location after processing")

    cmd_args = parser.parse_args()
    command = cmd_args.command
    input_data = cmd_args.input_data
    database_path=cmd_args.database_path
    output_file=cmd_args.output_file

    dhdl = database_handler.DatabaseHandler()
    phdl = participants_handler.ParticipantHandler()


    if command == 'db.create':
        dhdl.create_bids_db(create_bids_db=input_data,
                            database_path=database_path)

    if command == 'db.get':
        dhdl.get_bids_def(get_bids_def=input_data,
                          output_file=output_file)

    if command == 'sub.create':
        phdl.import_data(data_to_import=input_data,
                         database_path=database_path)

    if command == 'sub.get':
        phdl.get_sub_info(get_sub_info=input_data,
                          database_path=database_path,
                          output_file=output_file)

    if command == 'sub.remove':
        phdl.del_sub(sub_to_delete=input_data)
