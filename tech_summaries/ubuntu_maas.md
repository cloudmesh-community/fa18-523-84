## Ubuntu MaaS :smiley: fa18-523-84


|          |                 |
| -------- | --------------- |
| title    | Ubuntu MaaS     | 
| status   | 90              |
| section  | DevOps          |
| keywords | DevOps          |

Ubuntu MaaS (Metal as a Service) allows a user to deploy and manage physical hardware.  Similar to IaaS (Infrastructure as a Service) applications Ubuntu MaaS provides the capabilities to configure nodes, install a preferred OS and install applications [MaaS_Blog].  The difference is in the level of detail the user has access to. IaaS typically refers to the configuration of virtual machines, meaning that the user does not have access to the actual infrastructure [Stackexchange].  With Ubuntu MaaS data center managers have the capability to configure key details of individual servers for optimal performance. [MaaS Website]

Ubuntu MaaS works by utilizing a tiered architecture of region nodes and rack nodes that are used to manage the hardware [How_it_works].  The region controller deals with requests and works with the rack controller.  The rack controller provides local services and also cashes the operating system image [How_it_works].  Ubuntu MaaS also provides high availability at the database level.  To achieve this the region controller automatically switches gateways in the event of a rack controller failure [How_it_works].  In addition, Ubuntu MaaS allows grouping of machines to create physical availability zones.  This allows the service to scale and helps streamline the deployment of complex solutions [How_it_works].  

Ubuntu MaaS manages the implementation of a new node through a process called "The node lifecycle" [How_it works].  The first step is to bring the hardware into the ecosystem and to take an inventory of the physical components at its disposal.  Next, the set up phase gets the server ready for deployment.  Once the set up phase is complete the server can be deployed or retired. 

> "MAAS is designed for devops at scale, in places where bare metal is the best way to run your app. Big data, private cloud, PAAS and HPC all thrive on MAAS." [MaaS_Website]

Ubuntu MaaS was designed for situations where the user is managing a physical data center and where flexibility, control and efficiency are important.  IaaS is similar to MaaS and is ideal for setting up virtual machines in a cloud environment.  Some had questions about the need for Ubuntu MaaS due to these similarities [tech crunch].  However, as the product developed it has become a useful tool for data center mangers. 
