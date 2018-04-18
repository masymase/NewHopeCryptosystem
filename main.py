import logging
import os
import sys
import hashlib
from logging import debug, warning, info

NEWHOPE_N = 1024      # Security level of 233 (sect. 1.3)
NEWHOPE_Q = 12289     # Smallest prime st. q = 1 (mod 2n) so that NTT can be realized efficiently (sect. 1.3)
NEWHOPE_K  =8         # Distribution of RLWE secret using centered binomial distribution of parameter k=8 (sect. 1.3)
SQUEEZE_BLOCK_SIZE = 168

def GenA(publicseed):

    debug("Generating the polynomial a_hat")
    a_hat = [0]*NEWHOPE_N   # Declare polynomial of size NEWHOPE_N

    debug("Initializing extseed")
    extseed = bytearray(33)
    extseed[0:31] = publicseed[0:31]

    debug("Starting loop")
    for i in range(0, (NEWHOPE_N//64)):
        ctr = 0
        extseed[32] = i
        state = hashlib.shake_128(extseed)
        while ctr < 64:
            buf = state.digest(SQUEEZE_BLOCK_SIZE*1)
            j = 0
            while (j<168) and (ctr<64):     # The algorithm has this in a for-loop, but this while loop is equivalent
                buf0 = int(buf[j])
                buf1 = (int(buf[j+1]) << 8) % (4294967296)      # 2^32 = 4294967296
                val = buf0|buf1
                if val<(5*NEWHOPE_Q):
                    a_hat[(64*i)+ctr] = val % NEWHOPE_Q
                    ctr += 1
                j += 2

    debug("Done computing a_hat of length: {}".format(len(a_hat)))
    return a_hat

def Sample(noiseseed, nonce):

    debug("Sampling a random polynomial in Rq")
    r = [0]*NEWHOPE_N   # Declare polynomial of size NEWHOPE_N

    debug("Initializing extseed and setting nonce ")
    extseed = bytearray(34)
    extseed[0:31] = noiseseed[0:31]
    extseed[32] = nonce

    debug("Starting loop")
    for i in range(0, (NEWHOPE_N//64)):     # Generate noise in lbocks of 64 coefficients
        extseed[33] = i
        buf = hashlib.shake_256(extseed).digest(128)
        for j in range(0, 64):
            a = buf[2*j]
            b = buf[(2*j)+1]
            r[(64*i)+j] = (bin(a).count("1") + NEWHOPE_Q - bin(b).count("1")) % NEWHOPE_Q

    debug("Done sampling random polynomial in Rq")
    return r

def PolyBitRev():
    # TODO:
    return

def NTT():
    # TODO:
    return

def PKEGen():

    debug("Generating the 32-byte random seed")
    seed = os.urandom(32)

    debug("Creating publicseed and noiseseed")
    z = hashlib.shake_256(seed).digest(64)
    publicseed = z[0:31]
    noiseseed = z[32:63]

    debug("Generating polynomial a_hat")
    a_hat = GenA(publicseed)

    debug("Sampling polynomial s")
    s = Sample(noiseseed, 0)
    debug("Computing s_hat = NTT of s")
    debug("Sampling polynomial e")
    debug("Computing e_hat = NTT of e")
    debug("Computing b_hat = a_hat dot s_hat + e_hat")
    debug("Computing public key pk")
    debug("Computing secret key sk")
    debug("Public key generation complete.")
    print("SUCCESS.\nPublic key: \nPrivate key: ")


def main():
    print("=============================================================================")
    print("========================== Starting PKE generation ==========================")
    print("=============================================================================")

    PKEGen()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if str(sys.argv[1]).lower() == "debug":
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    main()
