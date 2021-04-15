---
title: "Space shooter game in Python using Pygame, part 2"
date: "15-04-2021"
categories:
  - Personal
tags:
  - Personal
  - Python
  - Pygame

---
For part 1 of the pygame project, where I implemented a ship that moves and shoot, click here: <a href="https://khkhiu.github.io/personal/personal-python-pygame-1/">Space shooter game in Python using Pygame, part 1</a>  

***

<strong>Review of project</strong>

***

After completing the player's space ship, we need to do the following:

1. Add a alien to the top of the screen with appropriate spacing

2. Using spacing of the first alien and overall screen size, write a loop to populate the top of the screen

3. Make the fleet move towards the player until one of the following happens. The entire alien fleet is shot down, in which case, spawn a new fleet. The alien fleet hits, the ground or player, then destroy the player ship, spawn a new player ship and fleet.

4. Limit number of ships player can use, end the game when supply is exhausted.

5. Refactor code as needed.

With this in mind, lets carry on.

***

<strong>Making an alien</strong>

***
To expedite this project(as I have more in the queue), I will not be making a custom alien, but rather be using the one provided by No Starch Press. A file: alien.py will also be created to control the alien's behaviour.

|![alien img](/assets/images/personal-python-pygame-pt2/alien.BMP)|
|<em>alien ship provided</em>|

|![alien file](/assets/images/personal-python-pygame-pt2/alien_file-1.png)|
|<em>alien.py</em>|

To ensure that the code was working properly, I imported the alien.py file to main game file(space_invaders.py).

|![alien img](/assets/images/personal-python-pygame-pt2/alien_file_import.png)|
|<em>Importing alien</em>|
|![alien img](/assets/images/personal-python-pygame-pt2/alien_file_init.png)|
|<em>updating initialise method</em>|

A method called _create_fleet() was made to hold the (eventual) fleet of aliens. In this method, one instance of Alien was made, then added to the group that will hold the fleet. The alien is the placed in the upper left of the screen. 

|![alien img](/assets/images/personal-python-pygame-pt2/alien_file_fleet.png)|
|<em>alien ship provided</em>|


To make the alien appear, I need to call the group’s draw() method to _update_screen(): When we call draw() on groups, Pygame draw elements of the group at positions defined by rect attributes. The draw() method
requires a surface to draw the elements from the group. 

|![alien update screen](/assets/images/personal-python-pygame-pt2/alien_update_screen.png)|
|<em>Adding alien to _update_screen()</em>|

|![1 alien op](/assets/images/personal-python-pygame-pt2/alien_file-1-op.png)|
|<em>Output of above code</em>|

***

<strong>Building the fleet</strong>

***

To build a fleet, I need to determine how many alien can fit across the screen. This is achieved by determining the horizontal spacing between aliens and forming a row. The vertical spacing is then determined to create the entire fleet

<strong>Aliens in a row</strong>

Screen width is stored in settings.screen_width. To ensure empty margins on both sides of the screen, I made the space available for aliens the screen width minus 2 alien widths. Spacing is also required between aliens, hence I made the spacing 1 alien width. Thus the space between an alien is 2 alien widths.

To actually add aliens in the code, I first pushed each alien right one alien width from the left margin. Second, I multiply the alien width by 2 to factor the space each alien takes up and empty space to their right. This value is then multiplied by the alien's position in the row, using the alien’s x attribute to set the position of its rect. Lastly, aliens are the added to the group alien

|![alien img](/assets/images/personal-python-pygame-pt2/alien_fleet_row.png)|
|<em>Code to implement alien in a row</em>|

|![alien img](/assets/images/personal-python-pygame-pt2/alien_fleet_row-OP.png)|
|<em>Alien in a row output</em>|

The method _create_fleet() was then refactored to making working with it easier.

|![refactored create fleet](/assets/images/personal-python-pygame-pt2/create_fleet_refactor.png)|
|<em>New _create_fleet() method</em>|

<strong>Adding columns</strong>

To build the fleet, I need to find the available vertical space by doing the following:

1. subtract the alien height from the top of the screen
2. subtract the ship height from the bottom of the screen
3. subtract 2 alien heights from the bottom

This will create some space above the ship, giving the player some time to start shotting at the aliens(which will be implemented later).

|![adding columns](/assets/images/personal-python-pygame-pt2/alien_fleet_file.png)|
|<em>New coded added</em>|

|![fleet op](/assets/images/personal-python-pygame-pt2/alien_fleet-op.png)|
|<em>Fleet created</em>|

***

<strong>Making the fleet move</strong>

***

In this segment, we will implement the following actions:
- The fleet move right across the screen until it hits the edge
- The fleet moves down slightly and changes direction after hitting the edge
- The movement continues until all aliens are shot down, hits the ship or hit the bottom of the screen

| Action     | code |
| ----------- | ----------- |
| Moving aliens right|![Moving aliens right setting](/assets/images/personal-python-pygame-pt2/move_right_setting.png)<br><em>adding settings</em><br>![Moving aliens right parameter](/assets/images/personal-python-pygame-pt2/move_right_alien.png)<br><em>new parameter to access the alien's speed</em><br>![Update alien](/assets/images/personal-python-pygame-pt2/move_right_SI-1.png)<br><em>call to update position of alien</em><br>![Update alien v1](/assets/images/personal-python-pygame-pt2/move_right_SI-2.png)<br><em>Updating alien position version 1</em>|

| Creating setting for fleet direction|![Moving aliens down](/assets/images/personal-python-pygame-pt2/fleet_direction_setting.png)<br><em>Making aliens move down</em>|

| Checking if alien has hit edge|![checking alien hit edge](/assets/images/personal-python-pygame-pt2/alien_hit_edge.png)<br><em>checking if alien hit edge in alien.py</em>|

| Moving fleet down and changing direction|![actual movement](/assets/images/personal-python-pygame-pt2/fleet_move_SI.png)<br><br>![actual movement 2](/assets/images/personal-python-pygame-pt2/fleet_move_SI-2.png)<br><em>Implementing movement and edge hit detection</em>|



![WIP](/assets/images/common/WIP.png)