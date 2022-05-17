---
title: "SMU - Legal Innovation & Technology (LIT) Hackathon, 2021"
date: "28-08-2021"
categories:
  - Competition
tags:
  - Hackathon
  - Amazon Web Services(AWS)

---

|![proof](/assets/images/Hackathon-SMU_LIT-2021/SMU_LIT-2021_cert.png)|
|<em>Proof of participation</em>|

**Note** The AWS instances and its associated resources have been terminated to ensure that I am not billed unnecessarily.
{: .notice--info}

***

<strong>Introduction</strong>

***
The SMU LIT Hacakathon 2021 is organised by the SMU Legal Innovation & Technology (LIT ) club. Held from <em>13 to 15 August 2021</em> over zoom and discord, the event brings together students from all Singapore Institutes of Higher Learning to tackle legal-tech problems faced in law, business and community. 

In groups of three to five with at least one law student, the participants were tasked to develop technological solutions to real-world problem statements provided by industry partners. These included topics such as automating research, legal analytics and access to justice under the theme of “The Next Decade in Legal Tech in Singapore”.

***

<strong>The team</strong>

***
The team I was in was called:<strong>Code Brigade</strong> which consisted of the following people(as of 28 August 2021)

1. Tan Ding Xiang, Singapore Management University (SMU), Information Systems
2. Adele neo, Singapore University of Social Sciences (SUSS), Juris Doctor
3. Vashawn Yeo, Singapore Polytechnic (SP), Information Technology 
4. Khiu Kim Hong, Singapore Polytechnic (SP), Electrical and Electronic Engineering

***

<strong>Problem statements(extracted, verbatim)</strong>

***
The team investigated the following themes:

<strong>Theme 1: Rise of Asia</strong>

Preamble: With a burgeoning middle class and rising demand for goods and services in and from Asia, Asia is expected to continue showing strong economic growth.1 This also signals a parallel demand for legal market services in the region.

| Title     | Description |
| ----------- | ----------- |
|<em>Inter-jurisdictional Streamlining</em>|<strong>Expanding Regionally:</strong> In this globalized and digital age, businesses are no longer confined to or defined by their home jurisdiction, and their lawyers need to keep pace as well.<br><br>How best can local lawyers who seek to expand their legal practice and regional expertise gather the relevant expertise and establish regional networks? <br>(By Linklaters)|


<strong>Theme 2: Operational Pressures amidst COVID-19</strong>

Preamble: COVID-19 has been a major driving force towards the digitalisation of the legal industry. At the same time, this has led to growing concerns about technological solutions
and a longing to further leverage it in the pursuit of justice.


| Title     | Description |
| ----------- | ----------- |
|<em>Remote Working/ Telecommuting:</em>|<strong>Psychological Risks: </strong>Telecommuting has blurred the line between work and home, and this is exacerbated by an increasingly prevalent "always-on" culture coupled with the accessibility availed by modern technology.<br><br>While circuit breaker and social distancing regulations have proven effective in reducing the spread of COVID-19, the measures put in place could also contribute to psychological and interpersonal risks that extend beyond the obvious health and economic repercussions of the COVID-19 pandemic. Even if an individual has the good fortune of remaining healthy and financially stable during this period, he/she could still be vulnerable to stress, anxiety and interpersonal tension and conflict.<br><br>With hybrid / remote working fast becoming the norm, how might we mitigate these psychological risks?<br><br>(By Dentons Rodyk)|
|<em>Cybersecurity </em>|<strong>Verification: </strong>The challenges brought about during the COVID-19 pandemic forced communications to go almost fully online. How can we create a solution to verify the authenticity of identity, signatures, timestamps and locations?<br><br>(By Dentons Rodyk)|

***

<strong>Solution</strong>

***
After some discussion, the team opted to build an interactive chatbot using Amazon Web Service(AWS) Sumerian. We intended to differentiate our chatbot by giving it a 3D model and by having users speak to it and have it respond in kind. The idea was to simulate speaking to a psychiatrist, thus giving it a more personal touch and making it more effective. The solution is also available on demand, making it more convenient than normal psychiatrist.

The solution was created using the following core technologies
1. AWS Sumerian, to create the virtual therapist and environment
2. AWS Polly, which turns text to speech
3. AWS Lex, allows for building the response of the chatbot

|![Programming chatbot](/assets/images/Hackathon-SMU_LIT-2021/AWS_Sumerian.png)|
|<em>Programming the chatbot</em>|

***

<strong>Video demonstration of solution</strong>

***
<em>The video is a reproduction of the solution after the event ended.</em>

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

<strong>Areas of improvement</strong>

***
The most important area of improvement is the involvement of actual psychiatrist and domain experts. This is important as no one  in the team is an expert on mental health, as such we need input from domain experts to make our chatbot effective in addressing mental health concerns.

Another area of improvement is the addition of machine learning to improve the performance of the chatbot. Machine learning can be used to learn the most effective response to any given scenario, thus making it more effective in addressing user needs.

lastly, the team still needed to find an effective way to package and deliver the chatbot into hands of users.