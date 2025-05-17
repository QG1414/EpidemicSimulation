# Outbreak Lab
Author: Kacper Potaczała


## Basic Info
The console version is the simplest version of this app and also not recommended to use because it lacks security measures for incorrect values. To use this version, you need these libraries and Python installed [here](#requirements)

All of the parameters that can be changed are located in the main.py file from line 10 to line 38.
All preset names are listed [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#presets)

## Usage
To run this app, download the ZIP version of the code from this [release](https://github.com/QG1414/OutbreakLab/releases/tag/Console_Version) or copy using Git. When this is done, make sure you have all the required libraries installed.

By default, the selected preset is COVID. For more info about presets, check [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#presets)

If you want to switch to a different preset, modify line 60: PRESETS.<Name of preset>.value

If you don't want to use presets and want to insert your own values, then comment out line 60 and uncomment lines 53 and 54.
Then you can modify the values above, or leave them as they are, and run the code.

In the console, you should see info that the simulation started and how many steps are completed.

When loading finishes, a plot should be displayed showing the number of infected people and a pie chart showing how many times there has been an epidemic, or it ended, or is still going but it's not an epidemic (Stable). For more about this, read [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#interpretation-of-results)

## Name Changes
In the console version, some parameters have changed names and you should know which value is which. For the full list, check [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#parameters)

Here are all the changes:
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
The app was built on Python version 3.12.2 and will work on this version.
Versions before 3.6 will not work for sure because of f-strings used in many places. Try to use versions between [3.10.0 - 3.13.0], but the best version is 3.12.2.

## Libraries
Libraries that are needed for correct operation of the app:
* matplotlib
* pandas
* numpy
* cupy

## Installation
For matplotlib, pandas, and numpy, use:

python -m pip install matplotlib pandas numpy

Using CUDA is more complicated. The app was created on CUDA 12.8, but you should check if you have CUDA and what version. To do this, run the command:

nvidia-smi

Then install:

python -m pip install cupy-cuda{version}x

where version is the version of your CUDA. For example, for CUDA 12.8:

python -m pip install cupy-cuda12x



