# Installation Instructions

This document informs you on how to run the Jupyter Notebooks within this repository. We offer two ways to do so. You can either run the projects on your machine or online with Binder.

## The approach we follow

We install Jupyter Notebook globally (only once) and make all dependencies of the sessions available through separated environments. Separating environments is important to avoid conflicting dependencies. For each environment we set up a kernel which is then used by Jupyter Notebook to access the dependencies of the sessions. 

## How to install Jupyter Notebook and session material on your machine

1. Download and install Anaconda: https://www.anaconda.com/

Run the following steps from the terminal/shell.

2. Install Jupyter Notebook globally. This way, we will install Jupyter only once and can use it across all environments: `conda install jupyter`. You can also install Jupyter within the "base" environment, then you would always have to activate the base environment before running Jupyter.
3. Clone this repository somewhere on your computer: `git clone https://github.com/CIXUniSaarland/SummerSchool2022.git`. Then, change directory into SummerSchool2022: `cd SummerSchool2022`
4. Create a conda environment for each session. For *session1* the command to do so would look like: `conda create -n session1 python=3.8`. You have to create six environments in total.
5.To activate an environment, run the command as follows (replace *session1* with any session environment you have already created): `conda activate session1`.
6. Change the directory to fit the session, e.g. for session1: `cd "Day 1 - Bayesian Inference"`
7. Install the requirements for the session (those packages will only be available within the currently activated environment): `pip install -r requirements.txt`
8. Add environment (here *session1*) as a kernel to Jupyter Notebook: `python -m ipykernel install --user --name=session1`
9. Deactivate environment after installing the requirements: `conda deactivate`

In case you need to remove an environment, run `conda remove --name session1 --all` to remove a ipykernel run `jupyter kernelspec uninstall session1`.

## How to run the Notebooks locally

1. Change the directory to fit the session, e.g. for session1: `cd "Day 1 - Bayesian Inference"`
2. From the terminal/shell run `jupyter notebook`. If you have installed Jupyter within the base environment, run `conda activate base` before. If you have installed Jupyter on your system globally, be sure to leave the environment by typing `conda deactivate`.
3. Jupyter Notebook will start and a browser window will open. The browser likely shows an error since it cannot open the local file. Instead check the URLs in the terminal and open the one that starts with: http://localhost:8888/?token=...`
4. You should now see the Jupyter frontend. You can create notebooks from there, be sure to select the right kernel for your notebook, e.g. `session1`. See: ![image](https://user-images.githubusercontent.com/8307823/173298493-cd96e8a1-40cf-48cf-92ab-7f296f65dbf0.png) 
5. Change the kernel for lecturer notebooks to fit to the session: ![image](https://user-images.githubusercontent.com/8307823/173306343-9817137e-b747-48e5-8941-87a280ff03c6.png)



## How to run the Notebooks with Binder

1. Go to https://mybinder.org/ 
2. Paste the repository's name `https://github.com/CIXUniSaarland/SummerSchool2022`  into the form field *GitHub repository name or URL* and the corresponding session branch into the field ` Git ref (branch, tag, or commit)`, e.g. `session1`. An overview of all branches can be found here: `https://github.com/CIXUniSaarland/SummerSchool2022/branches`
3. Launch the instance

**Note: Download your notebook files from Binder since they will not be persisted. Files get lost, for example, if you idle too long, since the Binder instance will shut down.**

## Install C++ dependencies (for Session 5 Part 2):

1. Install CMake: https://cmake.org/install/
2. Install Boost: https://www.boost.org/

About to change:
3. Clone the libigl repository: https://github.com/libigl/libigl/
