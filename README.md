CHEKMO-II
=========

Binary + UCI adapter
--------------------

This is the setup needed for playing a classical 1970s chess program CHEKMO-II on modern computers.
It will be useful for those who are interested in computer chess history.
CHEKMO-II was created for [PDP-8](https://en.wikipedia.org/wiki/PDP-8) computers by Digital Equipment Corporation instructor John E. Comeau. For detailed learning of programs's internal structure, see [original PAL-8 source code](http://pop.aconit.org/Programs/StandAlone/chekmo.lst), written in PAL-8, PDP-8 assembly.

### Running in simulator

You will need to install [SIMH](http://simh.trailing-edge.com), an archaic computers simulator.

On Mac, this can be done using brew:

```bash
brew install simh
```

On Ubuntu and other Debian-based Linux distributions, you can use apt:

```bash
sudo apt-get install simh
```

To run CHEKMO-II use the ``run`` script at the root of this repository:

```bash
./run
```

![](img/simh.png?raw=true)

To get to know the program's command set and other useful information, see the original user manual [chekmo.pdf](chekmo.pdf?raw=true).

### Using the UCI adapter

You can use any chess graphic interface program, that supports [Universal Chess Interface](https://chessprogramming.wikispaces.com/UCI). Set `chekmo-uci.py` as the chess engine executable to do that.

For example, in [XBoard](https://www.gnu.org/software/xboard/), set up the engine with Menu – Engine – Edit Engine List. Append the following string to the list:

```
"CHEKMO-2" -fcp "./chekmo-uci.py" -fd "/path/to/cloned/repo/" -fUCI
```

On Debian/Ubuntu you may will need to install `polyglot` manually:

```bash
sudo apt-get install polyglot
```

Now you can play against CHEKMO-II via graphic interface.

![](img/xboard.png?raw=true)

Using UCI clients, you can make CHEKMO-II to play against modern engines.

Example of CHEKMO-II, playing against the modern Fairy-Max engine:

![](img/vs.png?raw=true)
