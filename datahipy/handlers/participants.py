# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Manage BIDS participants using BIDS Manager."""

import os
import json
import shutil
from datetime import datetime
from sre_constants import SUCCESS

import datalad.api

# BIDS Manager Python package has to be accessible.
try:
    from bids_manager.ins_bids_class import (
        BidsDataset,
        Data2Import,
        Subject,
        Anat,
        Ieeg,
        CT,
    )
except ImportError:  # pragma: no cover
    print("WARNING: BIDS Manager Python package is not accessible.")

from datahipy.handlers.dataset import DatasetHandler
from datahipy.bids.participant import get_subject_bidsfile_info
from datahipy.bids.bids_manager import post_import_bids_refinement
from datahipy.bids.version import manage_bids_dataset_with_datalad


class ParticipantHandler:
    """Class to represent the handler of a dataset's participant with utility functions."""

    def __init__(self, dataset_path=None, input_path=None):
        self.dataset_path = os.path.abspath(dataset_path)
        self.input_path = input_path

    def sub_import(self, input_data=None):
        """Import subject(s) data into a BIDS dataset."""
        # Check if the dataset is managed by Datalad based on
        # the presence of the .datalad directory. If not, create it.
        # Otherwise, this would fail when trying to save the
        # dataset state with Datalad.
        if not os.path.isdir(os.path.join(self.dataset_path, ".datalad")):
           manage_bids_dataset_with_datalad(self.dataset_path)
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS dataset in BIDS Manager and check converters
        ds_obj = BidsDataset(self.dataset_path)
        DatasetHandler.check_converters(ds_obj=ds_obj)
        # Add clinical keys to the requirements.json
        clin_keys = list()
        for subject in input_data["subjects"]:
            for key in subject:
                if key != "sub" and key not in clin_keys:
                    clin_keys.append(key)
        DatasetHandler.add_keys_requirements(ds_obj=ds_obj, clin_keys=clin_keys)
        ds_obj.parse_bids()
        # Create the Data2Import object needed by BIDS_Manager to import the data
        data2import = self.create_data2import(ds_obj=ds_obj, input_data=input_data)
        # Saving the data2import now it is populated. Note: subjects without data to import are ignored
        data2import.save_as_json()
        # Importation of the data into the BIDS dataset using BIDS Manager
        ds_obj.make_upload_issues(data2import, force_verif=True)
        # Create a /sourcedata + source_data_trace.tsv
        ds_obj.import_data(
            data2import=data2import, keep_sourcedata=True, keep_file_trace=True
        )
        # Refresh
        ds_obj.parse_bids()
        # Post-importation BIDS Manager output refinements
        # to make BIDS Validator happy
        post_import_bids_refinement(ds_obj.dirname)
        # Save dataset state with Datalad
        save_params = {
            "dataset": ds_obj.dirname,
            "message": f'Add files for subject(s): {input_data["subjects"]}',
            "recursive": True,
        }
        datalad.api.save(**save_params)
        print(SUCCESS)

    def sub_delete(self, input_data=None):
        """Delete a subject from an already existing BIDS dataset."""
        # Check if the dataset is managed by Datalad based on
        # the presence of the .datalad directory. If not, create it.
        # Otherwise, this would fail when trying to save the
        # dataset state with Datalad.
        if not os.path.isdir(os.path.join(self.dataset_path, ".datalad")):
           manage_bids_dataset_with_datalad(self.dataset_path)
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS dataset in BIDS Manager
        ds_obj = BidsDataset(self.dataset_path)
        # Find the subject dict
        sub_dict = self.find_subject_dict(ds_obj=ds_obj, subject=input_data["subject"])
        # Delete the subject from the BIDS dataset
        # Will remove from /raw, /source, participants.tsv, source_data_trace.tsv
        # but not from derivatives
        ds_obj.remove(sub_dict, with_issues=True, in_deriv=None)
        # Refresh
        ds_obj.parse_bids()
        # Save dataset state with Datalad
        save_params = {
            "dataset": ds_obj.dirname,
            "message": f'Remove files for subject {input_data["subject"]}',
            "recursive": True,
        }
        datalad.api.save(**save_params)
        print(SUCCESS)

    def sub_delete_file(self, input_data=None):
        """Delete data files from /raw and /source."""
        # Check if the dataset is managed by Datalad based on
        # the presence of the .datalad directory. If not, create it.
        # Otherwise, this would fail when trying to save the
        # dataset state with Datalad.
        if not os.path.isdir(os.path.join(self.dataset_path, ".datalad")):
           manage_bids_dataset_with_datalad(self.dataset_path)
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS dataset in BIDS Manager
        ds_obj = BidsDataset(self.dataset_path)
        subjects = list()
        for file in input_data["files"]:
            sub_dict = self.find_subject_dict(ds_obj=ds_obj, subject=file["subject"])
            for file_dict in sub_dict[file["modality"]]:
                if file["fullpath"] == file_dict["fileLoc"]:
                    # Delete the file from the BIDS dataset:
                    # remove from /raw, /source, participants.tsv, source_data_trace.tsv
                    # but not from derivatives
                    ds_obj.remove(file_dict, with_issues=True, in_deriv=None)
                    print("{} was deleted.".format(file["fullpath"]))
                    if file["subject"] not in subjects:
                        subjects.append(file["subject"])
        # Save dataset state with Datalad
        save_params = {
            "dataset": ds_obj.dirname,
            "message": f"Remove files for subjects {subjects}",
            "recursive": True,
        }
        datalad.api.save(**save_params)
        print(SUCCESS)

    def sub_get(self, input_data=None, output_file=None):
        """Get info of a subject."""
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        sub_info = get_subject_bidsfile_info(
            bids_dir=self.dataset_path, subject=input_data["sub"]
        )
        if output_file:
            self.dump_output_file(output_data=sub_info, output_file=output_file)
        print(SUCCESS)

    def sub_edit_clinical(self, input_data=None):
        """Update subject clinical info in BIDS dataset."""
        # Check if the dataset is managed by Datalad based on
        # the presence of the .datalad directory. If not, create it.
        # Otherwise, this would fail when trying to save the
        # dataset state with Datalad.
        if not os.path.isdir(os.path.join(self.dataset_path, ".datalad")):
           manage_bids_dataset_with_datalad(self.dataset_path)
        # Load the input_data json in a dict
        input_data = self.load_input_data(input_data)
        # Load the targeted BIDS dataset in BIDS Manager
        ds_obj = BidsDataset(self.dataset_path)
        # Edit subject clinical info
        sub_exists, sub_info, sub_idx = ds_obj["ParticipantsTSV"].is_subject_present(
            input_data["subject"]
        )
        if sub_exists:
            DatasetHandler.add_keys_requirements(
                ds_obj=ds_obj, clin_keys=input_data["clinical"].keys()
            )
            for clin_key, clin_value in input_data["clinical"].items():
                if clin_value:
                    sub_info[clin_key] = clin_value
                else:  # pragma: no cover
                    sub_info[clin_key] = "n/a"
            del sub_info["sub"]
            ds_obj.parse_bids()  # To update the participants.tsv with the new columns
            ds_obj["ParticipantsTSV"].update_subject(input_data["subject"], sub_info)
            ds_obj["ParticipantsTSV"].write_file()
            # Save dataset state with Datalad
            save_msg = (
                f'Update participants.tsv file for subject {input_data["subject"]}'
            )
            datalad.api.save(dataset=ds_obj.dirname, message=save_msg, recursive=True)
        print(SUCCESS)

    @staticmethod
    def load_input_data(input_data):
        """Load the input_data JSON file."""
        with open(input_data, "r") as f:
            return json.load(f)

    @staticmethod
    def dump_output_file(output_data=None, output_file=None):
        """Dump output_data dict in a JSON file."""
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=4)

    @staticmethod
    def find_subject_dict(ds_obj=None, subject=None):
        """Find the subject dict in the parsed BIDS dataset object."""
        matched_sub = [
            sub_idx
            for sub_idx, sub_dict in enumerate(ds_obj["Subject"])
            if sub_dict["sub"] == subject
        ]
        if not matched_sub:
            raise IndexError("Could not find the subject in the BIDS dataset.")  # pragma: no cover
        elif len(matched_sub) > 1:
            raise IndexError(
                "Several subjects with the same ID found in the BIDS dataset."  # pragma: no cover
            )
        sub_dict = ds_obj["Subject"][matched_sub[0]]
        return sub_dict

    @staticmethod
    def create_data2import(ds_obj=None, input_data=None):
        """Create a data2import object.

        This object will be used to import data in the BIDS dataset.

        Parameters
        ----------
        ds_obj : BIDS Manager BidsDataset object
            The BIDS Manager object representing a BIDS dataset.

        input_data : dict
            The input_data dictionary containing the data to import in the BIDS dataset.

        Returns
        -------
        data2import : BIDS Manager Data2Import object
            The BIDS Manager object representing the data to import in the BIDS dataset.
        """
        # Init importation directory
        import_path = os.path.join("/tmp", "BIDS_import")
        if os.path.isdir(import_path):
            shutil.rmtree(import_path)
        if not os.path.isdir(import_path):
            os.makedirs(import_path)
        # Init a BIDS Manager data2import dict
        requirements_path = os.path.join(ds_obj.dirname, "code", "requirements.json")
        data2import = Data2Import(
            data2import_dir=import_path, requirements_fileloc=requirements_path
        )
        # Populate the data2import with the data extracted from the dataset_description.json of the BIDS dataset.
        data2import["DatasetDescJSON"] = ds_obj["DatasetDescJSON"]
        # Populate the data2import with the subjects found in the data_to_import dict
        # Need to track subject indexes to populate their respective modality dict later
        sub_idx = dict()
        for idx, subject in enumerate(input_data["subjects"]):
            # Init a BIDS Manager subject dict used for clinical info
            new_sub = Subject()
            # Populate the subject dict with the content of the data_to_import dict
            for bids_key, bids_value in subject.items():
                new_sub[bids_key] = bids_value
            data2import["Subject"].append(new_sub)
            sub_idx[subject["sub"]] = idx
        # Variable to track the RUN number of files to import
        runs = dict()
        # Populate the data2import with the files found in the data_to_import dict
        for file in input_data["files"]:
            # Copy the targeted file in a unique importation dir
            file_name = os.path.basename(file["path"])
            file_path = file["path"]
            token_dir = str(datetime.timestamp(datetime.now())).replace(".", "")
            output_file_path = os.path.join(
                os.path.join(import_path, "temp_bids"), token_dir, file_name
            )
            os.makedirs(os.path.dirname(output_file_path))
            shutil.copyfile(file_path, output_file_path)
            # Determine the BIDS data type to use and init a BIDS Manager modality dict
            bids_dtype = None
            bids_dtype_dict = dict()
            if file["modality"] in ["T1w", "T2w", "FLAIR"]:
                bids_dtype = "Anat"
                bids_dtype_dict = Anat()
            elif file["modality"] in ["ieeg"]:
                bids_dtype = "Ieeg"
                bids_dtype_dict = Ieeg()
            elif file["modality"] in ["ct"]:
                bids_dtype = "CT"
                bids_dtype_dict = CT()
            else:
                pass  # Add other BIDS data types here
            # Populate the modality dict with the BIDS entities found in the input_data dict
            for bids_key, bids_value in file["entities"].items():
                bids_dtype_dict[bids_key] = bids_value
            bids_dtype_dict["modality"] = file["modality"]
            bids_dtype_dict["fileLoc"] = os.path.join("temp_bids", token_dir, file_name)
            # Determine RUN
            bids_values = tuple(file["entities"].values())
            if bids_values not in runs:
                runs[bids_values] = DatasetHandler.get_run(
                    os.path.join(ds_obj.dirname, "sub-" + file["subject"]),
                    file["entities"],
                    file["modality"],
                )
            runs[bids_values] += 1
            bids_dtype_dict["run"] = runs[bids_values]
            data2import["Subject"][sub_idx[file["entities"]["sub"]]][bids_dtype].append(
                bids_dtype_dict
            )
        return data2import
