import gnupg

'''
Documentation for the library
Github: https://github.com/isislovecruft/python-gnupg
PyPi: https://pypi.python.org/pypi/gnupg

From what I can tell, this seems to only work with GPG1
'''

# Initialise GPG with binary, home and key db
gpg = gnupg.GPG(binary="/usr/bin/gpg1",
                homedir="./keys",
                keyring="pubring.gpg",
                secring="secring.gpg")

# Create a batch file for unattended key generation
batch_key_input = gpg.gen_key_input(key_type="RSA",
                                    key_length=1024,
                                    name_real="Saif Azmi",
                                    name_email="saif@azmi.com")

# Print the batch input for key
print(batch_key_input)

# Generate key and print its fingerprint
key = gpg.gen_key(batch_key_input)
print(key.fingerprint)

# Encrypt and decrypt a message using the freshly generated key
message = "The crow flies at midnight."
encrypted = str(gpg.encrypt(message, key.fingerprint))
decrypted = str(gpg.decrypt(encrypted))
print(decrypted == message)
