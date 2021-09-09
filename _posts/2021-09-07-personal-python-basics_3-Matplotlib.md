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

<strong>Changing the Label Type and Line Thickness</strong>

Next, the "linewidth" parameter, "set_" methods and "tick_params()" methods are used to customise the appearance of the graph. Where "tick_params()" is used to style tick marks.

|![customise graph code](/assets/images/LP-python-basics3-Data/custom_graph_code.png)|
|<em>Code for customising graph</em>|
|![customised graph actual](/assets/images/LP-python-basics3-Data/custom_graph_actual.png)|
|<em>Customised graph actual</em>|

<strong>Adjusting the plot</strong>

Code is now added to correct the plot of the graph so that the Y-axis value is the square value of th X-axis value.

|![correcting graph code](/assets/images/LP-python-basics3-Data/correct_graph_code.png)|
|<em>Code for correcting graph</em>|
|![correcting  graph actual](/assets/images/LP-python-basics3-Data/correct_graph_actual.png)|
|<em>Corrected graph actual</em>|

<strong>Using Built-in Styles</strong>

Built in styles are now added to improve readability of the graph.

|![Built-in Styles graph code](/assets/images/LP-python-basics3-Data/Built-in_graph_code.png)|
|<em>Code for built-in styles</em>|
|![Built-in Styles graph actual](/assets/images/LP-python-basics3-Data/Built-in_graph_actual.png)|
|<em>graph actual</em>|

***

<strong>Scatter plot</strong>

***

Using ".scatter" a scatter plot can be created.

|![scatter plot code](/assets/images/LP-python-basics3-Data/scatter_plot_code.png)|
|<em>Code for scatter plot</em>|
|![scatter plot actual](/assets/images/LP-python-basics3-Data/scatter_plot_actual.png)|
|<em>Scatter plot actual(only one point for now)</em>|

Similar to the line graph, scatter plots can be customised to improve readability. More points were also added at this point

|![custom scatter plot code](/assets/images/LP-python-basics3-Data/custom_scatter_plot_code.png)|
|<em>Code for customised scatter plot</em>|
|![custom scatter plot actual](/assets/images/LP-python-basics3-Data/custom_scatter_plot_actual.png)|
|<em>Customised scatter plot actual</em>|

<strong>Calculation of data</strong>

Here, i will use a loop to automatically calculate and plot points, colours were also added at this point

|![calculated scatter plot code](/assets/images/LP-python-basics3-Data/cal_scatter_plot_code.png)|
|<em>Code for calculated scatter plot</em>|
|![calculated scatter plot actual](/assets/images/LP-python-basics3-Data/cal_scatter_plot_actual.png)|
|<em>calculated scatter plot actual</em>|

<strong>Colour maps</strong>
Colour maps is a series of colours in a gradient that moves from a starting colour to another. Colour maps are used to display a pattern in the visualised data.

|![colour map scatter plot code](/assets/images/LP-python-basics3-Data/ColMap_scatter_plot_code.png)|
|<em>Code for scatter plot with colour map</em>|
|![colour map scatter plot actual](/assets/images/LP-python-basics3-Data/ColMap_scatter_plot_actual.png)|
|<em>Scatter plot with colour map actual</em>|

***

<strong>Random number generator</strong>

***
For this exercise, the "random" module will be used to create data from random walk and use a graph to represent the generated numbers.

|![Random walk class code](/assets/images/LP-python-basics3-Data/RandonWalk_class.png)|
|<em>Code for random walk class</em>|
|![Random walk plot code](/assets/images/LP-python-basics3-Data/RandonWalk_plot.png)|
|<em>Code for random walk plot</em>|
|![Random walk plot actual](/assets/images/LP-python-basics3-Data/RandonWalk_actual.png)|
|<em>Random walk with 5000 points</em>|

<strong>Making multiple random walks and styling</strong>

To make it so that the program does not have to be constantly restarted, code is added to generate multiple random walks.

|![multi random walk plot code](/assets/images/LP-python-basics3-Data/RandonWalk_plot-multi.png)|
|<em>Code for generating multiple random walk plots</em>|

<strong>Styling plots</strong>

Plots should be styled to emphasize important elements while de-emphasizing unimportant elements

1. Colouring

Colour maps are used to shown the order of points in the walk, while removing black outlines from each dot

|![colour random walk plot code](/assets/images/LP-python-basics3-Data/RandonWalk_plot_-colour_code.png)|
|<em>Code for colouring random walk plot</em>|
|![colour random walk plot actual](/assets/images/LP-python-basics3-Data/RandonWalk_plot_-colour_actual.png)|
|<em>Coloured random walk plot</em>|

2. Specifying starting and ending point

Self explanatory, done by emphasizing the first and last generated points

|![StartEnd random walk plot code](/assets/images/LP-python-basics3-Data/RandonWalk_plot_-StartEnd_code.png)|
|<em>Code for specifying starting and ending point on random walk plot</em>|
|![StartEnd  random walk plot actual](/assets/images/LP-python-basics3-Data/RandonWalk_plot_-StartEnd_actual.png)|
|<em>Random walk plot with green starting point and red ending point</em>|

3. Cleaning axes and adding plot points

The axes are now hidden to prevent them from distracting from the path of each walk, the number of steps are also increased to 50,000.

|![Step3 random walk plot code](/assets/images/LP-python-basics3-Data/RandonWalk_plot_step3_code.png)|
|<em>Code for cleaning axes and adding plot points on random walk plot</em>|
|![Step3 random walk plot actual](/assets/images/LP-python-basics3-Data/RandonWalk_plot_step3_actual.png)|
|<em>Random walk plot with green starting point and red ending point, cleaned axes and new plot points</em>|

***

<strong>Dice rolling</strong>

***


![WIP](/assets/images/common/WIP.png)