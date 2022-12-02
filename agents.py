from pysc2.agents import base_agent
from pysc2.lib.actions import FUNCTIONS, FunctionCall
from pysc2.lib import features
from pysc2.lib.units import Terran, Neutral

from time import sleep


# Functions (Function/Operation IDs)
_BUILD_BARRACKS = FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_REFINERY = FUNCTIONS.Build_Refinery_screen.id
_TRAIN_MARINE = FUNCTIONS.Train_Marine_quick.id
_NOOP = FUNCTIONS.no_op.id
_SELECT_POINT = FUNCTIONS.select_point.id

# Features (used as indexes to the obs.observation list)
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_SELECTED = features.SCREEN_FEATURES.selected.index

# Unit IDs
_COMMANDCENTER = Terran.CommandCenter
_SCV = Terran.SCV
_SUPPLYDEPOT = Terran.SupplyDepot
_BARRACKS = Terran.Barracks
_REFINERY = Terran.Refinery
_BUILDINGS = {Terran.SupplyDepot:0,
             Terran.Barracks:0,
             Terran.Refinery:0}
_VESPENE = [Neutral.VespeneGeyser, Neutral.RichVespeneGeyser, Neutral.ShakurasVespeneGeyser, Neutral.PurifierVespeneGeyser]

# Parameters
_PLAYER_SELF = features.PlayerRelative.SELF
_PLAYER_NEUTRAL = features.PlayerRelative.NEUTRAL  # beacon/minerals
_PLAYER_ENEMY = features.PlayerRelative.ENEMY
_NOT_QUEUED = [0]
_QUEUED = [1]
# _MAP_SIZE = (X,Y)


class Agent(base_agent.BaseAgent):

    def __init__(self):
        super(Agent, self).__init__()
    
    def setup(self, obs_spec, action_spec):
        super(Agent, self).setup(obs_spec, action_spec)
        # self.locate_base()
        self.buildings = _BUILDINGS.copy()

    def reset(self):
        super(Agent, self).reset()
        self.supply_depot_built = False
        self.barracks_built = False
        self.refinery_built = False

    # helper method to transform relative player view for 64x64 map
    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]
        return [x + x_distance, y + y_distance]

    # def locate_base(self):
    #     # To determine location of player's base on map
    #     # for 64x64 map, if player_x | player_y <= 64/2, then player base is top left of 64x64 map
    #     # otherwise the player base is bottom right of 64x64 map
    #     if self.base_top_left is None:
    #         player_y, player_x = (self.obs_spec["feature_minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
    #         self.base_top_left = player_y.mean() <= 31



class BuildingAgent(Agent):

    def step(self, obs):
        super(BuildingAgent, self).step(obs)
        # sleep(1)
        
        if not self.supply_depot_built or not self.refinery_built or not self.barracks_built:
            unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _SCV).nonzero()
            target = [unit_x[0], unit_y[0]]
            return FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
        
        # Checkes if Supply depot has been built
        # if Supply depot has not been built, then select SCV unit and build it
        if not self.supply_depot_built and _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
            unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _COMMANDCENTER).nonzero()
            target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)
            self.supply_depot_built = True
            self.buildings[_SUPPLYDEPOT] += 1
            return FunctionCall(_BUILD_SUPPLYDEPOT, [_NOT_QUEUED, target])
            
        elif not self.refinery_built and _BUILD_REFINERY in obs.observation["available_actions"]:
            unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
            unit_y, unit_x = (unit_type in _VESPENE).nonzero()
            target = [unit_x[0], unit_y[0]]
            self.refinery_built = True
            self.buildings[_REFINERY] += 1
            return FunctionCall(_BUILD_REFINERY, [_NOT_QUEUED, target])
        
        # Checkes if Barracks has been built
        # if Barracks has not been built, then select SCV unit and build it
        elif not self.barracks_built and _BUILD_BARRACKS in obs.observation["available_actions"]:
            unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _COMMANDCENTER).nonzero()
            target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)
            self.barracks_built = True
            self.buildings[_BARRACKS] += 1
            return FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])
            
        return FunctionCall(_NOOP, [])



class DefenceAgent(Agent):

    def step(self, obs):
        super(DefenceAgent, self).step(obs)
        
        return FunctionCall(_NOOP, [])



class ArmyAgent(BuildingAgent):

    def step(self, obs):
        super(ArmyAgent, self).step(obs)
        
        return FunctionCall(_NOOP, [])
