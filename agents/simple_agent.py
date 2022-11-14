from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
from pysc2.env.environment import StepType

import time

# Functions (Function/Operation IDs)
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id

# Features (used as indexes to the obs.observation list)
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SUPPLYDEPOT = 19
_TERRAN_SCV = 45

# Parameters
_PLAYER_SELF = 1
_NOT_QUEUED = [0]
_QUEUED = [1]

class SimpleAgent(base_agent.BaseAgent):
    # initial tracked flag values for decision making
    base_top_left = None
    supply_depot_built = False
    scv_selected = False
    barracks_built = False
    
    # helper method to transform relative player view for 64x64 map
    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]

        return [x + x_distance, y + y_distance]

    def step(self, obs):
        """
        Observes the game state and takes a step.
        Parameters
        --------------------
            obs  -- observations
                class: pysc2.env.environment.TimeStep
                keys: 
                    -- step_type    (StepType)
                    -- reward       (float)
                    -- discount     (float)
                    -- observation  (dict<str>)    
        Returns
        --------------------
            actions.FunctionCall(func_id, args) -- Next action to take
                    func_id: Store the function id
                    args: The list of arguments for that function, each being a list of ints.
        """
        super(SimpleAgent, self).step(obs)
        
        # TODO change this to check obs.observation every step and update the values
        if obs.step_type == StepType.FIRST:
            self.base_top_left = None
            self.supply_depot_built = False
            self.scv_selected = False
            self.barracks_built = False
            
        # time.sleep(0.5)
        
        # for 64x64 map, if player_x | player_y <= 64/2, then player base is top left of 64x64 map
        # otherwise the player base is bottom right of 64x64 map
        if self.base_top_left is None:
            player_y, player_x = (obs.observation["feature_minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = player_y.mean() <= 31

        # Checkes if Supply depot has been built
        # if Supply depot has not been built, then select SCV unit and build it
        if not self.supply_depot_built:
            if not self.scv_selected:
                unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()

                target = [unit_x[0], unit_y[0]]
                
                self.scv_selected = True
                
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                
                target = self.transformLocation(int(unit_x.mean()), 0, int(unit_y.mean()), 20)
                
                self.supply_depot_built = True
                
                return actions.FunctionCall(_BUILD_SUPPLYDEPOT, [_NOT_QUEUED, target])
        # Checkes if Barracks has been built
        # if Barracks has not been built, then select SCV unit and build it
        elif not self.barracks_built and _BUILD_BARRACKS in obs.observation["available_actions"]:
                unit_type = obs.observation["feature_screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()
                
                target = self.transformLocation(int(unit_x.mean()), 20, int(unit_y.mean()), 0)
                
                self.barracks_built = True
                
                return actions.FunctionCall(_BUILD_BARRACKS, [_NOT_QUEUED, target])
                
        return actions.FunctionCall(_NOOP, [])
