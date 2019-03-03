from hashlib import md5

def md5_hash(text):
    return md5(text.encode("utf-8")).hexdigest()
