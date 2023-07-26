def KSA(key):
    key_length = len(key)
    # 初始化S盒
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        # 交换S[i]和S[j]
        S[i], S[j] = S[j], S[i]
    return S
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        # 交换S[i]和S[j]
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

    # 加密函数，返回加密后的字节流
def encrypt(key,data):
    data_length = len(data)
    keystream = PRGA(KSA(key))
    res = []
    for i in range(data_length):
        res.append(next(keystream) ^ data[i])
    return bytes(res)
    # 解密函数，返回解密后的字节流
def decrypt(key,data):
    return encrypt(key,data)