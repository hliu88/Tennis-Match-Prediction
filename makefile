LINTER = flake8
APP_DIR = app

FORCE:

prod: tests #github

dev_env: FORCE
	#enable virtual env
	# pip install -r requirements.txt
	cd app; python app.py

# github: FORCE
# 	-git commit -a
# 	git push origin master

# docs: 
# 	# cd $(APP_DIR); pydoc3 -w main.py
# 	cd $(APP_DIR); python3 -m pydoc -w ./*.py

# tests: unit #lint

# unit: FORCE
# 	nosetests --with-coverage --cover-package=$(APP_DIR)

# lint: FORCE
# 	$(LINTER) $(APP_DIR)/*.py