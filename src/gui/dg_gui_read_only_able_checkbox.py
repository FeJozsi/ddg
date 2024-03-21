"""
This modul serves a child class for QCheckBox.
It can be set as read-only.
"""
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt

class ReadOnlyAbleCheckBox(QCheckBox):
    """
    This class is a version of QCheckBox.
    It can be set as read-only
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_read_only = False

    def set_read_only(self, read_only):
        """Set the read-only state of the checkbox."""
        self._is_read_only = read_only

    def is_read_only(self):
        """Return the read-only state of the checkbox."""
        return self._is_read_only

    def mousePressEvent(self, e):# pylint: disable=C0103 #doesn't conform to snake_case naming st.
        """
        Handle for mouse press events.
        This method over-writes the QCheckBox's one.
        """
        if not self._is_read_only:
            super().mousePressEvent(e)
        # Else ignore the event

    def keyPressEvent(self, e):# pylint: disable=C0103 # doesn't conform to snake_case naming style
        """
        Handle for key press events.
        This method over-writes the QCheckBox's one.
        """
        if not self._is_read_only:
            super().keyPressEvent(e)
        # Else ignore the event, except allow focus navigation
        elif e.key() not in (Qt.Key.Key_Space, Qt.Key.Key_Select):
            super().keyPressEvent(e)
