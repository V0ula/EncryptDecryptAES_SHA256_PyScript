from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random, sys, pkg_resources

def encrypt(key, file):
    chunksize = 64*1024
    outputFile = "(encrypted)"+file
    filesize = str(os.path.getsize(file)).zfill(16)
    IV = ''

    for i in range(16):
        IV += chr(random.randint(0, 0xFF))

    encyptor = AES.new(key, AES.MODE_CBC, IV)

    with open(file, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize)
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - (len(chunk) % 16))
                
                outfile.write(encyptor.encrypt(chunk))

def decrypt(key, file):
    chunksize = 64*1024
    outputFile = file[11:]

    with open(file, 'rb') as infile:
        filesize = long(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()

def main():
    choice = raw_input("Would you like to (E)ncrypt or (D)ecrypt?: ")

    if choice == 'E':
        file = raw_input("File to encrypt:")
        password = raw_input("Password: ")
        encrypt(getKey(password), file)
        print("Done!")
    elif choice == 'D':
        file = raw_input("File to decrypt: ")
        password = raw_input("Password: ")
        decrypt(getKey(password), file)
        print("Done!")
    else:
        print("No option selected, closing ..")
        sys.exit()

if __name__ == '__main__':
    main()
