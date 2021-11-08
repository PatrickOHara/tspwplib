# Scripts

To run the scripts you will need additional dependencies.
You can use conda to install osmnx, and pip/git to do the rest:


```bash
conda install -c conda-forge osmnx
git clone https://github.com/alan-turing-institute/urbanroute.git
pip install -e urbanroute/urbanroute
pip install -r requirements.txt
```

Each of the scripts has a `--help` option, e.g.

```bash
python from_urbanair.py --help
```