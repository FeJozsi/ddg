"""
This module serves as the "main building block" for the "black boxes"
that facilitate finding the optimal order of operations on machines
in a Disjunctive Graph.  
After this module, a chain of modules will follow, each relying
on its predecessors in the order below.
    diszjunktiv_graf.py,  
    diszjunktiv_graf_manipulacioi.py,  
    szabad_elek__korlatozas_egy_gepen.py,  
    finomitasok.py,  
    megoldasfa.py,  
    vezerles.py,  
    dg_high_level_pseudo_black_boxes.py .
    
The situation is analogous with classes.
Each module's main class shares the module's name and forms
a chain of subclasses in the same order.
"""
from typing import List

from dg_link import DgLink
from dg_link import dg_first
from dg_link import dg_link_elements

from dg_standard_input import dg_inint
from dg_standard_input import dg_inreal
# from dg_standard_input import dg_close_input

# In Python, you can disable assertions globally by running the interpreter with the -O (optimize) option.

# Alternatively, you can use the __debug__ global variable to conditionally enable or disable assertions based on whether Python is running in debug mode.
#  When Python is running normally (not in debug mode), __debug__ is False, and assertions are disabled.
#  When Python is running in debug mode, __debug__ is True, and assertions are enabled.
# By using __debug__, you can keep your assertions in the code and have them enabled or disabled automatically
#  based on whether Python is running in debug mode or not.
# It's generally a good practice to leave assertions in your code even in production,
#  as they can help catch programming errors and ensure that your code behaves as expected.
#  However, you may want to disable assertions in production for performance reasons.


class Muveletcsucs(DgLink):   #: CSak később, a Diszjunktiv_graf leszármazott osztályában fogjuk kihasználni, hogy a Muveletcsucs osztály a db_link-ből származik.
    """
    This class represents an operation.  
    """
    def __init__(self) -> None:
        super().__init__()                                                                      #: Kell a DgLink super()
        self.azonosito: int = 0; self.gepje: int = 0
        self.kiindultak: int = 0; self.kiindulok: int = 0
        self.beerkezettek: int = 0; self.beerkezok: int = 0
        self.idotartam: float = 0.0; self.forrastol1: float = 0.0; self.forrastol2: float = 0.0
        self.nyeloig1: float = 0.0; self.nyeloig2: float = 0.0
        self.megelozok: List[Csatlakozas] = []; self.rakovetkezok: List[Csatlakozas] = []       #: Csatlakozas  LIST
        self.gepen_elozo: Muveletcsucs = None; self.gepen_koveto: Muveletcsucs = None           #: Muveletcsucs
        self.opt_elozo: Muveletcsucs = None;   self.opt_koveto: Muveletcsucs = None             #: Muveletcsucs
        self.kritikus_elozo: Muveletcsucs = None                                                #: Muveletcsucs
        self.kritikus_elozo_sorrendi:bool = None
    def __repr__(self) -> str:
        if self.azonosito == 0: return super().__repr__()
        if self.azonosito == -1: return "Forras Muveletcsucs"
        if self.azonosito == -9: return "Nyelo Muveletcsucs"
        return f"{self.azonosito}. Muveletcsucs"

class Csatlakozas(DgLink):
    """
    This class represents a connection between operations.  
    It can be added to the list of predecessors for the operations.
    This indicates that the 'Csatlakozas.szomszed' operation must
    precede the owner operation of the list.  
    These relations may come from the input data of the Disjunctive Graph
    but can also come from operations such as fixing a 'free' sequential edge.
    """
    def __init__(self, szomszed: Muveletcsucs) -> None:                                         #: Muveletcsucs
        super().__init__()
        self.szomszed: Muveletcsucs = szomszed                                                  #: Muveletcsucs
    def __repr__(self) -> str:
        if self.szomszed is None: return super().__repr__()
        return f"Csatlakozas {repr(self.szomszed)} szomszeddal"

class Diszjunktiv_graf:
    """
    This class represents the first level of class and sub-classes,
    often referred to as 'pseudo "black boxes"'.  
    It can read the Disjunctive Graph and calculate critical (maximum length) path on it.  
    The entire list of these mentioned levels includes:   
        Diszjunktiv_graf,  
        Diszjunktiv_graf_manipulacioi,  
        Szabad_elek__korlatozas_egy_gepen,  
        Finomitasok,  
        Megoldasfa,  
        Vezerles.  
    """
    def __init__(self, muveletszam: int, gepszam: int) -> None:
        self.muveletszam: int = muveletszam
        self.gepszam: int = gepszam
        self.muvelet: List[Muveletcsucs] = [None] * muveletszam                                 #: Muveletcsucs ARRAY       # w: Muveletcsucs = None     # self.muvelet = [w] * muveletszam   # list (range(1, self.muveletszam + 1))
        self.forras: Muveletcsucs = None; self.nyelo: Muveletcsucs = None
        self.muvkod: List[int] =  [None] * muveletszam                                          #: int          ARRAY
        self.gep_muveletszama: List[int] =  [None] * gepszam                                    #: int          ARRAY
        self.gep_elso_muvelete: List[int] =  [None] * gepszam                                   #: int          ARRAY
        self.aktualis_opt_atfutasi_ido: float = 0.0                # 27. origin sor
    def kritikus_ut_odafele(self) -> None:
        elintezettek: List[Muveletcsucs] = []                                                   #: Muveletcsucs LIST
        elintezett_csucs: Muveletcsucs = None
        csatolo: Csatlakozas = None
        hossz: float = 0.0
        self.torles()
        elintezettek.append(self.forras)                            # INTO
        def figyelembevetel(muvelet: Muveletcsucs, sorrendi: bool): # sorrendi == True, ha technológiai élről van szó, és False, ha gépen való műveleti sorrendet kijelölő élről, mégpedig olyanról, amivel megegyező technológiai él nincs
            muvelet.beerkezettek += 1
            if muvelet.forrastol1 < hossz - 1.0e-10:
                muvelet.forrastol1 = hossz
                muvelet.kritikus_elozo = elintezett_csucs
                muvelet.kritikus_elozo_sorrendi = sorrendi
            if muvelet.beerkezettek < muvelet.beerkezok:
                pass
            else:
                if True if muvelet.gepen_elozo is None else muvelet.beerkezettek > muvelet.beerkezok:
                    muvelet.beerkezettek = 0
                    elintezettek.append(muvelet)                    # INTO
                    muvelet.forrastol2 = muvelet.forrastol1 + muvelet.idotartam
        while len(elintezettek) > 0:                                # EMPTY
            elintezett_csucs = dg_first(elintezettek)               # FIRST   Itt elintezettek[0] is jó lenne, mert tudjuk, hogy nem üres a lista
            elintezettek = elintezettek[1:]                         # OUT     De, ha üres is volna, x = [][1:] egy üres listát ad vissza szépen!
            csatolo = dg_first(elintezett_csucs.rakovetkezok)       # FIRST
            hossz = elintezett_csucs.forrastol2
            while csatolo is not None:
                figyelembevetel(csatolo.szomszed, False)            # (sorrendi fixen False ezen az ágon)
                csatolo = csatolo.suc
            if elintezett_csucs.gepen_koveto is not None:
                figyelembevetel(elintezett_csucs.gepen_koveto, True) # 84. origin sor    (sorrendi fixen True nem maradhat ezen az ágon, ha itt olyan élek is lehetnek, amelyeknek van technológiai él megfelelőjük is!)
    def kritikus_uthosszak_visszafele(self) -> None:
        elintezettek: List[Muveletcsucs] = []                                                   #: Muveletcsucs LIST
        elintezett_csucs: Muveletcsucs = None
        csatolo: Csatlakozas = None
        hossz: float = 0.0   # self.torles()  itt nincs!!!
        elintezettek.append(self.nyelo)                             # INTO
        def figyelembevetel(muvelet: Muveletcsucs): # sorrendi itt nincs
            muvelet.kiindultak += 1
            muvelet.nyeloig2 = max(muvelet.nyeloig2, hossz)
            if muvelet.kiindultak < muvelet.kiindulok:
                pass
            else:
                if True if muvelet.gepen_koveto is None else muvelet.kiindultak > muvelet.kiindulok:
                    muvelet.kiindultak = 0
                    elintezettek.append(muvelet)                    # INTO
                    muvelet.nyeloig1 = muvelet.nyeloig2 + muvelet.idotartam
        while len(elintezettek) > 0:                                # EMPTY
            elintezett_csucs = dg_first(elintezettek)               # FIRST   Itt elintezettek[0] is jó lenne, mert tudjuk, hogy nem üres a lista
            elintezettek = elintezettek[1:]                         # OUT     De, ha üres is volna, x = [][1:] egy üres listát ad vissza szépen!
            csatolo = dg_first(elintezett_csucs.megelozok)          # FIRST
            hossz = elintezett_csucs.nyeloig1
            while csatolo is not None:
                figyelembevetel(csatolo.szomszed)
                csatolo = csatolo.suc
            if elintezett_csucs.gepen_elozo is not None:
                figyelembevetel(elintezett_csucs.gepen_elozo)       # 133. origin sor
    def sorrendisegi_elek_nelkul_uthosszak_odafele(self) -> None:
        elintezettek: List[Muveletcsucs] = []                                                   #: Muveletcsucs LIST
        elintezett_csucs: Muveletcsucs = None
        csatolo: Csatlakozas = None
        hossz: float = 0.0
        self.torles()
        elintezettek.append(self.forras)                            # INTO
        while len(elintezettek) > 0:                                # EMPTY
            elintezett_csucs = dg_first(elintezettek)               # FIRST   Itt elintezettek[0] is jó lenne, mert tudjuk, hogy nem üres a lista
            elintezettek = elintezettek[1:]                         # OUT     De, ha üres is volna, x = [][1:] egy üres listát ad vissza szépen!
            csatolo = dg_first(elintezett_csucs.rakovetkezok)       # FIRST
            hossz = elintezett_csucs.forrastol2
            while csatolo is not None:
                csatolo.szomszed.beerkezettek += 1
                csatolo.szomszed.forrastol1 = max(csatolo.szomszed.forrastol1, hossz)
                if csatolo.szomszed.beerkezettek == csatolo.szomszed.beerkezok:
                    csatolo.szomszed.beerkezettek = 0
                    elintezettek.append(csatolo.szomszed)           # INTO
                    csatolo.szomszed.forrastol2 = csatolo.szomszed.forrastol1 + csatolo.szomszed.idotartam
                csatolo = csatolo.suc                               # 168. origin sor
    def sorrendisegi_elek_nelkul_uthosszak_visszafele(self) -> None:
        elintezettek: List[Muveletcsucs] = []                                                   #: Muveletcsucs LIST
        elintezett_csucs: Muveletcsucs = None
        csatolo: Csatlakozas = None
        hossz: float = 0.0   # self.torles()  itt nincs!!!
        elintezettek.append(self.nyelo)                             # INTO
        while len(elintezettek) > 0:                                # EMPTY
            elintezett_csucs = dg_first(elintezettek)               # FIRST   Itt elintezettek[0] is jó lenne, mert tudjuk, hogy nem üres a lista
            elintezettek = elintezettek[1:]                         # OUT     De, ha üres is volna, x = [][1:] egy üres listát ad vissza szépen!
            csatolo = dg_first(elintezett_csucs.megelozok)          # FIRST
            hossz = elintezett_csucs.nyeloig1
            while csatolo is not None:
                csatolo.szomszed.kiindultak += 1
                csatolo.szomszed.nyeloig2 = max(csatolo.szomszed.nyeloig2, hossz)
                if csatolo.szomszed.kiindultak == csatolo.szomszed.kiindulok:
                    csatolo.szomszed.kiindultak = 0
                    elintezettek.append(csatolo.szomszed)           # INTO
                    csatolo.szomszed.nyeloig1 = csatolo.szomszed.nyeloig2 + csatolo.szomszed.idotartam
                csatolo = csatolo.suc                               # 202. origin sor
    def aktualis_optimalis_megoldas_atirasa(self) -> None:
        for k in range(0, self.muveletszam):
            self.muvelet[k].opt_elozo = self.muvelet[k].gepen_elozo
            self.muvelet[k].opt_koveto = self.muvelet[k].gepen_koveto
        self.aktualis_opt_atfutasi_ido = self.nyelo.forrastol1
    def aktualis_optimalis_sorrend_visszaallitas(self) -> None:
        for k in range(0, self.muveletszam):
            self.muvelet[k].gepen_koveto = self.muvelet[k].opt_koveto
            self.muvelet[k].gepen_elozo = self.muvelet[k].opt_elozo # 223. origin sor
    def masodik_ut_forrastol(self, muvelet: Muveletcsucs) -> float:
        masodik_szomszed: Muveletcsucs = None
        csatolo: Csatlakozas = None
        seged: float = 0.0
        if muvelet.gepen_elozo is not None: masodik_szomszed = muvelet.gepen_elozo.gepen_elozo
        if masodik_szomszed is not None: seged = masodik_szomszed.forrastol2
        csatolo = dg_first(muvelet.megelozok)                       # FIRST
        while csatolo is not None:
            seged = max(seged, csatolo.szomszed.forrastol2)
            csatolo = csatolo.suc
        return seged
    def masodik_ut_nyeloig(self, muvelet: Muveletcsucs) -> float:
        masodik_szomszed: Muveletcsucs = None
        csatolo: Csatlakozas = None
        seged: float = 0.0
        if muvelet.gepen_koveto is not None: masodik_szomszed = muvelet.gepen_koveto.gepen_koveto
        if masodik_szomszed is not None: seged = masodik_szomszed.nyeloig1
        csatolo = dg_first(muvelet.rakovetkezok)                    # FIRST
        while csatolo is not None:
            seged = max(seged, csatolo.szomszed.forrastol2)
            csatolo = csatolo.suc
        return seged                                                # 265. origin sor

    def graf_beolvasasa(self) -> None:
        """
        This method reads the Disjunctive Graph
        """
        self.forras = Muveletcsucs(); self.forras.azonosito = -1
        self.nyelo  = Muveletcsucs(); self.nyelo.azonosito  = -9
        for k in range(0, self.muveletszam):
            self.muvelet[k] = Muveletcsucs()
        m: int = 0                                  #    1   helyett  az első gép első művelete (gep_elso_muvelete) 0 lesz!
        for k in range(0, self.gepszam):
            self.gep_elso_muvelete[k] = m
            self.gep_muveletszama[k] = dg_inint()
            m += self.gep_muveletszama[k]
        assert m == self.muveletszam, (f"Alert! A gépeken szereplő műveletek össz száma ({m}) nem adja ki a teljes műveletszámot ({self.muveletszam})")
        # dg_link_elements(self.muvelet)
        # for k in range(1, self.gepszam):                            # gép határakon ne legyenek átlinkelve a műveletek!  ??? !!!
        #     megelozo: Muveletcsucs = self.muvelet[self.gep_elso_muvelete[k]].pred            Ezt (vagy egy ilyen) összefűzést csak a használat előtt kellene megtenni... Különben egymás alól vágjuk a fát.
        #     megelozo.suc = None                                                              ÉS MÉG MINDIG KÉRDÉS, HA EGYSZERRE, EGY IDŐBEN TÖBB SIMSET LISTÁBAN IS ÉRDEKELT VAGYOK, amelyeknek lehet közös eleme!
        #     self.muvelet[self.gep_elso_muvelete[k]].pred = None                              SZERENCSÉRE, nincs ok aggodalomra, akkor ha Csatlakozas-ba burkoltan LINK-elünk.
        for k in range(0, self.muveletszam):
            self.muvkod[dg_inint() - 1] = k # a belső 0:muveletszam-1 tartományba képzése a külső 1:muveletszam művelet azonosító tartománynak. VIGYÁZAT! self.muvkod[k] = (dg_inint())  HELYETT fordítva van, és a tartomány is el van tolva eggyel!!!
        # print("** Az input adatok **")
        print("** Azon.  Gépje   Időtart.  Megelőzők         **")
        for k in range(0, self.muveletszam):                        # 284. origin sor
            m = dg_inint() - 1
            muv: Muveletcsucs = self.muvelet[self.muvkod[m]]    # muv éppen az a művelet, amelynek a tulajdonságait olvassuk
            muv.azonosito = m + 1                               # külső azonosító (1-től kezdődő tartomány!)
            muv.gepje = dg_inint()                              # külső sorszámozási tartományban (1-től keződően)
            muv.idotartam = dg_inreal()
            m = dg_inint() - 1          # technológiailag előzmény műveletek külső azonosítóinak felolvasása a 0-val kezdődő tartományba konvertáltan
            l: List = []                # egyelőre üres a techn. előzmény műveletek listája
            while m >= 0:
                l.append(m+1)           # technológiailag előzmény művelet külső azonosítója
                m = self.muvkod[m]      # technológiailag előzmény művelet belső indexe
                muv.megelozok.append(Csatlakozas(self.muvelet[m]))
                self.muvelet[m].rakovetkezok.append(Csatlakozas(muv))
                m = dg_inint() - 1      # technológiailag előzmény műveletek külső azonosítóinak folytatólagos olvasása a 0-val kezdődő tartományba konvertáltan
            print((f"[{muv.azonosito:6}, {muv.gepje:6}, {muv.idotartam:8.2f},   {str(l)} {' ' * (17-len(str(l)))}]")) # l szerepel (a külső művelet-azonosító int értékekkel) itt a muv.megelozok helyett, ami egy komplexebb lista
        # dg_close_input()
        for k in range(0, self.muveletszam):                        # 306. origin sor
            muv: Muveletcsucs = self.muvelet[k]    # muv az a művelet, amelyet szükség esetén a forráshoz és/vagy a nyelőhöz hozzákötjük
            if len(muv.megelozok) == 0:                             # EMPTY
                muv.megelozok.append(Csatlakozas(self.forras))
                self.forras.rakovetkezok.append(Csatlakozas(muv))
            if len(muv.rakovetkezok) == 0:                          # EMPTY
                muv.rakovetkezok.append(Csatlakozas(self.nyelo))
                self.nyelo.megelozok.append(Csatlakozas(muv))
        for k in range(0, self.muveletszam):                        # 326. origin sor
            muv: Muveletcsucs = self.muvelet[k]    # muv az a művelet, amelynél néhány db szám nyilvántartó attribútumot kitöltünk
            muv.kiindulok = len(muv.rakovetkezok)                   # CARDINAL
            muv.beerkezok = len(muv.megelozok)                      # CARDINAL
            dg_link_elements(muv.megelozok)                         # Link the nodes together for a linked list
            dg_link_elements(muv.rakovetkezok)                      # Link the nodes together for a linked list
        self.forras.kiindulok = len(self.forras.rakovetkezok)       # CARDINAL
        dg_link_elements(self.forras.rakovetkezok)                  # Link the nodes together for a linked list
        self.nyelo.beerkezok = len(self.nyelo.megelozok)            # CARDINAL
        dg_link_elements(self.nyelo.megelozok)                      # Link the nodes together for a linked list

    # The directed graph must be acyclic. It is a rigid test for this. 2024.02:
    def rigid_check_acyclicity(self) -> bool:
        """
        The directed graph must be acyclic. This methon is a rigid test for this.
        """
        def check_for_cycle(cobj: Muveletcsucs, pred: List[Csatlakozas], cpath: List[int], clevel: int, circle: List[int]) -> None:
            if circle: return
            if cobj.azonosito in cpath[1:] or len(cpath) > self.muveletszam:
                circle.extend(cpath)  # Preserve the original circle list
                return
            if not pred: return
            p: int = pred[0].szomszed.azonosito
            if p == cobj.azonosito:
                cpath.append(p)
                circle.extend(cpath)  # Preserve the original circle list
                return
            if len(pred) > 1:
                check_for_cycle(cobj= cobj, pred= pred[1:], cpath= cpath[0:], clevel= clevel, circle = circle)
            if p < 0:  return # i.g. pred[0].szomszed == self.nyelo
            if not p in cpath:
                cpath.append(p)
                pred = self.muvelet[self.muvkod[p-1]].megelozok # predecessors
                check_for_cycle(cobj= cobj, pred= pred[0:], cpath= cpath[0:], clevel= clevel + 1, circle = circle)
            else:
                i = cpath.index(p)
                cpath.append(p)
                # for k in range(i,len(cpath)): circle.append(cpath[k])
                circle.extend(cpath[i:])  # Preserve the original circle list
            return

        circle: List[Muveletcsucs] = None
        for o in self.muvelet:
            circle = []
            check_for_cycle(cobj= o, pred= o.megelozok[0:], cpath= [o.azonosito], clevel= 1, circle= circle)
            if circle: break
        if circle:
            # s: str = ""
            # for oid in circle: s += str(oid) + ","
            # print(s[0:-1])
            if circle[0] == circle[-1] and len(circle) >= 2:
                s: str = ",".join(str(oid) for oid in circle)
                print("*** The check of acyclicity of the disjunctive graph has failed. An example circle: " + s +" ***")
            else:
                print("*** The check of acyclicity of the directed disjunctive graph has totally failed. ***")
            return False
        return True


    def cpm_veget_ert(self) -> bool:                                # Check Critical Path Method ended
        seged: bool = self.nyelo.forrastol2 > 0
        # seged: bool = True    Csak teszteléshez kellett
        j: int = -1 # 0 helyett belső sorszámozásra felkészülve
        # while seged and j+1 < self.gepszam:
        while seged and j+1 < self.muveletszam :
            j += 1
            seged = seged and self.muvelet[j].forrastol2 > 0 and self.muvelet[j].idotartam > 0
            if not seged:
                print(f"*** The execution time is not positive ({self.muvelet[j].idotartam:.2f}) "
                      f"of the operation {self.muvelet[j].azonosito}. ***")
        return seged
    def torles(self) -> None:
        for k in range(0, self.muveletszam):
            self.muvelet[k].forrastol1 = -1.0
            self.muvelet[k].nyeloig2 = -1.0
            self.muvelet[k].kritikus_elozo = None           #  ???  2024.02. utólag/utóbb berakott két sor:  !!!
            self.muvelet[k].kritikus_elozo_sorrendi = False
        self.nyelo.forrastol1 = 0.0
        self.forras.nyeloig2 = 0.0                                  # 359. origin sor
