import tkinter

import customtkinter
import os
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("QTSaver")
        self.geometry("850x600")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../test/manual_integration_tests/test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "./my_files/splash-removebg-preview.png")), size=(28, 28))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "./my_files/home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "./my_files/home_light.png")), size=(20, 20))
        self.download = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "./my_files/download_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "./my_files/download_dark.png")), size=(20, 20))
        self.settings = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "./my_files/settings_light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "./my_files/settings_dark.png")), size=(20, 15))
        self.copy = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "./my_files/copy_light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "./my_files/copy_dark.png")), size=(20, 20))
        self.add_user = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "./my_files/add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "./my_files/add_user_light.png")), size=(20, 20))                                                    

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" QTSaver", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.download_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Download",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.download, anchor="w", command=self.download_button_event)
        self.download_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.settings, anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # HOME FRAME
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # DOWNLOAD FRAME
        # STEP 1 - [TAB 2]
        self.download_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.download_frame.grid_columnconfigure(0, weight=1)

        self.step1_txt = customtkinter.CTkLabel(self.download_frame, text="STEP 1 - NOT COMPLETE", text_color="#fff", bg_color="red", width=250, justify="left", anchor="w")
        self.step1_txt.grid(row=0, column=0, padx=(40, 40), pady=(20, 0))      

        self.download_tabview = customtkinter.CTkTabview(self.download_frame, height=160)
        self.download_tabview.grid(row=1, column=0, padx=(40, 40), pady=(20, 0)) 

        tab1_name = "Saved IDs"
        tab2_name = "Enter an ID"

        self.download_tabview.add(tab1_name)
        self.download_tabview.add(tab2_name)
        self.download_tabview.tab(tab1_name).grid_columnconfigure(0, weight=1)
        self.download_tabview.tab(tab2_name).grid_columnconfigure(0, weight=1)

        self.id_select = customtkinter.CTkOptionMenu(self.download_tabview.tab(tab1_name),
                                                        dynamic_resizing=False,
                                                        values=sorted(["@misterv", "Value 2", "AValue 2", "Value Long Long Long"]))
        self.id_select.grid(row=0, column=0, padx=(10, 10), pady=(20, 10))

        self.generate_URL_button_dict = customtkinter.CTkButton(self.download_tabview.tab(tab1_name),
                                                        text="Copy URL to clipboard", 
                                                        image=self.copy,
                                                        anchor= "bottom",
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.copy_url)
        self.generate_URL_button_dict.grid(row=0, column=1, padx=(10, 10), pady=(20, 10))  

        self.txt1 = "Hint: To save IDs in this\nlist, go to settings"
        self.hint1 = customtkinter.CTkLabel(self.download_tabview.tab(tab1_name), text=self.txt1, text_color="#fff", width=150, justify="center", anchor="w")
        self.hint1.grid(row=1, column=0, padx=(20, 10), pady=(0, 0)) 
 
        self.txt2 = "Paste the URL once copied in\nyour browser where you're\nalready logged into Instagram"
        self.hint2 = customtkinter.CTkLabel(self.download_tabview.tab(tab1_name), text=self.txt2, text_color="#fff", width=150, justify="center", anchor="w")
        self.hint2.grid(row=1, column=1, padx=(10, 10), pady=(0, 0)) 

        # STEP 1 - [TAB 2]
        self.entry = customtkinter.CTkEntry(self.download_tabview.tab(tab2_name), placeholder_text="Target's account ID")
        self.entry.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(20, 20))

        self.txt3 = "Paste the URL once copied in your browser where you're\nalready logged into Instagram"
        self.hint3 = customtkinter.CTkLabel(self.download_tabview.tab(tab2_name), text=self.txt3, text_color="#fff", width=150, justify="center", anchor="w")
        self.hint3.grid(row=1, column=0, padx=(20, 20), pady=(0, 0)) 

        self.generate_URL_button_string = customtkinter.CTkButton(self.download_tabview.tab(tab2_name),
                                                text="Copy URL to clipboard", 
                                                image=self.copy,
                                                anchor= "bottom",
                                                hover_color="orange",
                                                compound="top",
                                                command=self.copy_url)
        self.generate_URL_button_string.grid(row=2, column=0, padx=(10, 10), pady=(20, 10))

        # - STEP 2
        self.step2_txt = customtkinter.CTkLabel(self.download_frame, text="STEP 2 - NOT COMPLETE", text_color="#fff", bg_color="red", width=250, justify="left", anchor="w")
        self.step2_txt.grid(row=3, column=0, padx=(40, 40), pady=(20, 0))  

        self.box2 = customtkinter.CTkFrame(self.download_frame)
        self.box2.grid(row=4, column=0, padx=(40, 40), pady=(20, 20))

        self.switch_1 = customtkinter.CTkSwitch(self.box2, command=lambda: print("switch 1 toggle"), text="Get Pics")
        self.switch_1.grid(row=0, column=0, padx=(50,225), pady=(20, 20))
        self.switch_1.select()

        self.switch_2 = customtkinter.CTkSwitch(self.box2, command=lambda: print("switch 2 toggle"), text="Get Vids")
        self.switch_2.grid(row=0, column=0, padx=(225,50), pady=(20, 20))
        self.switch_2.select()

        self.txt4 = "Copy the entire response content from your browser before\nclicking this button"
        self.hint4 = customtkinter.CTkLabel(self.box2, text=self.txt4, text_color="red", width=150, justify="center", anchor="w")
        self.hint4.grid(row=1, column=0, padx=(20, 20), pady=(0, 0)) 

        self.paste_url_button = customtkinter.CTkButton(self.box2,
                                                        text="Paste & Download", 
                                                        image=self.download,
                                                        anchor= "bottom",
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.paste_url)
        self.paste_url_button.grid(row=2, column=0, padx=(10,10), pady=(20, 20))  

        self.progressbar_1 = customtkinter.CTkProgressBar(self.box2)
        self.progressbar_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        # SETTINGS FRAME
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure((0,1), weight=1)

        """
        self.txt_settings = "EACH OF THESE SETTINGS CAN BE\nDIRECTLY EDITED FROM THE .INI FILE"
        self.txt_settings = customtkinter.CTkLabel(self.settings_frame, text=self.txt_settings, text_color="red")
        self.txt_settings.grid(row=0, column=1, padx=(20, 300), pady=(20, 0)) 
        """

        self.settings_btn1 = customtkinter.CTkButton(self.settings_frame,
                                                        text="ADD USER", 
                                                        image=self.add_user,
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.button_presssed,
                                                        width=300,
                                                        height=100)
        self.settings_btn1.grid(row=1, column=0, padx=(10,0), pady=(20, 20))  
        
        self.settings_btn2 = customtkinter.CTkButton(self.settings_frame,
                                                        text="DELETE USER", 
                                                        image=self.add_user,
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.button_presssed,
                                                        width=300,
                                                        height=100)
        self.settings_btn2.grid(row=1, column=1, padx=(0,10), pady=(20, 20)) 

        self.settings_btn3 = customtkinter.CTkButton(self.settings_frame,
                                                        text="EDIT OUTPUT PATH", 
                                                        image=self.add_user,
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.button_presssed,
                                                        width=300,
                                                        height=100)
        self.settings_btn3.grid(row=2, column=0, padx=(10,0), pady=(20, 20)) 

        self.settings_btn3 = customtkinter.CTkButton(self.settings_frame,
                                                        text="OPEN OUTPUT FOLDER\nIN FILE EXPLORER", 
                                                        image=self.add_user,
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.button_presssed,
                                                        width=300,
                                                        height=100)
        self.settings_btn3.grid(row=2, column=1, padx=(0,10), pady=(20, 20)) 


        self.settings_switch_1 = customtkinter.CTkSwitch(self.box2, command=lambda: print("switch 1 toggle"), text="Create one folder per ID")
        self.settings_switch_1.grid(row=0, column=0, padx=(50,225), pady=(20, 20))

        self.settings_switch_2 = customtkinter.CTkSwitch(self.box2, command=lambda: print("switch 2 toggle"), text="Create one folder per day")
        self.settings_switch_2.grid(row=0, column=0, padx=(225,50), pady=(20, 20))      


        # DEFAULT FRAME SELECTED ON STARTUP
        self.select_frame_by_name("settings")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.download_button.configure(fg_color=("gray75", "gray25") if name == "download" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "download":
            self.download_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.download_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

        # set colors back to the red background
        self.step1_txt.configure(text="STEP 1 - NOT COMPLETE", bg_color="red")
        self.step2_txt.configure(text="STEP 2 - NOT COMPLETE", bg_color="red")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def download_button_event(self):
        self.select_frame_by_name("download")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def copy_url(self):
        print("URL COPIED TO CLIPBOARD")
        self.step1_txt.configure(text="STEP 1 - COMPLETE", bg_color="green")
        self.step2_txt.configure(text="STEP 2 - NOT COMPLETE", bg_color="red")

    def paste_url(self):
        print("URL PASTED - CODE RUNNING")
        self.step2_txt.configure(text="STEP 2 - COMPLETE", bg_color="green")

    def button_presssed(self):
        print("PRESSED !!")


if __name__ == "__main__":
    app = App()
    app.mainloop()

