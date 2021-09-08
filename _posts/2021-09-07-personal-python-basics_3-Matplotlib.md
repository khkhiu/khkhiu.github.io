---
title: "Python Basics 3: Data visualisation in Python using Matplotlib"
date: "07-09-2021"
categories:
  - Learning process
tags:
  - Python
  - Pygame
  - Learning process

---

**Background information** I am using the book: <a href="https://nostarch.com/pythoncrashcourse2e">Python Crash Course, 2nd Edition</a> to teach myself the basics of python. This is a follow up post: <a href="https://khkhiu.github.io/learning%20process/personal-python-basics/"> Python Basics. </a>
{: .notice--info}


Python Crash Course is split into 2 parts. The first part covers the basics of python , which can be found <a href="https://khkhiu.github.io/learning%20process/personal-python-basics/"> here </a>. The second part consist of 3 projects.

1. Space shooter with pygame
2. Data Visualisation with Matplotlib and Plotly
3. Web Applications with Django

This post covers part 2 "Data Visualisation with Matplotlib and Plotly" For part 1: Space shooter with pygame, click <a href="https://khkhiu.github.io/learning%20process/personal-python-basics_2-pygame/"> here </a>

***

<strong>Plotting a simple line graph</strong>

***
A simple graph can be generated using a list along with the functions: "fig", "ax" and "subplot". Where "fig" is the entire figure or collection of plots that are generated, "ax" is a single plot in the figure and is the variable we’ll use most of the time, and "subplot" allows for generation one or more plots in the same figure. Lastly, the "plot()" method was used to plot the graph.

|![line graph code](/assets/images/LP-python-basics3-Data/line_graph_code.png)|
|<em>Code for simple line graph</em>|
|![line graph actual](/assets/images/LP-python-basics3-Data/line_graph_actual.png)|
|<em>Line graph actual</em>|

***

<strong>Changing the Label Type and Line Thickness</strong>

***
Next, the "linewidth" parameter, "set_" methods and "tick_params()" methods are used to customise the appearance of the graph.

|![customise graph code](/assets/images/LP-python-basics3-Data/custom_graph_code.png)|
|<em>Code for customising graph</em>|
|![Customised graph actual](/assets/images/LP-python-basics3-Data/custom_graph_actual.png)|
|<em>Customised graph actual</em>|


![WIP](/assets/images/common/WIP.png)