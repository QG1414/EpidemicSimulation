# Outbreak Lab
Author: Kacper Potaczała


## Basic Info
It's an app that simulates pandemic outbreaks depending on different parameter setups. You can view the number of infected people on a plot and check how many times during simulations a pandemic started and how many people died on average.

If you want to check each parameter and what they do, they are listed [here](#parameters)

If your CUDA is not working, check this note [here](#cuda-information)

## App Versions

The app is separated into 3 forms:
  * [Console Version](https://github.com/QG1414/OutbreakLab/tree/ConsoleVersion)
  * [Visual Version](https://github.com/QG1414/OutbreakLab/tree/VisualVersion)
  * [Exe Version](https://github.com/QG1414/OutbreakLab/tree/ExeVersion)

Every version is different from each other, so each version has its own readme on its own branch, linked above.

## App Releases

If you want, you can also check releases that are provided for every version:
  * [Console](https://github.com/QG1414/OutbreakLab/releases/tag/Console_Version)
  * [Visual](https://github.com/QG1414/OutbreakLab/releases/tag/VisualVersionRelease)
  * [Exe](https://github.com/QG1414/OutbreakLab/releases/tag/ExeVersionRelease)

## Cuda Information

Every version of the app uses CUDA. This is only optional and can be disabled either by visual checkbox or by setting one parameter in the code to false. Nonetheless, the app was built on CUDA version 12.8 and it should work with this version. If you do not have this version, be careful when using the CUDA option, as it can block the app.

## Parameters

The app has many parameters that can be changed and that influence simulation.

Some of them are the cause of randomization; more about that [here](#randomization)

These are only the default app names of parameters, and when using the console version they might be different, but what they do stays the same.

Parameters are divided into categories:

 * People Settings - they change base params about the simulation itself:
    - Generation Size - how big our population is; it's an integer number between [0, inf)
    - Days to simulate - number of simulation days, so how long our x-axis will be; it's an integer number between [0, inf]
    - Number of simulations - how many lines will be on the plot, so how many simulations we will run; it's an integer number between [0, inf]

      
 * Sickness Settings - these are params that determine how our disease is spreading:
    - Chance to infect while meeting - this parameter determines the probability of becoming sick while meeting with a person who is sick; it's a float value between [0, 1]
    - Chance to meet - This field shows how many people we can meet and with what probability. It's a set of values: the first one is the number of people, it's an integer from [0,inf] and the second one is the chance to meet, with values from [0,1]

      
 * Curing Settings - these variables determine how long someone will be sick and what chance they have to be cured:
    - Minimal number of days to lose sickness - this is the smallest number of days to be cured or to die from sickness; it's an integer number between [0, inf]
    - Maximal number of days to lose sickness - this is the largest number of days to be cured or to die from sickness; it's an integer number between [0, inf]
    - Chance to cure from sickness - This is the chance to be cured. Important info: cured people gain resistance to sickness, and also (1 - Chance to cure from sickness) is the probability that someone will die from being sick instead of gaining resistance; it's a float value between [0, 1]


 * Resistance Settings - these variables determine how long someone will be resistant to sickness after vaccination or curing from sickness:
    - Minimal number of days to lose resistance to sickness - this is the smallest number of days to lose resistance to sickness; it's an integer number between [0, inf]
    - Maximal number of days to lose resistance to sickness - this is the largest number of days to lose resistance to sickness; it's an integer number between [0, inf]

  
 * Modifiers - modifiers are special fields that show real-life problems or solutions that can change how sickness is spreading and how deadly it is:
    - Hygiene Modifier - Changes the chance to infect, which may cause the disease to spread faster or slower; it's an enum value between [Very Bad, ..., Very Good]
    - Population Control Modifier - Changes the probability of meeting people; with good control we meet fewer people, with worse we meet more; it's an enum value between [Very Bad, ..., Very Good]
    - Healthcare Modifier - Changes how good or bad healthcare is and modifies the chance to cure from sickness; it's an enum value between [Very Bad, ..., Very Good]


 * Vaccines - it's a special type of modifier because it can be turned off and have different values. It simulates creating a vaccine and how it helps with reducing the number of people sick:
    - Vaccines Created - this only determines if vaccines are created or not; it's a boolean value {True, False}
    - Percentage of Population Vaccinated - this is a value to simulate how many people will take the vaccine; it's a float value between [0, 1]
    - Day of Vaccines Creation - it's the day of the simulation when vaccines are created. When we want them from the start, set 0. This is connected with the parameter Days to simulate; it's an integer number between [0, inf]


We also have additional params that are not connected with a symulation, rather they change how its calculated and displayed this options are:
 * Show animation - when this value is True then animation will play showing one symulation at a time, and one day at a time, It's better to disable it for bigger symulations, its a boolean value {True, False}
 * Use Log Scale - when this value is True plot will have a logarytmic scale on y-axis, its easier to read for symulations with big Generation Size, when disabled scale is linear, its a boolean value {True, False}
 * Use CUDA - its value that is optional and only for optimization, when on instead of using CPU for computation we will be using cuda, in case of problems with using it refer to [this](#cuda-information)



## Randomization

A few parameters in the app are randomized, so results can be really different. Here are some examples of randomized values:
 * Minimal number of days to lose sickness and Maximal number of days to lose sickness - output of that is a randomized value between them inclusively on both sides
 * Minimal number of days to lose resistance to sickness and Maximal number of days to lose resistance to sickness - output of that is a randomized value between them inclusively on both sides
 * Simulation of meeting is a randomized value to determine how many people we are meeting depending on the parameter (Chance to meet), and after getting the number of people we once more randomly check if we infect them with the parameter (Chance to infect while meeting)

## Presets

Every app version has a few presets that can be used to simulate real-life epidemics or pandemics.

List of presets:
* PLAGUE - simulation of the Black Death in Europe from 1346 to 1353
* SPANISH_FLU - simulation of the flu that took place in Europe at the end of WW1
* COVID - simulation of COVID in recent years
* VON_ECONOMO_ENCEPHALITIS - not very well-known epidemic taking place during the Spanish flu epidemic

## Interpretation Of Results

Results are shown in a few places:
* Plot - shows the number of infected people (y-axis) by days (x-axis)
* Pie chart - shows how many times an epidemic started, ended, or was stable. Stable means that it was not recognized as an epidemic but also never ended
* Text above the pie chart - shows the number of people that died during this simulation. It's only an average from all simulations
