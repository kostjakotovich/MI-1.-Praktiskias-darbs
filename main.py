
import random
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QMessageBox
)

# --- 1 CILVĒKA DAĻA: IEVADE --- 
# Viss tika ielikts iekš GUI, lai spēle nestrādātu terminālī
if False:
    while True:
        izvele = input("Kurš uzsāks spēli? (1 - Cilvēks, 2 - Dators): ")
        if izvele == '1':
            sakuma_speletajs = "cilveks"
            break
        elif izvele == '2':
            sakuma_speletajs = "dators"
            break
        else:
            print("Kļūda: Lūdzu, ievadiet 1 vai 2!")


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

# --- 2 Spēles mehānikas realizācija --

def pick_number(number_list):
    while len(number_list) > 1:
        while True:
            try:
                index = int(input("Izvēleties skaitļa numuru:"))
                if 1 <= index < len(number_list):
                    kreisais_skaitlis = number_list[index-1]
                    labais_skaitlis = number_list[index]

                    skaitla_summa = kreisais_skaitlis + labais_skaitlis

                    if skaitla_summa > 7:
                        jauns_skaitlis = 1
                    elif skaitla_summa < 7:
                        jauns_skaitlis = 3
                    else:
                        jauns_skaitlis = 2

                    number_list.pop(index)
                    number_list.pop(index-1)

                    number_list.insert(index - 1, jauns_skaitlis)
                    print (f"You choose numbers: {kreisais_skaitlis} and {labais_skaitlis}, summary - {skaitla_summa}")

                    print("Jauns saraksts:", number_list)

                    break

                else:
                    print("Kļūda")
            except ValueError:
                print("Nepreizs inputs")

# --- 3 (Gustavs). CILVĒKA DAĻA: PUNKTU UN GĀJIENU LOĢIKA KĀ KLASE ---
class Spele:

    def __init__(self, virkne, sakuma_speletajs):
        self.virkne = virkne
        self.punkti = {"cilveks": 0, "dators": 0}
        self.pasreizejais_speletajs = sakuma_speletajs

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

number_list = [] # Pievienoju, lai varētu izpildīt GUI 
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

# --- Kristiāns Neško GUI

class SpeleGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skaitļu spēle")
        self.setMinimumSize(600, 400)

        self.sakuma_speletajs = None
        self.number_list = []

        self.show_start()

    def show_start(self):

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        title = QLabel("Skaitļu spēle")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)

        self.garums_input = QLineEdit()
        self.garums_input.setPlaceholderText("Virknes garums (15-25)")
        layout.addWidget(self.garums_input)

        row = QHBoxLayout()

        self.btn_cilveks = QPushButton("Cilvēks sāk")
        self.btn_cilveks.clicked.connect(lambda: self.set_start("cilvēks"))

        self.btn_dators = QPushButton("Dators sāk")
        self.btn_dators.clicked.connect(lambda: self.set_start("dators"))

        row.addWidget(self.btn_cilveks)
        row.addWidget(self.btn_dators)

        layout.addLayout(row)

        start = QPushButton("Sākt spēli")
        start.clicked.connect(self.start_game)
        layout.addWidget(start)

        self.error = QLabel("")
        layout.addWidget(self.error)

        central.setLayout(layout)

    def set_start(self, player):

        self.sakuma_speletajs = player

        if player == "cilvēks":
            self.btn_cilveks.setStyleSheet("background-color: lightgreen")
            self.btn_dators.setStyleSheet("")
        else:
            self.btn_dators.setStyleSheet("background-color: lightgreen")
            self.btn_cilveks.setStyleSheet("")

    def start_game(self):

        if not self.sakuma_speletajs:
            self.error.setText("Izvēlieties kurš sāk!")
            return

        try:
            garums = int(self.garums_input.text())
            if garums < 15 or garums > 25:
                raise ValueError
        except:
            self.error.setText("Ievadiet skaitli 15-25")
            return

        self.virkne = [random.randint(1, 9) for _ in range(garums)]
        self.punkti = {"cilvēks": 0, "dators": 0}
        self.speletajs = self.sakuma_speletajs

        self.show_game()

    def show_game(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        self.punkti_label = QLabel()
        layout.addWidget(self.punkti_label)

        self.speletajs_label = QLabel()
        layout.addWidget(self.speletajs_label)

        self.numbers_layout = QHBoxLayout()
        layout.addLayout(self.numbers_layout)

        new_game = QPushButton("Jauna spēle")
        new_game.clicked.connect(self.show_start)
        layout.addWidget(new_game)

        central.setLayout(layout)

        self.update_ui()

    def update_ui(self):

        self.punkti_label.setText(
            f"Cilvēks: {self.punkti['cilvēks']}    Dators: {self.punkti['dators']}"
        )

        self.speletajs_label.setText(f"Gājiens: {self.speletajs}")

        while self.numbers_layout.count():
            self.numbers_layout.takeAt(0).widget().deleteLater()

        for i, n in enumerate(self.virkne):

            btn = QPushButton(str(n))

            if i < len(self.virkne) - 1:
                btn.clicked.connect(lambda _, x=i: self.move(x))
            else:
                btn.setEnabled(False)

            self.numbers_layout.addWidget(btn)

    def move(self, i):

        a = self.virkne[i]
        b = self.virkne[i+1]
        summa = a + b

        if summa > 7:
            jauns = 1
            self.punkti[self.speletajs] += 1
        elif summa < 7:
            jauns = 3
            pretinieks = "dators" if self.speletajs == "cilvēks" else "cilvēks"
            self.punkti[pretinieks] -= 1
        else:
            jauns = 2
            self.punkti["cilvēks"] += 1
            self.punkti["dators"] += 1

        self.virkne.pop(i+1)
        self.virkne.pop(i)
        self.virkne.insert(i, jauns)

        self.speletajs = "dators" if self.speletajs == "cilvēks" else "cilvēks"

        if len(self.virkne) == 1:
            self.end_game()
            return

        self.update_ui()

    def end_game(self):

        c = self.punkti["cilvēks"]
        d = self.punkti["dators"]

        if c > d:
            msg = "Uzvar cilvēks"
        elif d > c:
            msg = "Uzvar dators"
        else:
            msg = "Neizšķirts"

        QMessageBox.information(self, "Beigas", msg)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SpeleGUI()
    window.show()

    sys.exit(app.exec())