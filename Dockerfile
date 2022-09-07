FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG ANYWAVE_VERSION=2.1.3
ARG DCM2NIIX_VERSION=1.0.20211006
ARG BIDSMANAGER_VERSION=latest

WORKDIR /apps/

# Install anywave
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \ 
    curl ca-certificates libqt5charts5 libqt5concurrent5 libqt5multimediawidgets5 \
    libqt5printsupport5 libqt5qml5 libmatio9 libvtk7.1p-qt \
    libqwt-qt5-6 libqt5xml5 libqcustomplot2.0 libtbb2 && \ 
    curl -Ok https://meg.univ-amu.fr/AnyWave/anywave-${ANYWAVE_VERSION}_amd64.deb && \
    dpkg -i anywave-${ANYWAVE_VERSION}_amd64.deb && \
    rm anywave-${ANYWAVE_VERSION}_amd64.deb

# Install dcm2niix
RUN apt-get install --no-install-recommends -y unzip && \
    curl -O -L https://github.com/rordenlab/dcm2niix/releases/download/v${DCM2NIIX_VERSION}/dcm2niix_lnx.zip && \
    mkdir -p ./dcm2niix/install && \
    unzip -q -d ./dcm2niix/install dcm2niix_lnx.zip && \
    chmod 755 ./dcm2niix/install/dcm2niix && \
    ln -s /apps/dcm2niix/install/dcm2niix /usr/bin/dcm2niix && \
    rm dcm2niix_lnx.zip

# Install bids-manager
RUN apt-get install --no-install-recommends -y \ 
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

COPY ./scripts/ /scripts
COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

#######################################################################
# Container Image Metadata (label schema: http://label-schema.org/rc1/)
#######################################################################

# LABEL maintainer=""

LABEL org.label-schema.build-date=${BUILD_DATE} \
      org.label-schema.name="BIDS tool" \
      org.label-schema.description="Tool to import / update BIDS datasets in the HIP platform" \
      org.label-schema.url="" \
      org.label-schema.vcs-ref="" \
      org.label-schema.vcs-url="https://github.com/..." \
      org.label-schema.version="" \
      org.label-schema.maintainer="" \
      org.label-schema.vendor="" \
      org.label-schema.schema-version="1.0" \
      org.label-schema.docker.cmd="docker run"
