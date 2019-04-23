
import db.mellow


def test():
    mellow = db.mellow.mellow()
    count = mellow.Count("users")
    print "count:", count

    exist = mellow.Exist("users", {"id": 1})
    print "users@id=2, exist=", exist

    mellow.Insert("users", {"id":2, "name":"chuan"})
    mellow.Insert("users", {"id":3, "name":"tiger"})

    data = mellow.Find("users", out=dict)
    print data

    data = mellow.Find("users")
    print data



if __name__ == "__main__":
    test()
