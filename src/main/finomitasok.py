"""
This module contains of refinements.
"""

from typing import List, cast

from diszjunktiv_graf import Muveletcsucs
from szabad_elek__korlatozas_egy_gepen import Szabad_elek__korlatozas_egy_gepen

class Finomitasok(Szabad_elek__korlatozas_egy_gepen):               # 800. origin sor
    """
    This class represents the fourth level of sub-classes, often referred to
    as 'pseudo "black boxes"'.  
    Its primary responsibility to add additional functionalities (refinements).  
    The entire list of these mentioned levels includes:   
        Diszjunktiv_graf,  
        Diszjunktiv_graf_manipulacioi,  
        Szabad_elek__korlatozas_egy_gepen,  
        Finomitasok,  
        Megoldasfa,  
        Vezerles.  
    """
    def __init__(self, muveletszam: int, gepszam: int) -> None:
        super().__init__(muveletszam, gepszam)
        self.viszonyitasi_alap: float = 0.0
        self.kisk: float = 0.0
        self.nagyk: float = 0.0
        self.aktualis_optimalis_megvaltozott: bool = False
    def kiertekeles(self) -> None:
        self.kritikus_ut_odafele()
        assert self.nyelo
        if self.info:
            print("A kiertekeles() során elért kritikus úthossz "
                  f"(nyelo.forrastol1): {self.nyelo.forrastol1:.2f}")
        if self.nyelo.forrastol1 < self.aktualis_opt_atfutasi_ido:
            self.aktualis_optimalis_megoldas_atirasa()
            self.aktualis_optimalis_megvaltozott = True
        else: self.aktualis_optimalis_megvaltozott = False
    def korlatozas(self, korlatozas_sikeres: bool) -> bool:
        segedkisk: float = 0.0
        segednagyk: float = 0.0
        j: int = -1 # 0 helyett, igazodva a belső indexeléshez!
        self.sorrendisegi_elek_nelkul_uthosszak_odafele()
        self.sorrendisegi_elek_nelkul_uthosszak_visszafele()
        assert self.nyelo
        self.kisk = self.nagyk = self.nyelo.forrastol1
        if self.kisk > self.viszonyitasi_alap - 1.0e-10:            # nagyobb egyenlő (>=)  (vö. origin 470. sorral!)
            korlatozas_sikeres = True
        while not korlatozas_sikeres and j < self.gepszam - 1: # -1, igazodva a belső indexeléshez!
            j += 1
            if self.gep_muveletszama[j] >= 2:
                in_out_attr: List[float] = [segedkisk, segednagyk]
                self.gepen_korlatozas(j, in_out_attr)
                segedkisk = in_out_attr[0]
                segednagyk = in_out_attr[1]
                if segedkisk > self.kisk:
                    self.kisk = segedkisk
                    if self.kisk > self.viszonyitasi_alap - 1.0e-10:
                        korlatozas_sikeres = True
                self.nagyk = max(self.nagyk, segednagyk)
        if self.info:
            print(f"korlatozas_sikeres: {korlatozas_sikeres}, "
                  f"kisk: {self.kisk:.2f}, nagyk: {self.nagyk:.2f}, j: {j}, "
                  "viszonyitasi_alap: {:.2f}".format(0 
                                                     if self.viszonyitasi_alap >= 1.0e+299
                                                     else self.viszonyitasi_alap))
        return korlatozas_sikeres
    def aktualis_optimalis_megoldas_nyomtatasa(self) -> None:
        smuv: Muveletcsucs | None = None
        self.megmaradt_fixalt_elek_eltavolitasa()
        self.aktualis_optimalis_sorrend_visszaallitas()
        self.kritikus_ut_odafele()
        self.kritikus_uthosszak_visszafele()
        for k in range(self.gepszam):
            smuv = self.muvelet[self.gep_elso_muvelete[k]]
            while smuv.gepen_elozo is not None:
                smuv = smuv.gepen_elozo
            print(f"* {k+1}. gépen a műveletek sorrendje *")
            print("** Azon. Forrás  Időtart.   Nyelő **")
            while smuv is not None:
                print(f"{smuv.azonosito:6} {smuv.forrastol1:8.2f} "
                      f"{smuv.idotartam:8.2f} {smuv.nyeloig2:8.2f}")
                smuv = cast(Muveletcsucs, smuv.gepen_koveto)
        # print("* Átfutási idő: {:8.2f}, végső alsó korlát (viszonyitasi_alap): {:8.2f} *".format(self.nyelo.forrastol1, self.viszonyitasi_alap))
        assert self.nyelo
        print(f"* Átfutási idő: {self.nyelo.forrastol1:8.2f} *")
    def viszonyitasi_alap_ujraallitasa(self) -> None:
        self.viszonyitasi_alap = self.aktualis_opt_atfutasi_ido - 1.0e-10
    def osszes_gepen_valo_kezdeti_korlatozas_eredmenye(self) -> float:
        seged: bool = False
        # sreal: float = self.viszonyitasi_alap
        # self.viszonyitasi_alap = 1.0e+300
        self.korlatozas(seged)
        # self.viszonyitasi_alap = sreal
        return self.kisk
