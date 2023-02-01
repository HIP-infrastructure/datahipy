# Copyright (C) 2022-2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source XXX license.

"""Define constants used by packages of `bids_tools.bids`."""

BIDS_VERSION = "v1.7.0"

BIDS_ENTITY_MAP = {
    "subject": "sub",
    "session": "ses",
    "task": "task",
    "run": "run",
    "acquisition": "acq",
    "reconstruction": "rec",
    "ceagent": "ce",
    "direction": "dir",
    "space": "space",
    "proc": "proc",
    "modality": "mod",
    "recording": "recording",
    "staining": "stain",
    "tracer": "trc",
    "sample": "sample",
    "echo": "echo",
    "flip": "flip",
    "inv": "inv",
    "mt": "mt",
    "part": "part",
    "chunk": "chunk",
    "resolution": "res",
}

BIDSJSONFILE_DATATYPE_KEY_MAP = {
    "anat": "AnatJSON",
    "func": "FuncJSON",
    "dwi": "DWIJSON",
    "eeg": "EEGJSON",
    "meg": "MEGJSON",
    "ieeg": "IeegJSON",
}

BIDSTSVFILE_DATATYPE_KEY_MAP = {
    "eeg": "EEGChannelsTSV",
    "meg": "MEGChannelsTSV",
    "ieeg": "IeegChannelsTSV",
}

VALID_EXTENSIONS = [
    ".nii",
    ".nii.gz",
    ".edf",
    ".eeg",
    ".set",
    ".mgz",
]
