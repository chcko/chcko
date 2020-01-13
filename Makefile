.PHONY: test

test:
	py.test chcko/tests --db=sql
	py.test chcko/tests --db=ndb
