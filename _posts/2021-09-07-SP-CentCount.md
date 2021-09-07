---
title: "Singapore Polytechnic - Centroid Counter"
date: "07-09-2021"
categories:
  - Project
tags:
  - Singapore Polytechnic
  - Python
  - OpenCV

---

**Link to github:**
https://github.com/khkhiu/Singapore_Polytechnic-Centroid_Counter
{: .notice--info}

***

<strong>Introduction</strong>

***
The aim of the project is to develop a simple algorithm to count the number of people in the room. This algorithm was part of a bigger project, but his repository will only focus on the algorithm.

***

<strong>The team</strong>

***
The following are members of the team

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

<div class="embed-container">
  <iframe
      src="https://youtube.com/embed/nILaMWWoH28"
      width="700"
      height="480"
      frameborder="0"
      allowfullscreen="">
  </iframe>
</div>