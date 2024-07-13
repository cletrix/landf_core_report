git:
	git add .
	git commit -m "$(filter-out $@,$(MAKECMDGOALS))"
	git push origin $(word 2,$(MAKECMDGOALS))

clean: ## Clear *.pyc files, etc
	@find . -name \*.pyc -delete
	@find . -name \*__pycache__ -delete
	@echo "cleared"

init:
	pip install -r requirements.txt
