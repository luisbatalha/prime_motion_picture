##
## Takes an image and finds a prime that looks like that image
## Usage: python get_prime.py [Image path] {image_width} {image_height}
##
## Miller-Rabin implementation code from: http://code.activestate.com/recipes/410681-rabin-miller-probabilistic-prime-test/
##

import math
import copy
import os
import random
from PIL import Image
import sys

def ipow(a,b,n):
    #calculates (a**b)%n via binary exponentiation, yielding itermediate
    #results as Rabin-Miller requires
    A = a = long(a%n)
    yield A
    t = 1
    while t <= b:
        t <<= 1

    #t = 2**k, and t > b
    t >>= 2

    while t:
        A = (A * A)%n
        if t & b:
            A = (A * a) % n
        yield A
        t >>= 1

def MillerRabinTest(test, possible):
    # Output:
    # - True if not prime
    # - False if the number can be prime
    return 1 not in ipow(test, possible-1, possible)

smallprimes = (3,5,7,11,13,17,19,23,29,31,37,41,43,
               47,53,59,61,67,71,73,79,83,89,97)

def test_prime(p, k=None):
    if k==None:
        bits = math.log(p,2)+1
        k = int(2*bits)

    for i in smallprimes:
        if p % i == 0:
            return False
    for i in xrange(k):
        if i>20:
            print ("These are likely to be prime, test ",i, "of", k)
        test = random.randrange(2, p)|1
        if MillerRabinTest(test, p):
            return False
    return True


if len(sys.argv)<=3:
    print ("Missing arguments, to use the script:",sys.argv[0],"[Image path] {width} {height}")
    exit()

#gets the real size of the image
basefn = sys.argv[1]
img = Image.open(basefn)
w,h = img.size

W,H = int(sys.argv[2]),int(sys.argv[3])

def convert_image(img,W,H):
    # converts image into a sequence of 1's and 8's
    w,h = img.size
    img = img.resize((W,H), Image.ANTIALIAS)

    img = img.convert('L')
    avr = sum(img.getdata()) / (W*H)
    bw = img.point(lambda x: 0 if x<avr else 255,'1')
    ps ="".join( map( lambda c: "1" if c>128 else "8",bw.getdata()))
    ps = ps[:-1]+"1"
    # prints the image as a sequence of 1's and 8's
    print ("The image will look like this (warning: this number is not prime yet!).")
    for i in range(H):
      print (ps[i*W: i*W+W])
    return ps

def change(ps):
    #changes a random position in the image
    ran_pos = random.randrange(len(ps))
    c = ps[ran_pos]
    if c == "1":
       n = "7"
    else:
       n = random.choice(["0","9","6","4","5","2","3"])
    newps = ps[:ran_pos-1] + n + ps[ran_pos:]
    return newps

def find_prime(ps):
    #does random changes until a prime is found
    if test_prime(int(ps),50):
        return ps
    i = 1
    print ("Finding Prime")
    while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        if (i%50)==0:
          print (" ")
        i+=1
        P = change(ps)
        if test_prime(int(P),50):
            return P

if __name__ == "__main__":
    number_image = convert_image(img,W,H)
    prime_image = find_prime(number_image)
    print ("PRIME FOUND!")
    for i in range(H):
      print (prime_image[i*W: i*W+W])
