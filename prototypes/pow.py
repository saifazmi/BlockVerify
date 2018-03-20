from hashlib import sha256


class ProofOfWork:

    def __init__(self, msg, complexity):
        self.msg = msg
        self.complexity = complexity
        self.guess_hash = None
        self.nonce = self.calc_pow()

    def __str__(self):
        return 'Level: {} // Nonce: {} / Hash: {}'.format(
            self.complexity, self.nonce, self.guess_hash
        )

    def calc_pow(self):
        proof = 0
        while self.valid_proof(proof) is False:
            proof += 1
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
    pow0 = ProofOfWork(message, 0)
    print(pow0)
    pow1 = ProofOfWork(message, 1)
    print(pow1)
    pow2 = ProofOfWork(message, 2)
    print(pow2)
    pow3 = ProofOfWork(message, 3)
    print(pow3)
    pow4 = ProofOfWork(message, 4)
    print(pow4)
    pow5 = ProofOfWork(message, 5)
    print(pow5)
    pow6 = ProofOfWork(message, 6)
    print(pow6)
