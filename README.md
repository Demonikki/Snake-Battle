# Creating and experimenting with multiple AI's performance using a 2-player Snake Battle.

## Credits for the game engine go to user Scriptim's [Snake-Battle](https://github.com/Scriptim/Snake-Battle) Project.


-----

# Snake Battle 

Play **Snake** with two players

## Play Game

- Player 1:
    - Turn left with `A`
    - Turn right with `D`
- Player 2:
    - Turn left with `LEFT ARROW`
    - Turn right with `RIGHT ARROW`
- Collect Food to grow
- You lose, when you touch your opponent or the window borders
- When both players "lose" at once, the longer snake will win

## Arguments

`$ python2.7 snakebattle.py --help`

    usage: snakebattle.py [-h] [-r] [-s PX] [-t X Y] [-d] [-f TPS] [-b MS]
    
    optional arguments:
      -h, --help            show this help message and exit
      -r, --raspi           run snake battle on a raspberry pi
      -s PX, --tilesize PX  the size of a tile
      -t X Y, --tiles X Y   the number of tiles
      -d, --debug           show debug information on the screen
      -f TPS, --fps TPS     framerate in ticks per second
      -b MS, --delay MS     button delay (raspi mode)
