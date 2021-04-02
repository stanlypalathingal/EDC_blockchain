def cipher_en(plain_text, key):
    encrypted = ""
    for c in plain_text:
        
        if c.isupper(): # uppercase 
            encrypted += chr(((ord(c) - ord('A')) + key) % 26 + ord('A'))

        elif c.islower(): #lowecase 
            encrypted += chr(((ord(c) - ord('a')) + key) % 26 + ord('a'))

        elif c.isdigit(): #digit
            encrypted += str(((int(c) + key) % 10))

        else: #anything else just leave it 
            encrypted += c

    return encrypted

