# gcloud beta emulators datastore start --no-store-on-disk
# is run automatically in conftest.py
# but it fails sometimes, so better start it manually before testing

.PHONY: test cov check dist up

test:
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



