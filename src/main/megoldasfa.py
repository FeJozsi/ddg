"""
This module serves the solution tree.
"""
from typing import List

from finomitasok                    import Finomitasok
from dg_link                        import DgLink, dg_link_elements, dg_out
from diszjunktiv_graf_manipulacioi  import El


class Megoldascsucs(DgLink):
    """
    This class represents a "leaf" (node) of the solution tree.  
    """
    def __init__(self) -> None:
        super().__init__()
        self.szabad_elek: List[El] = []
        self.sorszam: int = 0
    def __repr__(self) -> str:
        if self.sorszam == 0:
            return super().__repr__()
        return f"{self.sorszam}. sorszámú Megoldascsucs"

class Megoldasfa(Finomitasok):                                      # 900. origin sor
    """
    This class represents the fifth level of sub-classes, often referred to
    as 'pseudo "black boxes"'.  
    Its primary responsibility to serve the "body" of the solution tree.  
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
        self.megoldasok_szama: int = 0
        self.ag: List[Megoldascsucs] = []    # It will be replaced soon

    def init_megoldascsucs(self, mcs: Megoldascsucs) -> None:
        self.megoldasok_szama += 1
        mcs.sorszam = self.megoldasok_szama
    def aktualis_megoldascsucs(self) -> Megoldascsucs: # feltételezi, hogy van már! Igen, mindig van, a root-nak mondott megoldás.
        return self.ag[-1]                                          # LAST
    def aktualis_szabad_elek(self) -> List[El]:
        return self.aktualis_megoldascsucs().szabad_elek
    def szabad_elek_valasztasi_sorrendjukben_valo_felsorolasa(self) -> None:
        self.kritikus_ut_odafele()      #  2024.02. ??? utóbb/utólag beszúrva. Lehet, hogy felesleges, mert mikor ideérünk, előtte megfutott már?
        self.kritikus_uthosszak_visszafele()
        self.felsorakoztatas(self.aktualis_szabad_elek())   # nem hiányzik egy clear() az átadott paraméter List-re???
    def gyokeret_megoldasfaba(self) -> None:
        self.ag = []
        mcs: Megoldascsucs = Megoldascsucs()
        self.init_megoldascsucs(mcs)
        self.ag.append(mcs)
        dg_link_elements(self.ag)              # INTO
        self.fixalt_elek = []
        self.aktualis_opt_atfutasi_ido = 1.0e+300
    def van_szabad_el(self) -> bool:
        return len(self.aktualis_szabad_elek()) > 0                 # CARDINAL
    def uj_megoldas_illesztese_megoldasfara(self) -> None:
        if not self.aktualis_szabad_elek()[0].is_linked() and self.aktualis_szabad_elek()[0].head: # 2024-02-27 09:23
            assert self.aktualis_szabad_elek()[0].is_linked() or not self.aktualis_szabad_elek()[0].head, (
                'Alert uj_megoldas_illesztese_megoldasfara! Link is wrong.'
            )
        self.el_konjugalasaval_uj_megoldas(self.aktualis_szabad_elek()[0])    # FIRST
        mcs: Megoldascsucs = Megoldascsucs()
        self.init_megoldascsucs(mcs)
        self.ag.append(mcs)
        dg_link_elements(self.ag)              # INTO
        if self.info:
            print(f"*** {self.aktualis_megoldascsucs().sorszam:6}. megoldásra lép ***")
    def gyokerben_vagyok(self) -> bool:
        return len(self.ag) == 1                                    # CARDINAL
    def visszalepes(self) -> None:
        self.elek_visszaallitasaval_regi_sorrend()
        dg_out(self.ag, self.aktualis_megoldascsucs())              # OUT
        if self.info:
            print(f"--> Visszalépés {self.aktualis_megoldascsucs().sorszam:6}. megoldásra ***")
    # def drop_used_free_edge(self) -> None: # 2024.02.        Erre régen (SIMULA) nem volt valóban szükség, mert a fixált élek közé kerülés automatikusan kivette a LINK elemet a szabad élek közül; így viszont most már, az új DbLink osztállyal itt sem lehet rá szükség!
    #     # self.ag[-1].szabad_elek = self.ag[-1].szabad_elek[1:]       # OUT (OUT FIRST)
    #     # dg_link_elements(self.ag[-1].szabad_elek)
    #     if self.ag[-1].szabad_elek:                                 # Ez nagyon is lehet, mert a SIMULA-ban is, és most (2 0 2 4-02-27 12:02:40) újfent, a fix élek közé rakással egy lépésben kikerült a szabad élek közül.
    #         self.ag[-1].szabad_elek[0].head.out_first() # 2 0 2 4-02-27 10:56  ez még mindig nem a végleges megoldás, a szabad_elek listája egy  head-be  kellene burkolva legyen
