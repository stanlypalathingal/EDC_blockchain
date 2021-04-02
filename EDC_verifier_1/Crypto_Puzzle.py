# The Decryption Function
def cipher_de(ciphertext, key):
    decrypted = ""

    for c in ciphertext:
        if c.isupper(): #uppercase 
            decrypted += chr((((ord(c) - ord('A')) - key) % 26 + ord('A')))

        elif c.islower(): #lowercase
            decrypted += chr((((ord(c) - ord('a')) - key) % 26 + ord('a')))

        elif c.isdigit(): #digit
            decrypted += str((int(c) - key) % 10)

        else:
            decrypted += c

    return decrypted

