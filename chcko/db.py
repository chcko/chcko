db = None
def use(_db):
    global db
    db = _db
    globals().update(db.models) #School, Period, Teacher, Class, Student, Problem
