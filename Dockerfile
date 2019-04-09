FROM ubuntu:bionic

# SHELL [ "/bin/bash", "-c" ]

ARG PYTHON_VERSION_TAG=3.7.3
ARG LINK_PYTHON_TO_PYTHON3=1

RUN apt-get -qq -y update && \
    apt-get -qq -y upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
        gcc \
        g++ \
        zlibc \
        zlib1g-dev \
        libssl-dev \
        libbz2-dev \
        libsqlite3-dev \
        libncurses5-dev \
        libgdbm-dev \
        libgdbm-compat-dev \
        liblzma-dev \
        libreadline-dev \
        uuid-dev \
        libffi-dev \
        tk-dev \
        wget \
        curl \
        git \
        make \
        sudo \
        tesseract-ocr \
        ghostscript \
        software-properties-common && \
    mv /usr/bin/lsb_release /usr/bin/lsb_release.bak && \
    apt-get -y autoclean && \
    apt-get -y autoremove && \
    rm -rf /var/lib/apt-get/lists/*

RUN dpkg --configure -a

# Needed for Java
RUN mkdir -p /usr/share/man/man1

# Java install
RUN apt-get install -f && \
    apt-get -y install default-jre && \
    apt-get clean

ADD install_python.sh install_python.sh
RUN bash install_python.sh ${PYTHON_VERSION_TAG} ${LINK_PYTHON_TO_PYTHON3} && \
    rm -r install_python.sh Python-${PYTHON_VERSION_TAG}

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /tmp

RUN mkdir /tmp/working

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY pdf_table_to_dataframe.py /tmp/pdf_table_to_dataframe.py
COPY pdf_to_tiff.sh /tmp/pdf_to_tiff.sh
COPY pdf_tables.sh /tmp/pdf_tables.sh

ENTRYPOINT ["./pdf_tables.sh"]
