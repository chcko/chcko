.PHONY: test

test:
	py.test chcko/test/test_db.py --db=ndb
	py.test chcko/test/test_integration.py --db=ndb
	py.test chcko/test/test_functional.py --db=ndb
	py.test chcko/test/test_db.py --db=sql
	py.test chcko/test/test_integration.py --db=sql
	py.test chcko/test/test_functional.py --db=sql
