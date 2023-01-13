from QT_saver import *
import traceback
from crash import *
from tkinter import *
from PIL import ImageTk, Image
import pyperclip
import os

class MyWindow:
    def __init__(self, win):

        self.URL = ""

        self.GENERAL_X = 6
        self.SECTION1_Y = 40
        self.SECTION2_Y = 180
        self.SECTION3_Y = 330

        self.BUTTONS_Y = 70

        self.title=Label(window, text="Download some user's Instagram public&private\nstories at once !", fg='#4ee44e', font=("Segoe UI Symbol", 10), bg = 'black')
        self.title.place(x=self.GENERAL_X, y=10)

        # - SIGNATURE

        self.signature=Label(window, text="BY MASH ", fg='black', bg='white', font=("Leelawadee", 8, "bold"))
        self.signature.place(x=self.GENERAL_X + 239,
                           y=self.SECTION3_Y + 185)

        # - QT PIC
        self.image1 = Image.open(os.path.join(dirname,"./res/splash-removebg-preview.png"))
        newsize = (60, 60)
        self.image1 = self.image1.resize(newsize)
        self.test = ImageTk.PhotoImage(self.image1)

        self.label1 = Label(image=self.test, width=51, height=50)
        self.label1.image = self.test
        self.label1.place(x=245, y=465)



        # - SECTION 1
        self.section1_title=Label(window, text="STEP 1 - NOT COMPLETE", fg='white', font=("Segoe UI Symbol", 10), bg = 'red')
        self.section1_title.place(x=self.GENERAL_X, 
                                  y=self.SECTION1_Y + 30)

        self.btn01=Button(window, text="Use the USERID\n in the .ini file", fg='white', bg='#7a8793', command=self.click_btn01)
        self.btn01.place(x=self.GENERAL_X + 20,
                         y=self.BUTTONS_Y + self.SECTION1_Y)

        self.btn02=Button(window, text="Use the USERID\nyou wrote below", fg='white', bg='#7a8793', command=self.click_btn02)
        self.btn02.place(x=self.GENERAL_X + 170,
                         y=self.BUTTONS_Y + self.SECTION1_Y)

        self.txtfld=Entry(window, text="Write here your user ID", bd=2)
        self.txtfld.place(x=self.GENERAL_X + 155,
                          y=self.BUTTONS_Y + self.SECTION1_Y + 60)

        # - SECTION 2

        self.section2_title=Label(window, text="STEP 2 - NOT COMPLETE", fg='white', font=("Segoe UI Symbol", 10), bg = 'red')
        self.section2_title.place(x=self.GENERAL_X, 
                                  y=self.SECTION2_Y + 30)

        self.btn03=Button(window, text="Copy URL to\nclipboard", fg='white', bg='#7a8793', command=self.click_btn03)
        self.btn03.place(x=self.GENERAL_X + 110,
                         y=self.BUTTONS_Y + self.SECTION2_Y)

        self.hint01=Label(window, text="Paste the URL once copied in your browser\nwhere you're already logged into Instagram", fg='red', bg='black', font=("Segoe UI Symbol", 8))
        self.hint01.place(x=self.GENERAL_X + 35, y=self.SECTION2_Y + 120)

        # - SECTION 3

        self.section3_title=Label(window, text="STEP 3 - NOT COMPLETE", fg='white', font=("Segoe UI Symbol", 10), bg = 'red')
        self.section3_title.place(x=self.GENERAL_X, 
                                  y=self.SECTION3_Y + 30)

        self.hint02=Label(window, text="Copy the entire response content from\nyour browser before clicking this button", fg='red', bg='black', font=("Segoe UI Symbol", 8))
        self.hint02.place(x=self.GENERAL_X + 35, y=self.SECTION3_Y + 65)

        self.btn04=Button(window, text="Paste & run", fg='white', bg='#7a8793', command=self.click_btn04)
        self.btn04.place(x=self.GENERAL_X + 110,
                         y=self.BUTTONS_Y + self.SECTION3_Y + 35)

        self.infomsg=Label(window, text="Idling...", fg='yellow', bg='black', font=("Segoe UI Symbol", 8))
        self.infomsg.place(x=self.GENERAL_X + 5,
                           y=self.SECTION3_Y + 160)


    def click_btn01(self):
        # - STYLE
        self.section1_title["bg"]="green"
        self.section2_title["bg"]="red"
        self.section3_title["bg"]="red"
        self.section1_title["text"]="STEP 1 - COMPLETE"
        self.section2_title["text"]="STEP 2 - NOT COMPLETE"
        self.section3_title["text"]="STEP 3 - NOT COMPLETE"
        self.infomsg["text"]="Idling..."
        # - ---

        self.URL = getURL()
        
    def click_btn02(self):
        # - STYLE
        self.section1_title["bg"]="green"
        self.section2_title["bg"]="red"
        self.section3_title["bg"]="red"
        self.section1_title["text"]="STEP 1 - COMPLETE"
        self.section2_title["text"]="STEP 2 - NOT COMPLETE"
        self.section3_title["text"]="STEP 3 - NOT COMPLETE"
        self.infomsg["text"]="Idling..."
        # - ---

        field_txt = self.txtfld.get()
        self.URL = getURL(id = field_txt)

    def click_btn03(self):
        # - STYLE
        self.section2_title["bg"]="green"
        self.section3_title["bg"]="red"
        self.section2_title["text"]="STEP 2 - COMPLETE"
        self.section3_title["text"]="STEP 3 - NOT COMPLETE"
        self.infomsg["text"]="Idling..."
        # - ---

        pyperclip.copy(self.URL)

    def click_btn04(self):
        # - STYLE
        self.section3_title["bg"]="green"
        self.section3_title["text"]="STEP 3 - COMPLETE"
        # - ---

        try:
            self.infomsg["text"]="Processing (the window might freeze)..."
            Tk.update(window)

            urls, count_pics, count_vids, = parser()
            saver(urls)

            self.infomsg["text"]="Done. {0} pics and {1} vids have successfully\nbeen saved.".format(count_pics, count_vids)

        except Exception as e:
            error_log(traceback.format_exc())


if __name__ == "__main__":

    try:
        #Relative path
        dirname = os.path.dirname(__file__)

        window=Tk()
        MyWindow(window)
        window.iconbitmap(os.path.join(dirname, "./res/splash-removebg-preview.ico"))
        window.title('QT saver')
        window.geometry("300x530+10+10")
        window['background']='#000000'
        window.resizable(False, False) 

        window.mainloop()
    except Exception as e:
        error_log(e)



    #pyinstaller --onefile --noconsole --icon=./res/splash-removebg-preview.ico gui.py