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
|![Built-in Styles  graph actual](/assets/images/LP-python-basics3-Data/Built-in_graph_actual.png)|
|<em>graph actual</em>|

***

<strong>Scatter plot</strong>

***
Using ".scatter" a scatter plot can be created.

|![scatter plot code](/assets/images/LP-python-basics3-Data/scatter_plot_code.png)|
|<em>Code for scatter plot</em>|
|![scatter plot  actual](/assets/images/LP-python-basics3-Data/scatter_plot_actual.png)|
|<em>Scatter plot actual(only one point for now)</em>|

Similar to the line graph, scatter plots can be customised to improve readability. More points were also added at this point

|![custom scatter plot code](/assets/images/LP-python-basics3-Data/custom_scatter_plot_code.png)|
|<em>Code for customised scatter plot</em>|
|![custom scatter plot  actual](/assets/images/LP-python-basics3-Data/custom_scatter_plot_actual.png)|
|<em>Customised scatter plot actual</em>|


![WIP](/assets/images/common/WIP.png)