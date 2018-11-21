# Cassandra on a Raspberry Pi Cluster :o:

TODO: See where this fits into the Pi book...

## Prerequsites:

  * [Assembling the Pi Cluster](https://github.com/cloudmesh-community/book/blob/master/chapters/pi/case.md#build-your-own-5-node-pi-cluster)
  * [Set up small cluster by hand](https://github.com/cloudmesh-community/book/blob/master/chapters/pi/setup-ultimate.md)
  
## Setting up a Small Pi Cluster by Hand 

:warning: (Should probably be moved to book/chapters/pi/setup-ultimate.md)

### Step 1: Burning OS image to SD cards

The first step in setting up the raspberry pi cluster is to burn the OS image to the SD cards.  In this example we are using [SanDisk 32GB microSD cards.](https://www.amazon.com/Sandisk-Ultra-Micro-UHS-I-Adapter/dp/B073JWXGNT/ref=sr_1_5?s=pc&ie=UTF8&qid=1542828848&sr=1-5&keywords=32+gb+micro+sd+card)  If your computer does not have an SD card reader you may need to [purchase one](https://www.amazon.com/Anker-Portable-Reader-RS-MMC-Micro/dp/B006T9B6R2/ref=sr_1_3?s=electronics&ie=UTF8&qid=1542828941&sr=1-3&keywords=sd+card+reader) for this step.  The first part of this step is to download the required software / files.

  * [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) - The OS we will be using for the nodes in our pi cluster.
  * [SD Formatter](https://www.sdcard.org/downloads/formatter_4/) - This will be used to ensure the SD card is formatted correctly.
  * [Etcher](https://www.balena.io/etcher/) - Software used to burn the OS image to the SD card.

Once you have the required software and OS image file we can set up each SD card.  In order to ensure the SD card is formatted correctly we will want to run the SD Card Formatter tool.  Ensure that you don't have any other drives connected to you computer and carefully select the drive that corresponds to your SD card.  Then select overwrite format and click format.  This step can take a few minutes but it is good practice to ensure the correct formatting.

![SD Card Formatter](images/SD_format.png)

While the SD card is formatting you will want to extract the Raspbian Lite image from the zipfle it was downloaded in.  Extract this to your desktop so that it can be used in the next step.  Once the SD card is formatted you can open Etcher.  Select the Raspbian Lite image we saved to the desktop and then check to make sure the correct SD drive is selected by Etcher.  Then click "Flash!".  Once this is done you should have the Raspbian Lite image burned to the SD card.

![Etcher](images/etcher.png)

Before pluging the SD card into the Raspberry Pi we will want to add a file to the boot partition.  Open notepad or another editor and save a blank file as "ssh" with no file extension.  When the raspberry pi boots up it will see this file and enable SSH connections.  At this point we will also edit the **config.txt** file.  In the file we need to uncomment this line: ```hdmi_force_hotplug=1```.  This will ensure that your monitor will work correctly should you need to plug it in to trouble shoot during the next step.

Another great resource for the initial set is a [youtube video](https://www.youtube.com/watch?v=H2rTecSO0gk) put together by Davy Wybiral [@Pi_Cluster_Setup_Youtube].

### Step 2: Setting up the nodes

setup for the first node
 * git setup: https://www.atlassian.com/git/tutorials/install-git
 * run shell script to load python packages needed
 * pull repository for code
 * Plug monitor and keyboard into first node.  We will set up wifi which will allow us to SSH to the parent node.  Also configure other settings and change hostname and password.  Lastly we will need to download the needed software for the node.
 * Find the IP addresses for each of the worker nodes.  ```arp -a```  if that command does not work we will need to plug the monitor in to view the IP address.
 * Once we have the IP addresses we can finish setting up the nodes using the fabric code.  (need to finish writing the script for this.)

## Sources (will be integrated in jabref)

* OS Install guide: https://www.raspberrypi.org/documentation/installation/installing-images/README.md
* Youtube Cluster Setup: https://www.youtube.com/watch?v=H2rTecSO0gk
* Headless setup: https://www.raspberrypi.org/forums/viewtopic.php?t=191252
* HDMI Monitor Signal issue: https://www.raspberrypi.org/forums/viewtopic.php?t=34061
* Fabric documentation: http://docs.fabfile.org/en/latest/getting-started.html
