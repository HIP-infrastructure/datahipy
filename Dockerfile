FROM ubuntu:20.04

WORKDIR /apps/

###############################################################################
# Install anywave
###############################################################################
ARG ANYWAVE_VERSION=2.1.3

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \ 
    curl ca-certificates libqt5charts5 libqt5concurrent5 libqt5multimediawidgets5 \
    libqt5printsupport5 libqt5qml5 libmatio9 libvtk7.1p-qt \
    libqwt-qt5-6 libqt5xml5 libqcustomplot2.0 libtbb2 && \ 
    curl -Ok https://meg.univ-amu.fr/AnyWave/anywave-${ANYWAVE_VERSION}_amd64.deb && \
    dpkg -i anywave-${ANYWAVE_VERSION}_amd64.deb && \
    rm anywave-${ANYWAVE_VERSION}_amd64.deb

###############################################################################
# Install dcm2niix
###############################################################################

# Set the version of dcm2niix to install
ARG DCM2NIIX_VERSION=1.0.20211006

# Install dcm2niix and dependencies
RUN apt-get install --no-install-recommends -y unzip && \
    curl -O -L https://github.com/rordenlab/dcm2niix/releases/download/v${DCM2NIIX_VERSION}/dcm2niix_lnx.zip && \
    mkdir -p ./dcm2niix/install && \
    unzip -q -d ./dcm2niix/install dcm2niix_lnx.zip && \
    chmod 755 ./dcm2niix/install/dcm2niix && \
    ln -s /apps/dcm2niix/install/dcm2niix /usr/bin/dcm2niix && \
    rm dcm2niix_lnx.zip

###############################################################################
# Install bids-validator
###############################################################################

# TODO: use this to install a specific version of bids-validator from the original repo
# once the schema option is fixed and schema >= v1.8.0 is supported

# Set the version of bids-validator to install
# ARG BIDSVALIDATOR_VERSION=1.9.9

# Install bids-validator and dependencies
# RUN apt-get update && curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
#     apt-get update && apt-get install --no-install-recommends -y \
#     nodejs && \
#     npm install -g npm && \
#     npm install -g bids-validator@${BIDSVALIDATOR_VERSION} && \
#     apt-get autoremove -y --purge && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# Use our oen fork of bids-validator with the schema option fixed
# Set the version of bids-validator to install
ARG BIDSVALIDATOR_BRANCH=dev-hip

# Clone and install the latest version of a specific branch of bids-manager
ADD https://api.github.com/repos/HIP-infrastructure/bids-validator/git/refs/heads/$BIDSVALIDATOR_BRANCH version.json
RUN apt-get update && curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get update && apt-get install --no-install-recommends -y \
    git nodejs && \
    mkdir -p bids-validator/install && \
    cd bids-validator/install && \
    git clone https://github.com/HIP-infrastructure/bids-validator.git bids-validator && \
    cd bids-validator && \
    git checkout $BIDSVALIDATOR_BRANCH && \
    npm install -g npm && \
    npm install && \
    npm -w bids-validator run build && \
    npm -w bids-validator pack && \
    npm install -g bids-validator-*.tgz && \
    apt-get remove -y --purge git && \
    apt-get autoremove -y --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf bidsmanager/install/bidsificator

# ###############################################################################
# # Install System and BIDS_Manager/BIDS_Pipelines Python dependencies
# ###############################################################################

# Install system and Python dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    git python3-pip python3-tk && \
    apt-get autoremove -y --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install BIDS_Manager/BIDS_Pipelines Python dependencies
RUN pip3 install \
    PyQt5==5.15.4 \
    nibabel \
    xlrd \
    PySimpleGUI \
    pydicom \
    paramiko \
    tkcalendar \
    bids_validator && \
    apt-get autoremove -y --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

###############################################################################
# Install most recent standalone version of git-annex for Datalad
###############################################################################

RUN apt-get update && apt-get install -y wget netbase openssh-client && \
    wget https://github.com/datalad/git-annex/releases/download/10.20230626/git-annex-standalone_10.20230626-1.ndall%2B1_amd64.deb && \
    dpkg -i git-annex-standalone_10.20230626-1.ndall+1_amd64.deb && \
    rm git-annex-standalone_10.20230626-1.ndall+1_amd64.deb && \
    apt-get autoremove -y --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

###############################################################################
# Install datahipy
###############################################################################

# Set the working directory to /app/datahipy
WORKDIR /apps/datahipy

# Copy necessary contents of this repository.
COPY ./.coveragerc ./.coveragerc
COPY setup.py ./setup.py
COPY setup.cfg ./setup.cfg
COPY README.md ./README.md
COPY datahipy ./datahipy
# COPY LICENSE ./LICENSE

# Install datahipy with static version taken from the argument
ARG VERSION=unknown
RUN echo "${VERSION}" > /apps/datahipy/datahipy/VERSION \
    && pip install -e ".[test]"

###############################################################################
# Create initial folders for testing / code coverage with correct permissions
###############################################################################

# Create directories for reporting tests and code coverage
RUN mkdir -p "/test/report" && chmod -R 775 "/test"

###############################################################################
# Set environment variables
###############################################################################

# Tell QT to use the offscreen platform
ENV QT_QPA_PLATFORM offscreen

# Set the environment variable for .coverage file
ENV COVERAGE_FILE="/test/report/.coverage"

###############################################################################
# Configure the entrypoint scripts
###############################################################################

# Copy the main entrypoint script 
COPY scripts/docker/entrypoint.sh /entrypoint.sh

# Copy the pytest entrypoint script and make it executable
COPY scripts/docker/entrypoint_pytest.sh /entrypoint_pytest.sh
RUN chmod +x /entrypoint_pytest.sh

# Set the entrypoint to the main entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

###############################################################################
# Container Image Metadata (label schema: http://label-schema.org/rc1/)
###############################################################################

ARG BUILD_DATE=today
ARG VCS_REF=unknown

LABEL org.label-schema.build-date=${BUILD_DATE} \
    org.label-schema.name="BIDS tools" \
    org.label-schema.description="Tools to handle BIDS datasets in the HIP platform" \
    org.label-schema.url="https://hip-infrastructure.github.io/" \
    org.label-schema.vcs-ref=${VCS_REF} \
    org.label-schema.vcs-url="https://github.com/HIP-infrastructure/bids-tools" \
    org.label-schema.version=${VERSION} \
    org.label-schema.maintainer="The HIP team" \
    org.label-schema.vendor="The HIP team" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.docker.cmd="docker run --rm \
    -v /path/to/dataset:/output \
    -v /path/to/input:/input \
    datahipy \
    USERNAME USERID \
    [--command {dataset.create,dataset.get,datasets.get,sub.get,sub.import,sub.edit.clinical,sub.delete,sub.delete.file}] \
    [--input_data /input/input_data.json] [--output_file /input/output_data.json] \
    [--dataset_path /output] [--input_path /input]" \
    org.label-schema.docker.cmd.test="docker run --rm \
    --entrypoint /entrypoint_pytest.sh \
    -v /path/to/datahipy/test:/test \
    -v /path/to/datahipy/datahipy:/apps/datahipy/datahipy \
    datahipy \
    USERNAME USERID \
    /test"
