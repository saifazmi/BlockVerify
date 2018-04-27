from hashlib import sha256
from time import time
import datetime


class ProofOfWork:

    def __init__(self, msg, complexity):
        self.msg = msg
        self.complexity = complexity
        self.guess_hash = None
        self.work_time = 0
        self.nonce = self.calc_pow()


    def __str__(self):
        return 'Level: {} // Nonce: {} / Hash: {} / Time: {}'.format(
            self.complexity, self.nonce, self.guess_hash, self.work_time)

    def calc_pow(self):
        proof = 0
        start = time()
        while self.valid_proof(proof) is False:
            proof += 1
        self.work_time = str(datetime.timedelta(seconds=time() - start))
        return proof

    def valid_proof(self, proof):
        guess = f'{self.msg}{proof}'
        guess_hash = sha256(guess.encode('utf-8')).hexdigest()
        if guess_hash[:self.complexity] == '0'*self.complexity:
            self.guess_hash = guess_hash
            return True
        else:
            return False


if __name__ == '__main__':
    message = 'Quick Brown Fox'
    for i in range(8):
        proof_test = ProofOfWork(message, i)
        print(proof_test)

# Sample Result
# Level: 0 // Nonce: 0 / Hash: 6308fc91d51aa5485d6fadc1521dccbb244cc2d96c96d2f1c46b60165d612b57 / Time: 0:00:00.000009
# Level: 1 // Nonce: 5 / Hash: 0e96b4a007dde467477f6a1e6d8d865bf38233609b44deeacd551e7e32804773 / Time: 0:00:00.000011
# Level: 2 // Nonce: 29 / Hash: 009971193c288656774218ab1889a570f7cc1046a23c6fca62bb1f9e65053aa0 / Time: 0:00:00.000040
# Level: 3 // Nonce: 1491 / Hash: 000a1358ce0043164a7511df85fdf894b45e3db8136ee72b66687c8799787405 / Time: 0:00:00.002011
# Level: 4 // Nonce: 218535 / Hash: 0000871bee945747000e640d2a7911227634bdaea8abefa82d1e2e2e15ca4d05 / Time: 0:00:00.261109
# Level: 5 // Nonce: 267913 / Hash: 00000b3ed59edf0f435f829438beeee35afcabde59aa9f11e1967021b9485057 / Time: 0:00:00.323308
# Level: 6 // Nonce: 30073947 / Hash: 000000f134ace3209bb7b29a1ebe32fd9b03660ac15d288463980264bbaccee6 / Time: 0:00:35.917765
# Level: 7 // Nonce: 407042007 / Hash: 00000009051f5421dd36cd631a84c217186a4ff6801739bbceeb84264937e602 / Time: 0:08:01.755404
