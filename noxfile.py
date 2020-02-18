import os
import nox

DEFAULT_INTERPRETER = "3.8"

def test_for_db(session, dbname):
    session.install('-r','requirements_'+dbname+'.txt')
    session.install('pytest','pytest-cov','psutil','webtest')
    run_args = ["pytest"]
    if session.posargs:
        run_args.extend(session.posargs)
    run_args.extend([f'--db={dbname}'])
    run_args.append(os.path.join('chcko','chcko','tests'))
    session.run(*run_args)

@nox.session(py=DEFAULT_INTERPRETER)
def test_sql(session):
    test_for_db(session,'sql')


@nox.session(py=DEFAULT_INTERPRETER)
def test_ndb(session):
    test_for_db(session,'ndb')
