# JiraCloudIssueCreator
Python utility to create Jira Cloud issues using commandline tool

Currently issue creation (and project key) has been hardcoded for an example.
Instead of password, Cloud Jira usage needs to use of a "token" which is generated for useraccount in Atlassian Cloud
Otherwise Python library seems to be ok for Cloud operations

Usage:

python createissue.py   -u USERNAME -w ATLASSIAN_TOKEN -s SERVER-URL 
