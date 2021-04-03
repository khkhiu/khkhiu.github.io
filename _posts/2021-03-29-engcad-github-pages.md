---
title: "Engineering Academy and Github Pages, HTML,CSS and Jekyll"
date: "29-03-2021"
categories:
  - Engineering Academy
tags:
  - Engineering Academy
  - Singapore Polytechnic
  - HTML
  - Jekyll

---

***

Introductions

***

**Engineering Academy(EA)** Engineering Academy is a programme taken along with our diplomas that aims to further educate us on aspects of engineering through practical experiences. 
<cite><a href="https://www.sp.edu.sg/engineering-cluster/engineering-academy">SP - Engineering Academy</a></cite>  
{: .notice--info}


Along with Git and GitHub, we were also required to create a personal website that will act as a repository for both our school projects and personal projects. To achieve this, we were to use Github pages to host our site. Github pages allows users to host a webpage directly from their Github repositories, which along with the advantages mentioned <a href="https://khkhiu.github.io/engineering%20academy/engcad-github/"> here </a>, also allows us to use jekyll(This will be important later).

***

Learning

***

Despite having learnt about both HTML and CSS in my previous course, I have largely forgotten most of it(In my defence, I learnt it in 2014). As such I spend quite some time watching youtube videos and following along with the on screen examples.

I mainly watched the following 2 videos. <a href="https://www.youtube.com/watch?v=pQN-pnXPaVg"> HTML Full Course - Build a Website Tutorial </a> by <a href="https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ"> FreeCodeCamp.org </a> and <a href="https://www.youtube.com/watch?v=UB1O30fR-EE">HTML Crash Course For Absolute Beginners </a> by <a href="https://www.youtube.com/channel/UC29ju8bIPH5as8OGnQzwJyA"> Traversy Media </a>.

***

Implementation with HTML

***

After watching the videos, I started by creating a Repository in Github. I used the name 'khkhiu.github.io', set to public to create it as a github pages repo. I then pulled the repo onto my computer using GitHub Desktop  

| ![create repo](/assets/images/2021-03-29-engcad-github-pages/Create_repo.png)<em>creating the repo</em> | ![Git init](/assets/images/2021-03-29-engcad-github-pages/Github_init.png) <em>initialising repo</em> |

| ![update read me](/assets/images/2021-03-29-engcad-github-pages/Vscode-Readme.png)<em>Updating the README file</em> | ![Git_init](/assets/images/2021-03-29-engcad-github-pages/Github_1st_commit.png) <em>1st commit to git hub</em> |

Next, I created the following files. An index.html file to act as a landing page, an about.html page for basic information about me, an engcad.html page for school based projects and a personal.html page for personal projects. A styles.css page was also created to manage the CSS and an 'img' folder to contain images. The file were then pushed to github.

| ![local machine](/assets/images/2021-03-29-engcad-github-pages/Local_machine.png)<em>Local machine folder</em> | ![site uploaded](/assets/images/2021-03-29-engcad-github-pages/Update_github.png)<em>personal website taking shape</em> |

I first created a top navigation bar with my desired pages. I used the example in <a href = "https://www.w3schools.com/howto/howto_js_topnav.asp"> W3 school </a> to do so. I also took the opportunity to fill each page with unique dummy text to make identification easier. Lastly, I used the 'live server' extension in VScode to simulate the website live 

![local machine 2](/assets/images/2021-03-29-engcad-github-pages/Local_machine_design.png)<em>website on local machine running on live server</em> 


|![live server](/assets/images/2021-03-29-engcad-github-pages/liverserver.png)|<em>live server extension</em> |

Referencing <a href="https://www.w3schools.com/howto/howto_css_dropdown_navbar.asp">W3 school </a> again, I added  dropdown menu in the navigation bar. The rationale for the drop down menu is that I will be working on many different projects, hence a dropdown menu will allow a visitor to see what projects I have done at once. 

***

Implementation with Jekyll

***

***

Closing thoughts

***