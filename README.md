skillmodels usage
=================

This repository illustrates the use of skillmodels - a python package for the estimation of non-linear skill formation models and other non-linear dynamic latent factor models.

The code is structured according to the Project Templates by Hans-Martin von Gaudecker that can be found [here](https://github.com/hmgaudecker/econ-project-templates). To run the code you need Conda. If you use Anaconda or Miniconda you already have it. Else, see [here](http://conda.pydata.org/docs/install/quick.html) for installation instructions.

After cloning the repository, open a shell in its main directory. You can then type:

* source set-env.sh (on Mac or Linux) or set-env.bat (on Windows). This will install the necessary Python packages (including skillmodels and its dependencies) in a [conda environment](http://conda.pydata.org/docs/using/envs.html).
* python waf.py configure to configure waf.
* python waf.py to run the project

The last step will take some time (on my laptop about 10 minutes) because it runs two example models: Model one from the replication files of the CHS paper and the same model corrected for the [critique](https://dl.dropboxusercontent.com/u/33774399/wiswall_webpage/agostinelli_wiswall_renormalizations.pdf) by Wiswall and Agostinelli. After it has completed you will find plots of a comparison of skillmodel results and the fortran results from the CHS [replication files](https://www.econometricsociety.org/content/supplement-estimating-technology-cognitive-and-noncognitive-skill-formation-0) in the bld directory.
