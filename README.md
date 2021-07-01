# Praktikum Technische Informatik

[![RWTHjupyter](https://jupyter.pages.rwth-aachen.de/documentation/images/badge-launch-rwth-jupyter.svg)](https://jupyter.rwth-aachen.de/hub/spawn?profile=pti&next=/user-redirect/lab/tree/pti%2Findex.ipynb) 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IENT/PTI.git/master?urlpath=lab/tree/index.ipynb)

## Introduction

This repository contains Jupyter Notebooks for the Praktikum Technische Informatik at RWTH Aachen University.

Visit the notebook [index.ipynb](index.ipynb) for a table of contents.

## Quick Start

Run the notebooks directly online [RWTHjupyter](https://jupyter.rwth-aachen.de): [![RWTHjupyter](https://jupyter.pages.rwth-aachen.de/documentation/images/badge-launch-rwth-jupyter.svg)](https://jupyter.rwth-aachen.de/hub/spawn?profile=pti&next=/user-redirect/lab/tree/pti%2Findex.ipynb)

* The starting process of the session may take up to one minute.

As a fall back: Use Binder or offline usage (see below).

## Binder

Run the notebooks directly online [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IENT/PTI.git/master?urlpath=lab/tree/index.ipynb). Please note the following limitations:

* The starting process of the session may take up to one minute.
* Please note that the session will be cancelled after 10 minutes of user inactivity.


## Offline Usage

To be able to open the PTI notebooks locally, you need to have a Python environment as well as JupyterLab installed. We recommend to use Anaconda for a local installation.

### Anaconda

To run the notebooks on your local machine, you may use [Anaconda](https://www.anaconda.com/) (using `pip` is also possible for experienced users. You have to install all the requirements listed in `binder/environment.yml` and install the two `jupyter labextension ...` commands listed in `binder/postBuild`).

#### Installation

* Install [Anaconda](https://www.anaconda.com/).
* Download this repository to your local disk. You can download it as a zip-File or use `git`:  `git clone --recurse-submodules git@git.rwth-aachen.de:IENT/pti.git`.
* It is highly recommended to run the PTI notebooks in an isolated Anaconda environment. You can create a new environment called `ptilab` from the provided `binder/environment.yml` by running `conda env create -f binder/environment.yml` in the Anaconda prompt. This makes sure that all required packages are installed amd don't interfere with the packages in your base environment.
* Activate this environment with `conda activate ptilab`.
* Run two final commands in the Anaconda prompt (with activated `ptilab` environment):

  ```bash
  chmod +x binder/postBuild
  binder/postBuild
  ```

  If the latter command fails, please open `binder/postBuild` and execute the commands listed there manually.

#### Run

* Activate the environment  with `conda activate ptilab`.
* Run JupyterLab  `jupyter lab`. In your browser, JupyterLab should start. You can then open `index.ipynb` for an overview over all notebooks.
* You can deactivate the environment with `conda deactivate` (and switch back to it with `conda activate ptilab`).

### Docker

For advanced users only: If you happen to have Docker installed, you can start a local dockerized JupyterLab with enabled PTI with

```bash
docker run --name='pti' --rm -it -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes registry.git.rwth-aachen.de/ient/pti:master
```

Copy and paste the displayed link to your favorite browser.

## Contact

* If you found a bug, please use the [issue tracker](https://git.rwth-aachen.de/IENT/pti/issues).
* In all other cases, please contact [Christian Rohlfing](http://www.ient.rwth-aachen.de/cms/c_rohlfing/).

The code is licensed under the [MIT license](https://opensource.org/licenses/MIT).