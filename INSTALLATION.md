# Installation Instructions

This document informs you on how to run the Jupyter Notebooks within this repository. We offer two ways to do so. You can either run the projects on your machine or online with Binder.

## How to install Jupyter Notebook and session material on your machine

1. Download and install Anaconda: https://www.anaconda.com/

Run the following steps from the terminal/shell.

2. Install Jupyter Notebook globally. This way, we will install Jupyter only once and can use it across all environments: `conda install jupyter`
3. Clone this repository somewhere on your computer: `git clone https://github.com/CIXUniSaarland/SummerSchool2022.git`. Then, change directory into SummerSchool2022: `cd SummerSchool2022`
5. Create a conda environment for each session. For *session1* the command to do so would look like: `conda create -n session1 python=3.8`. You have to create six environments in total.
6.To activate an environment, run the command as follows (replace *session1* with any session environment you have already created): `conda activate session1`.
7. Change the directory to fit the session, e.g. for session1: `cd "Day 1 - Bayesian Inference"`
8. Install the requirements for the session (those packages will only be available within the currently activated environment): `pip install -r requirements.txt`
9. Add environment (here *session1*) as a kernel to Jupyter Notebook: `python -m ipykernel install --user --name=session1`
10. Deactivate environment after installing the requirements: `conda deactivate`

In case you need to remove an environment, run `conda remove --name session1 --all` to remove a ipykernel run `jupyter kernelspec uninstall session1`.

## How to run the Notebooks locally

1. Change the directory to fit the session, e.g. for session1: `cd "Day 1 - Bayesian Inference"`
2. From the terminal/shell run `jupyter notebook`
3. Jupyter Notebook will start and a browser window will open. The browser likely shows an error since it cannot open the local file. Instead check the URLs in the terminal and open the one that starts with: http://localhost:8888/?token=...`

## How to run the Notebooks with Binder

1. Go to https://mybinder.org/ 
2. Paste the repository's name `https://github.com/CIXUniSaarland/SummerSchool2022`  into the form field *GitHub repository name or URL* and the corresponding session branch into the field ` Git ref (branch, tag, or commit)`, e.g. `session1`. An overview of all branches can be found here: `https://github.com/CIXUniSaarland/SummerSchool2022/branches`
3. Launch the instance

## Install C++ dependencies (for Session 5 Part 2):

1. Install CMake: https://cmake.org/install/
2. Install Boost: https://www.boost.org/

About to change:
3. Clone the libigl repository: https://github.com/libigl/libigl/
