import ctypes
import pyperclip

def msgbox(msg, title="Error", auto_copy=True, windowtype=1):
    """
        Pops a windows msgbox with the said message.
        If auto_copy is set to True, the message will be
        copied to the clipboard when the user hits "OK"

        windowtype corresponds to the type of window you
        want to use. Check the ctypes.MessageBox class
        for more details
    """
    MessageBox = ctypes.windll.user32.MessageBoxW
    result = MessageBox(None, msg, title, windowtype)

    if result == 1 and auto_copy == True:
        pyperclip.copy(msg)
