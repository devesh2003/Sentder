from hashlib import md5

def md5_hash(text):
    return md5(text.encode("utf-8")).hexdigest()

def sha1_hash(text):
    return sha1(text.encode("utf-8")).hexdigest()
