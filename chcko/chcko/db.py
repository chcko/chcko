db = None
def use(_db=None):
    global db
    if _db:
        db = _db
    return db
