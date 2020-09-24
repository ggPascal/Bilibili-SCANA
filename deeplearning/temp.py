sum_list = []
sum_number = [1,2,3,4,5,6]
bigger_than_7 = 0
number_is_odd = 0
sum_all = 0

for a in sum_number:
    for b in sum_number:
        sum_result = a+b
        if sum_result > 7:
            bigger_than_7 += 1
        if sum_result % 2 != 0:
            number_is_odd += 1
        sum_all += 1

print(number_is_odd)
print(bigger_than_7)
print(sum_all)