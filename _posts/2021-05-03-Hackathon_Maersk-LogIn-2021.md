---
title: "Maersk, Sealand - Asia Log-In Challenge, 2021"
date: "03-05-2021"
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

Sealand Asia Log-In Challenge is a forum where students can apply their knowledge and come up with fresh and innovative ideas that can be applied in shipping and logistics so that Sealand Maersk can enhance customers’ experience in shipping and logistics. 

***

<strong>Opportunity Statement and Guide Questions(verbatim)</strong>

***

From registering online to be our customer to finding a price, from making a booking to submitting shipping instruction, from retrieving invoice online to making payment online, from purchasing additional supply chain services to tracking shipment online, a customer’s shipment end-to-end journey requires backend involvement and coordination of many peoples, tasks, processes, documentations and systems.

Many of these tasks, processes and documentations are still heavily dependent on manual work and physical paperwork. In Sealand Maersk, we continuously strive for digitalization and automation in order to increase productivity, reduce manual work gap and improve digital customer experience by adopting digital innovations such AI chatbot, e-payment, electronic bill of lading etc.

With this scenario and what you may know of container shipping and logistics, we would like to invite you to propose ideas on digital innovations which Sealand Asia should consider to achieve the aims mentioned. You may submit a business case to us that talks about the current scenario, what is the idea, what benefits does the idea bring and what technology can be used to develop the idea. 

***

<strong>Solution</strong>

***

<strong>A supply chain that incorporates both Industrial Internet of Things (IIoT) and blockchain</strong>

Organizations operating in the Industrial Internet of Things (IIoT) domain require solutions that enable them to monitor and scrutinize their supply chains to ensure strict quality control and accurate product tracking. By utilizing AWS IoT, businesses can achieve operational efficiency at scale. IoT-enabled equipment installed on their production plant floors captures data from multiple sensors, such as load, pressure, temperature, humidity, and assembly metrics. This data can be transmitted in real-time directly to the cloud or through an on-premises AWS IoT gateway, such as any AWS IoT Greengrass compatible hardware, and stored and analyzed in AWS IoT. The devices or IoT gateway will then send MQTT messages to the AWS IoT Core endpoint.

This approach provides a data ingestion pipeline powered by IoT, storing the data in a private blockchain network accessible only to member organizations, serving as the immutable single source of truth for future audits. The Hyperledger Fabric network deployed on Managed Blockchain includes two members, but it can be extended to additional organizations as required, forming a comprehensive solution for effective supply chain monitoring and auditing.

|![Project architecture](/assets/images/Hackathon-SeaLand-2021/Architecture.png)|
|<em>Project architecture</em>|

The following components are involved in the IoT-based supply chain solution:

1. IoT sensors: These sensors are mounted on each piece of equipment throughout the supply chain and transmit data to the IoT gateway. To simulate multiple devices, you can use the IoT Device Simulator.

2. AWS IoT Greengrass: This gateway securely connects your edge devices to AWS services and enables local processing, messaging, and data management. It also includes pre-built components such as protocol conversion to MQTT.

3. AWS IoT Core: This service subscribes to data published by the IoT devices or gateway and ingests it into the cloud for analysis and storage.

4. AWS IoT rules: These rules allow your devices to interact with AWS services based on the MQTT topic stream. For example, you can trigger a Lambda function to extract and publish data to the Fabric Client or an HTTPS endpoint to access a private API Gateway.

5. Amazon API Gateway: This service provides a REST interface to invoke Lambda functions that communicate with the Hyperledger Fabric network.

6. AWS Lambda for the Fabric Client: With the Hyperledger Fabric SDK installed as a dependency, this function communicates with the Peer Nodes to read and write data from the blockchain. The Peer Nodes run smart contracts (chaincode) and store a local copy of the ledger.

7. Managed Blockchain: This fully managed service creates and manages blockchain networks using open-source frameworks. In the solution, the Fabric Client interacts with the Hyperledger Fabric network on Managed Blockchain components that run within a customer's VPC.

- Certificate Authority: Every user must register and enroll with their Certificate Authority before interacting with the blockchain.

- Peer Nodes: These nodes endorse transactions and store the ledger. We recommend creating a second Peer Node in another Availability Zone for redundancy.

***

<strong>Benefits of blockchain</strong>

***
Blockchain technology presents a novel approach to monitor supply chain events, leveraging immutable ledgers that offer cryptographic proof that each transaction remains unaltered since being recorded. This feature is especially advantageous for supply chain auditing, as it ensures that the manufacturing, transportation, storage, and usage history of a given product or part remains unaltered since the time of a failure event.

Furthermore, in addition to providing an immutable record-keeping system, many blockchain protocols enable the deployment of decentralized, programmable logic written as code, commonly known as "smart contracts." These contracts allow for the execution of multi-party business logic on the blockchain, providing network members such as retailers and suppliers with authorization to process specific transactions. By implementing a supply chain on a blockchain, network members can securely process authorized transactions, ensuring transparency and accountability across the entire supply chain.

Customers using Amazon Managed Blockchain can participate in either private Hyperledger Fabric networks or the Public Ethereum network. Managed Blockchain provides relief from the burdensome task of creating, configuring, and maintaining the infrastructure of a Hyperledger Fabric network, enabling you to concentrate on essential activities that drive value such as constructing consortia or developing components specific to use cases. By using this service, you can establish and supervise a scalable Hyperledger Fabric network to which multiple organizations can connect from their AWS account.

***

<strong>Appendix A - Proof of participation </strong>

***

|![proof](/assets/images/Hackathon-SeaLand-2021/SeaLand-2021_cert.png)|
|<em>Proof of participation</em>|