"""
This module manages the 'free edges' in the Disjunctive Graph
and establishes limits using a single machine.
"""
from typing import List, Sequence, cast

from dg_link import dg_first, dg_link_elements, dg_out # DgLink,

from diszjunktiv_graf import Muveletcsucs
from diszjunktiv_graf_manipulacioi import Diszjunktiv_graf_manipulacioi, El

# from dg_main import print_cp, print_fixed_edges, print_free_edges  cirkulális betöltési hibát okozna

class Szabad_elek__korlatozas_egy_gepen(Diszjunktiv_graf_manipulacioi): # 600. origin sor
    """
    This class represents the third level of sub-classes, often referred to
    as 'pseudo "black boxes"'.  
    It manages the 'free edges' in the Disjunctive Graph and establishes
    limits using a single machine.  
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
        self.info = False
    def felsorakoztatas(self, fej: Sequence[El]):  # nem hiányzik egy clear() a fej List-re?  # List[DgLink]
        kritikus_muvelet: Muveletcsucs
        megelozo_muvelet: Muveletcsucs
        a: float = 0.0; b: float = 0.0; c: float = 0.0
        szabad_el: El

        if self.info:  # 2024.02.
            print("---------- Szabad_elek__korlatozas_egy_gepen.felsorakoztatas() előtt -----------------")     #  These four rows are just for test purpose
            # self.print_free_edges(fej)           It is always empty here
            self.print_fixed_edges(self.fixalt_elek)
            self.print_cp()

        assert self.nyelo
        assert self.nyelo.kritikus_elozo
        kritikus_muvelet = self.nyelo.kritikus_elozo
        while kritikus_muvelet != self.forras:                      # ???!!! Diszjunktiv_graf.kritikus_ut_odafele()-re vonatkozik az alábbi:
            if kritikus_muvelet.kritikus_elozo_sorrendi:            # ITT KULCSMOZZANAT VAN! Ne mondjam, hogy a kritikus_elozo sorrendi, ha nem csak a sorrendről szól a dolog, hanem a szimpla technológiai gráf már maga megköveteli az adott egymásra következést. Kritikus útban vagyunk, tehát, a két művelet között más út nem lehet. Következésképpen nem sorrendi, ha megelőzók/rákövetkező viszonylatban egyik a másikra hivatkozik!
                assert kritikus_muvelet.kritikus_elozo
                megelozo_muvelet = kritikus_muvelet.kritikus_elozo
                a = self.masodik_ut_forrastol(kritikus_muvelet) - kritikus_muvelet.forrastol1
                b = self.masodik_ut_nyeloig(megelozo_muvelet) - megelozo_muvelet.nyeloig2
                c = kritikus_muvelet.idotartam + megelozo_muvelet.idotartam + a + b
                a = max(a, b) # if a < b: a = b
                a = max(a, c) # if a < c: a = c
                szabad_el = El(megelozo_muvelet, kritikus_muvelet)
                szabad_el.delta = a
                szabad_el.behelyezes(fej)
                kritikus_muvelet = megelozo_muvelet
            else:
                assert kritikus_muvelet.kritikus_elozo
                kritikus_muvelet = kritikus_muvelet.kritikus_elozo

        if self.info:  # 2024.02. (bővítve)
            # print("---------- Után")     #  These four rows are just for test purpose
            # self.print_cp()               It does not changed
            self.print_free_edges(cast(List[El], fej))
            # self.print_fixed_edges(self.fixalt_elek)  It does not changed
        # if self.info: print("Szabad él felsorakoztatás megtörtént. Új darabszámuk: {}".format(len(fej)))
                                                                    # CARDINAL  634. origin sor
    def gepen_korlatozas(self, j: int, in_out_attr: List[float]):   # j a kérdéses gép belső azonosítója
        also: float = in_out_attr[0]
        felso: float = in_out_attr[1]
                                                                    # 639. origin sor: (1) comment jelű blokk kezdete
        fej: List[Muveletcsucs] = [] # Ez legyen diszjunkt lista más listákhoz képest!     #: Muveletcsucs LIST
        tag: Muveletcsucs | None = None; tag1: Muveletcsucs = Muveletcsucs() # tag1 will be replaced soon
        kulcsszam: float = 0.0; max_ut: float = 0.0; becsles: float = 0.0; min_kieg: float = 0.0; seged: float = 0.0
        k: int = 0                                                  # 646. origin sor: (2) comment jelű blokk kezdete
        link_index: int = 0
        for k in range(self.gep_elso_muvelete[j], self.gep_elso_muvelete[j] + self.gep_muveletszama[j]): #  - 1 hozzáadása nem kell a range felső határához, mert az maga nyiott felső határú
            tag = cast(Muveletcsucs, dg_first(fej))                 # FIRST
            link_index = 0
            while False if tag is None else tag.nyeloig2 > self.muvelet[k].nyeloig2:
                link_index += 1
                assert tag
                tag = cast(Muveletcsucs, tag.suc)
            if tag is None:
                fej.append(self.muvelet[k])                         # INTO
            else: fej.insert(link_index, self.muvelet[k])           # PRECEDE(tag)
            dg_link_elements(fej)
        while len(fej) > 0:                                         # EMPTY (NOT EMPTY)
            tag = fej[0]                                            # 662. origin sor: (3) comment jelű blokk kezdete; FIRST
            seged = tag.forrastol1
            tag1 =tag
            tag = cast(Muveletcsucs, tag.suc)
            while tag is not None:
                if seged > tag.forrastol1:
                    seged = tag.forrastol1
                    tag1 = tag
                tag = cast(Muveletcsucs, tag.suc)
            dg_out(fej, tag1)                                       # OUT
            kulcsszam = tag1.forrastol1 + tag1.idotartam
            min_kieg = tag1.nyeloig2
            seged = kulcsszam +tag1.nyeloig2
            if max_ut < seged:
                max_ut = becsles = seged
            elif becsles < seged: becsles = seged
            tag = dg_first(fej)                                     # 686. origin sor; FIRST
            while False if tag is None else tag.forrastol1 > kulcsszam:
                tag = tag.suc
            while tag is not None:
                dg_out(fej, tag)                                    # OUT
                kulcsszam += tag.idotartam
                max_ut = max(max_ut, kulcsszam + tag.nyeloig2)
                min_kieg = min(min_kieg, tag.nyeloig2)
                becsles = max(becsles, kulcsszam + min_kieg)
                tag = dg_first(fej)                                 # 704. origin sor; FIRST
                while False if tag is None else tag.forrastol1 > kulcsszam:
                    tag = tag.suc
                                                                    # 710. origin sor: (3) comment jelű blokk vége
        also = becsles
        felso = max_ut
        if also < felso - 1.0e-10:
            becsles = max_ut = 0.0                                  # 714. origin sor: (4) comment jelű blokk kezdete
            for k in range(self.gep_elso_muvelete[j], self.gep_elso_muvelete[j] + self.gep_muveletszama[j]): #  - 1 hozzáadása nem kell a range felső határához, mert az maga nyiott felső határú
                tag = cast(Muveletcsucs, dg_first(fej))             # 719. origin sor: (5) comment jelű blokk kezdete; FIRST
                link_index = 0
                while False if tag is None else tag.forrastol1 > self.muvelet[k].forrastol1:
                    assert tag
                    link_index += 1; tag = cast(Muveletcsucs, tag.suc)
                if tag is None:
                    fej.append(self.muvelet[k])                     # INTO
                else: fej.insert(link_index, self.muvelet[k])       # PRECEDE(tag)
                dg_link_elements(fej)                               # (5) comment jelű blokk vége
            while len(fej) > 0:                                     # EMPTY (NOT EMPTY)
                tag = fej[0]                                        # 731. origin sor: (6) comment jelű blokk kezdete; FIRST
                seged = tag.nyeloig2
                tag1 =tag
                tag = cast(Muveletcsucs, tag.suc)
                while tag is not None:
                    if seged > tag.nyeloig2:
                        seged = tag.nyeloig2
                        tag1 = tag
                    tag = cast(Muveletcsucs, tag.suc)
                dg_out(fej, tag1)                                   # 746. origin sor: OUT
                kulcsszam = tag1.nyeloig2 + tag1.idotartam
                min_kieg = tag1.forrastol1
                seged = kulcsszam +tag1.forrastol1
                if max_ut < seged:
                    max_ut = becsles = seged
                elif becsles < seged: becsles = seged
                tag = dg_first(fej)                                 # 755. origin sor; FIRST
                while False if tag is None else tag.nyeloig2 > kulcsszam:
                    tag = tag.suc
                while tag is not None:
                    dg_out(fej, tag)                                # 764. origin sor: OUT
                    kulcsszam += tag.idotartam
                    max_ut = max(max_ut, kulcsszam + tag.forrastol1)
                    min_kieg = min(min_kieg, tag.forrastol1)
                    becsles = max(becsles, kulcsszam + min_kieg)
                    tag = dg_first(fej)                             # 774. origin sor; FIRST
                    while False if tag is None else tag.nyeloig2 > kulcsszam:
                        tag = tag.suc
                                                                    # 780. origin sor: (6) comment jelű blokk vége
            also = max(also, becsles)
            felso = min(felso, max_ut)
        in_out_attr[0] = also; in_out_attr[1] = felso           # 785. origin sor: (4), (2) és (1) comment jelű blokkok vége

    # # Functions for test (treadmill)  2024.02.
    # from diszjunktiv_graf import Diszjunktiv_graf, Muveletcsucs
    # from diszjunktiv_graf_manipulacioi import El
    def print_cp(self) -> None:
        l: List[int] = []
        assert self.nyelo
        m: Muveletcsucs | None = self.nyelo.kritikus_elozo
        i: int = 0
        while m is not None and not m == self.forras and i <= self.muveletszam:
            l.append(m.azonosito)
            m = m.kritikus_elozo
            i += 1
        l.reverse()
        assert self.nyelo
        print(f"Kritikus út hossza: {self.nyelo.forrastol1:.2f}, forrástól nyelőig egy kritikus útvonal: {str(l)}")
        if i > self.muveletszam:
            raise SystemExit(1)  # Indicates an error condition
    def print_free_edges(self, szabad_elek: List[El]) -> None:
        l: List[str] = []
        for e in szabad_elek:
            l.append(repr(e))
        print(f"Szabad élek száma: {len(l)}, listája: {str(l)}")
    def print_fixed_edges(self, fixalt_elek: List[El]) -> None:
        l: List[str] = []
        for e in fixalt_elek:
            l.append(repr(e))
        print(f"Fixált élek: {str(l)}")
