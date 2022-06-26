---
title: "AWS - BuildOn ASEAN, 2021"
date: "29-06-2021"
categories:
  - Competition
tags:
  - Hackathon
  - Amazon Web Services(AWS)

---

**Note** The AWS instances and its associated resources have been terminated to prevent unnecessary billing.
{: .notice--info}

***

<strong>Introduction</strong>

***
Amazon Web Services (AWS) Build On, ASEAN is a competitive hackathon that challenges the community to create technological initiatives and solutions to address challenges faced by participating sponsors.

***

<strong>The team</strong>

***
The team I was in,<strong>AWS_IDV_DESC</strong>consisted of the following members from Singapore Polytechnic(SP)(as of 28 August 2021). The name is a reference to the name of my previous team. For more information on that, see here: <a href="https://khkhiu.github.io/competition/Hackathon_AWS-BuildOn-ASEAN-2020/"> AWS - BuildOn ASEAN, 2020. </a>

1. Keh Zi Yang, Diploma in Electrical and Electronic Engineering
2. Andrew Chia Wei Ren, Diploma in Electrical and Electronic Engineering
3. Khiu Kim Hong, Diploma in Electrical and Electronic Engineering

***

<strong>Problem statement(verbatim)</strong>

***
<strong>AI for Predicting Complications in Chronic Diseases</strong> Hyperglycaemia (diabetes), Hyperlipidaemia (high cholesterol), and Hypertension (high blood
pressure) are three of the top chronic diseases that affect Singaporeans. Some of the major
complications for these diseases include cardiovascular disease, renal failure, and eye/foot problems.
Understanding which patients will develop major complications can allow for early diagnosis and
interventions to manage the complications and even prevent the development of complications.
Challenge: To predict the time to developing complications in patients with type 2 diabetes or
hypertension or hyperlipidaemia from the time of first diagnosis. You will be provided with a dataset
that includes patient demographics, information on hospital visits, lab test results, medication, and
diagnoses.

***

<strong>Significance of problem</strong>

***
According to the Ministry of Health (MOH) and related organizations, there is an increasing prevalence of chronic diseases in Singapore. Approximately 1 in 4 Singaporeans aged 40 and above reporting at least 1 chronic disease [1] and roughly 37% of those aged 60 and above reporting 3 or more chronic health conditions in 2017, up from 20% in 2009.[2] There are 2 primary reasons cited for this rise, firstly, greater health awareness resulting in a rise in the number of people willing to be tested and treated. Secondly, an increasingly sedentary lifestyle and an imbalance in diet. This is further corroborated by a study called: The Burden of Disease in Singapore, 1990–2017, commissioned by MOH which stated that dietary risk is the leading risk factor in increasing the years of healthy life lost to premature death and disability in Singapore as of 2017.[3]

Based on current estimations, 1 in 4 people in Singapore will be over the age of 65 by 2030[2]. Coupled with the increasing percentage of the population reporting chronic health issues would place a significant strain on the healthcare system in Singapore. Therefore, the National University Health System (NUHS) saw fit to design an AI system that can predict complications in Chronic Diseases, thereby allowing for early intervention and even prevention.

***

<strong>Solutions Introduction </strong>

***
The team proposes a cloud-based artificial intelligence system that will predict possible complications in patients with chronic illnesses and time to develop said chronic illnesses based on the patient profile. 
Being cloud based will allow the solution to be easily access by all institution, like hospitals and MOH, that requires it. The system will continually improve itself as more data becomes available, thus improving its accuracy and capabilities.

***

<strong>Impact of Solution  </strong>

***
The solution can positively impact the target audience and society in a multifaceted manner.

Firstly, the patients at hand. By giving the patients a rough estimate of the possible complications and the time to develop, we allow for more effective early diagnosis intervention or even prevention if applicable. This would improve the overall quality of life of the patient by firstly, reducing their years lived with disabilities (YLDs). [3] Secondly, by halting the progression of an illness, like Hyperlipidemia, at its early stages, we allow the patient and easier time managing their illness as it has not progressed to be more difficult to manage. For illustration, early issues like fatigue and headaches are far easier to manage compared to potential cardiovascular disease in later stages in a Hyperglycemia patient.

Secondly, the medical system. From 2012 to 2017 healthcare spending increased by about 11% a year, rising from about $13 billion to $22 billion. [4] Aging population has been cited as one of the key instigators in for this increase. By allowing for early intervention of chronic illnesses, we can prevent progression of the illness, thus reducing the need for costly medical procedures for more advanced stages of the said illnesses, which are as high as 75% in places like the United States.[5][6]

Based on the team’s research there is a wide spectrum of medical solutions that make use of artificial intelligence and other similar technologies. Examples of such technologies include Project InnerEye by Microsoft that uses AI for medical imaging and Pfizer that uses IBM Watson for immune-oncology research. However, the company we will focus on is KenSci. 

KenSci is a company that developed and AI platform that uses data to improve healthcare with 3 primary solutions. The first solution is called: Providers, which aims to improve the inpatient experience. The second solution is called: Health Plan, which aims to help doctors build and deploy health care and insurance policies. The third solution is called: Medical Devices, which aims to optimize the deployment of medical equipment and resources.[7]

The primary advantage our solution has over KenSci is that our solution focuses on prevention, whereas KenSci focuses on cure and remedy. By allow for early intervention with the growth of chronic illnesses, our solution can address the issues before it can escalate further, thereby reducing the need for cure entirely.

|SWOT| Explanation |
| ----------- | ----------- |
|Strength(S)|1. AWS has a web interface that can be accessed from any device.<br><br>2. AWS can automatically scale to meet demands.<br><br>3. The AI only needs patient data to operate. Medical personnel do not need to actively manage it. |
|Weakness(W)|1. Requires large amounts of data to be accurate.<br><br>2.Working with limited data can result in inaccurate predictions.|
|Opportunity(O)|1. An aging population that is more at risk of chronic illness will ensure that the solution will receive ample use.<br><br>2.The solution can be easily modified for other purposes like predicting and identifying those at risk of mental illnesses.|
|Threats(T)|1. The solution can be easily replicated by other companies.|

|PEST| Explanation |
| ----------- | ----------- |
|Political(P)|The Singapore government is looking to reduce healthcare cost and this solution can aid in that aim. [4]|
|Economical(E)|The GDP of Singapore grew by 1.3% in Q1 with predicted growth of 4% to 6% in 2021. [8]|
|Social(S)|The population is becoming more technologically literate. This allows for easy adoption of the solution|
|Technological(T)|The smart nation initiative in Singapore saw a general push towards embracing new technologies which our solution falls under.|

***

<strong>Impact of Solution  </strong>

***

|![FlowChart-General](/assets/images/Hackathon-AWS-BO-2021/FlowChart_general.png)|

Description of features:
1.	Data base: The data base will house patient data from MOH and associated institutions which is needed to train the AI algorithm. It will also need to be updated to add new patient data, thus requiring it to be scalable to allow for flexibility in administration.
2.	AI model: The AI model will consider all aspects of patient profiles to make prediction for future patients. It will also need to consider the feedback of medical personnel as well as future patients to further refine its predictive model.

***

<strong>Architecture of Solution   </strong>

***

|![FlowChart-General](/assets/images/Hackathon-AWS-BO-2021/FlowChart_AWS.png)|

Design notes:
1.	Amazon S3 are used to store and archive various patient data, as well as to send and retrieve data to and from Amazon Redshift.
2.	Amazon Redshift is used to stage data for the AI group,
3.	Amazon HealthLake is needed as we will be working with sensitive healthcare related data. It will also be used to clean and prepare data for further analysis.
4.	Amazon SageMaker will be used in conjunction with Deep Learning Containers to quickly train and deploy machine learning models.
5.	Amazon Augmented AI(A2I) will be used to allow for human oversight of the sensitive data to ensure maximum possible accuracy.
6.	Amazon QuickSight will be used to present the findings of the AI group.

***

<strong>Going further   </strong>

***

One of the key improvements to the solution is automation of data input. AWS glue can be used to better sort and prepare data for analysis, resulting in more accurate predictions. Other services, such as AWS StepFunctions, AWS Batch and Amazon Neptune could be used together to enhance data capture and transfer capabilities.

To bring the solution to market, the team would need to work with MOH and institutions to get access to patient data to train machine learning models. Funding would also need to secured from organizations such as Enterprise Singapore, which provides grants for startups. [9]

Lastly, the solution is data driven and can easily be used to predict other issues like mental illnesses when given the appropriate data. It is also cloud based which allows for easy deployment to various medical facilities throughout the globe. Lastly, as the solution is entirely based on AWS, we will only need to pay for the processing power used. 

***

<strong>References   </strong>

***
[1] www.hpb.gov.sg. n.d. Tips to Prevent and Manage Chronic Diseases in the Workplace. [online] Available at: <https://www.hpb.gov.sg/article/tips-to-prevent-and-manage-chronic-diseases-in-the-workplace>

[2] www.sgh.com.sg. 2019. Proportion of older adults with multiple chronic diseases surges. [online] Available at: <https://www.sgh.com.sg/news/tomorrows-medicine/proportion-of-older-adults-with-multiple-chronic-diseases-surges>

[3] Ministry of Health Singapore, 2018. The Burden of Disease in Singapore, 1990–2017. [online] Singapore: Ministry of Health Singapore, p.45. Available at: <https://www.moh.gov.sg/docs/librariesprovider5/default-document-library/gbd_2017_singapore_reportce6bb0b3ad1a49c19ee6ebadc1273b18.pdf>

[4] The Straits Time, 2020. Koh Poh Koon details key drivers of rising healthcare costs here. [online] Available at: <https://www.straitstimes.com/singapore/koh-poh-koon-details-key-drivers-of-rising-healthcare-costs-here>.

[5] he American Journal of Managed Care, 2019. Identification of chronic diseases in their early stages enables prompt treatment that can slow or prevent disease development and debilitating and costly health outcomes. [online] 25(11). Available at: <https://www.ajmc.com/view/population-health-screenings-for-the-prevention-of-chronic-disease-progression>

[6] Preventing Chronic Disease, 2011. Getting Serious About the Prevention of Chronic Diseases. [online] 8(4). Available at: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3136976/>.

[7] Kensci.com. n.d. Enterprise grade AI platform for digital health - KenSci. [online] Available at: <https://www.kensci.com/platform>.

[8] 2021. MTI Maintains 2021 GDP Growth Forecast at “4.0 to 6.0 Percent” Amidst Significant Uncertainties Arising from the COVID-19 Pandemic. [online] Singapore: Ministry of Trade and Industry. Available at: https://www.singstat.gov.sg/-/media/files/news/gdp1q2021.pdf

[9] Enterprisesg.gov.sg. n.d. Grants - Enterprise Singapore. [online] Available at: <https://www.enterprisesg.gov.sg/financial-assistance/grants#for-startups> 

***

<strong>Appendix A - Proof of participation </strong>

***

|![proof](/assets/images/Hackathon-AWS-BO-2021/AWS_BO-2021_cert.png)|
|<em>Proof of participation</em>|
