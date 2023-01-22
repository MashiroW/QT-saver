import tkinter
import customtkinter
import os
from PIL import Image
import datetime
import webbrowser
from datetime import datetime

from QT_saver import *

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "res/")
        
        self.title("QTSaver")
        self.geometry("1000x750")
        self.iconbitmap(os.path.join(image_path, "splash-removebg-preview.ico"))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Loading assets
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "splash-removebg-preview.png")), size=(28, 28))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "main.png")), size=(2001/2.5, 601/2.5))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.background = customtkinter.CTkImage(Image.open(os.path.join(image_path, "background.png")), size=(1080/1.7,1920/1.7))

        self.welcome = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "welcome_light.png")), 
                                                 dark_image=Image.open(os.path.join(image_path, "welcome_dark.png")), size=(914/2,315/2))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.download = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "download_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "download_dark.png")), size=(20, 20))
        self.settings = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "settings_light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "settings_dark.png")), size=(20, 15))
        self.copy = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "copy_light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "copy_dark.png")), size=(20, 20))
        self.add_user = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20)) 
        self.delete_user = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "delete_user_dark.png")),
                                                dark_image=Image.open(os.path.join(image_path, "delete_user_light.png")), size=(20, 20)) 
        self.discord = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "discord.png")),
                                                dark_image=Image.open(os.path.join(image_path, "discord.png")), size=(15, 15))    
        self.youtube = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "youtube.png")),
                                        dark_image=Image.open(os.path.join(image_path, "youtube.png")), size=(18, 12))      
        self.instagram = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "instagram.png")),
                                                dark_image=Image.open(os.path.join(image_path, "instagram.png")), size=(15, 15))    
        self.tiktok = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "tiktok.png")),
                                                dark_image=Image.open(os.path.join(image_path, "tiktok.png")), size=(15, 15))                                             
        
        # Navigation Frame Sidebar
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, 
                                                             text=" QTSaver", image=self.logo_image,
                                                             compound="left", 
                                                             font=customtkinter.CTkFont(size=15, 
                                                             weight="bold"))

        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, 
                                                    corner_radius=0, 
                                                    height=40, 
                                                    border_spacing=10,
                                                    text="Home",
                                                    fg_color="transparent", 
                                                    text_color=("gray10", "gray90"), 
                                                    hover_color=("gray70", "gray30"),
                                                    image=self.home_image, 
                                                    anchor="w", 
                                                    command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.download_button = customtkinter.CTkButton(self.navigation_frame, 
                                                        corner_radius=0, 
                                                        height=40, 
                                                        border_spacing=10, 
                                                        text="Download",
                                                        fg_color="transparent", 
                                                        text_color=("gray10", "gray90"), 
                                                        hover_color=("gray70", "gray30"),
                                                        image=self.download, 
                                                        anchor="w", 
                                                        command=self.download_button_event)
        self.download_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, 
                                                        corner_radius=0, 
                                                        height=40, 
                                                        border_spacing=10, 
                                                        text="Settings",
                                                        fg_color="transparent", 
                                                        text_color=("gray10", "gray90"), 
                                                        hover_color=("gray70", "gray30"),
                                                        image=self.settings, anchor="w", 
                                                        command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, 
                                                                values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # ------------------------------------
        # HOME FRAME
        # ------------------------------------
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure((0,1,2), weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=1, padx=20, pady=10)

        self.home_welcome = customtkinter.CTkLabel(self.home_frame, text="", image=self.welcome)
        self.home_welcome.grid(row=1, column=1, padx=10, pady=(30,10))
  
        self.home_yt1_button = customtkinter.CTkButton(self.home_frame,
                                                        text="Mash           ", 
                                                        image=self.youtube,
                                                        hover_color="orange",
                                                        fg_color="black",
                                                        compound="left",
                                                        command=self.home_mash_channel,
                                                        width=100,
                                                        height=22)
        self.home_yt1_button.grid(row=2, column=1, padx=(10,360), pady=(0, 10))  
        
        self.home_yt2_button = customtkinter.CTkButton(self.home_frame,
                                                        text="_mashiro", 
                                                        image=self.tiktok,
                                                        hover_color="orange",
                                                        fg_color="black",
                                                        compound="left",
                                                        command=self.home_tiktok,
                                                        width=100,
                                                        height=22)
        self.home_yt2_button.grid(row=2, column=1, padx=(10,125), pady=(0, 10))

        self.discord_server = customtkinter.CTkButton(self.home_frame,
                                                        text="Discord ", 
                                                        image=self.discord,
                                                        hover_color="orange",
                                                        fg_color="black",
                                                        compound="left",
                                                        command=self.home_discord,
                                                        width=100,
                                                        height=20)
        self.discord_server.grid(row=2, column=1, padx=(125,10), pady=(0, 10))

        self.home_instagram_button = customtkinter.CTkButton(self.home_frame,
                                                        text="Instagram ", 
                                                        image=self.instagram,
                                                        hover_color="orange",
                                                        fg_color="black",
                                                        compound="left",
                                                        command=self.home_instagram,
                                                        width=100,
                                                        height=20)
        self.home_instagram_button.grid(row=2, column=1, padx=(350,10), pady=(0, 10))

        self.home_tiktok_button = customtkinter.CTkButton(self.home_frame,
                                                        text="NRG_Mash", 
                                                        image=self.youtube,
                                                        hover_color="orange",
                                                        fg_color="black",
                                                        compound="left",
                                                        command=self.home_nrg_mash_channel,
                                                        width=100,
                                                        height=22)
        self.home_tiktok_button.grid(row=3, column=1, padx=(10,360), pady=(0, 10))


        # ------------------------------------
        # DOWNLOAD FRAME - STEP 1 - [TAB 1]
        # ------------------------------------
        self.download_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.download_frame.grid_columnconfigure(0, weight=1)

        self.download_step1_txt = customtkinter.CTkLabel(self.download_frame, 
                                                text="STEP 1 - NOT COMPLETE", 
                                                text_color="#fff", 
                                                bg_color="red", 
                                                width=250, 
                                                justify="left", 
                                                anchor="w")
        self.download_step1_txt.grid(row=0, column=0, padx=(40, 40), pady=(20, 0))      

        self.download_tabview = customtkinter.CTkTabview(self.download_frame, height=160)
        self.download_tabview.grid(row=1, column=0, padx=(40, 40), pady=(20, 0)) 

        tab1_name = "Saved IDs"
        tab2_name = "Enter an ID"

        self.download_tabview.add(tab1_name)
        self.download_tabview.add(tab2_name)
        self.download_tabview.tab(tab1_name).grid_columnconfigure(0, weight=1)
        self.download_tabview.tab(tab2_name).grid_columnconfigure(0, weight=1)

        self.download_id_droplist = customtkinter.CTkOptionMenu(self.download_tabview.tab(tab1_name),
                                                                    dynamic_resizing=False,
                                                                    values=sorted(getUsers().values()))
        self.download_id_droplist.grid(row=0, column=0, padx=(10, 10), pady=(20, 10))

        self.download_tab1_copy_URL_button = customtkinter.CTkButton(self.download_tabview.tab(tab1_name),
                                                        text="Copy URL to clipboard", 
                                                        image=self.copy,
                                                        anchor= "bottom",
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.download_copy_url_tab1)
        self.download_tab1_copy_URL_button.grid(row=0, column=1, padx=(10, 10), pady=(20, 10))  

        txt1 = "Hint: To save IDs in this\nlist, go to settings"
        self.download_hint1_txt = customtkinter.CTkLabel(self.download_tabview.tab(tab1_name), 
                                            text=txt1, 
                                            text_color="#fff", 
                                            width=150, 
                                            justify="center", 
                                            anchor="w")
        self.download_hint1_txt.grid(row=1, column=0, padx=(20, 10), pady=(0, 0)) 
 
        self.download_hint2_txt = "Paste the URL once copied in\nyour browser where you're\nalready logged into Instagram"
        self.hint2 = customtkinter.CTkLabel(self.download_tabview.tab(tab1_name), 
                                            text=self.download_hint2_txt, 
                                            text_color="#fff", 
                                            width=150, 
                                            justify="center", 
                                            anchor="w")
        self.hint2.grid(row=1, column=1, padx=(10, 10), pady=(0, 0)) 

        # ------------------------------------
        # DOWNLOAD FRAME - STEP 1 - [TAB 2]
        # ------------------------------------
        self.download_id_entry = customtkinter.CTkEntry(self.download_tabview.tab(tab2_name), 
                                                        placeholder_text="Target's account ID")
        self.download_id_entry.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(20, 20))

        self.download_text3 = "Paste the URL once copied in your browser where you're\nalready logged into Instagram"
        self.download_hint3 = customtkinter.CTkLabel(self.download_tabview.tab(tab2_name), 
                                            text=self.download_text3, 
                                            text_color="#fff", 
                                            width=150, 
                                            justify="center", 
                                            anchor="w")
        self.download_hint3.grid(row=1, column=0, padx=(20, 20), pady=(0, 0)) 

        self.download_tab2_copy_URL_button = customtkinter.CTkButton(self.download_tabview.tab(tab2_name),
                                                text="Copy URL to clipboard", 
                                                image=self.copy,
                                                anchor= "bottom",
                                                hover_color="orange",
                                                compound="top",
                                                command=self.download_copy_url_tab2)
        self.download_tab2_copy_URL_button.grid(row=2, column=0, padx=(10, 10), pady=(20, 10))

        # ------------------------------------
        # DOWNLOAD FRAME - STEP 2
        # ------------------------------------
        self.download_step2_txt = customtkinter.CTkLabel(self.download_frame, 
                                                text="STEP 2 - NOT COMPLETE", 
                                                text_color="#fff", bg_color="red",
                                                width=250, 
                                                justify="left", 
                                                anchor="w")
        self.download_step2_txt.grid(row=3, column=0, padx=(40, 40), pady=(20, 0))  

        self.download_step2_box = customtkinter.CTkFrame(self.download_frame)
        self.download_step2_box.grid(row=4, column=0, padx=(40, 40), pady=(20, 10))

        self.download_pics_switch_ = customtkinter.CTkSwitch(self.download_step2_box, text="Get Pics")
        self.download_pics_switch_.grid(row=0, column=0, padx=(50,225), pady=(20, 20))
        self.download_pics_switch_.select()

        self.download_vids_switch_ = customtkinter.CTkSwitch(self.download_step2_box, text="Get Vids")
        self.download_vids_switch_.grid(row=0, column=0, padx=(225,50), pady=(20, 20))
        self.download_vids_switch_.select()

        self.download_text4 = "Copy the entire response content from your browser before\nclicking this button"
        self.download_hint4 = customtkinter.CTkLabel(self.download_step2_box, 
                                            text=self.download_text4, 
                                            text_color="red", 
                                            width=150, 
                                            justify="center", 
                                            anchor="w")
        self.download_hint4.grid(row=1, column=0, padx=(20, 20), pady=(0, 0)) 

        self.download_paste_url_button = customtkinter.CTkButton(self.download_step2_box,
                                                        text="Paste & Download", 
                                                        image=self.download,
                                                        anchor= "bottom",
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.download_run)
        self.download_paste_url_button.grid(row=2, column=0, padx=(10,10), pady=(20, 20))  

        self.progressbar_1 = customtkinter.CTkProgressBar(self.download_step2_box)
        self.progressbar_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1.set(0)  

        self.download_console_textbox = customtkinter.CTkTextbox(self.download_frame, width=400, height=140)
        self.download_console_textbox.grid(row=5, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew", columnspan=2)   
        self.download_console_textbox.insert("0.0", "")
        self.download_console_textbox.configure(state=tkinter.DISABLED) 

        # ------------------------------------
        # SETTINGS FRAME
        # ------------------------------------
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure((0,1), weight=1)

        self.settings_btn1 = customtkinter.CTkButton(self.settings_frame,
                                                        text="ADD USER", 
                                                        image=self.add_user,
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.settings_add_user_button_event,
                                                        width=300,
                                                        height=100)
        self.settings_btn1.grid(row=1, column=0, padx=(10,0), pady=(50, 20))  
        
        self.settings_btn2 = customtkinter.CTkButton(self.settings_frame,
                                                        text="DELETE USER", 
                                                        image=self.delete_user,
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.settings_delete_user_button_event,
                                                        width=300,
                                                        height=100)
        self.settings_btn2.grid(row=1, column=1, padx=(0,10), pady=(50, 20)) 

        self.settings_btn3 = customtkinter.CTkButton(self.settings_frame,
                                                        text="EDIT OUTPUT PATH", 
                                                        image=self.add_user,
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.settings_set_output_button_event,
                                                        width=300,
                                                        height=100)
        self.settings_btn3.grid(row=2, column=0, padx=(10,0), pady=(20, 20)) 

        self.settings_btn4 = customtkinter.CTkButton(self.settings_frame,
                                                        text="OPEN OUTPUT FOLDER\nIN FILE EXPLORER", 
                                                        image=self.add_user,
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.settings_open_output_button_event,
                                                        width=300,
                                                        height=100)
        self.settings_btn4.grid(row=2, column=1, padx=(0,10), pady=(20, 20)) 

        self.settings_pathield_textbox = customtkinter.CTkTextbox(self.settings_frame, width=400, height=10)
        self.settings_pathield_textbox.grid(row=3, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew", columnspan=2)   
        self.settings_pathield_textbox.insert("0.0", getOutputPath())
        self.settings_pathield_textbox.configure(state=tkinter.DISABLED)     

        """
        # TICKABLE BUTTONS
        self.settings_checkbox_1 = customtkinter.CTkCheckBox(master=self.settings_frame, text="Create one folder per ID")
        self.settings_checkbox_1.grid(row=4, column=0, padx=(10, 10), pady=(20, 20), sticky="n")

        self.settings_checkbox_2 = customtkinter.CTkCheckBox(master=self.settings_frame, text="Create one folder per day")
        self.settings_checkbox_2.grid(row=4, column=1, padx=(10, 10), pady=(20, 20), sticky="n")
        """
        
      
        self.settings_id_folder_state = customtkinter.CTkSwitch(self.settings_frame,
                                                                command=self.settings_id_folder_switch_state_event, 
                                                                text="Create one folder per ID")
        self.settings_id_folder_state.grid(row=4, column=0, padx=(10, 10), pady=(20, 20), sticky="n")

        if getIdFolderState() == True:
            self.settings_id_folder_state.select()

        self.settings_daily_folder_state = customtkinter.CTkSwitch(self.settings_frame,
                                                                    command=self.settings_daily_folder_switch_state_event, 
                                                                    text="Create one folder per day")
        self.settings_daily_folder_state.grid(row=4, column=1, padx=(10, 10), pady=(20, 20), sticky="n")   

        if getDailyFolderState() == True:
            self.settings_daily_folder_state.select()
        
        # ------------------------------------
        # SETTINGS FRAME - ADD USER
        # ------------------------------------
        self.settings_add_user_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_add_user_frame.grid_columnconfigure(0, weight=1)

        self.settings_add_user_textbox = customtkinter.CTkTextbox(self.settings_add_user_frame, width=250)
        self.settings_add_user_textbox.grid(row=0, column=0, padx=(20, 20), pady=(30, 10), sticky="nsew")
        self.settings_add_user_textbox.insert("0.0", self.dictToString(getUsers()))
        self.settings_add_user_textbox.configure(state=tkinter.DISABLED)

        self.settings_add_user_id_entry = customtkinter.CTkEntry(self.settings_add_user_frame, 
                                                                placeholder_text="ACC ID (ex: 16771389)", 
                                                                width=180)
        self.settings_add_user_id_entry.grid(row=1, column=0, columnspan=2, padx=(10, 230), pady=(20, 20))

        self.settings_add_user_name_entry = customtkinter.CTkEntry(self.settings_add_user_frame,
                                                                    placeholder_text="ACC name (ex: @nrg_mash)",
                                                                    width=180)
        self.settings_add_user_name_entry.grid(row=1, column=0, columnspan=2, padx=(230, 10), pady=(20, 20))

        self.settings_add_user_button = customtkinter.CTkButton(self.settings_add_user_frame,
                                                        text="ADD USER", 
                                                        image=self.add_user,
                                                        fg_color="green",
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.settings_add_user_add_button_event,
                                                        width=200,
                                                        height=70)
        self.settings_add_user_button.grid(row=2, column=0, padx=(10,0), pady=(0, 20))

        # ------------------------------------
        # SETTINGS FRAME - DELTE USER
        # ------------------------------------
        self.settings_delete_user_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_delete_user_frame.grid_columnconfigure(0, weight=1)

        self.settings_delete_user_textbox = customtkinter.CTkTextbox(self.settings_delete_user_frame, width=250)
        self.settings_delete_user_textbox.grid(row=0, column=0, padx=(20, 20), pady=(30, 10), sticky="nsew")
        self.settings_delete_user_textbox.insert("0.0", self.dictToString(getUsers()))
        self.settings_delete_user_textbox.configure(state=tkinter.DISABLED)

        self.settings_delete_user_option_menu = customtkinter.CTkOptionMenu(self.settings_delete_user_frame,
                                                        dynamic_resizing=False,
                                                        values=sorted(getUsers().values()))
        self.settings_delete_user_option_menu.grid(row=1, column=0, padx=(10, 10), pady=(20, 20))

        self.settings_delete_user_button = customtkinter.CTkButton(self.settings_delete_user_frame,
                                                        text="DELETE USER", 
                                                        image=self.delete_user,
                                                        fg_color="red",
                                                        hover_color="orange",
                                                        compound="top",
                                                        command=self.settings_delete_user_delete_button_event,
                                                        width=200,
                                                        height=70)
        self.settings_delete_user_button.grid(row=2, column=0, padx=(10,0), pady=(0, 20))

        # ------------------------------------
        # STARTUP FRAME SELECTION
        # ------------------------------------
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name : str):
        """
            Takes care of the frames transitioning between
            the different tabs of the app. It also resets
            some events to its default value when the
            transition is made such as the 'STEPS' colors
            in the Download frame.
        """

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

        if name == "settings_add_user":
            self.settings_add_user_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_add_user_frame.grid_forget()

        if name == "settings_delete_user":
            self.settings_delete_user_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_delete_user_frame.grid_forget()

        # set colors back to the red background
        self.download_step1_txt.configure(text="STEP 1 - NOT COMPLETE", bg_color="red")
        self.download_step2_txt.configure(text="STEP 2 - NOT COMPLETE", bg_color="red")

    # - Frame Transitioning > Sidebar
    def home_button_event(self):
        """
            Changes the current frame to the 'home' one
        """
        self.select_frame_by_name("home")

    def download_button_event(self):
        """
            Changes the current frame to the 'download' one
        """
        self.select_frame_by_name("download")

    # - Frame Transitioning > Settings
    def settings_button_event(self):
        """
            Changes the current frame to the 'settings' one
        """
        self.select_frame_by_name("settings")

    def settings_add_user_button_event(self):
        """
            Changes the current frame to the 'settings_add_user' one
        """
        self.select_frame_by_name("settings_add_user")

    def settings_delete_user_button_event(self):
        """
            Changes the current frame to the 'settings_delete_user' one
        """
        self.select_frame_by_name("settings_delete_user")

    # ------------------------
    # BUTTONS FUNCTIONS CALLED IN init()
    # ------------------------
    # - Home - page
    def home_mash_channel(self):
        """
            Uses the default system browser to open the
            'Mash' Youtube channel
        """
        webbrowser.open("https://www.youtube.com/@MashMash")

    def home_nrg_mash_channel(self):
        """
            Uses the default system browser to open the
            'NRG_Mash' Youtube channel
        """
        webbrowser.open("https://www.youtube.com/@nrg_mash6676")

    def home_discord(self):
        """
            Uses the default system browser to take you
            to my discord
        """
        webbrowser.open("https://discord.gg/4gSWzdadhR")

    def home_instagram(self):
        """
            Uses the default system browser to take you
            to my instagram
        """
        webbrowser.open("https://www.instagram.com/nrg_mash/")

    def home_tiktok(self):
        """
            Uses the default system browser to take you
            to my Tiktok
        """
        webbrowser.open("https://www.tiktok.com/@_mashiro")

    # - Download - page
    def download_copy_url_tab1(self):
        """
            Copies to the clipboard the URL associated with 
            the selected user in the droplist that's selected
            in the download tab1 section.
        """

        self.download_step1_txt.configure(text="STEP 1 - COMPLETE", bg_color="green")
        self.download_step2_txt.configure(text="STEP 2 - NOT COMPLETE", bg_color="red")

        username = self.download_id_droplist.get()
        copyUrlByName(userName=username)

    def download_copy_url_tab2(self):
        """
            Copies to the clipboard the URL associated with 
            the specified user in the texfield in the
            download tab2 section.
        """
        self.download_step1_txt.configure(text="STEP 1 - COMPLETE", bg_color="green")
        self.download_step2_txt.configure(text="STEP 2 - NOT COMPLETE", bg_color="red")

        id = self.download_id_entry.get()
        copyUrlById(userid=id)

    def download_run(self):
        """
            Downloads the content and updates the console text
            in the download section.
        """

        self.download_step2_txt.configure(text="STEP 2 - COMPLETE", bg_color="green")

        try:
            data, userId = getContentDict()
        except Exception as e:
            self.download_console_textbox.configure(state=tkinter.NORMAL)
            self.download_console_textbox.insert("0.0", "[{0}] {1}\n".format(datetime.now().strftime("%H:%M:%S"), "No Response JSON recognized. Are you sure you did copy to your clipboard the whole response before clicking download ?"))
            self.download_console_textbox.configure(state=tkinter.DISABLED)           

        idx = 0
        for url, type in data.items():
            filename = url.split(type)[0].split("/")[-1]
            
            if type == ".mp4":
                log_msg_success = "VID - SUCCESS - {0}...".format(filename)
                log_msg_failure = "VID - !FAIL!  - {0}...".format(filename)
                log_msg_ignored = "VID - IGNORED - {0}...".format(filename)
            elif type == ".jpg":
                log_msg_success = "PIC - SUCCESS - {0}...".format(filename)
                log_msg_failure = "PIC - !FAIL!  - {0}...".format(filename)
                log_msg_ignored = "PIC - IGNORED - {0}...".format(filename)

            if type == ".jpg" and self.download_pics_switch_.get() == 1 or type == ".mp4" and self.download_vids_switch_.get() == 1:
                status = getFileByUrl(url=url, type=type, userId=userId, dailyFolderState=getDailyFolderState(), idFolderState=getIdFolderState())


            else:
                status = "Ignored"

            if status == 1:
                log_message = log_msg_failure
            elif status == 0:
                log_message = log_msg_success
            else:
                log_message = log_msg_ignored

            #history = self.download_console_textbox.get("0.0", "end")
            self.download_console_textbox.configure(state=tkinter.NORMAL)
            self.download_console_textbox.insert("0.0", "[{0}] {1}\n".format(datetime.now().strftime("%H:%M:%S"), log_message))
            self.download_console_textbox.configure(state=tkinter.DISABLED)

            idx+=1
            self.progressbar_1.set((1/len(data))*idx)
            app.update()
            
    # - Settings - page
    def settings_id_folder_switch_state_event(self):
        """
            Switches the status of the value 'idfolders' in
            the .ini file
        """
        setIdFolderState(getIdFolderState())

    def settings_daily_folder_switch_state_event(self):
        """
            Switches the status of the value 'dailyfolder' in
            the .ini file
        """
        setDailyFolderState(getDailyFolderState())

    def settings_set_output_button_event(self):
        """
            Changes the specified output path in the .ini file
            using the file explorer
        """

        setOutputPath()
        self.displayDBUpdate()

    def settings_open_output_button_event(self):
        """
            Open the specified output path in the .ini file
            using the file explorer
        """
        openOuputPath()

    # - Settings > add_user - page
    def settings_add_user_add_button_event(self):
        """
            Add an user to the database using the two fields
            present in the options: ID/Name
        """

        name = self.settings_add_user_name_entry.get()
        id   = self.settings_add_user_id_entry.get()
        addUser(id, name)
        self.displayDBUpdate()

    # - Settings > delete_user - page
    def settings_delete_user_delete_button_event(self):
        """
            Delete an user to the database using the droplist
            in the options
        """
        
        username = self.settings_delete_user_option_menu.get()
        deleteUserByName(username)
        self.displayDBUpdate()

    # - [GENERAL]
    def displayDBUpdate(self):
        """
            Updates all the Droplists and Textboxes 's data
            and should be called at when a modification in the database is
            performed.
        """

        # Download
        # ---------> Droplist
        self.download_id_droplist.configure(values=sorted(getUsers().values()))

        # Settings
        # ---------> Textbox
        self.settings_pathield_textbox.configure(state=tkinter.NORMAL)
        self.settings_pathield_textbox.delete("0.0", "end")
        self.settings_pathield_textbox.insert("0.0", getOutputPath())
        self.settings_pathield_textbox.configure(state=tkinter.DISABLED)

        # Settings > add_user
        # ---------> Textbox
        self.settings_add_user_textbox.configure(state=tkinter.NORMAL)
        self.settings_add_user_textbox.delete("0.0", "end")
        self.settings_add_user_textbox.insert("0.0", self.dictToString(getUsers()))
        self.settings_add_user_textbox.configure(state=tkinter.DISABLED)

        # Settings > delete_user
        # ---------> Textbox
        self.settings_delete_user_textbox.configure(state=tkinter.NORMAL)
        self.settings_delete_user_textbox.delete("0.0", "end")
        self.settings_delete_user_textbox.insert("0.0", self.dictToString(getUsers()))
        self.settings_delete_user_textbox.configure(state=tkinter.DISABLED)

        # ---------> Droplist
        self.settings_delete_user_option_menu.configure(values=sorted(getUsers().values()))

    def dictToString(self, my_dict : dict) -> str:
        """
            Returns the list of users and their IDs used in the 
            ADD_USER/DELETE_USER section in a str format for Textboxes display.
        """

        final_string = ""
        for key, value in my_dict.items():
            final_string = final_string + "{0} | {1}\n".format(key, value)
        return final_string

    def change_appearance_mode_event(self, new_appearance_mode):
        """
            Changes the window theme.
        """
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()