from generationScripts.generation import GenerationData
from enums.epidemyEnums import *
from enums.presetEnums import PRESETS
from SymulationData import SymulationData


#region raw_values_input

#people variables
generation_size : int = 300000 # population size if its more then 10_000_000 then cuda should be used
chance_to_meet_people : dict[int, int] = {0:0.1, 1:0.1, 2:0.8} # chance to meet people with given prob, sum of the values should add up to 1
n : int = 30 # numbers of days to simulate with cuda good value is 60 without 30
k : int = 15 # amount of simulations with cuda good value is 30 without 15

#sickness variables
threshold : float = 0.005 # threshold when new number of infections are considered epidemy
p : float = 0.9 # chance to infect when meeting

#curing
curing_time_min : int = 3 # minimal amount of days before people die or are cured
curing_time_max : int = 5 # maximal amount of days before people die or are cured
curing_prob : float = 0.6 # chance to cure, chance to die is 1 - curing_prob

#resistance
res_time_min : int = 5 # minimal amount of days before people lose resistance to sickness
res_time_max : int = 7 # maximal amount of days before people lose resistance to sickness

#modifiers
hygiene : MODIF_LEVELS = MODIF_LEVELS.VERY_GOOD # when hygiene is good chance to infect is lower when bad its worse
population_control : MODIF_LEVELS = MODIF_LEVELS.VERY_GOOD # when population control is good chance to meet a lot of people is lower when bad its bigger
healthcare : MODIF_LEVELS = MODIF_LEVELS.VERY_BAD # when healthcare is good chance to cure is bigger when bad its lower
vaccines : MODIF_ENABLED = MODIF_ENABLED.ENABLED # when vaccines are enabled then we add info about how many people are vaccinated and from wchich day

#population vaccinated is how much percentage of people is vaccinated
#day of vaccines is info from wchich day vaccines are starting
vaccines_params : dict[VACCINES_PARAMS:any] = {
    VACCINES_PARAMS.POPULATION_VACCINATED : 0.4, VACCINES_PARAMS.DAY_OF_VACCINES : 0 
    }

#modif is only for easier data manipulation
modif : dict[str,any] = {
    MODIFIERS.HYGIENE.value : hygiene,
    MODIFIERS.POPULATION_CONTROL.value : population_control,
    MODIFIERS.HEALTHCARE.value : healthcare,
    MODIFIERS.VACCINES.value : vaccines,
    VACCINES_PARAMS.VACCINES_PARAM.value : vaccines_params
    }

#endregion raw_values_input


# GenerationData and SymulationData needs to be uncommented only when we are not using presets
#generation_data = GenerationData( generation_size, threshold, curing_time_min, curing_time_max , curing_prob, res_time_min, res_time_max )
#sd = SymulationData( generation_data, chance_to_meet_people, n, k, p, modif, enable_cuda=True )



# PRESETS some presets are created and autmaticly selected when cuda is available and enabled
# all possible presets are in enum PRESETS
sd : SymulationData = SymulationData.import_preset(PRESETS.COVID.value, enable_cuda=False)

#here we set is scale should be logarytmic
sd.path_generator_visual.set_scale_log(True)

if __name__ == "__main__":
    # we start the simulation, when number of simulations is greater then 30 then animate should be false
    sd.start_gaphing(animate=True)
