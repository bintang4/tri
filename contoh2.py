import string
import random,sys
def random_(y):
 randomchoi ='0123456789'
 return ''.join(random.choice(randomchoi) for x in range(y))

i = 1
while i <= 50000:
 i += 1
 ss = "+1"+random_(10)
 cok = open("gnmbr.txt", "a")
 cok.write(ss+"\n")
 cok.close()
print("Sudah Selesai")
