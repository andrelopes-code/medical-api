
format:
	isort .
	black .

pre-commit:
	make format
	git add .