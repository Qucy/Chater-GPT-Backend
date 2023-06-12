activate:
	@echo "Activating virtual environment"
	poetry env use /bin/python3.10
	poetry shell
	
## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache%

## Also there is `refurb`, but we won't include that here.
format:
	@echo "Formatting..."
	black ./
	flake8 ./
	isort ./
	interrogate -vv ./
	