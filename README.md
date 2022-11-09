# StarCraft 2 Resource Management Project

A StarCraft 2 AI Agent by Hassan Hage Hassan, Onariaginosa Igbinedion, Jason Kalili, and Yuepeng Liu to optimize resource management.

We are using [PySC2](https://github.com/deepmind/pysc2) as the foundation of this project.  

## Getting Started

### Install Python Libraries

Using python 3.10, create a virtual environment, and activate it.
Change the directory of the terminal/CMD to this folder
Run either of the following with the virtual env active:

```shell
pip install pysc2
```

or using pip with the requirements.txt

```shell
pip install -r requirements.txt
```

### Installing StarCraft 2

[PySC2](https://github.com/deepmind/pysc2) depends on the full StarCraft II game and only works with versions that include the API, which is 3.16.1 and above.

#### Linux

Follow Blizzard's [documentation](https://github.com/Blizzard/s2client-proto#downloads) to get the linux version. By default, PySC2 expects the game to live in `~/StarCraftII/`. You can override this path by setting the `SC2PATH` environment variable or creating your own run_config.

#### Windows/MacOS

Install of the game as normal from [Battle.net](https://battle.net). Even the [Starter Edition](http://battle.net/sc2/en/legacy-of-the-void/) will work. If you used the default install location PySC2 should find the latest binary. You will need to set the `SC2PATH` environment variable with the correct location. The default installation directory for Windows is `C:\Program Files (x86)\StarCraft II`.

### Get the maps

PySC2 has many maps pre-configured, but they need to be downloaded into the SC2 `Maps` directory before they can be played.

Download the [mini games](https://github.com/deepmind/pysc2/releases/download/v1.2/mini_games.zip) maps and extract them to your `StarCraftII/Maps/` directory.

## Useful Links

* [PySC2 GitHub Repo](https://github.com/deepmind/pysc2)
* [StarCraft II Paper](https://arxiv.org/abs/1708.04782)
* [PySC2 Tutorial GitHub](https://github.com/skjb/pysc2-tutorial)
* [PySC2 Tutorial Article by Chat Bots Life](https://chatbotslife.com/building-a-basic-pysc2-agent-b109cde1477c)
* [Steven Brown's Introduction to PySC2: Part 1](https://youtu.be/js79cmg2b2Q)
* [Siraj Raval's A Guide to DeepMind's StarCraft AI Environment](https://youtu.be/URWXG5jRB-A)
