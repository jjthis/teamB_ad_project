import hashlib


def getHash(strs):
    return hashlib.md5(("adProject&@*^%*!($" + strs + "aja&5^4$&2&!abhk").encode('utf-8')).hexdigest()
