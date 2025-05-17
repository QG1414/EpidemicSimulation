# Outbreak Lab
Author: Kacper Potaczała


## Basic Info
The Visual Version is more complicated but also more user-friendly. It has a visual interface made in Kivy, and all options, presets, and simulations are in one place—no need to change anything in the main.py file.

To use this version, you have to install all packages and make sure the Python version is correct. This info can be checked [here](#requirements)

## Usage
To run this app, download the ZIP version of the code from this [release](https://github.com/QG1414/OutbreakLab/releases/tag/VisualVersionRelease) or copy it using Git. When this is done, make sure you have all the required libraries installed.

By default, some values are set. You can check them in the Set Data menu option. These values are the same as those listed in the parameters section [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#parameters)

If you want to change values, just type a new value in the field and click Save at the bottom of the page.

If you want to switch to using a preset, click the Set Presets menu option, select the preset you want from the list, and then click Save and Back. If you want to know what the options refer to, check [this](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#presets)

On the left side of the main menu, there are additional options listed in the parameters [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#parameters)

To run the simulation, click Start Simulation and wait for loading to finish.

You can cancel loading at any time if it takes too long.

When loading finishes, a new window will open, and you can return to the menu by closing it.

To understand how to interpret results, check [this](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#interpretation-of-results)

## Visualas and what they do

There are some visuals and buttons, so we will list them all:

* Main menu
  - The label on the left indicates what preset is used. When "None" is active, then options from Set Data are used.
  - Checkboxes under the label are additional options to simulate. For more info, refer to [this](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#parameters)
  - Buttons on the right are different screens, each with different options:
    - Start Simulation – starts simulation and data loading
    - Set Data – lets you change settings for simulation listed [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#parameters)
    - Set Presets – lets you choose one preset from your choice; all presets are listed [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#presets)
    - Exit – closes the application
* Loading
   - The circle with a percentage is just a loading visualization of how much data was calculated
   - Cancel Loading button stops loading and returns to the main screen
* Set data
   - The number of options is too great to list—refer to this [page](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#parameters)
   - Back button returns to the main screen without saving changes
   - Save button saves changes and returns to the main screen
* Set Preset
   - The label at the top indicates which preset is selected
   - The spinner below lets you choose one of the presets listed [here](https://github.com/QG1414/OutbreakLab?tab=readme-ov-file#presets)
   - Back button returns to the main menu without saving changes
   - Save button sets the preset to the selected one, but does not exit to the main menu—click Back to return

## Cuda set info
When using CUDA, sometimes it cannot be detected on a computer. If this happens, a notification will be displayed and CUDA will be automatically disabled.

## Requirements
Here are some requirements:
The app was built on Python version 3.12.2 and will work on this version.
Versions before 3.6 will not work due to the use of f-strings in many places. Try to use versions between [3.10.0 – 3.13.0], but the best version is 3.12.2.
Kivy allows versions from [3.8 – 3.13], so these should work as well.

This app operates on Kivy version 2.3.1.

## Libraries
Libraries that are needed for correct operation of the app:
* matplotlib
* pandas
* numpy
* cupy
* kivy

## Installation
For matplotlib, pandas, and numpy, use:

* python -m pip install matplotlib pandas numpy

Using CUDA is more complicated. The app was created on CUDA 12.8, but you should check if you have CUDA and what version. To do this, run the command:

* nvidia-smi

Then install:

* python -m pip install cupy-cuda{version}x

where version is the version of your CUDA. For example, for CUDA 12.8:

* python -m pip install cupy-cuda12x

For kivy

* python -m pip install "kivy[base]"



