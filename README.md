# Score Engine
Scoring Engine used for UBNETDEF's Cyber Security Competition

## Requirements
* python 2.7
* python module: mysql-connector
* MySQL
* curl [for http/https check]
* sshpass [for ssh check]
* lftp [for ftp check]

## Installation
* Clone this repository
* Import initial MySQL DB
* Edit "config.ini", and fill in all the information

## How to use
Simply run "start", and hope for the best

## Notes
If you wish to run an individual check, run "check" with the TEAM ID and SERVICE ID as arguments.  This will not save to the database.

This was quickly created in the span of a few days. I also didn't know python, prior to writing this. Apologies if how I wrote my code offends you (or python best practices)
