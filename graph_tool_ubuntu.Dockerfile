FROM ubuntu:20.04

# Non interactive argument for dockerfiles
ARG DEBIAN_FRONTEND=noninteractive

# Update package managers
RUN apt -y update --fix-missing && \
    apt -y upgrade

# Add graph tool as a source for apt
RUN apt install -y software-properties-common
RUN apt-key adv --keyserver keys.openpgp.org --recv-key 612DEFB798507F25
RUN add-apt-repository "deb [ arch=amd64 ] https://downloads.skewed.de/apt focal main"

# Update again then install packages
RUN apt -y update --fix-missing && \
    apt -y upgrade && \
    apt install -y \
        git \
        python3-graph-tool \
        python3-pip

WORKDIR /app

# Download data for oplib
ENV OPLIB_ROOT /app/OPLib
RUN git clone https://github.com/bcamath-ds/OPLib.git ${OPLIB_ROOT}

# Download data for tspwplib
ENV TSPLIB_ROOT=/app/tsplib95/archives/problems/tsp
RUN git clone https://github.com/rhgrant10/tsplib95.git /app/tsplib95