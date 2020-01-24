db = None
def use(_db=None):
    global db
    if _db:
        db = _db
    return db
    #globals().update(
    #    {'School':db.School, 
    #     'Period':db.Period,
    #     'Teacher':db.Teacher,
    #     'Class':db.Class,
    #     'Student':db.Student,
    #     'Problem':db.Problem
    #     })
