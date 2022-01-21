from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from uuid import uuid4

with open("cred/public.pem", "rb") as f:
    public_key_str = f.read()
public_key = load_pem_public_key(public_key_str)
with open("cred/private.pem", "rb") as f:
    private_key_str = f.read()
print(private_key_str.decode("utf-8"))
private_key = load_pem_private_key(private_key_str, password="namth".encode("utf-8"))
# api_key = str(uuid4())
api_key = "0f9c8e55-70b5-42f4-bc5b-f7e59ed0f30d"
print(api_key)
plain_text = api_key.encode("utf-8")
padding = OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
encrypted = public_key.encrypt(plain_text, padding)
encrypted = '\xa7\xe6.fia\x1f\xc0\xddT\xa8\x88\xd3W\xf1\x1c\x8290;,\xf1\xfa/\xe2n<\xfbIb\t\xd9\xd4C\xca\x89Z\xf3\xd9Q\xcbO\xed\xa6\xa5u\xcc\xe0\xf5\xdb\xdf\x06\x0f\xb9m\x9a\xb9@\xaf\xea\xda4\x8e\x0b\x06\x0f\r<\x9bz\xb6\xc7\x84c\xd5Y\xcd8;\x06\x00\xa0\x99>\x138\xe3\xef\xa1\xd8@\x11Y@JB\x02\xb35\xe6\x1c!K[\r\xe6\xe4\x01%\xb7QP\x14\x8a\x9c%6\x87\r\x84\xde8p\xe6\xe1oU-'
print(encrypted)
decrypted = private_key.decrypt(encrypted, padding)
print(decrypted)