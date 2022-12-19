FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG ANYWAVE_VERSION=2.1.3
ARG DCM2NIIX_VERSION=1.0.20211006
ARG BIDSMANAGER_VERSION=latest

WORKDIR /apps/
###############################################################################
# Install anywave
###############################################################################
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
RUN apt-get install --no-install-recommends -y unzip && \
    curl -O -L https://github.com/rordenlab/dcm2niix/releases/download/v${DCM2NIIX_VERSION}/dcm2niix_lnx.zip && \
    mkdir -p ./dcm2niix/install && \
    unzip -q -d ./dcm2niix/install dcm2niix_lnx.zip && \
    chmod 755 ./dcm2niix/install/dcm2niix && \
    ln -s /apps/dcm2niix/install/dcm2niix /usr/bin/dcm2niix && \
    rm dcm2niix_lnx.zip

###############################################################################
# Install bids-manager
###############################################################################
RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-pip python3-tk python3-scipy && \
    pip3 install gdown setuptools PyQt5==5.15.4 nibabel xlrd \
    PySimpleGUI pydicom paramiko tkcalendar bids_validator && \
    gdown --id 1lwAgqS6fXKqWRzZhBntdLGGF4AIsWZx6 && \
    filename="bidsificator.zip" && \
    mkdir -p bidsmanager/install && \
    unzip -q -d bidsmanager/install ${filename} && \
    rm ${filename} && \
    cd bidsmanager/install/$(basename $filename .zip)/ && \
    python3 setup.py install && \
    apt-get remove -y --purge curl unzip && \
    apt-get autoremove -y --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

###############################################################################
# Install bids-tools
###############################################################################

# Set the working directory to /app/bids_tools
WORKDIR /apps/bids_tools

# Install Python dependencies of bids-tools
RUN pip3 install pybids==0.15.3 pandas==1.3.5 asyncio nest-asyncio

# Install dependencies for testing
RUN pip3 install pytest pytest-console-scripts pytest-cov

# Copy necessary contents of this repository.
COPY ./.coveragerc ./.coveragerc
COPY setup.py ./setup.py
COPY README.md ./README.md
COPY bids_tools ./bids_tools
# COPY LICENSE ./LICENSE

# Install bids-tools
RUN pip install -e .

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
ARG VERSION=0.0.1

LABEL org.label-schema.build-date=${BUILD_DATE} \
    org.label-schema.name="BIDS tools" \
    org.label-schema.description="Tools to handle BIDS datasets in the HIP platform" \
    org.label-schema.url="" \
    org.label-schema.vcs-ref=${VCS_REF} \
    org.label-schema.vcs-url="https://github.com/..." \
    org.label-schema.version=${VERSION} \
    org.label-schema.maintainer="The HIP team" \
    org.label-schema.vendor="The HIP team" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.docker.cmd="docker run"
