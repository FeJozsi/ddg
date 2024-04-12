"""
This module serves high level functionalities based on the class and subclasses
    Diszjunktiv_graf,
    Diszjunktiv_graf_manipulacioi,
    Szabad_elek__korlatozas_egy_gepen,
    Finomitasok,
    Megoldasfa,
    Vezerles
 for the main module ('dg_main.py').  
 This module continues the concept of "black boxes" of the above classes but
 it does not create new classes for all level as was the case in the origin SIMULA program.
"""
from typing import TypedDict

from vezerles  import Vezerles

# visszalepes_kovetkezik: bool - Instead of this origin property see my_control_dict["step_back"]
# grabowsky_algoritmus_nem_allt_le: bool -
#                                Instead of this origin property see my_control_dict["my_continue"]


# class GuiControlInfo(TypedDict):
#     """
#     Typing gui_control_dict
#     """
#     prev_state: DgState | None
#     last_influ_event: InfluEventSet | None
#     last_put_accross: InfluEventSet | None
#     rec_state: DgState
#     rec_inp_type : DimInpT
#     quick_flow: bool
#     success: bool

# # gui_control_dict: dict[str, None | DgState | InfluEventSet | DimInpT | bool] = {
# gui_control_dict: GuiControlInfo = {
#     "prev_state" : None,
#     "last_influ_event" : None,
#     "last_put_accross" : None,
#     "rec_state": DgState.INIT,
#     "rec_inp_type" : DimInpT.TYPE_NONE,
#     "quick_flow" : False,
#     "success" : False
# }

class MyControlInfo(TypedDict):
    """
    Typing my_control_dict
    """
    dg_o : Vezerles | None
    step_back: bool
    my_continue: bool

# my_control_dict: Dict[str, Optional[Union[Vezerles, bool]]] = {
# my_control_dict: dict[str, Vezerles | None | bool] = {
my_control_dict: MyControlInfo = {
    "dg_o"       : None,  # a Vezerles object. The dg_main module is responsible for it.
    "step_back"  : False, # Controls stepping back on the solution tree
    "my_continue": True   # Controls the main loop of solution tree traversaling
}
"""
This global variable includes some important main control property:  
"dg_o"        :  a Vezerles object, representing the whole "Disjunctiv Graph'.
                  The dg_main module is responsible for its production and propagation this place.
"step_back"   : Controls stepping back on the solution tree
"my_continue" : Controls the main loop of solution tree traversaling
"""

# These functions below forming a pseudo class or pseudo black box implement
#   the original SIMULA program's class named "KORLATOZAS     ISMETELT KORLATOZAS".
# @pseudo black box
# Vezerles                                          # 1080. origin sor
#   CLASS KORLATOZAS     ISMETELT KORLATOZAS

def korlatozas_alapjan_visszalephetek() -> bool:
    """
    This method is responsible for

        TODO:
    """
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    return dg_o.korlatozas(False)

def regi_csucs_vizsgalata() -> None:
    """
    This method is responsible for

        TODO:
    """
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    if dg_o.van_szabad_el():
        esszeru_ismetelt_korlatozas()

def esszeru_ismetelt_korlatozas() -> None:
    """
    This method is responsible for

        TODO:
    """
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    korlatozas_sikeres: bool = False
    if dg_o.remenyteli_az_ismetelt_korlatozas():
        korlatozas_sikeres = dg_o.korlatozas(korlatozas_sikeres)
        if dg_o.info:
            print("* . *")
        dg_o.ismetelt_korlatozasok_szama += 1
    if korlatozas_sikeres:
        dg_o.sikeres_ismetelt_korlatozasok_szama += 1
    else:
        my_control_dict["step_back"] = False

# This function below–alone–making a pseudo class or pseudo black box implement
#   the original SIMULA program's class named "REGI MEGOLDASOKON KERESZTUL UJ MEGOLDASBA".
# @pseudo black box
# KORLATOZAS     ISMETELT KORLATOZAS                # 1120. origin sor
#   CLASS REGI MEGOLDASOKON KERESZTUL UJ MEGOLDASBA

def uj_megoldas_kereses_hatra_indulva() -> None:
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    my_control_dict["step_back"]  = True
    while my_control_dict["step_back"] :
        if dg_o.gyokerben_vagyok():
            my_control_dict["my_continue"] = False
            my_control_dict["step_back"]  = False
        else:
            dg_o.visszalepes()
            dg_o.visszalepesek_szama += 1
            regi_csucs_vizsgalata()
    if my_control_dict["my_continue"]: # itt my_control_dict["step_back"] == False
        dg_o.uj_megoldas_illesztese_megoldasfara()

# These functions below forming a pseudo class or pseudo black box implement
#   the original SIMULA program's class "UJ MEGOLDASOKON KERESZTUL UJ KIERTEKELENDO MEGOLDASBA".
# @pseudo black box
# REGI MEGOLDASOKON KERESZTUL UJ MEGOLDASBA         # 1140. origin sor
#   CLASS UJ MEGOLDASOKON KERESZTUL UJ KIERTEKELENDO MEGOLDASBA

def uj_kiertekelendo_megoldas_keresese() -> None:
    uj_megoldas_kereses_elore_indulva()
    while False if not my_control_dict["my_continue"] else korlatozas_alapjan_visszalephetek():
        uj_megoldas_kereses_hatra_indulva()

def uj_megoldas_kereses_elore_indulva() -> None:
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    if dg_o.megoldasfa_melyitheto() and dg_o.van_szabad_el():
        dg_o.uj_megoldas_illesztese_megoldasfara()
    else:
        uj_megoldas_kereses_hatra_indulva()

# These functions below forming a pseudo class or pseudo black box implement
#   the original SIMULA program's class "GRABOWSKY ALGORITMUS VEGET FIGYELI".
# @pseudo black box
# UJ MEGOLDASOKON KERESZTUL UJ KIERTEKELENDO MEGOLDASBA     # 1170. origin sor
#   CLASS GRABOWSKY ALGORITMUS VEGET FIGYELI

def iteracio() -> None:
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    if dg_o.megoldasfa_melyitheto():
        dg_o.szabad_elek_valasztasi_sorrendjukben_valo_felsorolasa()
    uj_kiertekelendo_megoldas_keresese()
    if my_control_dict["my_continue"]:
        dg_o.kiertekeles()
        dg_o.kiertekelesek_szama += 1

def kell_a_tovabbi_kutatas() -> bool:
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    return my_control_dict["my_continue"] and not dg_o.egyeb_ok_van_leallasra()

def elso_iteracio() -> None:
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    dg_o.gyokeret_megoldasfaba()
    dg_o.kiertekeles()
    dg_o.kiertekelesek_szama += 1
    if dg_o.info:
        print("** A kezdeti sorrend **")
        dg_o.aktualis_optimalis_megoldas_nyomtatasa()
    else:
        assert dg_o.nyelo
        print("* A kezdetként felállított sorrend kritikus úthossza: "
              f"{dg_o.nyelo.forrastol1:8.2f} *\n")

# These functions below forming a pseudo class or pseudo black box implement
#   the original SIMULA program's class "CLASS VEZERLESI HELYEK".
# @pseudo black box
# GRABOWSKY ALGORITMUS VEGET FIGYELI                # 1200. origin sor
#   CLASS VEZERLESI HELYEK

def adatelokeszites() -> None:
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    dg_o.vezerles_inicializalasa()
    dg_o.graf_beolvasasa()

def iteraciok() -> None:
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    elso_iteracio()
    dg_o.vezerles_aktualizalasa()
    i: int = 1
    b: bool = dg_o.info  # 2024-02-27
    while kell_a_tovabbi_kutatas():
        if b:
            if (True if i <= 1000 else
                True if i < 10000 and i % 100 == 0 else
                True if i < 100000 and i % 1000 == 0 else
                True if i < 1000000 and i % 10000 == 0 else
                not bool( i % 100000 )
               ):
                if dg_o.info:
                    print("***************")
                print((f"{i}. iteration, Length of solution tree: {len(dg_o.ag)}, "
                        "ID of max. last ten solutions:"
                      ),
                        ",".join(str(x.sorszam) for x in dg_o.ag[-10:]))
                if i >= 1000 and dg_o.info:
                    dg_o.info = False
                    print("*" * 75)
                    print("Wrinting detailed LOG has been stopped "
                          "because of the amount of iterations.")
                    print("*" * 75)  # 2024-02-27
        i += 1
        iteracio()
        dg_o.vezerles_aktualizalasa()

def eredmeny() -> None:
    assert my_control_dict["dg_o"]
    dg_o: Vezerles = my_control_dict["dg_o"]
    dg_o.informaciok_nyomtatasa()
    print("** A talált legjobb megoldás **")
    dg_o.aktualis_optimalis_megoldas_nyomtatasa()
