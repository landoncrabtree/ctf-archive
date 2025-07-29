padding = 29 # longest line is 29 bits

qr = []
with open("qr_code.txt", "r") as file:
    for line in file:
        line = line.strip()
        line = int(line)
        line = bin(line)[2:]
        line = line.zfill(padding)
        #print(line)
        qr.append(line)

scale_factor = 2
black = "\33[40m  \33[0m"
white = "\33[47m  \33[0m"

for row in qr:
    print()
    for col in row:
        if col == "1":
            print(black, end="")
        else:
            print(white, end="")