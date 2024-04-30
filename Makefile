flask:
	python3 app/flask_app.py

install:
	pip install -r requirements.txt

submit: 
	git commit -m "final submission" -a
	git push

MKDIR_P ?= mkdir -p
