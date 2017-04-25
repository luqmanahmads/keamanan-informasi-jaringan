import binascii
import codecs

def string2bits(s=''):
    return ''.join(format(ord(x), 'b').zfill(8) for x in s)

def encrypt(string, key):
    k0 = key
    block = string

    # convert to binary
    bin_k0 = string2bits(k0)
    list_k0 = map(int, bin_k0)

    list_k1 = []
    for i in range(len(list_k0)):
        list_k1.append(list_k0[len(list_k0) - i - 1])

    bin_block = string2bits(block)
    list_block = map(int, bin_block)

    print "this is list of binary k0"
    print list_k0

    print "this is bin block map"
    print list_block

    # perform exclusicve bitwise or
    list_xor = []
    for i in range(len(list_k0)):
        # print (i, " ", list_k0[i]^list_block[i])
        list_xor.append(list_k0[i] ^ list_block[i])

    # addition modulo 2^64 with k1
    list_addition = []
    carry = 0
    for i in range(len(list_k1)):
        n = len(list_k1) - 1 - i
        s = list_xor[n] + list_k1[n]
        total = carry + s
        # print "n : ", n, "s : ", s , "carry : ", carry,"total : ", total
        if total == 0:
            list_addition.insert(0, 0);
            carry = 0
        elif total == 1:
            list_addition.insert(0, 1);
            carry = 0
        elif total == 2:
            list_addition.insert(0, 0);
            carry = 1
        elif total == 3:
            list_addition.insert(0, 1);
            carry = 1

    print "this is list xor"
    print list_xor

    print "this is list of binary k1"
    print list_k1

    print "this is list of addition"
    print list_addition

    # get the chiper text
    bin_chiper_text = ''.join(str(e) for e in list_addition)
    print bin_chiper_text
    n = int(bin_chiper_text, 2)
    print "n : ", n

    chiper_text = binascii.unhexlify('%x' % n)
    print chiper_text
    return chiper_text

def decrypt(string, key):
    k0 = key
    chiper_text = string

    # convert to binary
    bin_k0 = string2bits(k0)
    list_k0 = map(int, bin_k0)

    list_k1 = []
    for i in range(len(list_k0)):
        list_k1.append(list_k0[len(list_k0) - i - 1])

    # convert chiper text to binary
    bin_chiper_text = string2bits(chiper_text)
    list_chiper_text = map(int, bin_chiper_text)
    print "list of chiper text"
    print list_chiper_text

    # find inverse of k1
    list_inverse_k1 = []
    for i in range(len(list_k1)):
        if list_k1[i] == 0:
            list_inverse_k1.append(1);
        elif list_k1[i] == 1:
            list_inverse_k1.append(0);

    print "list inverse of k1"
    print list_inverse_k1

    # find list of one
    list_one = []
    for i in range(len(list_inverse_k1)):
        if i == 0:
            list_one.insert(0, 1)
        else:
            list_one.insert(0, 0)

    print "list one"
    print list_one

    # find additive inverse
    list_additive_inverse_k1 = []
    carry = 0
    for i in range(len(list_k1)):
        n = len(list_k1) - 1 - i
        s = list_one[n] + list_inverse_k1[n]
        total = carry + s
        # print "n : ", n, "s : ", s , "carry : ", carry,"total : ", total
        if total == 0:
            list_additive_inverse_k1.insert(0, 0);
            carry = 0
        elif total == 1:
            list_additive_inverse_k1.insert(0, 1);
            carry = 0
        elif total == 2:
            list_additive_inverse_k1.insert(0, 0);
            carry = 1
        elif total == 3:
            list_additive_inverse_k1.insert(0, 1);
            carry = 1

    print "additive inverse of k1"
    print list_additive_inverse_k1

    # perform addition a chipper text with additive inverse k1
    list_addition = []
    carry = 0
    for i in range(len(list_additive_inverse_k1)):
        n = len(list_additive_inverse_k1) - 1 - i
        s = list_chiper_text[n] + list_additive_inverse_k1[n]
        total = carry + s
        # print "n : ", n, "s : ", s , "carry : ", carry,"total : ", total
        if total == 0:
            list_addition.insert(0, 0);
            carry = 0
        elif total == 1:
            list_addition.insert(0, 1);
            carry = 0
        elif total == 2:
            list_addition.insert(0, 0);
            carry = 1
        elif total == 3:
            list_addition.insert(0, 1);
            carry = 1

    print "\nlist of addition"
    print list_addition

    print "list of k0"
    print list_k0

    # perform exlusive bitwise or with k0
    list_xor = []
    for i in range(len(list_additive_inverse_k1)):
        list_xor.append(list_k0[i] ^ list_addition[i])
    print "\nlist xor"
    print list_xor

    # get the plain text
    bin_plain_text = ''.join(str(e) for e in list_xor)
    n = int(bin_plain_text, 2)
    print "n : ", n

    plain_text = binascii.unhexlify('%x' % n)
    print "PLAIN TEXT :"
    print plain_text
    return plain_text

#=================================================
#----------------MAIN START HERE------------------
#=================================================

#define a key
key = 'abcdefgh'

#open input file
input_file =open('sample_file.txt', 'r')

#open output file
output_file = open('encrypted.txt', 'w')

#encrypting
data = ''
block = input_file.read(8)
counter = 0

#---------------
encrypted_text = ''

while block != '':
    counter = counter + 1
    print "this is block : >>"+block+"<<"
    if len(block)<8:
        n = 8 - len(block)
        for i in range(n):
            block = block + '0'
    chiper_text = encrypt(block, key)
    output_file.write(chiper_text)

    #--------------
    encrypted_text = encrypted_text + chiper_text

    block = input_file.read(8)

#decrypting

decrypted_text = ''
for i in range(0, len(encrypted_text), 8):
    block = encrypted_text[i:i+8]
    plain_text = decrypt(block, key)
    decrypted_text = decrypted_text + plain_text

print "counter : ", counter
print 'Encrypted >>',encrypted_text
print 'Decrypted >>',decrypted_text

input_file.close()
output_file.close()