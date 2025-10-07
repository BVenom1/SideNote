from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class TextBrowser(QTextBrowser):
    def __init__(self, parent=None, link_handle=None):
        super().__init__(parent)
        
        self.p_pos = -1
        self.p_len = 0
        
        self.c_pos = -1
        
        self.setReadOnly(False)
        self.setOpenLinks(False)
        
        if link_handle:
            self.anchorClicked.connect(link_handle)
        
        self.cursorPositionChanged.connect(self.text_changed)
        
        self.is_shift_key_pressed = False
        
    def keyPressEvent(self, ev: QKeyEvent):
        
        if ev.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.is_shift_key_pressed = True
            
        if ev.modifiers() & Qt.KeyboardModifier.ControlModifier:
            cursor = self.textCursor()
            self.c_pos = cursor.position()
            cursor.setPosition(0)
            self.setTextCursor(cursor)
            self.setReadOnly(True)
            self.setTextInteractionFlags(
                Qt.TextInteractionFlag.LinksAccessibleByMouse |
                Qt.TextInteractionFlag.TextBrowserInteraction
            )
        
        return super().keyPressEvent(ev)
    
    def keyReleaseEvent(self, e: QKeyEvent):
        
        if e.key() == Qt.Key.Key_Shift:
            self.is_shift_key_pressed = False
        
        if e.key() == Qt.Key.Key_Control:
            cursor = self.textCursor()
            if self.c_pos != -1: cursor.setPosition(self.c_pos)
            self.setTextCursor(cursor)
            self.setReadOnly(False)
            self.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextEditorInteraction
            )
        
        return super().keyReleaseEvent(e)
        
    def text_changed(self):
        if self.is_shift_key_pressed: return
        self.blockSignals(True)
        cursor = self.textCursor()
        first_pos = cursor.position()
        
        # get to the beginning of the current word
        t = ''
        while True:
            cursor.movePosition(
                QTextCursor.MoveOperation.NextCharacter,
                QTextCursor.MoveMode.KeepAnchor
            )
            t = cursor.selectedText()
            if t == '' or t[len(t)-1].isspace() or cursor.atEnd():
                break
        e_pos = cursor.position()
        if t != '' and t[len(t)-1].isspace():
            cursor.setPosition(
                e_pos-1,
                QTextCursor.MoveMode.MoveAnchor
            )
            e_pos -= 1
            
        # keep anchor and get to the beginning of the current word
        while True:
            cursor.movePosition(
                QTextCursor.MoveOperation.PreviousCharacter,
                QTextCursor.MoveMode.KeepAnchor
            )
            t = cursor.selectedText()
            if t == '' or t[0].isspace() or cursor.atStart():
                break
        s_pos = cursor.position()
        if t != '' and t[0].isspace():
            cursor.setPosition(
                s_pos+1,
                QTextCursor.MoveMode.KeepAnchor
            )
            s_pos += 1
        t = cursor.selectedText()
        
        # remove formatting of current text
        cursor.removeSelectedText()
        cursor.insertText(t)
        
        s_len = e_pos-s_pos
        
        if s_pos != self.p_pos:
            if self.p_pos != -1:
                # get previous selection
                cursor.setPosition(self.p_pos, QTextCursor.MoveMode.MoveAnchor)
                cursor.movePosition(
                    QTextCursor.MoveOperation.Right,
                    QTextCursor.MoveMode.KeepAnchor,
                    self.p_len
                )
                p_t = cursor.selectedText()
                
                # format previous text
                regex = QRegularExpression(r"#[A-Za-z0-9_\-]+")
                match = regex.match(p_t)
                if match.hasCaptured(0):
                    cursor.removeSelectedText()
                    cursor.insertHtml(f"<a href='{p_t}'>{p_t}</a>")

            else:
                pass
            self.p_pos = s_pos
            self.p_len = s_len
        
        cursor.setPosition(
            first_pos,
            QTextCursor.MoveMode.MoveAnchor
        )
        self.setTextCursor(cursor)
        self.blockSignals(False)