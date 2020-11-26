# Installation

Install via pip and git:

```bash
python -m pip install git+https://github.com/PatrickOHara/tspwplib.git
```

You will also need access to the OPLib dataset:

```bash
git clone https://github.com/bcamath-ds/OPLib.git
```

Optionally you may also want to download the original tsplib95 dataset:

```bash
git clone git://github.com/rhgrant10/tsplib95
```

It is convenient to define environment variables to define the location of OPLib and tsplib95:

```bash
TSPLIB_ROOT="$(pwd)/tsblib95/archives/problems/tsp"
OPLIB_ROOT="$(pwd)/OPLib/"
```

Replace `$(pwd)` with the appropriate directory where you cloned OPLib and tsplib95.
