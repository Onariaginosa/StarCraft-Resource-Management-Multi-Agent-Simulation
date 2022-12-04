from pysc2.agents import base_agent
from pysc2.lib.actions import FUNCTIONS, FunctionCall, ActionSpace
from pysc2.lib import features
from pysc2.lib.units import Terran, Neutral


# Functions (Function/Operation IDs)
_BUILD_BARRACKS = FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_REFINERY = FUNCTIONS.Build_Refinery_screen.id
_TRAIN_MARINE = FUNCTIONS.Train_Marine_quick.id
_RALLY_UNITS_MINIMAP = FUNCTIONS.Rally_Units_minimap.id
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

# Parameters
_PLAYER_SELF = features.PlayerRelative.SELF
_PLAYER_NEUTRAL = features.PlayerRelative.NEUTRAL  # beacon/minerals
_PLAYER_ENEMY = features.PlayerRelative.ENEMY
_NOT_QUEUED = [0]
_QUEUED = [1]
_SUPPLY_USED = 3
_SUPPLY_MAX = 4


class Agent(base_agent.BaseAgent):
    base_top_left = None
    supply_depot_built = False
    barracks_built = False
    refinery_built = False
    scv_selected = False
    barracks_selected = False
    barracks_rallied = False
    supply_depot_num = 0

    def __init__(self):
        super(Agent, self).__init__()

    def setup(self, obs_spec, action_spec):
        super(Agent, self).setup(obs_spec, action_spec)

    def reset(self):
        super(Agent, self).reset()
        self.base_top_left = None
        self.supply_depot_built = False
        self.barracks_built = False
        self.refinery_built = False
        self.scv_selected = False
        self.barracks_selected = False
        self.barracks_rallied = False
        self.supply_depot_num = 0

    # helper method to transform relative player view for 64x64 map
    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]
        return [x + x_distance, y + y_distance]

    def locate_base(self, obs):
        # To determine location of player's base on map
        # for 64x64 map, if player_x | player_y <= 64/2, then player base is top left of 64x64 map
        # otherwise the player base is bottom right of 64x64 map
        if self.base_top_left is None:
            player_y, player_x = (obs.observation["feature_minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = player_y.mean() <= 31



class BuildingAgent(Agent):

    def step(self, obs):
        super(BuildingAgent, self).step(obs)
        # sleep(1)

        if self.base_top_left is None:
            self.locate_base(obs)

        # Checkes if Supply depot has been built
        # if Supply depot has not been built, then select SCV unit and build it
        if not self.supply_depot_built:
            if not self.scv_selected:
                unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _SCV).nonzero()
                target = [unit_x[0], unit_y[0]]
                self.scv_selected = True
                self.barracks_selected = False
                return FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _COMMANDCENTER).nonzero()
                self.supply_depot_num += 1
                target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)
                self.supply_depot_built = True
                self.scv_selected = False
                return FunctionCall(_BUILD_SUPPLYDEPOT, [_NOT_QUEUED, target])

        # Checkes if Barracks has been built
        # if Barracks has not been built, then select SCV unit and build it
        elif not self.barracks_built and _BUILD_BARRACKS in obs.observation["available_actions"]:
            unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _COMMANDCENTER).nonzero()
            target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)
            self.barracks_built = True
            return FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])

        # elif not self.refinery_built and _BUILD_REFINERY in obs.observation["available_actions"]:
        #     unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
        #     unit_y, unit_x = (unit_type == Neutral.VespeneGeyser).nonzero()
        #     target = [int(unit_x.mean()), int(unit_y.mean())]
        #     self.refinery_built = True
        #     self.scv_selected = False
        #     return FunctionCall(_BUILD_REFINERY, [_NOT_QUEUED, target])

        return FunctionCall(_NOOP, [])



class ArmyAgent(BuildingAgent):

    def step(self, obs):
        base = super(ArmyAgent, self).step(obs)

        if base != FunctionCall(_NOOP, []):
            return base

        elif not self.barracks_rallied:
            if not self.barracks_selected:
                unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _BARRACKS).nonzero()
                if unit_y.any():
                    target = [int(unit_x.mean()), int(unit_y.mean())]
                    self.barracks_selected = True
                    self.scv_selected = False
                    return FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            else:
                self.barracks_rallied = True
                if self.base_top_left:
                    return FunctionCall(_RALLY_UNITS_MINIMAP, [_NOT_QUEUED, [29, 21]])
                return FunctionCall(_RALLY_UNITS_MINIMAP, [_NOT_QUEUED, [29, 46]])

        elif obs.observation["player"][_SUPPLY_USED] < obs.observation["player"][_SUPPLY_MAX] and _TRAIN_MARINE in obs.observation["available_actions"]:
            if not self.barracks_selected:
                unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _BARRACKS).nonzero()
                if unit_y.any():
                    target = [int(unit_x.mean()), int(unit_y.mean())]
                    self.barracks_selected = True
                    self.scv_selected = False
                    return FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            else:
                return FunctionCall(_TRAIN_MARINE, [_QUEUED])

        elif obs.observation["player"][_SUPPLY_USED] == obs.observation["player"][_SUPPLY_MAX]:
            if not self.scv_selected:
                if FUNCTIONS.select_idle_worker.id in obs.observation["available_actions"]:
                    self.scv_selected = True
                    self.barracks_selected = False
                    return FUNCTIONS.select_idle_worker("select", ActionSpace.FEATURES, _SCV)
            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _SUPPLYDEPOT).nonzero()
                xy_shifts = [(10,0), (0,10), (-10,0), (0,-10)]
                for (x,y) in xy_shifts:
                    self.supply_depot_num += 1
                    target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 0)
                    return FunctionCall(_BUILD_SUPPLYDEPOT, [_QUEUED, target])

        return FunctionCall(_NOOP, [])



# class AttackAgent(ArmyAgent):

#     def step(self, obs):
#         super(DefenceAgent, self).step(obs)

#         return FunctionCall(_NOOP, [])
