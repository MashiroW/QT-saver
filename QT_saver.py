from configparser import ConfigParser
import pyperclip
import requests
import json
import os
import ast


#Relative path
dirname = os.path.dirname(__file__)

# Application configuration
app_config = ConfigParser()
app_config.read(os.path.join(dirname, "./config.ini"))
SYSTEM_SECTION_APP    = app_config.sections()[0]
SAVEPATH              = str(app_config.get(SYSTEM_SECTION_APP, 'savepath'))

def getUsers():
    return json.loads(str(app_config.get(SYSTEM_SECTION_APP, 'savedusers')))

def addUser(userId, userName):
    savedUsers = getUsers()
    if userId in savedUsers or userName in savedUsers.values():
        return 1

    else:
        savedUsers[userId] = userName
        savedUsers         = json.dumps(ast.literal_eval(str(savedUsers)))

        app_config.set(SYSTEM_SECTION_APP, 'savedusers', str(savedUsers))

        with open('config.ini', 'w') as configfile:
            app_config.write(configfile)
        return 0

def deleteUserById(userId):
    savedUsers = getUsers()
    if userId in savedUsers:
        savedUsers.pop(userId)
        savedUsers = json.dumps(ast.literal_eval(str(savedUsers)))

        app_config.set(SYSTEM_SECTION_APP, 'savedusers', str(savedUsers))

        with open('config.ini', 'w') as configfile:
            app_config.write(configfile)

        return 0

    else:
        return 1

def deleteUserByName(userName):
    savedUsers = getUsers()
    for key, value in savedUsers.items():
        if value == userName:
            savedUsers.pop(key)
            savedUsers = json.dumps(ast.literal_eval(str(savedUsers)))

            app_config.set(SYSTEM_SECTION_APP, 'savedusers', str(savedUsers))

            with open('config.ini', 'w') as configfile:
                app_config.write(configfile)

            return 0
    return 1

def getURL(id = "None"):

    if id == "None":
        ACCOUNT_ID    = str(app_config.get(SYSTEM_SECTION_APP, "userid"))

    else:
        ACCOUNT_ID    = id

    URL = "https://www.instagram.com/graphql/query/?query_hash=de8017ee0a7c9c45ec4260733d81ea31&variables=%7B%22reel_ids%22%3A%5B%22{0}%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A50%2C%22story_viewer_cursor%22%3A%22%22%7D".format(ACCOUNT_ID)

    return URL

def welcome():
    print("------TURBO CUTIE SAVER 3000-----")
    print("---------------------------------")
    print("Open the following URL in your browser that's already logged in to Instagram:\n")
    print(getURL(), "\n")

    print("Now copy to your clipboard the JSON API response then press ENTER")
    os.system("Pause")

def parser():
    urls = []
    src_dict = json.loads(pyperclip.paste())
    count_vids = 0
    count_pics = 0

    for element_idx in range (0, len(src_dict["data"]["reels_media"][0]["items"])):

        # - If video
        if src_dict["data"]["reels_media"][0]["items"][element_idx]["is_video"] == True:
            print("Element #{} (VID):".format(element_idx+1))
            url = src_dict["data"]["reels_media"][0]["items"][element_idx]["video_resources"][0]["src"]
            count_vids +=1

        # - If picture
        else:
            print("Element #{} (PIC):".format(element_idx+1))
            url = src_dict["data"]["reels_media"][0]["items"][element_idx]["display_url"]   
            count_pics +=1      

        urls.append(url)
        #print(url, "\n")

    return urls, count_pics, count_vids

def saver(urls):

    for url in urls:
        response = requests.get(url)

        if ".mp4" in url:
            type = ".mp4"
        else:
            type = ".jpg"

        print(SAVEPATH)
        if SAVEPATH[0] == ".":
            try:
                os.makedirs(dirname + SAVEPATH[1:])
            except FileExistsError:
                # directory already exists
                pass

            filename = dirname + SAVEPATH[1:] + "/" + url.split(type)[0].split("/")[-1] + type
            print("1 Saving to ", filename)
            filename = filename.replace("\\", '//')

        else:
            try:
                os.makedirs(SAVEPATH)
            except FileExistsError:
                # directory already exists
                pass


            filename = SAVEPATH + "/" + url.split(type)[0].split("/")[-1] + type

        print("2 Saving to ", filename)
        open(filename, "wb").write(response.content)

def get_content():
    urls, _, _, = parser()
    saver(urls)

if __name__ == "__main__":
    get_content()



    
