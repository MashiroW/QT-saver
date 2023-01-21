import os
import ctypes
import pyperclip

def msgbox(msg, title="Error", auto_copy=1, windowtype=1):
    MessageBox = ctypes.windll.user32.MessageBoxW
    result = MessageBox(None, msg, title, windowtype)

    if result == 1 and auto_copy == 1:
        pyperclip.copy(msg)

def list_files(startpath):
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
    title     = "Fatal Error"
    start     = "Oh no ! QT_saver crashed !\n\nConsider sending me this output for me to fix the issue in future versions. To do so, just press 'OK' to have it copied to your clipboard.\n\n\n[LOG OUTPUT]"
    delimiter = "------------------------------------------"

    dirname = os.path.dirname(__file__)
    message = "{0}\n{1}\n[FILES]\n{2}\n[EXCEPTION]\n{3}".format(start, delimiter, list_files(dirname), exception)
    msgbox(message, title)

if __name__ == "__main__":
    error_log("Traceback most recent call last:File")