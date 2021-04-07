---
title: "Space shooter game in Python using Pygame, part 1"
date: "31-03-2021"
categories:
  - Personal
tags:
  - Personal
  - Python
  - Pygame

---
**Legacy tag** Post containing the Legacy tag are projects that have been completed prior to the creation of this site. As such, I have attempted to recreate the events to the best of my abilities.   
{: .notice--warning}

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

![pygame install](/assets/images/common/Placeholder.png)

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

|Storing bullets in group|![bullet main file](/assets/images/personal-python-pygame/bullet_file_main.png)|
|<em>added code in main file to manage bullets</em>|



<s>he he, ship goes pew pew</s>

![WIP](/assets/images/common/WIP.png)