---
title: "Space shooter game in Python using Pygame, part 2"
date: "10-04-2021"
categories:
  - Personal
tags:
  - Personal
  - Python
  - Pygame

---
For part 1 of the pygame project, where I implemented a ship that moves and shoot, click here: <a href="https://khkhiu.github.io/personal/personal-python-pygame-1/">Space shooter game in Python using Pygame, part 1</a>  

For this segment of the project, we will be adding the aliens for our space invader game. This will be achieved with the following steps:
1. Add rows of aliens that move downwards and sideways. The aliens must have appropriate spacing between them.

2. Generate a new fleet if all aliens are shot down 

3. If an alien hits the ground or the player's ship, destroy the ship and generate a new fleet

4. Limit the number of ship the play can use. End the game when all ships are used up

5. Refactor and refine code as needed

***

Creating the alien

***

![WIP](/assets/images/common/WIP.png)