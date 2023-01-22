import os
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

def list_files(startpath) -> str:
    """
        Returns a string containing a tree view of the hold
        folder in input with all its subfolders.
    """

    output = ""

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)

        line = '{}{}/'.format(indent, os.path.basename(root))
        output += "{0}\n".format(line)

        subindent = ' ' * 4 * (level + 1)
        for f in files:
            line = "{}{}".format(subindent, f)
            output += "{0}\n".format(line)

    return output

def error_log(exception):
    """
        Displays in a windows msgbox window a traceback of the
        issue met
    """
    title     = "Fatal Error"
    start     = "Oh no ! QT_saver crashed !\n\nConsider sending me this output for me to fix the issue in future versions. To do so, just press 'OK' to have it copied to your clipboard.\n\n\n[LOG OUTPUT]"
    delimiter = "------------------------------------------"

    dirname = os.path.dirname(__file__)
    message = "{0}\n{1}\n[FILES]\n{2}\n[EXCEPTION]\n{3}".format(start, delimiter, list_files(dirname), exception)
    msgbox(message, title)

if __name__ == "__main__":
    error_log("Traceback most recent call last:File")