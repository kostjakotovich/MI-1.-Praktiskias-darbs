
import random
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import QTimer

# --- 1 CILVĒKA DAĻA: IEVADE --- 
# Tika ielikta iekš GUI
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
        self.vertiba = None

class SpelesKoks:
    def __init__(self):
        self.virsotnu_kopa = []
        self.loku_kopa = dict()

    def pievienot_virsotni(self, virsotne):
        self.virsotnu_kopa.append(virsotne)

    def pievienot_loku(self, sakuma_virsotnes_id, beigu_virsotnes_id):
        if sakuma_virsotnes_id in self.loku_kopa:
            self.loku_kopa[sakuma_virsotnes_id].append(beigu_virsotnes_id)
        else:
            self.loku_kopa[sakuma_virsotnes_id] = [beigu_virsotnes_id]

def nakamais_speletajs(speletajs):
    return "dators" if speletajs == "cilveks" else "cilveks"

def heiristiska_funkcija(virkne, punkti):
    starpiba = punkti["dators"] - punkti["cilveks"]
    bonuss = 0

    if len(virkne) == 2 and virkne[0] + virkne[1] == 7:
        bonuss = 1

    return starpiba + bonuss

def generet_bernus(virkne, punkti, pasreizejais_speletajs):
    berni = []
    pretinieks = nakamais_speletajs(pasreizejais_speletajs)

    for i in range(len(virkne) - 1):
        jauna_virkne = virkne[:]
        jaunie_punkti = punkti.copy()
        sk_summa = jauna_virkne[i] + jauna_virkne[i + 1]

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

        jauna_virkne.pop(i + 1)

        berni.append((i, jauna_virkne, jaunie_punkti))

    return berni

def visu_apakskoku_generesana(koks, id, virkne, punkti, limenis, pasreizejais_speletajs, max_limenis):
    vecaku_id = id

    if limenis >= max_limenis or len(virkne) <= 1:
        return id

    for i in range(len(virkne) - 1):
        id += 1
        berna_id = id

        jauna_virkne = virkne[:]
        jaunie_punkti = punkti.copy()
        sk_summa = jauna_virkne[i] + jauna_virkne[i + 1]

        pretinieks = nakamais_speletajs(pasreizejais_speletajs)

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

        jauna_virkne.pop(i + 1)

        child = Virsotne(berna_id, jauna_virkne, jaunie_punkti, limenis + 1)
        koks.pievienot_virsotni(child)
        koks.pievienot_loku(vecaku_id, berna_id)

        id = visu_apakskoku_generesana(
            koks,
            berna_id,
            jauna_virkne,
            jaunie_punkti,
            limenis + 1,
            nakamais_speletajs(pasreizejais_speletajs),
            max_limenis
        )

    return id

def atrast_virsotni(koks, virsotnes_id):
    for v in koks.virsotnu_kopa:
        if v.id == virsotnes_id:
            return v
    return None


def minimax_pa_koku(koks, virsotne_id, max_limenis, saknes_speletajs):
    virsotne = atrast_virsotni(koks, virsotne_id)

    if virsotne is None:
        return None

    if virsotne.limenis == max_limenis or len(virsotne.virkne) == 1 or virsotne_id not in koks.loku_kopa:
        virsotne.vertiba = heiristiska_funkcija(virsotne.virkne, virsotne.punkti)
        return virsotne.vertiba

    if saknes_speletajs == "dators":
        max_limenis_paritate = (virsotne.limenis % 2 == 0)
    else:
        max_limenis_paritate = (virsotne.limenis % 2 == 1)

    bernu_vertibas = []
    for child_id in koks.loku_kopa[virsotne_id]:
        vertiba = minimax_pa_koku(koks, child_id, max_limenis, saknes_speletajs)
        bernu_vertibas.append(vertiba)

    if max_limenis_paritate:
        virsotne.vertiba = max(bernu_vertibas)
    else:
        virsotne.vertiba = min(bernu_vertibas)

    return virsotne.vertiba


def dabut_labako_gajienu_no_koka(koks, saknes_speletajs, max_limenis):
    minimax_pa_koku(koks, 0, max_limenis, saknes_speletajs)

    saknes_berni = koks.loku_kopa.get(0, [])
    if not saknes_berni:
        return None

    labakais_id = saknes_berni[0]
    labaka_vertiba = atrast_virsotni(koks, labakais_id).vertiba

    for child_id in saknes_berni[1:]:
        child = atrast_virsotni(koks, child_id)
        if saknes_speletajs == "dators":
            if child.vertiba > labaka_vertiba:
                labaka_vertiba = child.vertiba
                labakais_id = child_id
        else:
            if child.vertiba < labaka_vertiba:
                labaka_vertiba = child.vertiba
                labakais_id = child_id

    sakne = atrast_virsotni(koks, 0)
    saknes_berns = atrast_virsotni(koks, labakais_id)

    berni = generet_bernus(sakne.virkne, sakne.punkti, saknes_speletajs)
    for gajiens, b_virkne, b_punkti in berni:
        if b_virkne == saknes_berns.virkne and b_punkti == saknes_berns.punkti:
            return gajiens

    return None

def alpha_beta(virkne, punkti, speletajs, dzilums, max_dzilums, alpha, beta):
    if len(virkne) == 1 or dzilums == max_dzilums:
        return heiristiska_funkcija(virkne, punkti), None

    berni = generet_bernus(virkne, punkti, speletajs)

    if speletajs == "dators":
        vertiba = float("-inf")
        labakais_gajiens = None

        for gajiens, b_virkne, b_punkti in berni:
            b_vertiba, _ = alpha_beta(
                b_virkne,
                b_punkti,
                nakamais_speletajs(speletajs),
                dzilums + 1,
                max_dzilums,
                alpha,
                beta
            )

            if b_vertiba > vertiba:
                vertiba = b_vertiba
                labakais_gajiens = gajiens

            alpha = max(alpha, vertiba)
            if beta <= alpha:
                break

        return vertiba, labakais_gajiens

    else:
        vertiba = float("inf")
        labakais_gajiens = None

        for gajiens, b_virkne, b_punkti in berni:
            b_vertiba, _ = alpha_beta(
                b_virkne,
                b_punkti,
                nakamais_speletajs(speletajs),
                dzilums + 1,
                max_dzilums,
                alpha,
                beta
            )

            if b_vertiba < vertiba:
                vertiba = b_vertiba
                labakais_gajiens = gajiens

            beta = min(beta, vertiba)
            if beta <= alpha:
                break

        return vertiba, labakais_gajiens

# --- Kristiāns Neško GUI

class SpeleGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skaitlu spele")
        self.setMinimumSize(600, 400)

        self.sakuma_speletajs = None
        self.number_list = []
        self.algoritms = None # pievienots prieks algoritma izvelei

        self.show_start()

    def show_start(self):
        self.sakuma_speletajs = None
        self.algoritms = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        title = QLabel("Skaitlu spele")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)

        self.garums_input = QLineEdit()
        self.garums_input.setPlaceholderText("Virknes garums (15-25)")
        layout.addWidget(self.garums_input)

        row = QHBoxLayout()

        self.btn_cilveks = QPushButton("Cilveks sak")
        self.btn_cilveks.clicked.connect(lambda: self.set_start("cilveks"))

        self.btn_dators = QPushButton("Dators sak")
        self.btn_dators.clicked.connect(lambda: self.set_start("dators"))

        row.addWidget(self.btn_cilveks)
        row.addWidget(self.btn_dators)

        layout.addLayout(row)

        alg_row = QHBoxLayout()

        self.btn_minimax = QPushButton("MiniMax")
        self.btn_minimax.clicked.connect(lambda: self.set_algorithm("minimax"))

        self.btn_alphabeta = QPushButton("Alpha-Beta")
        self.btn_alphabeta.clicked.connect(lambda: self.set_algorithm("alphabeta"))

        alg_row.addWidget(self.btn_minimax)
        alg_row.addWidget(self.btn_alphabeta)

        layout.addLayout(alg_row)

        start = QPushButton("Sakt spele")
        start.clicked.connect(self.start_game)
        layout.addWidget(start)

        self.error = QLabel("")
        layout.addWidget(self.error)

        central.setLayout(layout)

    def set_start(self, player):

        self.sakuma_speletajs = player

        if player == "cilveks":
            self.btn_cilveks.setStyleSheet("background-color: lightgreen")
            self.btn_dators.setStyleSheet("")
        else:
            self.btn_dators.setStyleSheet("background-color: lightgreen")
            self.btn_cilveks.setStyleSheet("")

    def set_algorithm(self, algoritms):
        self.algoritms = algoritms

        if algoritms == "minimax":
            self.btn_minimax.setStyleSheet("background-color: lightgreen")
            self.btn_alphabeta.setStyleSheet("")
        else:
            self.btn_alphabeta.setStyleSheet("background-color: lightgreen")
            self.btn_minimax.setStyleSheet("")

    def start_game(self):

        if not self.sakuma_speletajs:
            self.error.setText("Izveleties kurs sak!")
            return

        if not self.algoritms:
            self.error.setText("Izveleties algoritmu!")
            return

        try:
            garums = int(self.garums_input.text())
            if garums < 15 or garums > 25:
                raise ValueError
        except:
            self.error.setText("Ievadiet skaitli 15-25")
            return

        self.virkne = [random.randint(1, 9) for _ in range(garums)]
        self.punkti = {"cilveks": 0, "dators": 0}
        self.speletajs = self.sakuma_speletajs

        self.show_game()

        if self.speletajs == "dators":
            QTimer.singleShot(300, self.datora_gajiens)

    def datora_gajiens(self):
        if self.speletajs != "dators" or len(self.virkne) <= 1:
            return

        if self.algoritms == "minimax":
            self.koks = SpelesKoks()
            self.root = Virsotne(0, self.virkne, self.punkti, 0)
            self.koks.pievienot_virsotni(self.root)

            visu_apakskoku_generesana(
                self.koks,
                0,
                self.virkne,
                self.punkti,
                0,
                self.speletajs,
                3
            )

            gajiens = dabut_labako_gajienu_no_koka(self.koks, self.speletajs, 3)

        else:
            _, gajiens = alpha_beta(
                self.virkne,
                self.punkti,
                self.speletajs,
                0,
                3,
                float("-inf"),
                float("inf")
            )

        if gajiens is not None:
            self.move(gajiens)

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

        new_game = QPushButton("Jauna spele")
        new_game.clicked.connect(self.show_start)
        layout.addWidget(new_game)

        central.setLayout(layout)

        self.update_ui()

    def update_ui(self):
        self.punkti_label.setText(
            f"Cilveks: {self.punkti['cilveks']}    Dators: {self.punkti['dators']}"
        )

        self.speletajs_label.setText(f"Gajiens: {self.speletajs}")

        while self.numbers_layout.count():
            self.numbers_layout.takeAt(0).widget().deleteLater()

        for i, n in enumerate(self.virkne):
            btn = QPushButton(str(n))

            if i < len(self.virkne) - 1 and self.speletajs == "cilveks":
                btn.clicked.connect(lambda _, x=i: self.move(x))
            else:
                btn.setEnabled(False)

            self.numbers_layout.addWidget(btn)

    def move(self, i):
        a = self.virkne[i]
        b = self.virkne[i+1]
        summa = a + b

        pretinieks = nakamais_speletajs(self.speletajs)

        if summa > 7:
            jauns = 1
            self.punkti[self.speletajs] += 1
        elif summa < 7:
            jauns = 3
            self.punkti[pretinieks] -= 1
        else:
            jauns = 2
            self.punkti["cilveks"] += 1
            self.punkti["dators"] += 1

        self.virkne.pop(i+1)
        self.virkne.pop(i)
        self.virkne.insert(i, jauns)

        self.speletajs = nakamais_speletajs(self.speletajs)

        if len(self.virkne) == 1:
            self.update_ui()
            self.end_game()
            return

        self.update_ui()

        if self.speletajs == "dators":
            QTimer.singleShot(300, self.datora_gajiens)

    def end_game(self):

        c = self.punkti["cilveks"]
        d = self.punkti["dators"]

        if c > d:
            msg = "Uzvar cilveks"
        elif d > c:
            msg = "Uzvar dators"
        else:
            msg = "Neizskirts"

        QMessageBox.information(self, "Beigas", msg)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SpeleGUI()
    window.show()

    sys.exit(app.exec())
