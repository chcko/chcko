# gcloud beta emulators datastore start --no-store-on-disk
# is run automatically in conftest.py
# but it fails sometimes, so better start it manually before testing

.PHONY: test cov

test:
	py.test chcko/chcko/tests --db=sql
	py.test chcko/chcko/tests --db=ndb

cov:
	py.test chcko/chcko/tests --db=sql --cov
