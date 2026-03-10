
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


    def mainit_gajienu(self):
        if self.pasreizejais_speletajs == "cilveks":
            self.pasreizejais_speletajs = "dators"
        else:
            self.pasreizejais_speletajs = "cilveks"


    def radit_punktus(self):
        print(f"REZULTĀTS: Cilvēks {self.punkti['cilveks']} | Dators {self.punkti['dators']}")

    # Galvenā funkcija ko var izmantot pārējie
    def izpildit_gajienu(self, summa):
        print(f"\nGājienu veic: {self.pasreizejais_speletajs}")
        print(f"Pāra summa: {summa}")
        self.aprekinat_punktus(summa)
        self.radit_punktus()
        self.mainit_gajienu()
        print(f"--- Tagad gājienu veic: {self.pasreizejais_speletajs} ---")



# --- (K.Kotovičs). SPĒLES KOKS
class Virsotne:
    def __init__(self, id, virkne, punkti, limenis):
        self.id = id
        self.virkne = virkne[:]
        self.punkti = punkti.copy()
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
def pectecu_generesana(id, virkne, punkti, limenis):
    vecaku_id = id
    if limenis % 2 == 0:
        pasreizejais_speletajs = "cilveks"
        pretinieks = "dators"
    else:
        pasreizejais_speletajs = "dators"
        pretinieks = "cilveks"

    for i in range(len(virkne)-1):
        id += 1
        berna_id = id
        jauna_virkne = virkne[:]
        jaunie_punkti = punkti.copy()
        sk_summa = jauna_virkne[i]+jauna_virkne[i+1]

        if sk_summa > 7:
            jauna_virkne[i] = 1
            jaunie_punkti[pasreizejais_speletajs] += 1
        elif sk_summa < 7:
            jauna_virkne[i] = 3
            jaunie_punkti[pretinieks] -= 1
        else:
            jauna_virkne[i] = 2
            jaunie_punkti["cilveks"] += 1
            jaunie_punkti["dators"] += 1

        jauna_virkne.pop(i+1)

        child = Virsotne(berna_id, jauna_virkne, jaunie_punkti, limenis+1)

        koks.pievienot_virsotni(child)
        koks.pievienot_loku(vecaku_id, berna_id)
    return id



