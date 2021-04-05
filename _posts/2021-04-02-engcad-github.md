---
title: "Engineering Academy and Github"
date: "02-04-2021"
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
<cite><a href="https://www.sp.edu.sg/engineering-cluster/engineering-academy">SP - Engineering Academy</a></cite>  
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

| Github Desktop| Git CLI |
| ----------- | ----------- |
|![Github Desktop](/assets/images/engcad-github/Github_blank.png)|![Git CLI](/assets/images/engcad-github/Git_CLI.png)|


I am aware that Git has a GUI interface, however Git GUI only allows us to create, clone and open repositories.

|![Git GUI](/assets/images/engcad-github/Git_GUI.png)|
|<em>Git GUI</em>|

The following table will go through the common functions of Git and GitHub desktop.

| Git Function| GitHub Desktop |
| ----------- | ----------- |
| <strong>Git init / clone </strong><br> Used to create or clone a repo | ![Git init](/assets/images/engcad-github/Github_desktop_setup.png)    |
| <strong>Git commit, Git push</strong><br> Used to track changes in the local repo, before committing and pushing to GitHub | ![Git init](/assets/images/engcad-github/Github_desktop_commit_readme.png) <em>Tracking changes made to local repo</em> <br> ![Git init](/assets/images/engcad-github/Github_desktop_push-readme.png)<em>Pushing changes to GitHub</em> |
| <strong>Git fetch, Git pull </strong><br> Used to check for new changes and pulling it to local repo | ![Git init](/assets/images/engcad-github/Github_fetch.png) <em>Fetching changes from GitHub</em> <br> ![Git init](/assets/images/engcad-github/Github_pull.png) <em>Pulling changes from GitHub</em> |

There is another aspect of GitHub called branches. Branches allow for users to build and test their code in a separate branch before committing to the master branch. This allows for bugs and issues to be resolved before publishing to 'production'.


| Explanation| Image |
| ----------- | ----------- |
| <strong>Testing branch </strong><br> A testing branch can be cloned from the master branch to do testing | ![Git init](/assets/images/engcad-github/Testing_branch_create.png)<em>creating testing branch</em> <br> ![Git init](/assets/images/engcad-github/Testing_branch_switch.png)<em>changes can be directly carried over to new branch</em> <br> ![Git init](/assets/images/engcad-github/Testing_Publish.png) <em>publishing testing branch</em>  |
| <strong>Choosing and merging branches </strong><br> Users can select which branch to push code to and which way branch merging can be made | ![Git init](/assets/images/engcad-github/Testing_branch_select.png)<em>selecting branches</em> <br> ![Git init](/assets/images/engcad-github/Testing_branch_merge.png) <em>merging branches</em>  |
| <strong>Pull request </strong><br> Users can create pull request to collaborate on proposed changes to the source code| ![Git init](/assets/images/engcad-github/Testing_branch_pull_request.png)<em>creating a pull request</em> <br> ![Git init](/assets/images/engcad-github/Github_create_pull_request.png) <em>creating a pull request on github</em> <br> ![Git init](/assets/images/engcad-github/Github_merge_pull_request.png) <em>merging pull request on github</em> <br> ![Git init](/assets/images/engcad-github/Github_merge_pull_request_confirm.png) <em>confirming merge of pull request on github</em>  |

Another collaboration tool is the issues tab on GitHub. This tab allows users to alert each other of issues in the code. It also allows to add comments and mark issues as resolved.

|![Github create issue](/assets/images/engcad-github/Create_issue.png)|![Github resolve issue](/assets/images/engcad-github/Create_issue_resolve.png)|
|<em>Issues tab</em>|
