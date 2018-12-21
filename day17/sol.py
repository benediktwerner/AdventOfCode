INPUT = 370

curr_pos = 0
pos_zero = 0
length = 1
val_after_zero = None

for i in range(1, 50000001):
    curr_pos = ((curr_pos + INPUT) % length) + 1
    length += 1
    if curr_pos < pos_zero:
        pos_zero += 1
    if curr_pos == (pos_zero + 1) % length:
        val_after_zero = i

##print(output[curr_pos-5:curr_pos+5])
##print(output[curr_pos+2])
print(val_after_zero)
