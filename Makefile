build:
	docker build -t music-docker .

run:
	docker run -p 5000:5000 music-docker

flask:
	python app/app.py


