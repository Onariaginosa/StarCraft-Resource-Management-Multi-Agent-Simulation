# NOTES

## Command notes

Running the simple_agent with map Simple64 with terran race
`python -m pysc2.bin.agent --map Simple64 --agent simple_agent.SimpleAgent --agent_race terran`

So the form is:
`python -m pysc2.bin.agent --map <MapName> --agent <PythonFilename>.<AgentClass> --agent_race <random|protoss|terran|zerg>`

Flags:
`--action_space`: <FEATURES|RGB|RAW>: Which action space to use. Needed if you take both feature and rgb observations.
`--agent`: Which agent to run, as a python path to an Agent class. (default: 'pysc2.agents.random_agent.RandomAgent')
`--agent2`: Second agent, either Bot or agent class. (default: 'Bot')
`--agent2_name`: Name of the agent in replays. Defaults to the class name.
`--agent2_race`: <random|protoss|terran|zerg>: Agent 2's race. (default: 'random')
`--agent_name`: Name of the agent in replays. Defaults to the class name.
`--agent_race`: <random|protoss|terran|zerg>: Agent 1's race. (default: 'random')
`--[no]battle_net_map`: Use the battle.net map version. (default: 'false')
`--bot_build`: <random|rush|timing|power|macro|air>: Bot's build strategy. (default: 'random')
`--difficulty`: <very_easy|easy|medium|medium_hard|hard|harder|very_hard|cheat_vision|cheat_money|cheat_insane>: If agent2 is a built-in Bot, it's strength. (default: 'very_easy')
`--[no]disable_fog`: Whether to disable Fog of War. (default: 'false')
`--feature_minimap_size`: Resolution for minimap feature layers. (default: '64,64')
`--feature_screen_size`: Resolution for screen feature layers. (default: '84,84')
`--game_steps_per_episode`: Game steps per episode. (an integer)
`--map`: Name of a map to use.
`--max_agent_steps`: Total agent steps. (default: '0') (an integer)
`--max_episodes`: Total episodes. (default: '0') (an integer)
`--parallel`: How many instances to run in parallel. (default: '1') (an integer)
`--[no]profile`: Whether to turn on code profiling. (default: 'false')
`--[no]render`: Whether to render with pygame. (default: 'true')
`--rgb_minimap_size`: Resolution for rendered minimap.
`--rgb_screen_size`: Resolution for rendered screen.
`--[no]save_replay`: Whether to save a replay at the end. (default: 'true')
`--step_mul`: Game steps per agent step. (default: '8') (an integer)
`--[no]trace`: Whether to trace the code execution. (default: 'false')
`--[no]use_feature_units`: Whether to include feature units. (default: 'false')
`--[no]use_raw_units`: Whether to include raw units. (default: 'false')

## obs.observations keys and stored types

single_select               `<array, shape=(0, 7), dtype=int32>`,
multi_select                `<array, shape=(0, 7), dtype=int32>`,
build_queue                 `<array, shape=(0, 7), dtype=int32>`,
cargo                       `<array, shape=(0, 7), dtype=int32>`,
production_queue            `<array, shape=(0, 2), dtype=int32>`,
last_actions                `<array, dtype=int32>`,
cargo_slots_available       `<array([0])>`,
home_race_requested         `<array([1])>`,
away_race_requested         `<array([4])>`,
map_name                    `<String>`,
feature_screen              `<NamedNumpyArray>`,
feature_minimap             `<NamedNumpyArray>`,
action_result               `<array, dtype=int32>`,
alerts                     `<array, dtype=int32>`,
game_loop                  `<array([0])>`,
score_cumulative           `<NamedNumpyArray>`,
score_by_category          `<NamedNumpyArray>`,
score_by_vital             `<NamedNumpyArray>`,
player                     `<NamedNumpyArray>`,
control_groups             `<array>`,
upgrades                   `<array, dtype=int32>`,
available_actions          `<array([0, 1, 2, 3, 4])>`
