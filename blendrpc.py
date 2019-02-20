from pypresence import Presence
from const import CONST
import threading
import traceback
import time
import bpy
import os
import re

bl_info = {
	"name": "BlendRPC",
	"description": "Adds Rich Presence support to Blender",
	"author": "@SoulSenGaming#1321",
	"version": (1, 0),
	"github": "https://github.com/SoulSen/blendrpc",
	"support": "COMMUNITY",
	"category": "System"
	}

CYCLE = bpy.app.version_cycle
VERSION = re.sub("[\(\[].*?[\)\]]", "", bpy.app.version_string) + " " +  CYCLE
blendrpc = Presence(client_id=CONST.CLIENT_ID)


def getFileName():
    try:
        PATH, FILENAME = os.path.split(bpy.data.filepath)
        if FILENAME == "":
            FILENAME = "None"
        return FILENAME
    except AttributeError:
        FILENAME = "None"
        return FILENAME


def updatePresenceAlways():
    threading.Timer(30, updatePresenceAlways).start()
    
    try:
        _filename = getFileName()
        if _filename == "None":
            blendrpc.update(large_image="blender_logo", large_text="Blender {}".format(VERSION), small_image="blender_file_icon", small_text="Nothing",
                            details="Doing Nothing", state="Blender {}".format(VERSION), start=int(time.time()))
        else:
            blendrpc.update(large_image="blender_logo", large_text="Blender {}".format(VERSION), small_image="blender_file_icon", small_text=_filename,
                            details="Editing {}".format(_filename), state="Blender {}".format(VERSION), start=int(time.time()))
    except Exception as e:
        print("[BlendRPC] An error has occurred, please contact developer with this information:\n{}".format(traceback.format_exc()))
        unregister()
        

def register():
	print("[BlendRPC] Starting BlendRPC")

	try:
            blendrpc.connect()
            print("[BlendRPC] Successfully Connected!")
            updatePresenceAlways()
	except Exception as e:
	    print("[BlendRPC] An error has occurred, please contact developer with this information:\n{}".format(traceback.format_exc()))
	    unregister()


def unregister():
        try:
            blendrpc.close()
            print("[BlendRPC] Closing Connection...")
        except Exception as e:
            print("[BlendRPC] An error has occurred, please contact developer with this information:\n{}".format(traceback.format_exc()))


if __name__ == "__main__":
    register()
