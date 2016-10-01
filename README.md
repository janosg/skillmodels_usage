skillmodels usage
=================

This repository illustrates the use of [skillmodels](https://github.com/suri5471/skillmodels) - a python package for the estimation of non-linear skill formation models and other non-linear dynamic latent factor models.

The code is structured according to the Project Templates by Hans-Martin von Gaudecker that can be found [here](https://github.com/hmgaudecker/econ-project-templates). To run the code you need Conda. If you use Anaconda or Miniconda you already have it. Else, see [here](http://conda.pydata.org/docs/install/quick.html) for installation instructions.

After cloning the repository, open a shell in its main directory. You can then type:

* source set-env.sh (on Mac or Linux) or set-env.bat (on Windows). This will install the necessary Python packages (including skillmodels and its dependencies) in a [conda environment](http://conda.pydata.org/docs/using/envs.html).
* python waf.py configure to configure waf.
* python waf.py to run the project

The last step will take a minute or two because it runs one model with each estimator:

* An example model from the replication files of the CHS paper is estimated with the chs estimator. (In order to save computation time the maximization of the likelihood function is started with the correct values; with worse start values it takes more than an hour to fit the models but the results are the same).
* A model with simulated data is estimated with the WA estimator. (In order to save computation timpe, the number of bootstrap replications for the standard error was set to a very low number.)

After it has completed you will find plots of a comparison of skillmodels results and the fortran results from the CHS [replication files](https://www.econometricsociety.org/content/supplement-estimating-technology-cognitive-and-noncognitive-skill-formation-0) in the bld directory. In the same place you can find csv files with the estimated parameters of both models.

