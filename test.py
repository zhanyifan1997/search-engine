number=10
def test():
    global number
    number=5
    print(number)

print(number)
test();
print(number)