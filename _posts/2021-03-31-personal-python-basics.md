---
title: "Python Basics"
date: "31-03-2021"
categories:
  - Personal
tags:
  - Personal
  - Python
  - Legacy

---
**Legacy tag** Post containing the Legacy tag are projects that have been completed prior to the creation of this site. As such, aspects of the documentation may be incomplete   
{: .notice--warning}

For reasons that have been lost to time, I decided to start learning python. I learnt the basics of python using the book: Python Crash Course, 2nd edition by Eric Matthes, published by No Starch Press.

|![book](/assets/images/2021-03-31-personal-python-basics/pcc2e_cover.png)|
|<em>The book I used</em>|

Unlike other post, this post will be a summary of various checkpoints instead of a walk-through(mostly because python basics is 223 pages across 11 chapter and later chapters heavily utilize concepts in earlier chapters).

***

() VS [] VS {}<br>
Tuple vs list vs dictionary

***
In python , different bracket types are used for different purposes. Standard brackets () are used for tuples, solid brackets [] are used for list while curly brackets {} are used for dictionaries.Tuples are groups of items stored as a single variable that cannot be changed.  Lists, are groups of items stored as a single variable that can be changed. Dictionaries, store data in sets of key value pairs that can be changed, but keys do not allow duplicates.

|![py tuple](/assets/images/2021-03-31-personal-python-basics/tuple.png)|
|![py list](/assets/images/2021-03-31-personal-python-basics/list.png) |
|![py dictionary](/assets/images/2021-03-31-personal-python-basics/dictionary.png)|
|<em>tuple vs list vs dictionary</em>|

***

Functions (fx)

***

fx are block of code that do a specific job, which are called when needed.

|![simple fx](/assets/images/2021-03-31-personal-python-basics/fx/fx_simple.png)|![simple fx output](/assets/images/2021-03-31-personal-python-basics/fx/fx_simple_op.png)
|<em>simple hello world fx</em>|

What I have learnt is demonstrated in the table below:

| Action    | image |
| ----------- | ----------- |
| <strong>Passing information to fx</strong> <br>same fx as simple hello world fx | ![info to fx](/assets/images/2021-03-31-personal-python-basics/fx/fx_simple_info.png)<br><br>![info to fx op](/assets/images/2021-03-31-personal-python-basics/fx/fx_simple_op.png) |

| <strong>Positional arguments <br> with multiple fx calls</strong> <br> Python matches each argument <br> in the fx call with a parameter <br> in the fx definition.| ![fx positional argument](/assets/images/2021-03-31-personal-python-basics/fx/fx_posi.png)<br><br>![fx positional argument op](/assets/images/2021-03-31-personal-python-basics/fx/fx_posi_op.png)      |

| <strong>Default values in fx</strong> <br> Default values can be assigned <br> when making fx.  | ![fx default val](/assets/images/2021-03-31-personal-python-basics/fx/fx_default.png)<br><br>![fx default val op](/assets/images/2021-03-31-personal-python-basics/fx/fx_default_op.png)      |

| <strong>Returning a value</strong> <br> The return command <br> takes a value from an fx and passes <br> it to the fx call  | ![fx default val](/assets/images/2021-03-31-personal-python-basics/fx/fx_return_val.png)<br><br>![fx default val op ](/assets/images/2021-03-31-personal-python-basics/fx/fx_return_val_op.png)<br><br>![fx return val 2](/assets/images/2021-03-31-personal-python-basics/fx/fx_return_val2.png)<br><em>making an argument optional</em><br><br>![fx return val op 2](/assets/images/2021-03-31-personal-python-basics/fx/fx_return_val2_op.png)  |

| <strong>Returning a dictionary</strong> <br> Dictionaries can be returned with FX  | ![fx return dictionary](/assets/images/2021-03-31-personal-python-basics/fx/fx_dictionary.png)<br><br>![fx return dictionary op](/assets/images/2021-03-31-personal-python-basics/fx/fx_dictionary_op.png)  |

| <strong>while loop in fx</strong> <br>Using a while loop in fx then prints| ![fx while](/assets/images/2021-03-31-personal-python-basics/fx/fx_while.png)<br><em>allows users to enter their name and formats it</em> |

| <strong>Passing a list</strong> <br> Defining a list then passing to fx  | ![fx past list](/assets/images/2021-03-31-personal-python-basics/fx/fx_list.png)<br><br>![fx past list op](/assets/images/2021-03-31-personal-python-basics/fx/fx_list_op.png)  |

| <strong>Modding a list</strong> <br> List can be modified by passing <br> arguments changes are <br> permanent unless modified again | ![fx mod list](/assets/images/2021-03-31-personal-python-basics/fx/fx_mod_list.png)<br><br>![fx mod list op](/assets/images/2021-03-31-personal-python-basics/fx/fx_mod_list_op.png)  |

| <strong>Passing X number <br> of arguments</strong> <br> Use * when declaring a <br>fx to pack an<br> undeclared number of fx into a tuple | ![fx x arg](/assets/images/2021-03-31-personal-python-basics/fx/fx_x_arg.png)<br><br>![fx x,positional arg](/assets/images/2021-03-31-personal-python-basics/fx/fx_x_arg2.png) <br><em>Combining positional and arbitrary arguments</em><br><br>![fx mod list op](/assets/images/2021-03-31-personal-python-basics/fx/fx_x_arg_op.png) |

| <strong>Passing X keyword <br> arguments</strong> <br> Use ** write to fx that accepts<br> as many key-value pairs as provided | ![fx x key](/assets/images/2021-03-31-personal-python-basics/fx/fx_y_arg.png)<br><br>![fx x key op](/assets/images/2021-03-31-personal-python-basics/fx/fx_y_arg_op.png) |


| <strong>Passing X keyword <br> arguments</strong> <br> Use ** write to fx that accepts<br> as many key-value pairs as provided | ![fx x key](/assets/images/2021-03-31-personal-python-basics/fx/fx_y_arg.png)<br><br>![fx x key op](/assets/images/2021-03-31-personal-python-basics/fx/fx_y_arg_op.png) |

| <strong>Importing module <br> arguments</strong> <br> Use import command <br> to import fx to other files. | ![fx import from](/assets/images/2021-03-31-personal-python-basics/fx/fx_import.png)<br><br>![fx import to](/assets/images/2021-03-31-personal-python-basics/fx/fx_import2.png)<br><br>![fx import op](/assets/images/2021-03-31-personal-python-basics/fx/fx_import_op.png) |

***

Classes

***

Classes is part of the object oriented programing paradigm where classes define general operations for an entire category of objects.Creating objects from classes is called instantiation as we work with instances of a class.

What I have learnt is demonstrated in the table below:

| Action    | image |
| ----------- | ----------- |
|<strong>Creating classes</strong>|![create class](/assets/images/2021-03-31-personal-python-basics/class/class_create.png)<br><br>![create class op](/assets/images/2021-03-31-personal-python-basics/class/class_create_op.png)|

|Classes need to be explicitly define, all classes need a __init__ method to be initialised. All method in classes need a self argument, which is a reference to itself. The method will automatically pass the self argument when python calls the method.|




![WIP](/assets/images/common/WIP.png)

For my first projects, click here: <a href="https://khkhiu.github.io/personal/personal-python-pygame/">Space shooter game in Python using Pygame, part 1 </a>
