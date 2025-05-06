from enum import Enum

class PRESETS( Enum ):
    PLAGUE = "dzuma_preset.json"
    SPANISH_FLU = "hiszpanka_preset.json"
    COVID = "covid_preset.json"
    VON_ECONOMO_ENCEPHALITIS = "zapalenie_mozgu_Economo_preset.json"
    NONE = ""

class PRESETS_NAMES( Enum ):
    PLAGUE = "plague"
    SPANISH_FLU = "spanish flu"
    COVID = "covid"
    VON_ECONOMO_ENCEPHALITIS = "Von Economo's Encephalitis"
    NONE = "none"

class PRESETS_BASE( Enum ):
    CPU = "presets\\cpu\\"
    GPU = "presets\\gpu\\"

class MainPresets( Enum ):
    NAME = "preset_name"
    SYMULATION = "symulation_params"
    GENERATION = "generation_params"
    EPIDEMY = "epidemy_params"
    CURING = "curing_params"
    RESISTANCE = "resistance_params"
    MODIFIERS = "modifiers_params"
    VACCINES = "vaccines_params"

#region enum_subpresetes

class SymulationSubPresets( Enum ):
    MEETING_CHANCE = "chance_to_meet"
    DAYS = "days"
    SYMULATIONS = "symulations"

class GenerationSubPresets( Enum ):
    SIZE = "size"
    THRESHOLD = "epidemy_threshold"

class CuringSubPresets( Enum ):
    MIN_TIME = "curing_min"
    MAX_TIME = "curing_max"
    PROB = "curing_prob"

class ResistanceSubPresets( Enum ):
    MIN_TIME = "res_min"
    MAX_TIME = "res_max"

class EpidemySubPresets( Enum ):
    INFECTION_PROB = "prob_to_infect"

class ModifiersSubPresets( Enum ):
    HYGIENE = "hygiene"
    POPULATION = "population_control"
    HEALTHCARE = "healthcare"
    VACCINES = "vaccines"

class VaccinesSubPresets( Enum ):
    POPULATION = "population_vaccinated"
    DAY = "day_of_vaccines"

#endregion enum_subpresetes