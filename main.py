# import random

# start_array_length = input("Lūdzu ievadiet virknes garumu (no 15 līdz 25): ")
# try:
#     start_array_length = int(start_array_length)
# except:
#     print("Nepareiza ievade, lūdzu, ievadiet veselo skaitli.")

# number_list = []
# for i in range(0, start_array_length):
#     number_list.append(random.randint(1, 9))

# def print_list():
#     for i in range(0, len(number_list)):
#         print(number_list[i], end=" ")

# print_list()


import random

# --- 1 CILVĒKA DAĻA: IEVADE ---
while True:
    try:
        user_input = input("Lūdzu, ievadiet virknes garumu (no 15 līdz 25): ")
        array_length = int(user_input)
        if 15 <= array_length <= 25:
            break 
        else:
            print("Kļūda: Skaitlim jābūt robežās no 15 līdz 25!")
    except ValueError:
        print("Nepareiza ievade! Lūdzu, ievadiet veselu skaitli.")

# Ģenerēšana (Pievienoju šo daļu, lai varētu testēt punktu loģiku)
number_list = [random.randint(1, 9) for _ in range(array_length)]
print(f"\nSākuma skaitļu virkne: {number_list}")


# --- 3 (Gustavs). CILVĒKA DAĻA: PUNKTU UN GĀJIENU LOĢIKA KĀ KLASE ---
class Spele:
    def __init__(self, virkne):
        self.virkne = virkne
        self.punkti = {"cilveks": 0, "dators": 0}
        self.pasreizejais_speletajs = "cilveks"

    def aprekinat_punktus(self, summa):

        if self.pasreizejais_speletajs == "cilveks":
            pretinieks = "dators"
        else:
            pretinieks = "cilveks"
        
        if summa > 7:
            self.punkti[self.pasreizejais_speletajs] += 1
        elif summa < 7:
            self.punkti[pretinieks] -= 1
        else:
            self.punkti["cilveks"] += 1
            self.punkti["dators"] += 1
        
        self.radit_punktus()

    def mainit_gajienu(self):
        if self.pasreizejais_speletajs == "cilveks":
            self.pasreizejais_speletajs = "dators"
        else:
            self.pasreizejais_speletajs = "cilveks"
        print(f"--- Tagad gājienu veic: {self.pasreizejais_speletajs} ---")

    def radit_punktus(self):
        print(f"REZULTĀTS: Cilvēks {self.punkti['cilveks']} | Dators {self.punkti['dators']}")


game = Spele(number_list)



# --- TESTA BLOKS ---
print("\n--- TESTA SĀKUMS ---")
game.aprekinat_punktus(10) # Cilvēks saņem 1
game.mainit_gajienu()
game.aprekinat_punktus(4)  # Cilvēks zaudē 1 (jo dators gāja un summa < 7)


# Apraksts:

# Izveidoju klasi - "Spele" datu strukturētai glabāšanai ( jo bija obigāta prasība).

# Uzstaisīju punktu skaitīšanas loģiku:

# Summa > 7: spēlētājam +1 punkts.

# Summa < 7: pretiniekam -1 punkts.

# Summa = 7: abiem spēlētājiem +1 punkts.

# Izstrādju funkciju mainit_gajienu().

# Pievienoju radit_punktus().

# Loretas kodā pievienoju testa bloku pārbaudei.

# --- (K.Kotovičs). SPĒLES KOKS
class Virsotne:
    def __init__(self, id, virkne, punkti, limenis):
        self.id = id
        self.virkne = virkne[:]
        self.punkti = punkti.copy
        self.limenis = limenis

class SpelesKoks:
    def __init__(self):
        self.virsotnu_kopa = []
        self.loku_kopa = dict()

    def pievienot_virsotni(self, Virsotne):
        self.virsotnu_kopa.append(Virsotne)

    def pievienot_loku(self, sakuma_virsotnes_id, beigu_virsotnes_id):
        if sakuma_virsotnes_id in self.loku_kopa:
            self.loku_kopa[sakuma_virsotnes_id].append(beigu_virsotnes_id)
        else:
            self.loku_kopa[sakuma_virsotnes_id] = [beigu_virsotnes_id]

koks = SpelesKoks()

root = Virsotne(0, number_list, {"cilveks": 0, "dators": 0}, 0)
koks.pievienot_virsotni(root)

# Bloku apakšā var izmantot kad veidosies spēles gājieni. Virsotņu pievienošanai, visu pēcteču ģenerēšana

def pectecu_generesana():
    for i in range(len(virkne)-1):
        id += 1
        jauna_virkne = virkne[:]
        jaunie_punkti = punkti.copy
        sk_summa = virkne[i]+virkne[i+1]

        if sk_summa > 7:
            jauna_virkne[i] = 1
        elif sk_summa < 7:
            jauna_virkne[i] = 3
        else:
            jauna_virkne[i] = 2

        jauna_virkne.pop(i+1)

        child = Virsotne(id, jauna_virkne, jaunie_punkti, gajienu_skaits+1)
        koks.pievienot_virsotni(child)
