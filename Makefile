package_name = gumo-task-emulator

export PATH := venv/bin:$(shell echo ${PATH})

.PHONY: setup
setup:
	[ -d venv ] || python3 -m venv venv
	pip3 install --ignore-installed twine wheel pytest pip-tools
	pip3 install --ignore-installed -r requirements.txt

.PHONY: deploy
deploy: clean build
	python -m twine upload \
		--repository-url https://upload.pypi.org/legacy/ \
		dist/*

.PHONY: test-deploy
test-deploy: clean build
	python -m twine upload \
		--repository-url https://test.pypi.org/legacy/ \
		dist/*

.PHONY: test-install
test-install:
	pip --no-cache-dir install --upgrade \
		-i https://test.pypi.org/simple/ \
		${package_name}

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: clean
clean:
	rm -rf $(subst -,_,${package_name}).egg-info dist build

.PHONY: pip-compile
pip-compile:
	pip-compile \
		--upgrade-package gumo-core \
		--upgrade-package gumo-datastore \
		--upgrade-package gumo-task \
		--output-file requirements.txt \
		requirements.in
	pip3 install --ignore-installed -r requirements.txt

.PHONY: run
run: clean build
	pip uninstall -y ${package_name}
	pip3 install dist/${package_name}*.tar.gz
	python sample/task_emulator_server.py
