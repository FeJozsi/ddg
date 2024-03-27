"""
This module introduces the machines (Gepelem class)
and defines sequential edges (El class)
to establish the order of operations on them.  
It maintains records of machines states.  
It adds functionalities to the Disjunctive Graph,
such as specifying the beginning order of the operations on the machines.
"""
from typing import List, Sequence, cast

from dg_link import DgLink
from dg_link import dg_first
from dg_link import dg_out
from dg_link import dg_link_elements

from diszjunktiv_graf import Muveletcsucs
from diszjunktiv_graf import Csatlakozas
from diszjunktiv_graf import Diszjunktiv_graf

class El(DgLink):                                                  # 363. origin sor
    """
    This class represents a sequential edge.  
    The sequential edges define the order of operations on the machines
    in cases where the order is not defined by the initial graph.
    """
    def __init__(self, kezdet: Muveletcsucs, veg: Muveletcsucs) -> None:
        super().__init__()
        self.kezdet: Muveletcsucs = kezdet
        self.veg: Muveletcsucs = veg
        self.delta: float = 0.0
        self.normal: bool = True                                    # (419. origin sorból előre hozva)
    def __repr__(self) -> str:
        try:
            ret_val: str = ""
            if self.kezdet.gepje == self.veg.gepje:
                ret_val += ( f"{self.kezdet.gepje}. gep: "
                             f"{self.kezdet.azonosito}->{self.veg.azonosito} muv. el"
                           )
            else:
                ret_val += f"nem ua gép: {self.kezdet.azonosito}->{self.veg.azonosito} muv. el"
            return ret_val
        except AttributeError:
            return super().__repr__()
    def behelyezes(self, p_fej) -> None:   # FIGYELEM! ÁLLATIRA figyelni kell, hogy ugyanaz az objektum (muvelet-csucs) ne legyen berakva több LIST-be! Ezen problémával kapcsolatos a Csatlakozas CLASS. !!!!!
        fej: Sequence[El] = p_fej
        bentlevo: El | None = cast(El, dg_first(fej))
        link_index: int = 0
        while False if bentlevo is None else bentlevo.delta < self.delta:
            link_index += 1
            assert bentlevo
            bentlevo = cast(El, bentlevo.suc)
        assert isinstance(fej, list) # cast(list, fej)
        if bentlevo is None: fej.append(self)                       # INTO
        else: fej.insert(link_index, self)                          # PRECEDE(bentlevo)
        dg_link_elements(fej)
    def konjugalas(self) -> None:
        self.kezdet, self.veg = self.veg, self.kezdet # (self.kezdet, self.veg) = (self.veg, self.kezdet)   so-called tuple assignment. It's common in Python to omit the parentheses, resulting in the cleaner and more concise syntax. In Kotlin, the statement swaps the values using destructuring declarations an a Pair: self.kezdet, self.veg = self.veg to self.kezdet
    def eltavolitas(self) -> None:
        self.kezdet.rakovetkezok = self.kezdet.rakovetkezok[:-1]    # LAST.OUT
        self.veg.megelozok = self.veg.megelozok[:-1]                # LAST.OUT
        dg_link_elements(self.kezdet.rakovetkezok); dg_link_elements(self.veg.megelozok)
        self.kezdet.kiindulok -= 1
        self.veg.beerkezok -= 1
    def fixalas(self, p_fixalt_elek) -> None:
        fixalt_elek: List[El] = p_fixalt_elek
        self.kezdet.rakovetkezok.append(Csatlakozas(self.veg))      # INTO
        self.veg.megelozok.append(Csatlakozas(self.kezdet))         # INTO
        dg_link_elements(self.kezdet.rakovetkezok); dg_link_elements(self.veg.megelozok)
        self.kezdet.kiindulok += 1
        self.veg.beerkezok += 1
        if self.is_linked():  # 2024-02-27 08:38   Ez egyben kiszedi a szabad élek (szabad_elek) közül!!!
            self.out()
        if self.head: # 2024-02-27 09:14
            assert not self.head, 'Alert fixalas, DgLink elem with head is not linked.'
        fixalt_elek.append(self); dg_link_elements(fixalt_elek)     # INTO
    def konjugalasaval_sorrend_modositas(self) -> None:             # 405. origin sor
        elso: Muveletcsucs | None = self.kezdet.gepen_elozo
        utolso: Muveletcsucs | None = self.veg.gepen_koveto
        if elso is not None: elso.gepen_koveto = self.veg
        self.kezdet.gepen_elozo = self.veg
        self.kezdet.gepen_koveto = utolso
        self.veg.gepen_elozo = elso
        self.veg.gepen_koveto = self.kezdet
        if utolso is not None: utolso.gepen_elozo = self.kezdet

class Gepelem():                                                    # (424. origin sorból előre hozva)
    """
    This class represents a machine.  
    """
    def __init__(self, gepazon: int) -> None:
        self.gepazon: int = gepazon
        self.so: List[Muveletcsucs] = [] # Ezek legyenek diszjunkt listák egymáshoz képest!     #: Muveletcsucs LIST
        self.utolso: Muveletcsucs | None = None
        self.c: float = 0.0
        self.h: float = 1.0e+300 # 1.8 × 10 a 308-okon in magnitude (a maximális float nagyságrend)
    def __repr__(self) -> str:
        return f"{self.gepazon}. Gepelem"

class Diszjunktiv_graf_manipulacioi(Diszjunktiv_graf):              # 360. origin sor
    """
    This class represents the second level of sub-classes, often referred to
    as 'pseudo "black boxes"'.  
    It maintains records of machines' states,
    and adds functionalities to the Disjunctive Graph, such as
    specifying the beginning order of operations (see kezdeti_sorrend_felallitasa).  
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
        self.fixalt_elek: List[El] = []                             # 421. origin sor           #: El           LIST
    def kezdeti_sorrend_felallitasa(self) -> None:
        """
        This method specifies the beginning order of operations.  
        The Disjunctive Graph must be loaded before running (see Diszjunktiv_graf.graf_beolvasasa).
        """
        gepj: Gepelem                                               # 432. origin sor
        sgep: Gepelem
        gep: List[Gepelem] =  [Gepelem(-1)] * self.gepszam                                      #: Gepelem      ARRAY     The elements will be replaced soon
        muvj: Muveletcsucs
        smuv: Muveletcsucs | None = None
        csatolo: Csatlakozas | None = None
        nyelo_maradt: bool = False
        seged: float
        for k in range(self.gepszam):           # a shorthand notation for range(0, self.gepszam)
            gep[k] = Gepelem(k+1)   # külső, 1-től kezdődő azonosítása lesz a gépeknek is
        self.torles()
        self.sorrendisegi_elek_nelkul_uthosszak_visszafele()
        assert self.forras
        csatolo = cast(Csatlakozas, dg_first(self.forras.rakovetkezok)) # FIRST
        aktmuvelet : Muveletcsucs
        while csatolo is not None:              # a forrás közvetlen rákövetkező műveleteit rárakjuk a gépjeikre:
            aktmuvelet = csatolo.szomszed
            aktgep: Gepelem = gep[aktmuvelet.gepje - 1]             # belső, 0-val kezdődő tartományba konvertálni
            aktgep.so.append(aktmuvelet)                            # INTO
            dg_link_elements(aktgep.so) # A műveleteket gépenként különböző sorrendező LIST-be helyezzük. A LIST-eknek, melyekbe csupasz műveleteket pakolunk - disznjunktaknak kell lenniük! Egyelőre ez ezekre a sorrendező LIST-ekre igaz, mert gépenként elkülönülnek a műveletek.
            aktmuvelet.forrastol1 = 0.0
            aktgep.h = min(aktgep.h, aktmuvelet.idotartam)
            csatolo = cast(Csatlakozas, csatolo.suc)
        while not nyelo_maradt:                                     # 456. origin sor: (1) comment jelű blokk kezdete
            gepj = gep[0]  # gep[1] helyett a belső tartomány szerinti indexeléssel (vö. Muveletcsucs.gepje külső, 1-től kezdődő sorszámozásával)!
            seged = gepj.h
            for k in range(1,self.gepszam): # range(2,self.gepszam) helyett belső sorszámozással (0-től kezdve)
                if seged > gep[k].h:
                    gepj = gep[k]
                    seged = gepj.h
            muvj = cast(Muveletcsucs, dg_first(gepj.so))            # 467. origin sor: (2) comment jelű blokk kezdete; FIRST - ilyen most itt biztos hogy van, mert gepj.h nem a végtelen nagy érték már.
            k = 0    # 1 helyett  (belső sorszámozás miatt)
            while muvj.forrastol1 > gepj.h - 1.0e-10:  # 1e-8 # ITT FEL VAN TÉTELEZVE, hogy, amennyiben ez teljesül, akkor nem az utolsó műveleten állunk a gépre rakott műveletek között. Legelején mindenesetere ez nem teljesül, így a feltételezés egyelőre megáll.
                muvj = cast(Muveletcsucs, muvj.suc)  # keressük az első olyan elemet, ahol muvj.forrastol1 < gepj.h egy pici tűréssel. A kód feltételezi, hogy van ilyen. Induláskor ez teljesül, mert a forrás rákövetkező műveleteinél forrastol1 = 0, gepj.h pedig > 0
                k += 1
            smuv = muvj                                             # 475. origin sor
            for _ in range(k + 1, len(gepj.so)):                    # CARDINAL
                smuv = cast(Muveletcsucs, smuv.suc)                 # 478. origin sor: (2a) comment jelű blokk kezdete
                if smuv.forrastol1 > gepj.h - 1.0e-10:  # 1e-8
                    pass
                elif smuv.nyeloig2 > muvj.nyeloig2 + 1.0e-10:  # 1e-8
                    muvj = smuv
                elif smuv.nyeloig2 < muvj.nyeloig2 - 1.0e-10:  # 1e-8
                    pass
                elif smuv.forrastol1 < muvj.forrastol1:
                    muvj = smuv
                elif smuv.forrastol1 > muvj.forrastol1:
                    pass
                elif smuv.idotartam < muvj.idotartam:
                    muvj = smuv
                else:
                    pass                                            # 498. origin sor: (2a) comment jelű blokk vége
            dg_out(gepj.so, muvj)                                   # OUT      Kivesszük - az ezek szerint csak átmeneti sorrendező LIST-ből - és ténylegesen a gépre rakjuk - aktuálisan - utolsóként
            if gepj.utolso is not None: gepj.utolso.gepen_koveto = muvj
            muvj.gepen_elozo = gepj.utolso
            gepj.utolso = muvj
            gepj.c = muvj.forrastol1 + muvj.idotartam
            gepj.h = 1.0e+300                                       # 509. origin sor
            smuv = cast(Muveletcsucs, dg_first(gepj.so))            # FIRST
            while smuv is not None:
                smuv.forrastol1 = max(smuv.forrastol1, gepj.c)
                gepj.h = min(gepj.h, smuv.forrastol1 + smuv.idotartam)
                smuv = cast(Muveletcsucs, smuv.suc)
            csatolo = dg_first(muvj.rakovetkezok)                   # FIRST
            while csatolo is not None:                              # 522. origin sor: (3) és (4) comment jelű blokk kezdete
                aktmuvelet = csatolo.szomszed
                aktmuvelet.beerkezettek += 1
                aktmuvelet.forrastol1 = max(aktmuvelet.forrastol1, gepj.c)
                if aktmuvelet.beerkezettek == aktmuvelet.beerkezok:
                    aktmuvelet.beerkezettek = 0                     # 530. origin sor: (5) comment jelű blokk kezdete
                    if aktmuvelet == self.nyelo: nyelo_maradt = True
                    else:                                           # (6) comment jelű blokk kezdete
                        sgep = gep[aktmuvelet.gepje - 1]  # belső, 0-val kezdődő tartományba konvertálni
                        sgep.so.append(aktmuvelet)                  # INTO
                        dg_link_elements(sgep.so)
                        aktmuvelet.forrastol1 = max(aktmuvelet.forrastol1, sgep.c)
                        sgep.h = min(sgep.h, aktmuvelet.forrastol1 + aktmuvelet.idotartam)
                                                                    # (6), (5) és (4) commentjelű blokk vége
                csatolo = csatolo.suc                               # (3), (2) és (1) commentjelű blokk vége
        for k in range(self.gepszam):
            gep[k].utolso.gepen_koveto = None                       # 550. origin sor

    def el_konjugalasaval_uj_megoldas(self, jelolt: El) -> None:
        jelolt.konjugalasaval_sorrend_modositas()
        jelolt.konjugalas()
        jelolt.normal = False
        jelolt.fixalas(self.fixalt_elek)
    def elek_visszaallitasaval_regi_sorrend(self) -> None:
        folosleges_el: El = self.fixalt_elek[-1]                    # LAST
        while folosleges_el.normal:
            # self.fixalt_elek = self.fixalt_elek[:-1]                # LAST OUT
            # dg_link_elements(self.fixalt_elek)
            assert self.fixalt_elek[-1].head
            self.fixalt_elek[-1].head.out_last()    # 2024-02-27 09:00 ez még mindig nem a végleges megoldás, a fixalt_elek listája egy  head-be  kellene burkolva legyen
            folosleges_el.eltavolitas()
            folosleges_el = self.fixalt_elek[-1]                    # LAST
        # self.fixalt_elek = self.fixalt_elek[:-1]                    # LAST OUT   Ezt is kivesszük, de alább rögtön visszatesszük egy módosított formában
        # dg_link_elements(self.fixalt_elek)                          #    2024.02.
        assert self.fixalt_elek[-1].head
        self.fixalt_elek[-1].head.out_last()    # 2024-02-27 09:00 ez még mindig nem a végleges megoldás, a fixalt_elek listája egy  head-be  kellene burkolva legyen
        folosleges_el.konjugalasaval_sorrend_modositas()
        folosleges_el.eltavolitas()
        folosleges_el.konjugalas()
        folosleges_el.normal = True
        folosleges_el.fixalas(self.fixalt_elek)
    def megmaradt_fixalt_elek_eltavolitasa(self) -> None:
        while len(self.fixalt_elek) > 0:                            # EMPTY (NOT EMPTY)
            self.fixalt_elek[-1].eltavolitas()
            # self.fixalt_elek = self.fixalt_elek[:-1]                # LAST OUT
            assert self.fixalt_elek[-1].head
            self.fixalt_elek[-1].head.out_last()    # 2024-02-27 09:00 ez még mindig nem a végleges megoldás, a fixalt_elek listája egy  head-be  kellene burkolva legyen
