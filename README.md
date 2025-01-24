# Download Jira Attachments

This is a small script I made to download attachments from a Jira project and save them to issue-specific folders.

It was initially designed to download files from a large amount of Jira issues for local data transformation processes.

## Installation
1. Install requests `pip install requests`
2. Install jira `pip install jira`

## Usage
1. Open the script in your python ide of choice and fill out the following global variables:
- user
	The email used for your Jira account.
	
- apikey
	Your Jira API token. Follow this guide to create an API token: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
	
- base_url
	The base url of your organization's Jira instance. You can find this by accessing your org's Jira instance and viewing the url. It will be in the following format:
`https://[INSTANCE NAME].atlassian.net/`

- base_dir
	The file path of the directory you want issue folders to be created in.

- jql
	The default jql included will query all issues assigned to the current user. For more information on jql syntax, see Atlassian's documentation:	https://confluence.atlassian.com/jira064/advanced-searching-720416661.html

- limit
	Defaults to 100. The Jira api pulls issue data by "pages". Basically, this is the number of issues pulled per request. The Jira api will paginate through issues until all applicable issues are pulled.
	
2. Run!

It may take several minutes for all issues to be pulled. Don't be alarmed if it seems like the script is stalling.

## Future improvements
Currently, the script only checks to see if a folder has been created for an issue to determine if an issue's attachments have been downloaded. It doesn't check to see if there have been attachments added to an issue.
