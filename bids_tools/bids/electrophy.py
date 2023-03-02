# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Utility functions to retrieve information about electrophysiology files (EEG/MEG/iEEG) from a BIDS dataset."""

import pandas as pd


def get_channels_info(channels_tsv_file):
    """Extract the content from a BIDS _channels.tsv file in JSON format.

    Parameters
    ----------
    channels_tsv_file : str
        Path to the BIDS _channels.tsv file.

    Returns
    -------
    channels_info : str
        JSON representation of the content of the BIDS _channels.tsv file.
    """
    channels_df = pd.read_csv(channels_tsv_file, sep="\t")
    return channels_df.to_json(orient="records")


def get_ieeg_info(layout):
    """Return iEEG data information to be integrated in the dictionary summarizing a BIDS dataset for indexing.

    Parameters
    ----------
    dataset_desc : dict
        Input dictionary with the dataset content to be indexed.

    layout : BIDSLayout
        BIDSLayout object for the dataset.

    Returns
    -------
    ieeg_info : dict
        Dictionary storing iEEG data information to be integrated in the dataset content to be indexed.
    """
    ieeg_info = {}
    ieeg_info_tmp = {
        "ECOGChannelCount": 0,
        "SEEGChannelCount": 0,
        "EEGChannelCount": 0,
        "EOGChannelCount": 0,
        "ECGChannelCount": 0,
        "EMGChannelCount": 0,
        "MiscChannelCount": 0,
        "TriggerChannelCount": 0,
        "SamplingFrequency": 0,
        "RecordingDuration": 0,
    }
    for f in layout.get(suffix="ieeg"):
        f_entities_keys = f.entities.keys()
        for info_key in ieeg_info_tmp:
            if info_key in f_entities_keys:
                # Keep the maximal value in case it is heterogeneous
                if f.entities[info_key] > ieeg_info_tmp[info_key]:
                    ieeg_info_tmp[info_key] = f.entities[info_key]
    for key, val in ieeg_info_tmp.items():
        if val > 0:
            ieeg_info[key] = val
    return ieeg_info
