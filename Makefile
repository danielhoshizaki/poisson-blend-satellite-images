project_name=poisson_blend
pwd=$(shell pwd)

build:
	docker build -t $(project_name) .

run:
	docker run --rm -v $(pwd):/main $(project_name) python src/main.py