# Docker Dash Frontend

This is the client end of the application, that users directly interface with. 
It contains three distinct pages and allows the user to visualize and manage activity on the network.

## Table of Contents:
1. [General Notes](#general-Notes)
1. [Setup Guide](#setup-guide)
1. [Page Details](#Page-Details)
1. [Disclaimers](#Disclaimers)
   
</br>

# General Notes
### Server Status Light
The colored circle on the top right of the server cards flashes green to indicate the system is running smoothly and red otherwise.
### Naming Conventions for the Servers
The name of the server is indicated on each server panel below the type of its system. The type of the system will be either solo or swarm. 
### Request Image / Create App
The request image modal grabs an image file from docker's image repository, which can be used to create instances of apps.

## Prerequisites:
- Integrated Development Environment on your computer
- Internet connection
- Admin privileges

# Setup Guide
- Open terminal 
- Navigate to client folder: `cd client`
- In Terminal run: `npm install` and `npm run dev` to start your development server.

</br>

# Page Details
The following outlines the structure of the website page by page. The pages can be navigated by the user via the navbar.
</br>

## View Servers
This page displays the servers active on the network as well as some of their important metrics. 
Included is CPU%, memory%, amount of unique users, and number of applications running on that unit.

![Web capture_14-7-2023_143334_192 168 98 74](https://github.com/JaxsonP/docker-dash/assets/106226308/c58a2f27-b409-4cc2-a073-99943c2b9d45)
</br>
</br>

## View Applications
This page allows the user to see the complete list of applications running on the network and allows them to perform tasks on these applications.
### Functionality 
- Start: starts selected application
- Pause: Pauses the specified app. The app must be running in order to pause
- Unpause: Unpauses the specified app. The app must be paused in order to unpause
- Restart: Restarts the specified app.
- Remove: Removes an application from the network
- Kill: Forcefully stops the specified app.
  
![Web capture_14-7-2023_143648_192 168 98 74](https://github.com/JaxsonP/docker-dash/assets/106226308/bba863da-c27e-4567-8d73-a6a31e97f987)

</br>
</br>

## View Images
This page allows the user to see what iso images that apps can be created from, update this list, and use the image to create apps.
#### Functionality
- Request Image: Adds an iso image to the images page
- Create App: Generates an application  of the selected iso image, that can be found in the apps page.

![Web capture_14-7-2023_143418_192 168 98 74](https://github.com/JaxsonP/docker-dash/assets/106226308/39cbb371-e75c-4f33-87b5-6c14045a3036)

</br>
</br>

# Disclaimer
This is a demo mode, so only solo servers are available and swarm servers are unavailable.
</br>
</br>

