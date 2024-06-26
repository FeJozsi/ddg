"""
This module encapsulates the functionality of the SIMSET class from SIMULA'67,
with a focus on the `HEAD` and `LINK` classes, representing a *linked list structure*.
"""

from typing import Sequence # , List, Any

from typing_extensions import deprecated

class DgLink:
    """
    This class represents the elements of a linked list.
    It replaces the original `LINK` class.
    """
    def __init__(self, head = None) -> None:
        """
        Args:
            head: refers to the `DgHead` object managing the element's linked list
        """
        self.head: DgHead | None = head    # the linked list itself
        self.suc:  DgLink | None = None    # successor DgLink element
        self.pred: DgLink | None = None    # predecessor DgLink element
    def is_free(self) -> bool:
        """
        Ensure that the DgLink element is not already part of a linked list
        """
        loc_bool: bool = self.head is None and self.suc is None and self.pred is None
        if loc_bool:    # 2024-02-29 07:27:21
            if self.head is not None:
                assert self.head is None, "Alert is_free! A DgLink element is headed a corrupt way."
            if self.suc is not None or self.pred is not None:
                assert self.suc is None and self.pred is None, (
                       "Alert is_free! A DgLink element is inked a corrupt way."
                )
        return loc_bool
    def is_linked(self) -> bool:
        """
        Ensure that the DgLink element is already part of a linked list
        """
        loc_bool: bool = (self.head is not None and self.head.is_loaded() and
                     not (self.suc is None and self.pred is None and len(self.head.l) > 1)
        )
        if loc_bool:    # 2024-02-27 08:51
            if not self.head:
                assert bool(self.head), "Alert is_linked! A DgLink element's head is empty."
                return False
            if not self in self.head.l:
                assert self in self.head.l, "Alert is_linked! A DgLink element's head is corrupt."
        return loc_bool
    def into(self, head) -> None:
        """
        Insert the DgLink element into a linked list after the last element if any exists.  
        It throws exception if the self is not free, i.e. is_free() False,
        and if the head is totally empty, i. e. is None or head.is_loaded() False.

        Args:
            head: refers to the `DgHead` object managing the element's linked list
        """
        assert self.is_free(), "Alert INTO! The DgLink element is already member of a DgHead!"
        h: DgHead = head
        assert h is not None and h.is_loaded(), "Alert INTO! The DgHead is totally empty!"
        assert isinstance(h.l, list) # cast(list, h.l)
        h.l.append(self)
        h.link_elements()
    def precede(self, internal) -> None:
        """
        Insert the DgLink element into a linked list before a specified internal element.  
        It throws exception if the self is not free, i.e. is_free() False,
        and if the internal is not in a linked list, i.e. is_linked() False.

        Args:
            internal: refers to the `DgLink` object that should follow the element being inserted.
        """
        assert self.is_free(), "Alert PRECEDE! The DgLink element is already member of a DgHead!"
        s: DgLink = internal
        assert s is not None and s.is_linked(), (
            "Alert PRECEDE! The following element (internal) is not linked yet!"
        )
        h: DgHead | None = s.head
        if not h:
            assert bool(h), "Alert PRECEDE! The internal.head is empty!"
            return
        assert isinstance(h.l, list) # cast(list, h.l)
        h.l.insert(h.l.index(s), self)
        h.link_elements()
    def out(self) -> None:
        """
        Take the DgLink element out from the linked list.  
        It throws exception if the self is not linked yet, i.e. is_linked() False.
        """
        assert self.is_linked(), "Alert OUT! The DgLink element is not linked yet!"
        h: DgHead | None = self.head
        self.suc = None
        self.pred = None
        self.head = None
        if not h:
            assert bool(h), "Alert OUT! The self.head is empty!"
            return
        assert isinstance(h.l, list) # cast(list, h.l)
        h.l.remove(self)
        h.link_elements()

class DgHead:
    """
    This class represents HEAD of the linked list.
    Actually, it contains the whole linked list in a Python list also.
    """
    def __init__(self, l: Sequence[DgLink] | None = None) -> None: # List[DgLink] helyett
        self.l:  Sequence[DgLink] = []      # the whole linked list # List[DgLink] helyett
        if l is not None:
            self.l = l
    def is_loaded(self) -> bool:
        """
        Ensure that the DgHead is not totally empty
        """
        return self.l is not None
    def link_elements(self) -> None:
        """
        This method updates the successor (SUC) and predecessor (PRED)
        information throughout the entire linked list.  
        It throws exception if the head is totally empty, i. e. head.is_loaded() False.
        """
        assert self.is_loaded(), "Alert link_elements! The DgHead object totally empty!"
        for i, node in enumerate(self.l):
            if i > 0:
                node.pred = self.l[i - 1]    # prev
            else:
                node.pred = None
            if i < len(self.l) - 1:
                node.suc = self.l[i + 1]     # next
            else:
                node.suc = None
    def first(self) -> DgLink | None:
        """
        This method presents the first element of the linked list, if any exists in.  
        It throws exception if the head is totally empty, i. e. head.is_loaded() False.
        """
        assert self.is_loaded(), "Alert FIRST! The DgHead object totally empty!"
        if self.l:
            return self.l[0]
        return None
    def last(self) -> DgLink | None:
        """
        This method presents the last element of the linked list, if any exists in.  
        It throws exception if the head is totally empty, i. e. head.is_loaded() False.
        """
        assert self.is_loaded(), "Alert LAST! The DgHead object totally empty!"
        if self.l:
            return self.l[-1]
        return None
    def out_first(self) -> DgLink | None:
        """
        Take the first DgLink element out from the linked list, and returns it.
        It throws exception if the head is totally empty, i. e. head.is_loaded() False.
        """
        assert self.is_loaded(), "Alert out_first! The DgHead object totally empty!"
        if not self.l:
            return None
        f: DgLink | None = self.first()
        if f:
            f.out()
        return f
    def out_last(self) -> DgLink | None:
        """
        Take the last DgLink element out from the linked list, and returns it.
        It throws exception if the head is totally empty, i. e. head.is_loaded() False.
        """
        assert self.is_loaded(), "Alert out_last! The DgHead object totally empty!"
        if not self.l:
            return None
        l: DgLink | None = self.last()
        if l:
            l.out()
        return l

# class Dg_link:
#     def __init__(self) -> None:
#         self.suc:  Dg_link = None       # successor
#         self.pred: Dg_link = None       # predecessor

# def dg_first(l: List[Dg_link]) -> Dg_link:
#     if len(l) > 0: return l[0]
#     return None

# "List" is invariant; Consider using "Sequence" instead, which is covariant
@deprecated("Use DgHead.first() instead of it.")
def dg_first(l: Sequence[DgLink]) -> DgLink | None:  # instead of Link[DgLink]
    """
    Deprecated: This method presents the first element of the linked list, if any exists in.  
    It is deprecated. Use DgHead.first() instead of it.
    """
    if len(l) > 0:
        return l[0]
    return None

# def dg_out(l: List[Dg_link], e: Dg_link) -> None:
#     e.suc = None
#     e.pred = None
#     l.remove(e)
#     dg_link_elements(l)

@deprecated("Use DgLink.out() instead of it.")
def dg_out(l: Sequence[DgLink], e: DgLink) -> None:  # List[DgLink]
    """
    Deprecated: Take the DgLink element out from the linked list.  
    It throws exception if the element e is not linked yet, i.e. e.is_linked() False,
    or l is empty, or not l == e.head.l .  
    It is deprecated. Use DgLink.out() instead of it.
    """
    assert e is not None and e.is_linked(), (
        "Alert dg_out! The e not linked yet, i.e. e is None or e.is_linked() False.!"
    )
    assert l, "Alert dg_out! The parameter l (list) is empty!"
    if not l or not e.head:
        return
    assert l == e.head.l, "Alert dg_out! The parameter l (list) is different from e.head.l!"
    e.out()

# def dg_link_elements(nodes: List[Dg_link]) -> None:         # Link the nodes together
#     for i in range(len(nodes)):
#         if i > 0:
#             nodes[i].pred = nodes[i - 1]    # prev
#         else:
#             nodes[i].pred = None
#         if i < len(nodes) - 1:
#             nodes[i].suc = nodes[i + 1]     # next
#         else:
#             nodes[i].suc = None

# "List" is invariant; Consider using "Sequence" instead, which is covariant
@deprecated("Use DgHead.link_elements() instead of it.")
def dg_link_elements(nodes: Sequence[DgLink]) -> None: # instead of Link[DgLink]
    """
    Deprecated: This method updates the successor (SUC) and predecessor (PRED)
    information throughout the entire linked list (it links the nodes together).  
    It is deprecated. Instead, use DgHead.link_elements().
    However, you do not need to explicitly call it, as it is
    invoked automatically if necessary.
    """
    for i, node in enumerate(nodes):
        if i > 0:
            node.pred = nodes[i - 1]    # prev
        else:
            node.pred = None
        if i < len(nodes) - 1:
            node.suc = nodes[i + 1]     # next
        else:
            node.suc = None
    dg_set_head(nodes)                  # only for backward compatibility

def dg_set_head(nodes: Sequence[DgLink]) -> None: # instead of Link[DgLink]
    """
    This method complements DgLink objects by setting the missing
    'head' attribute for backward compatibility purposes.  2024-02-27
    """
    h: DgHead | None = None
    for node in nodes:
        if node.head is not None:
            if h is not None:
                if not h == node.head:
                    assert h == node.head, 'Alert dg_set_head! Eltérő fej objektumok.'
            else:
                h = node.head
    if nodes and h is None:
        h = DgHead(nodes)
    for node in nodes:
        if not node.head:
            node.head = h
