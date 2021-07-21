---
title: "Space shooter game in Python using Pygame"
date: "07-04-2021"
categories:
  - Personal - Learning process
tags:
  - Personal
  - Python
  - Pygame
  - Learning process

---

**Background information** I am using the book: <a href="https://nostarch.com/pythoncrashcourse2e">Python Crash Course, 2nd Edition</a> to teach myself the basics of python. This is a follow up post: <a href="https://khkhiu.github.io/personal/personal-python-basics/"> Python Basics. </a>
{: .notice--info}


Python Crash Course is split into 2 parts. The first part covers the basics of python , which can be found <a href="https://khkhiu.github.io/personal/personal-python-basics/"> here </a>. The second part consist of 3 projects.

1. Space shooter with pygame
2. Data Visualisation with Matplotlib and Plotly
3. Web Applications with Django

Even though I am unlikely to go into game development, I am embarking on this project because I think it will be interesting (may or may not attempt a Tetris-esk game in the future, we will see).

***

<strong>Installing Pygame module</strong>

***
Using the command, <strong>python -m pip install --user pygame<strong> , the pygame module can be installed.

|![pygame install](/assets/images/personal-python-pygame/pygame_install.jpg)|
|<em>Updating my pip module, because I already installed the pygame module</em>|


***

<strong>Creating a window that responds to user input<br>(also setting background colour)<strong>

***

First order of business, setting the background. Using the code below, I did the following:
1. Imported pygame module and set the display size to 1200 by 800 pixels
2. Set background colour to white 
3. Exits the game if user click 'x' in the top right
4. Run the file, when file is called directly

|![main file](/assets/images/personal-python-pygame/main_file.png)|
|<em>main file start</em>|

|![main file op](/assets/images/personal-python-pygame/main_file_op.png)|
|<em>file output</em>|

***

<strong>Creating a 'settings' file<strong>

***
To make things easier in the long term, I moved all customisation settings to a separate settings file. This will prevent adding of settings throughout the code

|![settings](/assets/images/personal-python-pygame/settings.png)|
|<em>settings.py</em>|

|![main file refactored](/assets/images/personal-python-pygame/main_file_RE.png)|
|<em>refactored code</em>|


***

<strong>Adding ship image<strong>

***

Using, LibreOffice-draw, I created a custom ship bit map file and inserted it into the screen. I used GIMP to convert the exported PDF file from LibreOffice-draw into a bit map file.

|![ship](/assets/images/personal-python-pygame/Ship.bmp)|![ship default](/assets/images/personal-python-pygame/ship_default.bmp)|
|<em>the custom ship sprite VS original sprite</em>|

Using the following code, I inserted the sprite into screen.

|![ship file](/assets/images/personal-python-pygame/ship_file.png)|
|<em>ship.py</em>|
|![main file ship](/assets/images/personal-python-pygame/main_file_ship.png)|
|<em>refactored code with ship</em>|
|![main file ship output](/assets/images/personal-python-pygame/ship_file_op.png)|
|<em>ship output on screen</em>|

***

<strong>Refactoring code<br>check_events() and _update_screen() method<strong>

***

Refactoring code involves re-structuring code to make future support easier. For this case, I will be breaking the run_game() into 2 smaller helper methods. A helper method, indicated by 1 leading underscore, does work inside a class but is not meant to be called through an instance.

|![Refactored SpaceInvader class](/assets/images/personal-python-pygame/SI_refactor.png)|
|<em>refactoring code</em>|

***

<strong>Controlling the ship<strong>

***
Through the events in the following table, I implemented ship movement into the game.

| Action     | code |
| ----------- | ----------- |
| Responding to key press|![Right key press](/assets/images/personal-python-pygame/R_keypress.png)<br><em>ship moves right on key press</em>|
| Allowing continuous movement|![Continuous movement ship](/assets/images/personal-python-pygame/con_movement_ship_R.png)<br><em>updated ship code</em><br>![Continuous movement main](/assets/images/personal-python-pygame/con_movement_main_R.png)<br><em>updated _check_events code</em><br>![Continuous movement call](/assets/images/personal-python-pygame/con_movement_call.png)<br><em>updated while loop</em>|
|Moving left and right|![Adding left movement](/assets/images/personal-python-pygame/con_movement_ship_RL.png)<br><em>adding moving left</em><br>![Continuous movement main](/assets/images/personal-python-pygame/con_movement_main_RL.png)<br><em>new _check_events code</em>|
|Adjusting ship speed|![Ship speed](/assets/images/personal-python-pygame/R_keypress.png)<br><em>ship moves right on key press</em>|
| Changing speed ship|![Speed settings](/assets/images/personal-python-pygame/speed_setting.png)<br><em>increase speed to 1.5 pixel per loop pass</em><br>![Ship speed](/assets/images/personal-python-pygame/speed_ship.png)<br><em>adding speed setting to ship.py</em>|
| Limiting ship range|![Ship range](/assets/images/personal-python-pygame/range_ship.png)<br><em>prevents ships from going out out of bounds in ship.py</em>|
| Refactoring check events|![check event refactor](/assets/images/personal-python-pygame/check_event_refactor.png)<br><em>Refactoring check events in SpaceInvader.py. Also added exit on 'q' press</em>|

***

<strong>Shooting bullets<strong>

***

Through the events in the following table, I implemented bullets into the game.

|Updating settings.py to include bullets.|![bullet settings](/assets/images/personal-python-pygame/bullet_setting.png)<br><em>create 3 by 15 pixel dark grey bullets that travel slightly slower than the ship.</em>|

|Creating the bullet.py|![bullet.py](/assets/images/personal-python-pygame/bullet_file.png)|

Some notes regarding bullet.py. The bullet class inherits properties from pygame.sprite module. Sprites allow for grouping of related elements and acting on all of them at once. To make a bullet instance, the __init()__ uses the current instance of SpaceInvaders. The super() call is used to inherit properties from pygame.sprite. Other attributes of the bullet were also set.

|Make bullet appear moving|![bullet moving](/assets/images/personal-python-pygame/bullet_file_move.png)|

|Storing bullets in<br> group|![bullet main file](/assets/images/personal-python-pygame/bullet_file_grp.png)<em>added code in main file to manage bullets</em>|

|Firing bullets|![bullet main file](/assets/images/personal-python-pygame/bullet_file_grp.png)<em>added code in main file to manage bullets</em><br><br>![bullet import](/assets/images/personal-python-pygame/bullet_import.png)<br><em>importing bullet<br><br>![bullet update](/assets/images/personal-python-pygame/bullet_update.png)<br><em>bullet in main loop</em><br><br>![bullet fire](/assets/images/personal-python-pygame/bullet_input_space.png)<br><em>fire bullet with 'space'</em><br><br>![bullet fx](/assets/images/personal-python-pygame/bullet_fx.png)<br><em>bullet function</em><br><br>![bullet on screen](/assets/images/personal-python-pygame/bullet_screen.png)<br><em>bullet appears on screen</em><br><br>![bullet output](/assets/images/personal-python-pygame/bullet_op.png)<br><em><s>he he, ship goes pew pew</s> firing bullets</em><br>|

I did not implement limiting the number of bullets as stated in the book as I felt it was not needed.

***

<strong>Review of project thus far</strong>

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

|![alien img](/assets/images/personal-python-pygame/alien.BMP)|
|<em>alien ship provided</em>|

|![alien file](/assets/images/personal-python-pygame/alien_file-1.png)|
|<em>alien.py</em>|

To ensure that the code was working properly, I imported the alien.py file to main game file(space_invaders.py).

|![alien img](/assets/images/personal-python-pygame/alien_file_import.png)|
|<em>Importing alien</em>|
|![alien img](/assets/images/personal-python-pygame/alien_file_init.png)|
|<em>updating initialise method in Space_invaders.py</em>|

A method called _create_fleet() was made to hold the (eventual) fleet of aliens. In this method, one instance of Alien was made, then added to the group that will hold the fleet. The alien is the placed in the upper left of the screen. 

|![alien img](/assets/images/personal-python-pygame/alien_file_fleet.png)|
|<em>alien ship provided in Space_invaders.py</em>|


To make the alien appear, I need to call the group’s draw() method to _update_screen(): When we call draw() on groups, Pygame draw elements of the group at positions defined by rect attributes. The draw() method
requires a surface to draw the elements from the group. 

|![alien update screen](/assets/images/personal-python-pygame/alien_update_screen.png)|
|<em>Adding alien to _update_screen() in Space_invaders.py</em>|

|![1 alien op](/assets/images/personal-python-pygame/alien_file-1-op.png)|
|<em>Output of above code</em>|

***

<strong>Building the fleet</strong>

***

To build a fleet, I need to determine how many alien can fit across the screen. This is achieved by determining the horizontal spacing between aliens and forming a row. The vertical spacing is then determined to create the entire fleet

<strong>Aliens in a row</strong>

Screen width is stored in settings.screen_width. To ensure empty margins on both sides of the screen, I made the space available for aliens the screen width minus 2 alien widths. Spacing is also required between aliens, hence I made the spacing 1 alien width. Thus the space between an alien is 2 alien widths.

To actually add aliens in the code, I first pushed each alien right one alien width from the left margin. Second, I multiply the alien width by 2 to factor the space each alien takes up and empty space to their right. This value is then multiplied by the alien's position in the row, using the alien’s x attribute to set the position of its rect. Lastly, aliens are the added to the group alien

|![alien img](/assets/images/personal-python-pygame/alien_fleet_row.png)|
|<em>Code to implement alien in a row in Space_invaders.py</em>|

|![alien img](/assets/images/personal-python-pygame/alien_fleet_row-OP.png)|
|<em>Alien in a row output </em>|

The method _create_fleet() was then refactored to making working with it easier.

|![refactored create fleet](/assets/images/personal-python-pygame/create_fleet_refactor.png)|
|<em>New _create_fleet() method in Space_invaders.py</em>|

<strong>Adding columns</strong>

To build the fleet, I need to find the available vertical space by doing the following:

1. subtract the alien height from the top of the screen
2. subtract the ship height from the bottom of the screen
3. subtract 2 alien heights from the bottom

This will create some space above the ship, giving the player some time to start shotting at the aliens(which will be implemented later).

|![adding columns](/assets/images/personal-python-pygame/alien_fleet_file.png)|
|<em>New coded added to Space_invaders.py</em>|

|![fleet op](/assets/images/personal-python-pygame/alien_fleet-op.png)|
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
| Moving aliens right|![Moving aliens right setting](/assets/images/personal-python-pygame/move_right_setting.png)<br><em>adding settings</em><br>![Moving aliens right parameter](/assets/images/personal-python-pygame/move_right_alien.png)<br><em>new parameter to access the alien's speed in Space_invaders.py</em><br>![Update alien](/assets/images/personal-python-pygame/move_right_SI-1.png)<br><em>call to update position of alien in Space_invaders.py</em><br>![Update alien v1](/assets/images/personal-python-pygame/move_right_SI-2.png)<br><em>Updating alien position version 1 in Space_invaders.py</em>|

| Creating setting for fleet direction|![Moving aliens down](/assets/images/personal-python-pygame/fleet_direction_setting.png)<br><em>Making aliens move down in settings.py</em>|

| Checking if alien has hit edge|![checking alien hit edge](/assets/images/personal-python-pygame/alien_hit_edge.png)<br><em>checking if alien hit edge in alien.py</em>|

| Moving fleet down and changing direction|![actual movement](/assets/images/personal-python-pygame/fleet_move_SI.png)<br><br>![actual movement 2](/assets/images/personal-python-pygame/fleet_move_SI-2.png)<br><em>Implementing movement and edge hit detection in Space_invaders.py</em>|

***

<strong>Shooting aliens and making new fleet</strong>

***

| Action     | code |
| ----------- | ----------- |
|Detecting bullet collision<br>in Space_invaders.py|![Bullet collision](/assets/images/personal-python-pygame/bullet_collide.png)<br><em>Making bullets collide with aliens</em><br>![new fleet](/assets/images/personal-python-pygame/new_fleet.png)<br><em>Generating new fleet</em>|

***

<strong>Ending the game</strong>

***

| Action     | code |
| ----------- | ----------- |
|Detecting alien and ship collisions|![Alien ship collision](/assets/images/personal-python-pygame/alien_ship_collide.png)<br><em>detecting alien ship collision in Space_invaders.py</em>|
|Responding to alien ship collisions|![Collision respond](/assets/images/personal-python-pygame/GameStat.png)<br><em>New file to enable responds to collisions</em><br>|
|Limiting number of ships players have in setting.py|![lives](/assets/images/personal-python-pygame/ShipLimit.png)<br>|

|Adding GameStat to Space_invader.py|![import](/assets/images/personal-python-pygame/GameStat_import.png)<br><em>Importing GameStat</em><br>![score](/assets/images/personal-python-pygame/score.png)<br><em>Instance to store game stats</em><br>![ship hit method](/assets/images/personal-python-pygame/ship_hit.png)<br><br>![ship hit method](/assets/images/personal-python-pygame/ship_hit-2.png)<br><br>![ship hit method](/assets/images/personal-python-pygame/ship_hit-3.png)<br><em>consequence of ship hit</em>|


|Alien Reaching Bottom of screen in Space_invaders.py|![alien hit bottom](/assets/images/personal-python-pygame/alien_bottom.png)<br><br>![alien hit bottom 2](/assets/images/personal-python-pygame/alien_bottom-2.png)<br><em>Make game respond same way as when alien hits ship</em>|

|Game over|![Game over](/assets/images/personal-python-pygame/GameOver.png)<br><br>![Game over 2](/assets/images/personal-python-pygame/GameOver-2.png)<br><em>End game when player runs out of ship</em>|

|Identifying parts of game that should run|![Game over](/assets/images/personal-python-pygame/GameRun.png)<br><em>Some parts of the game should always run, while others only when the game is active</em>|

This conclude my attempts at trying to code a space invaders clone using Pygame. There is a part 3 where more functionalities are added. However, due to time constraints, I will not be delving into that. Stay tuned for more post in other subjects and technologies. 

The original source code can be found here: <a href="https://ehmatthes.github.io/pcc_2e/regular_index/">Python Crash Course, Second Edition</a>





