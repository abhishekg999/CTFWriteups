from pyrage import passphrase
poss = ["standardsignwatergivenchosen", "standardwatersigngivenchosen"]
with open('secret.age', 'rb') as f:
    encrypted = f.read()
    for p in poss:
        try:
            print(passphrase.decrypt(encrypted, p))
        except:
            pass