import sys

earnings={}

for line in sys.stdin:
    line = line.strip()
    seller, price = line.split('\t', 1)
    try:
        price = int(price)
        earnings[seller] = earnings.get(seller, 0)+ price
    except ValueError:
        pass

for word in earnings:
    print('%s\t%s'% (word, earnings[word]))