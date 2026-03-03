import random

start_array_length = input("Lūdzu ievadiet virknes garumu (no 15 līdz 25): ")
try:
    start_array_length = int(start_array_length)
except:
    print("Nepareiza ievade, lūdzu, ievadiet veselo skaitli.")

number_list = []
for i in range(0, start_array_length):
    number_list.append(random.randint(1, 9))

def print_list():
    for i in range(0, len(number_list)):
        print(number_list[i], end=" ")

print_list()
