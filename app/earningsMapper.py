import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split('\t')
    seller = ''
    price = 0
    count = 0
    for word in words:
        #print('%s\t1' % (word))
        count = count+1
        if(count == 4):
            seller = word
        if(count == 5):
            price = word
            print('%s\t%s' % (seller, price))