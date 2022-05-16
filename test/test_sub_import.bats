export DATABASE_NAME=BIDS_DB

setup() {
    load 'test_helper/_common_setup'
    _common_setup

    # copy existing database and subject to import
    cp -r ${PROJET_TEST_FOLDER}/test_data/* $PROJET_TMP_FOLDER
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-converter
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/sub_import.json 
{
    "database": "${DATABASE_NAME}",
    "subjects": [
        {
            "sub": "carole",
            "age": "25",
            "sex": "M",
            "hospital": "CHUV"
        }
    ],
    "files": [
        {
            "modality": "ieeg",
            "subject": "carole",
            "path": "sub-carole/SZ1.TRC",
            "entities": {
                "sub": "carole",
                "ses": "postimp",
                "task": "stimulation",
                "acq": "1024hz"
            }
        },
        {
            "modality": "ieeg",
            "subject": "carole",
            "path": "sub-carole/SZ2.TRC",
            "entities": {
                "sub": "carole",
                "ses": "postimp",
                "task": "stimulation",
                "acq": "1024hz"
            }
        },
        {
            "modality": "T1w",
            "subject": "carole",
            "path": "sub-carole/3DT1post_deface.nii",
            "entities": {
                "sub": "carole",
                "ses": "postimp",
                "acq": "lowres",
                "ce": "gadolinium"
            }
        },
        {
            "modality": "T1w",
            "subject": "carole",
            "path": "sub-carole/3DT1post_deface_2.nii",
            "entities": {
                "sub": "carole",
                "ses": "postimp",
                "acq": "lowres",
                "ce": "gadolinium"
            }
        },
        {
            "modality": "T1w",
            "subject": "carole",
            "path": "sub-carole/3DT1pre_deface.nii",
            "entities": {
                "sub": "carole",
                "ses": "preimp",
                "acq": "lowres"
            }
        }
    ]
}
EOT
}

@test 'assert_dir_not_exists()' {
    assert_dir_exists  ${PROJET_TMP_FOLDER}/${DATABASE_NAME}
    assert_dir_not_exists  ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/sub-carole
}

@test "can run docker sub.import" {
    run docker run -it --rm \
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}/${DATABASE_NAME}:/output \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-converter  \
        ${USER} $(id -u $USER) \
        --command=sub.import \
        --input_data=/input/sub_import.json
}

@test 'assert_db_files_exists()' {
    assert_dir_exists  ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/sub-carole
    assert_file_exists  ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/participants.tsv
    assert_file_exists  ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/dataset_description.json
    assert_dir_exists  ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/code
    assert_file_exists  ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/code/requirements.json
}

@test 'assert_file_contains()' {
    assert_file_contains  ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/participants.tsv 'sub-carole'
}

@test 'assert_file_owner()' {
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATABASE_NAME} 
    # assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/sub-carole
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/participants.tsv
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/code
    assert_file_owner ${USER} ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/code/requirements.json
}

@test 'delete files with user ${USER}' {
    rm  ${PROJET_TMP_FOLDER}/sub_import.json
}