---
title: "Engineering Academy and Github"
date: "29-03-2021"
categories:
  - Engineering Academy
tags:
  - Engineering Academy
  - Singapore Polytechnic
  - Github

---

***

Introductions

***

**Engineering Academy(EA)** Engineering Academy is a programme taken along with our diplomas that aims to further educate us on aspects of engineering through practical experiences. 
<cite><a href="https://www.sp.edu.sg/engineering-cluster/engineering-academy">SP - Engineering Academy/</a></cite>  
{: .notice--info}

As part of our introduction to Engineering Academy we were introduced to Git and github. There are several reasons for this introduction.

1. It introduces us to a tool that is commonly used in both professional and hobbyist circles
2. It allows us to easily store and retrieve our projects from any device
3. It allows us to easily collaborate with each other

**Git** Git is a free and open source(FOSS) version control software that allows for seamless branching and merging of source code.
<cite><a href="https://git-scm.com/">git-scm.com/</a></cite>
{: .notice--info}

**GitHub** GitHub is is a website used for software development that allows for version control using Git.
<cite><a href="https://github.com">github.com</a></cite>
{: .notice--info}

Fortunately, I have previous experience using Github and as such am writing this post for posterity.

***

Workflow - Windows 10

***
For windows 10, I will be using Github Desktop. Github desktop is a programme that allows the user to use a graphical user interface(GUI) to perform version control instead of using the command line interface(CLI)

|![Github Desktop](/assets/images/2021-03-29-engcad-github/Github_blank.png)|![Git CLI](/assets/images/2021-03-29-engcad-github/Git_CLI.png)|
|<em>Github Desktop vs Git CLI</em>|

I am aware that Git has a GUI interface, however Git GUI only allows us to create, clone and open repositories.

|![Git GUI](/assets/images/2021-03-29-engcad-github/Git_GUI.png)|
|<em>Git GUI</em>|

| Git Function| GitHub Desktop |
| ----------- | ----------- |

| <strong>Git init / clone </strong><br> Used to create or clone a repo | ![Git init](/assets/images/2021-03-29-engcad-github/Github_desktop_setup.png)    |

| <strong>Git commit, Git push</strong><br> Used to track changes in the local repo, before committing and pushing to GitHub | ![Git init](/assets/images/2021-03-29-engcad-github/Github_desktop_commit_readme.png) <em>Tracking changes made to local repo</em> <br> ![Git init](/assets/images/2021-03-29-engcad-github/Github_desktop_push-readme.png)<em>Pushing changes to GitHub</em> |

| <strong>Git fetch, Git pull </strong><br> Used to check for new changes and pulling it to local repo | ![Git init](/assets/images/2021-03-29-engcad-github/Github_fetch.png) <em>Fetching changes from GitHub</em> <br> ![Git init](/assets/images/2021-03-29-engcad-github/Github_pull.png) <em>Pulling changes from GitHub</em> |

There is another aspect of GitHub called branches. Branches allow for users to build and test their code in a separate branch before committing to the master branch. This allows for bugs and issues to be resolved before publishing to 'production'.



| <strong>Testing branch </strong><br> A testing branch can be cloned from the master branch to do testing | ![Git init](/assets/images/2021-03-29-engcad-github/Testing_branch.png) <br> ![Git init](/assets/images/2021-03-29-engcad-github/Testing_Publish.png) <em>publishing testing branch</em>  |



***

Workflow - Linux

***
Use command line
Fedora 33, at the time of this post, is the latest version

![WIP](/assets/images/bios/WIP.png)

***

Workflow - FreeBSD and similar

***

You can do it! I believe in you!
