.PHONY: test

test:
	py.test chcko/chcko/tests --db=sql
	py.test chcko/chcko/tests --db=ndb
