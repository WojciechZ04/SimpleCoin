import hashlib

data = b"Hello, World!"  # Zakładając, że data to ciąg bajtów
hash_object = hashlib.sha256(data)
hexdigest_result = hash_object.hexdigest()

print("Data:", data)
print("hash_object: ",hash_object)
print("hexdigest_result: ", hexdigest_result)
