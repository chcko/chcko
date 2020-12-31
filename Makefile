# gcloud beta emulators datastore start --no-store-on-disk --data-dir .
# is run automatically in conftest.py
# but it fails sometimes, so better start it manually before testing

.PHONY: content test cov check dist up deploy install datastore tag

datastore:
	gcloud beta emulators datastore start --no-store-on-disk --data-dir .

content: install
	cd ../chcko-r && doit -kd. html && doit -kd. initdb

test: content
	py.test chcko/chcko/tests --db=sql
	py.test chcko/chcko/tests --db=ndb

cov:
	py.test chcko/chcko/tests --db=sql --cov

check:
	restview --long-description --strict

dist:
	sudo python setup.py bdist_wheel

up:
	twine upload dist/`ls dist -rt | tail -1`

deploy:
	cat app.yaml > .app.yaml
	cat ~/my/mam/chcko/environment.yaml >> .app.yaml
	# gcloud app deploy .app.yaml --project chcko-262117
	gcloud app deploy index.yaml
	gcloud app deploy .app.yaml --project mamchecker

install:
	pip install --user -r requirements_dev.txt
	sudo pip install --user -e .

tag: install
	$(eval TAGMSG="v$(shell runchcko --version | cut -d ' ' -f 2)")
	echo $(TAGMSG)
	git tag -s $(TAGMSG) -m"$(TAGMSG)"
	git verify-tag $(TAGMSG)
	git push origin $(TAGMSG) --follow-tags
