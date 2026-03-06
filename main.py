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


# mazliet savādāks variants

import random


while True:
    try:
        user_input = input("Lūdzu, ievadiet virknes garumu (no 15 līdz 25): ")
        array_length = int(user_input)
        
        if array_length >= 15 and array_length <= 25:
            break 
        else:
            print("Kļūda: Skaitlim jābūt robežās no 15 līdz 25!")
            
    except:
        
        print("Nepareiza ievade! Lūdzu, ievadiet veselu skaitli.")


number_list = []

for i in range(0, array_length):
    
    new_number = random.randint(1, 9)
    number_list.append(new_number)


print("Sākuma skaitļu virkne:")
print(number_list)
