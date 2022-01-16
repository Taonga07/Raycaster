# Raycaster Game
[![Pylint](https://github.com/Taonga07/Raycaster/actions/workflows/pylint.yml/badge.svg)](https://github.com/Taonga07/Raycaster/actions/workflows/pylint.yml)
[![Run on Repl.it](https://repl.it/badge/github/Taonga07/Raycaster)](https://repl.it/github/Taonga07/Raycaster)
![closed pullrequests](https://img.shields.io/github/issues-pr-closed-raw/taonga07/Raycaster)
![closed issues](https://img.shields.io/github/issues-closed-raw/Taonga07/Raycaster)
![open pull requets](https://img.shields.io/github/issues-pr/taonga07/Raycaster)
![activity](https://img.shields.io/github/commit-activity/y/taonga07/Raycaster)
![open issues](https://img.shields.io/github/issues-raw/Taonga07/Raycaster)

 This is a 3D game using pygame. Currently only shows a 3d image with pyplot but moving to pygame.
 For a list of features I Plan to add to the game see [here](https://github.com/Taonga07/Raycaster/projects/1):
 - [x] move to pygame
 - [ ] add movement
 - [ ] add z axis

jb notes
By colouring in the wall segments you can see why the image doesn't look quite right - when the raytracing transitions from a distant wall to a closer wall it doesn't draw the polygon to the next 'hidden' section of distant wall, it draws it to the next segment of closer wall, resulting in the apparent 'bowing' of walls as you walk towards a corner