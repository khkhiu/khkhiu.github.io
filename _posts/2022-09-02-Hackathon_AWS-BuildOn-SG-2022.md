---
title: "AWS - BuildOn Singapore, 2022"
date: "02-09-2022"
categories:
  - Competition
tags:
  - Hackathon
  - Amazon Web Services(AWS)

---

***

<strong>Introduction</strong>

***
Amazon Web Services (AWS) Build On is a competitive hackathon that challenges the community to create technological initiatives and solutions to address challenges faced by participating sponsors

As the finale was held in person at AWS Singapore, Build ON 2022 was ran at a much smaller scale compared to previous years.

**Note**<cite><a href="https://aws-build-on-2022.devpost.com/">Click here </a></cite>for the AWS Build ON 2022, devpost page</a></cite>
{: .notice--info}

***

<strong>Problem Statements</strong>

***

Select from one of the following problem statements and present a solution that leverages on AWS Services:

<strong>ZALORA</strong>

Helping shoppers to select the right sized apparel and shoes without having to worry about returns is one of the biggest challenges faced by the fashion e-commerce industry. Develop a solution that provides ZALORA's diverse range of shoppers with the confidence that they are selecting the right size when shopping online.

<strong>National University Health System (NUHS)</strong>

One of the most common tasks in a ward is to dispense and deliver medication to patients, which must be undertaken in a timely manner as patients are waiting to receive their medication before going home. Develop a robot to deliver medication from a satellite pharmacy to a desk beside the patient's bed in the shortest possible time without collision. The robot must be capable of autonomous navigation, optimal route planning and dynamic object avoidance using video-based object recognition. A training set consisting of a virtual ward environment simulating the random movement of people and objects will be provided. The challenge will be split into two parts, with participants selecting one of the following key problems to tackle:

1. Object detection
2. Advanced navigation capability

***

<strong>Solution</strong>

***

Unlike previous years, the submission this year is in the format of a pitch video. Hence, I will be using the slides of the pitch video to explain my solution.

|![Problem statement](/assets/images/Hackathon-AWS-BO-2022/Slide3.PNG)|
|<em>I have opted to tackle the 'Object detection' problem as posed by NUHS</em>|

|![Proposed solution](/assets/images/Hackathon-AWS-BO-2022/Slide4.PNG)|
|<em>I propose an object detection algorithm utilizing AWS Sagemaker and AWS IOT Greengrass</em>|

|![Solution architecture](/assets/images/Hackathon-AWS-BO-2022/Slide6.PNG)|
|<em>Solution architecture</em>|

This will be operation sequence for the algorithm is as follows

1. The camera will be used as the ‘eyes’ of the robot

2. IOT Greengrass will be used to perform machine learning inference locally on devices, while using models that are created, trained, and optimized in the cloud. 

3. IOT core will be used to manage the camera and interface with Kinesis Data Firehose

4. Kinesis Data Firehose will be used to captures, transform and upload camera footage to the S3 bucket

5. Data from S3 will be sent to SageMaker Ground Truth for labelling

6. The labelled data will be sent to SageMaker for training, building, and deployment of the machine learning model

7. The model will be uploaded to SageMaker Neo for optimization. SageMaker Neo automatically optimizes machine learning models for inference on cloud instances and edge devices to run faster with no loss in accuracy.

8. After optimisation, the model will be uploaded to SageMaker Neo runtime, allowing the compiled model to be deployed to the camera.

9. This establish a feedback loop that will allow the robot to detect objects in its path.

***

<strong>Intended Impact</strong>

***

![Enable navigation](/assets/images/Hackathon-AWS-BO-2022/Slide8.PNG)

The most important impact is that the algorithm will allow the robot to navigate without colliding into other objects

![Fleet deployment and management](/assets/images/Hackathon-AWS-BO-2022/Slide9.PNG)

AWS allows this solution to be deployed to the entire fleet of robots, thus making it easy for staff to administer and manage all robots. At the same time, the robots are able to use data from each other to improve object detection capabilities.


![Comparison with current market solutions](/assets/images/Hackathon-AWS-BO-2022/Slide8.PNG)

There currently are a few medical robots on the market, one of which is shown here.I will only be comparing the software. Market solutions also provide similar fleet management functionality and collision avoidance capability. However, the majority of medical robots on the market utilize proprietary software. This prevents users from customizing the software to best suit their needs.Therefore, the key advantage of the proposed solution is the flexibility in software implementation through integration with other AWS services

![Integration with other AWS services](/assets/images/Hackathon-AWS-BO-2022/Slide10.PNG)

Here are some examples of aforementioned flexibility of software implementation.

To improve functionality:
1. Athena can be used to run big data analysis
2. IOT Device defender can be used to improve device security
3. Cost explorer to monitor cost

To add new functions:
Polly and Lex can be used to allow the robot to speak.


|![References](/assets/images/Hackathon-AWS-BO-2022/Slide13.PNG)|
|<em>References</em>|

***

<strong>Pitch Video</strong>

***

<iframe width="560" height="315" src="https://www.youtube.com/embed/BbHyT9OMDUY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>