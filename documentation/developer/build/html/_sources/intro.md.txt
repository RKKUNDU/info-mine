## Getting started

### Quick Intro

The info-mine project aims at bringing together the information spread across various locations at IIT-B into one spot for a user to be able to access information faster and cleaner. As of now, when a student wants to get any information, from the cse website, their emails, or moodle, they login to each of the portals and then look for the information. Also, sometimes, a student can miss out on some announcements and due dates. Info-Mine helps to gather all of this information and provide it to the student as a command line tool for linux users and also a whatsapp bot for non-linux users, where they can just type a command and information will be fetched for them.   
For the command line tool, in the CSE component, we fetch information from the cse website regarding students, faculties, news and courses. In the moodle component we fetch all sorts of information for a student, like quizzes, grades, assignments, announcements, discussions, courses and forums. We also have a component which will send and retrieve emails with simple commands, instead of logging in to see one email, we can just send a simple command to fetch the email for us, or even filter multiple emails directly from the command line. All of these components are also made available on Whatsapp for students who do not use the terminal.

### Motivation

Many of the courses tend to prefer certain platforms over the others for providing updates, quiz info, discussions etc.
Also, apart from the courses, we have two emails, which are insti and department.
This causes a student to visit multiple sites many times which can get discomforting after a certain point, and students can also miss out on some updates.
Thus, the aim of this project is to reduce the hindrance in visting many places and create a tool that helps students to get all their info in one spot. 
The term Info-Mine comes from mining for information from cse websites, moodle and the emails.

### Installation guide for developers

To install the command line tool, we have a standalone script which clones the source code, it creates an executable in the bin folder of the user and moves the code to 

* Should have git installed
* Before getting started off with the developer docs, please do read the user docs.
* cd into the directory that you want to install this tool
* To download the installer to this directory, on your command line per-form:wget  –no-check-certificate  –content-dispositionhttps://raw.githubusercontent.com/RKKUNDU/info-mine/main/infomine-installer.sh
* Run the installer script with root priviliges, by:sudo bash infomine-installer.sh
* Now that it has been installed, please familiarize yourself with the tool.
* Please clone the repository by performing: git clone https://github.com/RKKUNDU/info-mine.git
* Go through the rest of the developer docs to add features, experiment and so on.

