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

|![main file](/assets/images/personal-python-pygame/main_file.png)<em>main file start</em>|

|![main file op](/assets/images/personal-python-pygame/main_file_op.png)<em>file output</em>|

***

<strong>Creating a 'settings' file<strong>

***
To make things easier in the long term, I moved all customisation settings to a separate settings file. This will prevent adding of settings throughout the code

|![settings](/assets/images/personal-python-pygame/settings.png)<em>settings.py</em>|

|![main file refactored](/assets/images/personal-python-pygame/main_file_RE.png)<em>refactored code</em>|


***

<strong>Adding ship image<strong>

***

Using, LibreOffice-draw, I created a custom ship bit map file and inserted it into the screen. I used GIMP to convert the exported PDF file from LibreOffice-draw into a bit map file.

|![ship](/assets/images/personal-python-pygame/Ship.bmp)<br><em>the custom ship sprite</em>|







![WIP](/assets/images/common/WIP.png)