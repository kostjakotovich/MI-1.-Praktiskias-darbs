import random
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import QTimer
import time

class Virsotne:
    def __init__(self, id, virkne, punkti, limenis, gajiens=None):
        self.id = id
        self.virkne = virkne[:]
        self.punkti = punkti.copy()
        self.limenis = limenis
        self.vertiba = None
        self.gajiens = gajiens

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

        child = Virsotne(berna_id, jauna_virkne, jaunie_punkti, limenis + 1, i)
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

def dabut_bernus_no_koka(koks, virsotne_id):
    berni = []
    for child_id in koks.loku_kopa.get(virsotne_id, []):
        child = atrast_virsotni(koks, child_id)
        if child is not None:
            berni.append(child)
    return berni

def notirit_vertibas_apakskoka(koks, virsotne_id):
    virsotne = atrast_virsotni(koks, virsotne_id)
    if virsotne is None:
        return

    virsotne.vertiba = None
    for child_id in koks.loku_kopa.get(virsotne_id, []):
        notirit_vertibas_apakskoka(koks, child_id)


def saskaitit_novertetas_virsotnes(koks, virsotne_id):
    virsotne = atrast_virsotni(koks, virsotne_id)
    if virsotne is None:
        return 0

    skaits = 1 if virsotne.vertiba is not None else 0
    for child_id in koks.loku_kopa.get(virsotne_id, []):
        skaits += saskaitit_novertetas_virsotnes(koks, child_id)

    return skaits

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

def alpha_beta_pa_koku(koks, virsotne_id, max_limenis, saknes_speletajs, alpha, beta):
    virsotne = atrast_virsotni(koks, virsotne_id)

    if virsotne is None:
        return None

    if virsotne.limenis == max_limenis or len(virsotne.virkne) == 1 or virsotne_id not in koks.loku_kopa:
        virsotne.vertiba = heiristiska_funkcija(virsotne.virkne, virsotne.punkti)
        return virsotne.vertiba

    if saknes_speletajs == "dators":
        ir_max = (virsotne.limenis % 2 == 0)
    else:
        ir_max = (virsotne.limenis % 2 == 1)

    berni = dabut_bernus_no_koka(koks, virsotne_id)

    if ir_max:
        vertiba = float("-inf")

        for berns in berni:
            berns_vertiba = alpha_beta_pa_koku(
                koks,
                berns.id,
                max_limenis,
                saknes_speletajs,
                alpha,
                beta
            )

            if berns_vertiba > vertiba:
                vertiba = berns_vertiba

            alpha = max(alpha, vertiba)
            if beta <= alpha:
                break

        virsotne.vertiba = vertiba
        return vertiba

    else:
        vertiba = float("inf")

        for berns in berni:
            berns_vertiba = alpha_beta_pa_koku(
                koks,
                berns.id,
                max_limenis,
                saknes_speletajs,
                alpha,
                beta
            )

            if berns_vertiba < vertiba:
                vertiba = berns_vertiba

            beta = min(beta, vertiba)
            if beta <= alpha:
                break

        virsotne.vertiba = vertiba
        return vertiba

def dabut_labako_gajienu_minimax(koks, saknes_id, saknes_speletajs, max_limenis):
    minimax_pa_koku(koks, saknes_id, max_limenis, saknes_speletajs)

    saknes_berni = koks.loku_kopa.get(saknes_id, [])
    if not saknes_berni:
        return None

    labakais_id = saknes_berni[0]
    labaka_vertiba = atrast_virsotni(koks, labakais_id).vertiba

    for child_id in saknes_berni[1:]:
        child = atrast_virsotni(koks, child_id)

        if child is None or child.vertiba is None:
            continue

        if saknes_speletajs == "dators":
            if child.vertiba > labaka_vertiba:
                labaka_vertiba = child.vertiba
                labakais_id = child_id
        else:
            if child.vertiba < labaka_vertiba:
                labaka_vertiba = child.vertiba
                labakais_id = child_id

    return atrast_virsotni(koks, labakais_id).gajiens

def dabut_labako_gajienu_alpha_beta(koks, saknes_id, saknes_speletajs, max_limenis):
    alpha_beta_pa_koku(koks, saknes_id, max_limenis, saknes_speletajs, float("-inf"), float("inf"))

    saknes_berni = koks.loku_kopa.get(saknes_id, [])
    if not saknes_berni:
        return None

    labakais_id = None
    labaka_vertiba = None

    for child_id in saknes_berni:
        child = atrast_virsotni(koks, child_id)

        if child is None or child.vertiba is None:
            continue

        if labakais_id is None:
            labakais_id = child_id
            labaka_vertiba = child.vertiba
            continue

        if saknes_speletajs == "dators":
            if child.vertiba > labaka_vertiba:
                labaka_vertiba = child.vertiba
                labakais_id = child_id
        else:
            if child.vertiba < labaka_vertiba:
                labaka_vertiba = child.vertiba
                labakais_id = child_id

    if labakais_id is None:
        return None

    return atrast_virsotni(koks, labakais_id).gajiens

class SpeleGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skaitlu spele")
        self.setMinimumSize(600, 400)

        self.sakuma_speletajs = None
        self.algoritms = None # pievienots prieks algoritma izvelei

        self.max_limenis = 3
        self.koks = None
        self.tekosa_virsotne = None

        self.kopa_generetas_virsotnes = 0
        self.kopa_novertetas_virsotnes = 0
        self.datora_gajienu_laiki = []

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

        start = QPushButton("Sakt speli")
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

        self.error.setText("")

        self.virkne = [random.randint(1, 9) for _ in range(garums)]
        self.punkti = {"cilveks": 0, "dators": 0}
        self.speletajs = self.sakuma_speletajs

        self.kopa_generetas_virsotnes = 0
        self.kopa_novertetas_virsotnes = 0
        self.datora_gajienu_laiki = []

        self.uzbuvet_jaunu_apakskoku()

        self.show_game()

        if self.speletajs == "dators":
            QTimer.singleShot(300, self.datora_gajiens)

    def datora_gajiens(self):
        if self.speletajs != "dators" or len(self.virkne) <= 1:
            return

        if self.koks is None or self.tekosa_virsotne is None:
            self.uzbuvet_jaunu_apakskoku()

        start_time = time.perf_counter()

        notirit_vertibas_apakskoka(self.koks, self.tekosa_virsotne.id)

        if self.algoritms == "minimax":
            gajiens = dabut_labako_gajienu_minimax(
                self.koks,
                self.tekosa_virsotne.id,
                self.speletajs,
                self.max_limenis
            )
        else:
            gajiens = dabut_labako_gajienu_alpha_beta(
                self.koks,
                self.tekosa_virsotne.id,
                self.speletajs,
                self.max_limenis
            )

        self.kopa_novertetas_virsotnes += saskaitit_novertetas_virsotnes(
            self.koks,
            self.tekosa_virsotne.id
        )

        elapsed = time.perf_counter() - start_time
        self.datora_gajienu_laiki.append(elapsed)

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
        b = self.virkne[i + 1]
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

        self.virkne.pop(i + 1)
        self.virkne.pop(i)
        self.virkne.insert(i, jauns)

        self.pariet_uz_bernu(i)

        self.speletajs = nakamais_speletajs(self.speletajs)

        if len(self.virkne) == 1:
            self.update_ui()
            self.end_game()
            return

        if self.tekosa_virsotne is None or self.tekosa_virsotne.limenis == self.max_limenis:
            self.uzbuvet_jaunu_apakskoku()

        self.update_ui()

        if self.speletajs == "dators":
            QTimer.singleShot(300, self.datora_gajiens)

    def uzbuvet_jaunu_apakskoku(self):
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
            self.max_limenis
        )

        self.tekosa_virsotne = self.root
        self.kopa_generetas_virsotnes += len(self.koks.virsotnu_kopa)

    def pariet_uz_bernu(self, gajiens):
        if self.koks is None or self.tekosa_virsotne is None:
            self.tekosa_virsotne = None
            return

        jaunais = None

        for child_id in self.koks.loku_kopa.get(self.tekosa_virsotne.id, []):
            child = atrast_virsotni(self.koks, child_id)
            if child is not None and child.gajiens == gajiens:
                if child.virkne == self.virkne and child.punkti == self.punkti:
                    jaunais = child
                    break

        self.tekosa_virsotne = jaunais

    def end_game(self):
        c = self.punkti["cilveks"]
        d = self.punkti["dators"]

        if c > d:
            msg = "Uzvar cilveks"
        elif d > c:
            msg = "Uzvar dators"
        else:
            msg = "Neizskirts"

        if self.datora_gajienu_laiki:
            videjais_laiks = sum(self.datora_gajienu_laiki) / len(self.datora_gajienu_laiki)
        else:
            videjais_laiks = 0

        print("----- SPELES STATISTIKA -----")
        print(f"Algoritms: {self.algoritms}")
        print(f"Sakuma speletajs: {self.sakuma_speletajs}")
        print(f"Uzvaretajs: {msg}")
        print(f"Genereto virsotnu skaits: {self.kopa_generetas_virsotnes}")
        print(f"Noverteto virsotnu skaits: {self.kopa_novertetas_virsotnes}")
        print(f"Videjais datora gajiena laiks: {videjais_laiks:.6f} s")
        print("----------------------------")

        stats = (
            f"\n\nĢenerēto virsotņu skaits: {self.kopa_generetas_virsotnes}"
            f"\nNovērtēto virsotņu skaits: {self.kopa_novertetas_virsotnes}"
            f"\nVidējais datora gājiena laiks: {videjais_laiks:.6f} s"
        )

        QMessageBox.information(self, "Beigas", msg + stats)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SpeleGUI()
    window.show()

    sys.exit(app.exec())
