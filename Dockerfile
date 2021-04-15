FROM python:3.8

WORKDIR /app

# Download data for oplib
ENV OPLIB_ROOT /app/OPLib
RUN git clone https://github.com/bcamath-ds/OPLib.git ${OPLIB_ROOT}

# Download data for tspwplib
ENV TSPLIB_ROOT /app/tsplib95/archives/problems/tsp
RUN git clone https://github.com/rhgrant10/tsplib95.git /app/tsplib95

COPY . tspwplib

RUN pip3 install -e tspwplib
