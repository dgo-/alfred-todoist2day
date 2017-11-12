# Todoist2day
Todoist2day is an Alfred Workflow to manage your Todoist task from Alfred. It use the Todoist v8 REST API.

## Installation
To install the Workflow have a look on the following steps.

### Prerequisites
For this workflow to work you need Alfred version 3 or above and a powerpack licence.

### Install workflow
Download the Workflow here and add it to alfred.

### Configure the workflow
To access the API from Todoist you have to configure the API token. You finde your API token under: Settings > Integrations > API token.
```
t-token YOUR_API_TOKEN
```

To set up the language for parsing the time format. (Default is 'en') 
``` 
t-lang de
```

## List all tacks for today
The following command list all your task for today
```
2day
```
with pressing ENTER the task will be marked as done. 

## Add a new task
The follwoing command add a new task to your account. 
```
tadd do something; personal; tomorrow
```
This line will add the task "do something" to the project "personal" and set the date to "tomorrow" 

