#!/usr/bin/python3
# -*-coding:Utf-8 -*

import argparse
from database_handler import DatabaseHandler
from participants_handler import ParticipantHandler

database_path = '/output'
input_path='/input'

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='BIDS database handler.')
    parser.add_argument('--command', help="Method to be run, db.create, db.get, sub.get, sub.create, sub.remove")
    parser.add_argument('--input_data', help="Input JSON data")
    parser.add_argument('--output_file', help="File location after processing")

    cmd_args = parser.parse_args()
    command = cmd_args.command
    input_data = cmd_args.input_data
    output_file = cmd_args.output_file

    dhdl = DatabaseHandler(database_path=database_path)
    phdl = ParticipantHandler(database_path=database_path, input_path=input_path)

    if command == 'db.create':
        dhdl.db_create(input_data=input_data)
    if command == 'db.get':
        dhdl.db_get(input_data=input_data,
                    output_file=output_file)
    if command == 'sub.import':
        phdl.sub_import(input_data=input_data)
    if command == 'sub.get':
        phdl.sub_get(input_data=input_data,
                     output_file=output_file)
    if command == 'sub.delete':
        phdl.sub_delete(input_data=input_data)
    if command == 'sub.delete.file':
        phdl.sub_delete_file(input_data=input_data)
