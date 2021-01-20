FROM patrickohara/graph_tool_ubuntu:latest

WORKDIR /app

COPY . tspwplib

RUN pip3 install -e tspwplib
