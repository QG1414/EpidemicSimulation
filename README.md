# Outbreak Lab
Author: Kacper Potaczała


## Basic Info
Console version is the simpliest version of this app and also not recomended to use because it lacks security measures for incorrect values. To use this version you need this libraries and python installed [here](#requirements)

All of the parameters that can be changed are located in the main.py file from line 10 to line 38
And all presets name are listed [here]

## Usage
To run this app download zip version of code from this [release](https://github.com/QG1414/OutbreakLab/releases/tag/Console_Version) or copy using git, when this is done make sure you have all libraries installed 

On start there is selected preset Covid on more info about presets check [here]

If you want to change to different preset modifie line 60 PRESETS.<Name of preset>.value

If you don't want to use presets and insert your own values then comment line 60 and uncomment line 53 and 54
Then you can modifi values above or leave them as they are and run the code.

In console you should see info that symulation started and how many steps are done.

When loading finishes then plot should be displayed that shows number of infected people and a pie chart showing how many times there has been epidemy or it ended or is still going but its not a epidemy (Stable) on more about it read [here]

## Name Changes
In console version some parameters have changed name and you should know which value is wchich. For whole list check [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#parameters)
here are all changes:

* generation_size == Generation Size
* chance_to_meet_people == Chance to meet
* n == Days to simulate
* k == Number of simulations
* p == Chance to infect while meeting
* curing_time_min == Minimal number of days to lose sickness
* curing_time_max == Maximal number of days to lose sickness
* curing_prob == Chance to cure from sickness
* res_time_min == Minimal number of days to lose resistance to sickness
* res_time_max == Maximal number of days to lose resistance to sickness
* hygiene == Hygiene Modifier
* population_control == Population Control Modifier
* healthcare == Healthcare Modifier
* vaccines == Vaccines Created
* vaccines_params[VACCINES_PARAMS.POPULATION_VACCINATED] == Percentage of Population Vaccinated
* vaccines_params[VACCINES_PARAMS.DAY_OF_VACCINES] == Day of Vaccines Creation


## Requirements
Here are some requirements:
App was builded on python version 3.12.2 and it will work on this version.
Versions before 3.6 will not work for sure because of f format in a lot of places so try to use versions: [3.10.0 - 3.13.0] but best version is 3.12.2

## Libraries
Libraries that are needed for correct work of app:
* matplotlib
* pandas
* numpy
* cupy

## Installation
for matplotlib, pandas and numpy we use

python -m pip install matplotlib pandas numpy

Using cuda is more complicated app was created on Cuda 12.8 but you should check if you have cuda and what version to do it run command

nvidia-smi

and then install

python -m pip install cupy-cuda{version}x

where version is the version of our cude so for example for Cuda 12.8

python -m pip install cupy-cuda12x



