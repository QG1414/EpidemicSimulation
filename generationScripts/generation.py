from enums.epidemyEnums import EpidemyState
import numpy as np

#region additional_classes

class InfectionData:
    def __init__( self, diesesed_number : int, generation_number : int, timer : int, percentage : float = 0 ) -> None:
        self.diesesed_number : int = diesesed_number
        self.generation_number : int = generation_number
        self.timer : int = timer
        self.percentage : float = percentage
    
    def final_timer( self ) -> int:
        return self.generation_number + self.timer

    def update( self, newGenerationNumber : int ) -> int:
        if newGenerationNumber >= self.final_timer():
            return self.diesesed_number
        return -1

    def update_percentage( self, newGenerationNumber : int ) -> float:
        if newGenerationNumber >= self.final_timer():
            return self.percentage
        return -1

class GenerationData:
    def __init__( self, generation_size:int, epidemy_treshold:int, curing_time_min:int, curing_time_max : int, curing_prob:float, resTime_min : int, resTime_max : int ) -> None:
        self.generation_size : int = generation_size
        self.curing_time_min : int = curing_time_min
        self.curing_time_max : int = curing_time_max
        self.curing_prob : float = curing_prob
        self.base_curing_prob: float = curing_prob
        self.resTime_min : int = resTime_min
        self.resTime_max : int = resTime_max
        self.epidemy_treshold : int = epidemy_treshold
        self.have_vacc : bool = False
        self.vacc_population : float = 0
        self.vacc_day : int = 0
    
    def add_vaccines( self, population : float, day : int ) -> None:
        self.have_vacc : bool = True
        self.vacc_population : float = population
        self.vacc_day : int = day

#endregion additional_classes


class Generation:

    #region Init

    def __init__( self,  gd : GenerationData ) -> None:
        self.__set_population_data(gd.generation_size)
        self.__set_curing_vars(gd.curing_time_min, gd.curing_time_max, gd.curing_prob, gd.resTime_min, gd.resTime_max)
        self.__set_epidemy_vars(gd.epidemy_treshold)
        self.__set_vaccines_vars( gd.have_vacc, gd.vacc_day, gd.vacc_population )
        self.__reset_timeline()

    def __set_population_data( self, generation_size : int ) -> None:
        self.generation_size : int = generation_size
        self.vulnerable_population : int = generation_size-1
        self.resistant_population : int = 0
        self.dead_population : int = 0
        self.infecting_population : int = 1
        self.deaths_threshold : float = 0.5
    
    def __set_curing_vars( self, curing_time_min : int, curing_time_max : int, curing_prob : float, resTime_min : int, resTime_max : int ) -> None:
        self.curing_prob : float = curing_prob
        self.curing_time_min : int = curing_time_min
        self.curing_time_max : int = curing_time_max
        self.resTime_min : int = resTime_min
        self.resTime_max : int = resTime_max
        self.__randomize_params()
    
    def __randomize_params(self) -> None:
        self.curing_time : int = np.random.randint(self.curing_time_min, self.curing_time_max + 1)
        self.resistant_time : int = np.random.randint(self.resTime_min, self.resTime_max + 1)

    def __set_epidemy_vars( self, epidemy_treshold : int ) -> None:
        self.epidemy_treshold : int = epidemy_treshold
    
    def __set_vaccines_vars( self, have_vacc : bool, vacc_day : int, vacc_population : float ):
        self.have_vacc = have_vacc
        self.vacc_day = vacc_day
        self.vacc_population = vacc_population
    
    def __reset_timeline( self ):
        self.epidemy_states : list[EpidemyState] = []
        self.infection_timeline : list[InfectionData] = [InfectionData(1, 0, self.curing_time)]
        self.resistance_timeline : list[InfectionData] = []
        self.path_positions : tuple[int, int] = None
        self.vaccines_timeline : InfectionData = None
        if self.have_vacc:
            self.vaccines_timeline = InfectionData(0,0,self.vacc_day, self.vacc_population)

    #endregion Init

    #region updateTimeline

    def update_timeline( self, generationNumber : int, new_infections : int ) -> None:
        to_remove : list[InfectionData] = []
        for i in self.infection_timeline:
            update_value = i.update(generationNumber)
            if update_value == -1:
                break
            self.__update_population(update_value, generationNumber)
            to_remove.append(i)
        
        for i in self.resistance_timeline:
            update_value = i.update(generationNumber)
            if update_value == -1:
                break
            self.__update_population_resistance(update_value)
            to_remove.append(i)
        
        for i in to_remove:
            if i in self.infection_timeline:
                self.infection_timeline.remove(i)
            else:
                self.resistance_timeline.remove(i)
        
        if self.vaccines_timeline != None:
            update_value = self.vaccines_timeline.update_percentage(generationNumber)
            if update_value >= 0:
                new_pop = int(self.vulnerable_population * update_value)
                self.resistant_population += new_pop
                self.vulnerable_population -= new_pop
                new_resistance = InfectionData(new_pop, generationNumber, self.resistant_time ) 
                self.__sort_value_into(new_resistance, is_infection_timeline=False)
                self.vaccines_timeline = None

        self.epidemy_states.append( self.__update_infection_state( new_infections ) )
        self.__randomize_params()
    
    def __update_infection_state( self, new_infections : int ) -> EpidemyState:
        if self.infecting_population == 0 and (self.dead_population / self.generation_size) < self.deaths_threshold:
            return EpidemyState.ENDED
        elif ( (self.dead_population / self.generation_size) >= self.deaths_threshold ) or ( ( new_infections / (self.generation_size - self.dead_population) ) > self.epidemy_treshold ) or ( self.vulnerable_population == 0 and self.infecting_population != 0 ):
            return EpidemyState.EPIDEMY
        
        return EpidemyState.STABLE
    
    def __update_population( self, update_value : int, generation_number : int ) -> None:
        self.infecting_population -= update_value
        res_val = int(update_value * self.curing_prob)
        self.resistant_population += res_val
        new_data = InfectionData(res_val, generation_number, self.resistant_time )
        self.__sort_value_into(new_data, is_infection_timeline=False)
        self.dead_population += update_value - res_val
    
    def __update_population_resistance( self, update_value : int ) -> None:
        self.vulnerable_population += update_value
        self.resistant_population -= update_value

    def __sort_value_into( self, newInfectionData : InfectionData, is_infection_timeline : bool = True ) -> None:
        if is_infection_timeline:
            if len(self.infection_timeline) == 0:
                self.infection_timeline.append(newInfectionData)
                return
            for index, val in enumerate( self.infection_timeline ):
                if val.final_timer() >= newInfectionData.final_timer():
                    self.infection_timeline.insert(index, newInfectionData)
                    return
            self.infection_timeline.append(newInfectionData)
        else:
            if len(self.resistance_timeline) == 0:
                self.resistance_timeline.append(newInfectionData)
                return
            for index, val in enumerate( self.resistance_timeline ):
                if val.final_timer() >= newInfectionData.final_timer():
                    self.resistance_timeline.insert(index, newInfectionData)
                    return
            self.resistance_timeline.append(newInfectionData)

    #endregion updateTimeline
    
    #region addInfectionInfo
    
    def add_infection_info( self, generation_number : int, new_dieses : int ) -> None:
        if self.vulnerable_population < new_dieses:
            new_dieses = self.vulnerable_population
        
        new_data =  InfectionData( new_dieses, generation_number, self.curing_time )
        self.__sort_value_into(new_data)
        self.vulnerable_population -= new_dieses
        self.infecting_population += new_dieses
        self.update_timeline(generation_number, new_dieses)

    def add_path( self, xy : tuple[ int, int ] ) -> None:
        self.path_positions = xy

    #endregion addInfectionInfo

    def get_dominating_state( self ) -> EpidemyState:
        if len(self.epidemy_states) == 0:
            return EpidemyState.STABLE

        if (self.dead_population / self.generation_size) >= self.deaths_threshold:
            return EpidemyState.EPIDEMY
        
        if self.epidemy_states[-1] == EpidemyState.ENDED:
            return EpidemyState.ENDED

        stable = 0
        epidemy = 0
        for i in self.epidemy_states:
            if i == EpidemyState.EPIDEMY:
                epidemy += 1
            else:
                stable += 1
        
        return EpidemyState.EPIDEMY if epidemy >= (stable / 2) else EpidemyState.STABLE