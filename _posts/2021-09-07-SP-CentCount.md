---
title: "Singapore Polytechnic - Centroid Counter using OpenCV in Python"
date: "07-09-2021"
categories:
  - Project
tags:
  - Singapore Polytechnic
  - Python
  - OpenCV

---

**Link to github:**
<cite><a href="https://github.com/khkhiu/Singapore_Polytechnic-Centroid_Counter">https://github.com/khkhiu/Singapore_Polytechnic-Centroid_Counter</a></cite>
{: .notice--info}

***

<strong>Introduction</strong>

***
The aim of the project is to develop a simple algorithm to count the number of people in the room. This algorithm was part of a bigger project, for <cite><a href="https://www.sp.edu.sg/engineering-cluster/eee/engineering-academy/the-programme">the Engineering Academy Programme</a></cite> but his post will only focus on the algorithm.

***

<strong>The team</strong>

***
The following are members of the team(As of 7 Sep 2021)

1. Khiu Kim Hong, Diploma in Electrical and Electronic Engineering
2. Cheam Zhi Kai, Diploma in Engineering with Business
3. Ang Yong En, Diploma in Computer Engineering
4. Chan Qing Yi, Diploma in Mechanical Engineering
5. Ngo Bing Han, Diploma in Electrical and Electronic Engineering

***

<strong>Solution</strong>

***
**OpenCV** OpenCV is an open source computer vision and machine learning software library.
<cite><a href="https://opencv.org/about/">opencv.org/about/</a></cite>
{: .notice--info}

Using OpenCV and python, the team achieved the aim by counting centroids. The way we ‘count’ the number of people in the room is to detect centroids moving pass a given threshold. A centroid is created and given and ID number when moving is detected. If the centroid moves past the ‘entry’ threshold, the program considers it as a person entering the room. Similarly, if a centroid moves past the ‘exit’ threshold, the program considers it as a person leaving the room.

If movement is detected near an existing centroid, that centroid is reused instead of making a new one.


***

<strong>Video demonstration</strong>

***

<iframe width="560" height="315" src="https://www.youtube.com/embed/nILaMWWoH28" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>