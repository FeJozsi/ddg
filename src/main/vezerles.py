"""
This module is responsible for controlling the traversal of solution tree.
"""

from datetime import datetime, timedelta

from megoldasfa        import Megoldasfa
from dg_standard_input import dg_inreal, dg_inint


class Vezerles(Megoldasfa):                                         # 960. origin sor
    """
    This class represents the sixth level of sub-classes, often referred to
    as 'pseudo "black boxes"'.  
    Its primary responsibility lies in control.  
    The entire list of these mentioned levels includes:   
        Diszjunktiv_graf,  
        Diszjunktiv_graf_manipulacioi,  
        Szabad_elek__korlatozas_egy_gepen,  
        Finomitasok,  
        Megoldasfa,  
        Vezerles.  
    """
    kezdesi_ido: datetime

    def __init__(self, muveletszam: int, gepszam: int) -> None:
        super().__init__(muveletszam, gepszam)
        self.also_felso_korlat_megegyezik: bool = False
        self.idohiany: bool = False
        self.keresesi_stadiumban_tartunk = False
        self.maximalis_melysegszint: int = 0
        self.melyseghatar_eleresenek_szama: int = 0
        self.reached_max_solution_tree_depth: int = 1 # 2024.02.
        self.kiertekelesek_szama: int = 0
        self.visszalepesek_szama: int = 0
        self.ismetelt_korlatozasok_szama: int = 0
        self.sikeres_ismetelt_korlatozasok_szama: int = 0
        self.kezdesi_ido = datetime.now() # Record the start time
        self.futas_maximalis_ideje: float = 0.0
        self.feladat_also_korlatja: float = 0.0
        self.remenybeli_felso_korlat: float = 0.0

    def duration_in_seconds(self) -> float:
        duration: timedelta = datetime.now() - self.kezdesi_ido
        return duration.total_seconds()

    def megelozo_elemzes_mast_nem_mond(self) -> bool:
        if self.rigid_check_acyclicity(): # This test inserted at 2024.02.
            self.sorrendisegi_elek_nelkul_uthosszak_odafele()
            if self.cpm_veget_ert():
                self.viszonyitasi_alap = 1.0e+300
                self.feladat_also_korlatja  = self.osszes_gepen_valo_kezdeti_korlatozas_eredmenye()
                self.remenybeli_felso_korlat = self.feladat_also_korlatja * 1.18
                return True
        print("***** A techonológiai követelmények ellentmondásosak! *****")
        return False
    def vezerles_inicializalasa(self) -> None:
        self.kezdesi_ido = datetime.now() # Record the start time
        self.futas_maximalis_ideje = dg_inreal()
        self.maximalis_melysegszint = dg_inint()
        if dg_inint() > 0:
            self.info = True
        self.keresesi_stadiumban_tartunk = True
        # print("** Futás maximális ideje (sec), maximális mélységszint, lépésenkénti információ kérése **")
        # print((f"[{self.futas_maximalis_ideje}, {self.maximalis_melysegszint}, {self.info}]"))
    def vezerles_aktualizalasa(self) -> None:
        # if (datetime.datetime.now() - self.kezdesi_ido).total_seconds() > self.futas_maximalis_ideje and self.futas_maximalis_ideje > 0: # 2. tag: 2024.02.
        if  self.duration_in_seconds() > self.futas_maximalis_ideje and self.futas_maximalis_ideje > 0:
            self.idohiany = True
        if self.aktualis_optimalis_megvaltozott:
            self.viszonyitasi_alap_ujraallitasa()
            if self.viszonyitasi_alap <= self.remenybeli_felso_korlat:
                self.keresesi_stadiumban_tartunk = False
            if self.viszonyitasi_alap <= self.feladat_also_korlatja + 1.0e-10:
                self.also_felso_korlat_megegyezik = True
    def egyeb_ok_van_leallasra(self) -> bool:
        return self.idohiany or self.also_felso_korlat_megegyezik
    def megoldasfa_melyitheto(self) -> bool:
        self.reached_max_solution_tree_depth = max(self.reached_max_solution_tree_depth, len(self.ag)) # 2024.02.
        if len(self.ag) >= self.maximalis_melysegszint and self.maximalis_melysegszint > 0:  # 2. tag: 2024.02.
            self.melyseghatar_eleresenek_szama += 1
            return False
        return True
    def remenyteli_az_ismetelt_korlatozas(self) -> bool:
        return ( not self.keresesi_stadiumban_tartunk
                 and len(self.aktualis_szabad_elek()) > 5 )         # CARDINAL
    def informaciok_nyomtatasa(self) -> None:
        if self.also_felso_korlat_megegyezik:
            # print("* Alsó-, felső korlát megegyezik. *")
            print("**************  SUCCESS! We have founnd an optimal order for the operations on the machines.  **************")
            print("* The lower and upper bounds are equal. Therefore, the maximum critical path will be minimal in this case. *")
        if self.idohiany:
            print("**************  TIMEOUT! We halted the search as the runtime reached the configured maximum.  **************")
            # print("* Időhiány lépett föl. *")
        elif not self.also_felso_korlat_megegyezik:  # and self.maximalis_melysegszint: nem tűzhető ki, lásd az alábbi kommentblokkot!
            # print("* Normál befejeződés. *") # de nem biztos, hogy a legoptimálisabbhoz eljutottunk, mivel a megoldásfa elérhető maximális mélységszintje korlátozva volt
            print("******************* Normal termination. We traversed the entire solution tree we established.  *******************")
            print("*            We considered the necessity of further deepening at each step based on the current bound.           *")
            print("* It is uncertain whether we have found the optimal solution, even if the maximum depth is set to 0 (unlimeted). *")
        # else:   2 0 2 4-02-27 14:49:
        #     # print("* Normál befejeződés. *")    NEM JELENTHETŐ KI, MERT NEM JÁRJUK BE AZ ÖSSZES LEHETSÉGES MEGOLDÁST, VAGY LEGALÁBBIS NINCS(?!) BIZONYÍTVA, HOGY BEJÁRJUK (LEGALÁBB A RELEVÁNSAKAT). Legalább azt megtehetnénk, hogy a szabad élek közé (szabad_elek) felvennénk minden kritikus sorrendi élet (vagyis az összes olyat, amelynél bármilyen kicsi időtartam növelés a teljes kritikus úthosszat megnövelné).
        #     print("********************** Normal termination. We traversed the entire solution tree.  **********************")
        #     print("*              SUCCESS! We have founnd an optimal order for the operations on the machines.             *")
        print("   Eltöltött idő: "
            #   f"{1000 * (datetime.datetime.now() - self.kezdesi_ido).total_seconds():.3f} "
              f"{1000 * self.duration_in_seconds():.3f} "
              "ms (millisecond)")
        print(f"   Feladat kezdeti alsó korlátja: {self.feladat_also_korlatja:.2f}")
        print(f"   Kiértékelések száma: {self.kiertekelesek_szama:6}")
        print(f"   Megoldások    száma: {self.megoldasok_szama:6}")
        print(f"   Visszalépések száma: {self.visszalepesek_szama:6}")
        if self.ismetelt_korlatozasok_szama > 0:
            print(f"   Ismételt korlátozás: {self.ismetelt_korlatozasok_szama:6}")
            print(f"   Sikeres ism. korlát: {self.sikeres_ismetelt_korlatozasok_szama:6}")
        if self.maximalis_melysegszint > 0 and self.melyseghatar_eleresenek_szama > 0:
            print(f"   Mélységhatár elérésének száma: {self.melyseghatar_eleresenek_szama:6}")
        else:   # 2024.02.
            print(f"   Maximum solution-tree depth: {self.reached_max_solution_tree_depth:6}")
