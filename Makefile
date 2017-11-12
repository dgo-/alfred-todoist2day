all: 
	cd src ; \
	zip ../alfred-todoist2day.alfredworkflow . -r --exclude=*.DS_Store* --exclude=*.pyc*

clean:
	rm alfred-todoist2day.alfredworkflow
