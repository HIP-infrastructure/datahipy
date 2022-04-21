export DATABASE_NAME=BIDS_DB

setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "can build docker image" {
    run docker build ${PROJECT_ROOT} -t bids-converter
}

@test "can create input file" {
    cat <<EOT > ${PROJET_TMP_FOLDER}/sub_delete_file.json 
{
    "owner": "${USER}",
    "database": "${DATABASE_NAME}",
    "files": [{
            "subject": "carole",
            "modality": "anat",
            "filename": "sub-carole/ses-postimp/anat/sub-carole_ses-postimp_acq-lowres_ce-gadolinium_run-02_T1w.nii"
        }
    ]
}
EOT
}

@test 'assert_dir_exists()' {
    assert_dir_exists ${PROJET_TMP_FOLDER}/${DATABASE_NAME}
    assert_dir_exists ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/sub-carole
}

@test "can run docker sub.delete.file" {
    run docker run -it --rm \
        -v ${PROJET_TMP_FOLDER}:/input \
        -v ${PROJET_TMP_FOLDER}:/output \
        -v ${PROJECT_ROOT}/scripts:/scripts \
        bids-converter  \
        --command=sub.delete.file \
        --input_data=/input/sub_delete_file.json
}

@test 'assert_file_not_exists()' {
    assert_file_not_exists ${PROJET_TMP_FOLDER}/${DATABASE_NAME}/sub-carole/ses-postimp/anat/sub-carole_ses-postimp_acq-lowres_ce-gadolinium_run-02_T1w.nii
}

@test 'delete files with user ${USER}' {
    rm ${PROJET_TMP_FOLDER}/sub_delete_file.json
}