# Métodos Matemáticos

This repository illustrates how to solve differential equations symbolically using Python.

It mainly uses sympy to solve equations and matplotlib + numpy to plot particular results.

Examples were taken from Lista 1 e 2, from Kreyszig's Advanced Engineering Mathematics book, 10th Edition.

To run the notebooks with the examples you must have a python environment with **jupyter notebook, numpy, sympy and matplotlib**.

There is a "recipe" to install the environment using the file *pyproject.toml*.

First, install **uv** dependency manager:

```bash
pip install uv
```

Then use uv to install the dependencies:

```bash
uv pip install .
```

This will build a virtual environment under *.venv* folder with the python executable.
Select the corresponding executable to use as a Jupyter Python kernel, if using (VSCode)[https://code.visualstudio.com/docs/datascience/jupyter-kernel-management]

### Stability analysis app

To run the stability analysis app use the following command:

```bash
uv run streamlit run app/app.py
```