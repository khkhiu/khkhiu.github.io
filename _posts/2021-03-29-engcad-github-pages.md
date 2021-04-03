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

| ![create repo](/assets/images/2021-03-29-engcad-github-pages/HTML/Create_repo.png)<em>creating the repo</em> | ![Git init](/assets/images/2021-03-29-engcad-github-pages/HTML/Github_init.png) <em>initialising repo</em> |

| ![update read me](/assets/images/2021-03-29-engcad-github-pages/HTML/Vscode-Readme.png)<em>Updating the README file</em> | ![Git_init](/assets/images/2021-03-29-engcad-github-pages/HTML/Github_1st_commit.png) <em>1st commit to git hub</em> |

Next, I created the following files. An index.html file to act as a landing page, an about.html page for basic information about me, an engcad.html page for school based projects and a personal.html page for personal projects. A styles.css page was also created to manage the CSS and an 'img' folder to contain images. The file were then pushed to github.

| ![local machine](/assets/images/2021-03-29-engcad-github-pages/HTML/Local_machine.png)<em>Local machine folder</em> |
| ![push to github](/assets/images/2021-03-29-engcad-github-pages/HTML/Upload_local_machine.png)<em>personal website taking shape</em> |
| ![site uploaded](/assets/images/2021-03-29-engcad-github-pages/HTML/Update_github.png)<em>personal website taking shape</em> |

I first created a top navigation bar with my desired pages. I used the example in <a href = "https://www.w3schools.com/howto/howto_js_topnav.asp"> W3 school </a> to do so. I also took the opportunity to fill each page with unique dummy text to make identification easier. Lastly, I used the 'live server' extension in VScode to simulate the website live 

![local machine 2](/assets/images/2021-03-29-engcad-github-pages/HTML/Local_machine_design.png)<em>website on local machine running on live server</em> 


|![live server](/assets/images/2021-03-29-engcad-github-pages/HTML/liverserver.png)|<em>live server extension</em> |

Referencing <a href="https://www.w3schools.com/howto/howto_css_dropdown_navbar.asp">W3 school </a> again, I added  dropdown menu in the navigation bar. The rationale for the drop down menu is that I will be working on many different projects, hence a dropdown menu will allow a visitor to see what projects I have done at once. 

| ![dropdown code](/assets/images/2021-03-29-engcad-github-pages/HTML/Local_machine_design2_code.png)<em>code inspired by W3</em> | ![dropdown site](/assets/images/2021-03-29-engcad-github-pages/HTML/Local_machine_design2.png) <em>Site in action</em> |

I then refactored both the HTML and CSS to allow for both 'EngCad' and 'Projects' to have their individual dropdown menus. Simultaneously, the 'about' and 'index' page buttons were altered to have a unified appearance.

| ![refactor HTML](/assets/images/2021-03-29-engcad-github-pages/HTML/refactored_HTML.png)<em>refactoring HTML</em> | ![refactor CSS](/assets/images/2021-03-29-engcad-github-pages/HTML/refactored_CSS.png) <em>refactoring CSS</em> |

![drop down](/assets/images/2021-03-29-engcad-github-pages/HTML/Local_machine_design_drop.png) <em>Drop down design complete</em>

I also used font-awesome to add GitHub and Linkedin icons.

| ![awesome font](/assets/images/2021-03-29-engcad-github-pages/HTML/fa_icons.png)<em>adding awesome font</em> | ![icons](/assets/images/2021-03-29-engcad-github-pages/HTML/Local_machine_design_icons.png) <em>icons added</em> |

However, despite my progress, I realised that I have spend about 3 hours on my website and I have just barely started. Hence, I decided to look into Jekyll to expedite my progress.


***

Implementation with Jekyll

***

According to <a href="https://pages.github.com/">github-pages</a> and the <a href="https://jekyllrb.com/">official site</a>, jekyll is program that will generate a site for me. Thus letting me focus on the content without having to worry about managing my site.

| ![github pages jekyll](/assets/images/2021-03-29-engcad-github-pages/Jekyll/github_jekyll.png) | ![jekyll site](/assets/images/2021-03-29-engcad-github-pages/Jekyll/jekyll_site.png) |


***

Closing thoughts

***