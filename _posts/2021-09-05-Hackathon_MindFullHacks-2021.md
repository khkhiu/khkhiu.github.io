---
title: "MindfulHacks Hackathon, 2021"
date: "05-09-2021"
categories:
  - Competition
tags:
  - Hackathon
  - Amazon Web Services(AWS)

---

**Note** The "Competition" post are not in chronological order, but rather the order which I updated the post.
{: .notice--success}

**Note** The AWS instances and its associated resources have been terminated to ensure that I am not billed unnecessarily.
{: .notice--info}

***

<strong>Introduction(verbatim)</strong>

***
MindfulHacks was founded as Singapore's first Mental Health-themed Student Hackathon. It is a 24-hour overnight hackathon taking place between<em> 4 to 5 September 2021</em> where attendees work to build a software project that addresses mental health issues. Our mission is to encourage students to come together and innovate solutions to mental health issues and combat the stigma of mental illness. We welcome students from Universities, Polytechnics, ITEs, and Junior Colleges.

***
<strong>Problem Statement(verbatim)</strong>

***

 Create a tool that will address a specific or multiple mental health issues in your community, whether you want to design and develop an app, create a data visualisation or anything else you can think of!

***

<strong>Function of application</strong>

***
This chatbot is a cosmetically improved version of the one from 
<a href="https://khkhiu.github.io/competition/Hackathon_SMU-LIT-Hackathon-2021/"> SMU - Legal Innovation & Technology (LIT) Hackathon, 2021 </a>. Firstly, a background that mimics a therapist's office was added to make it feel more authentic. Secondly, additional lighting sources were added to illuminate the scene better.

|![Programming chatbot](/assets/images/Hackathon-MindFull/AWS_Sumerian.png)|
|<em>Programming the chatbot, background clearly visible</em>|

The idea is to create a virtual therapist that is available on demand. This would not only make mental health support more accessible by the general public, it can also reduce the stigma around mental health as people can try therapy for themselves without fear of judgement or any monetary or time commitments.

The solution was created using the following core technologies
1. AWS Sumerian, to create the virtual therapist and environment
2. AWS Polly, which turns text to speech
3. AWS Lex, allows for building the response of the chatbot

The chat-bot is a proof of concept and hence has very little functionality. for it to be fully operational, mental health experts need to be involve as I do not have the needed domain expertise to execute the project on my own. Furthermore, data from the chat-bot would need to be analysed to improve the functionality of the chat-bot.

The main unique selling point of this chat-bot is that users can speak directly to it, thus giving it a more life-like feel compared to text based chatbot.

***

<strong>Challenges faced</strong>

***

1. Getting the lighting source into the desired position was a bit tricky

2. Programming the chat-bot to feel like natural speech was also another issue

3. The chat-bot did not respond to speech using push-to-talk initially(incidentally, I am still not sure what the issue is as it miraculously started working for seemingly no reason)


***

<strong>Video Demonstration:</strong>

***

<div class="embed-container">
  <iframe
      src="https://youtube.com/embed/Qk_C7c5Wzqs"
      width="700"
      height="480"
      frameborder="0"
      allowfullscreen="">
  </iframe>
</div>


***

<strong>Closing thoughts:</strong>

***
While I am highly like going to continue with AWS and cloud computing, this and <a href="https://khkhiu.github.io/competition/Hackathon_SMU-LIT-Hackathon-2021/"> SMU-LIT Hackathon 2021. </a> will most likely be the only times that AWS Sumerian will be deployed for the time being as I focus on other fields. Although this makes me wonder if a similar solution can be deployed more effectively using Unreal Engine or Unity Engine.