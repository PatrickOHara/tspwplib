# Installation

Install via pip:

```bash
pip install tspwplib
```

You will also need access to the OPLib dataset:

```bash
git clone https://github.com/bcamath-ds/OPLib.git
```

Optionally you may also want to download the original tsplib95 dataset:

```bash
git clone https://github.com/rhgrant10/tsplib95.git
```

It is convenient to define environment variables to define the location of OPLib and tsplib95:

```bash
TSPLIB_ROOT="$(pwd)/tsblib95/archives/problems/tsp"
OPLIB_ROOT="$(pwd)/OPLib/"
```

Replace `$(pwd)` with the appropriate directory where you cloned OPLib and tsplib95.

## Docker

You can also use docker, useful if you are having problems installing graph-tool.

```bash
docker pull patrickohara/tspwplib:latest
```

To build the graph-tool docker file for Ubuntu:20.04:

```bash
docker build -f graph_tool_ubuntu.Dockerfile -t patrickohara/graph_tool_ubuntu:latest .
```

To build the tspwplib docker image (based on the graph-tool image):
```bash
docker build -t patrickohara/tspwplib:latest .
```
