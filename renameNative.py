#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys
import random
import string
import re
import md5
import time
import json
import shutil
import hashlib 
import time
import argparse

import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

old_prefix = "musk"
script_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
target_project_path = ""
new_prefix = ""

#首字母大写
def getUpperPrefix(prefix):
    return prefix.capitalize()

def replaceStringInFile(full_path, old_text, new_text):
    with open(full_path, "r") as fileObj:
        all_text = fileObj.read()
        fileObj.close()

    all_text = all_text.replace(old_text, new_text)
    with open(full_path, "w") as fileObj:
        fileObj.write(all_text)
        fileObj.close()

def getProjFile():
    global old_prefix, new_prefix, target_project_path
    for file in os.listdir(target_project_path):
        if file.endswith(".xcodeproj"):
            return os.path.join(target_project_path, file + "/project.pbxproj")
    return ""

def renameFileInXcodeProj(old_file_name, new_file_name):
    global old_prefix, new_prefix, target_project_path
    proj_file_path = getProjFile()
    if not os.path.exists(proj_file_path):
        print "\tproject.pbxproj不存在"
        return
    replaceStringInFile(proj_file_path, old_file_name, new_file_name)

def renameInAllFile(old_text, new_text):
    global old_prefix, new_prefix, target_project_path
    ios_path = os.path.join(target_project_path, "ios")
    for parent, folders, files in os.walk(ios_path):
        for file in files:
            full_path = os.path.join(parent, file)
            replaceStringInFile(full_path, old_text, new_text)

def dealWithIos():
    print "开始重命名类名"
    global old_prefix, new_prefix, target_project_path
    old_upper_prefix = getUpperPrefix(old_prefix)
    new_upper_prefix = getUpperPrefix(new_prefix)

    ios_path = os.path.join(target_project_path, "ios")
    for parent, folders, files in os.walk(ios_path):
        for file in files:
            if file.startswith(old_upper_prefix):
                print "\t重命名文件" + file
                new_file_name = file.replace(old_upper_prefix, new_upper_prefix)
                old_full_path = os.path.join(parent, file)
                new_full_path = os.path.join(parent, new_file_name)
                os.rename(old_full_path, new_full_path)
                renameFileInXcodeProj(file, new_file_name)

                old_file_base_name = os.path.splitext(file)[0]
                new_file_base_name = old_file_base_name.replace(old_upper_prefix, new_upper_prefix)
                renameInAllFile(old_file_base_name, new_file_base_name)

    for parent, folders, files in os.walk(ios_path):
        for folder in folders:
            if folder.startswith(old_upper_prefix):
                new_folder_name = folder.replace(old_upper_prefix, new_upper_prefix)
                print "\t重命名文件夹: %s -> %s" %(folder, new_folder_name)
                old_full_path = os.path.join(parent, folder)
                new_full_path = os.path.join(parent, new_folder_name)
                os.rename(old_full_path, new_full_path)
                renameFileInXcodeProj(folder, new_folder_name)
    print "finish\n"

def dealWithSrc():
    print "开始复制src"
    global script_path, target_project_path, new_prefix
    target_src_path = os.path.join(target_project_path, "src")
    origin_src_path = os.path.join(script_path, "../../src")
    if os.path.exists(target_src_path):
        shutil.rmtree(target_src_path)
    shutil.copytree(origin_src_path, target_src_path)

    src_relative_path = "Resources/%s/src" %(new_prefix)
    replace_src_path = os.path.join(script_path, src_relative_path)
    if os.path.exists(replace_src_path):
        for parent, folders, files in os.walk(replace_src_path):
            for file in files:
                old_full_path = os.path.join(parent, file)
                new_full_path = old_full_path.replace(replace_src_path, target_src_path)
                shutil.copy(old_full_path, new_full_path)

    print "修改src引用"
    renameFileInXcodeProj("path = ../../../src; sourceTree", "path = src; sourceTree")
    print "finish\n"

def dealWithIcon():
    print "开始替换Icon"
    global script_path, target_project_path, new_prefix
    target_icon_path = os.path.join(target_project_path, "icons/icon.xcassets/AppIcon.appiconset")
    icon_relative_path = "Resources/%s/ios-icon" %(new_prefix)
    replace_icon_path = os.path.join(script_path, icon_relative_path)
    for file in os.listdir(target_icon_path):
        target_full_path = os.path.join(target_icon_path, file)
        replace_full_path = os.path.join(replace_icon_path, file)
        if not file.endswith(".png"):
            continue
        if not os.path.exists(replace_full_path):
            print "\ticon不存在: " + file
            continue
        shutil.copy(replace_full_path, target_full_path)
    print "finish\n"

def dealWithStartImg():
    print "开始替换启动页"
    global script_path, target_project_path, new_prefix
    target_start_path = os.path.join(target_project_path, "ios/LaunchScreenBackground.png")

    start_relative_path = "Resources/%s/startImg/LaunchScreenBackground.png" %(new_prefix)
    replace_start_path = os.path.join(script_path, start_relative_path)
    if not os.path.exists(replace_start_path):
        print "\tResources不存在启动页LaunchScreenBackground.png"
        return
    shutil.copy(replace_start_path, target_start_path)
    print "finish\n"

def getTips():
    text = [
        "接下来的步骤:",
        "1. 更换工程、Target、Scheme、entitilements、info.plist名称、ucode",
        "2. 更换Appid、导入更改证书",
        "3. 检查Build Phase里src的路径(copy和shell touch)、密钥; 编译",
        "4. 提交工程代码",
        "5. 执行addNative.py --replace导入垃圾oc代码",
        "6. 编译+发布",
    ]
    return "\n".join(text)

def initProject(app_args):
    global script_path, new_prefix, target_project_path
    new_prefix = app_args.proj_name
    target_project_path = os.path.join(script_path, "../../frameworks/runtime-src/proj.ios_mac_" + new_prefix)
    project_origin_path = os.path.join(script_path, "../../frameworks/runtime-src/proj.ios_mac")
    if not os.path.exists(target_project_path):
        print "开始拷贝proj.ios_mac"
        shutil.copytree(project_origin_path, target_project_path)

    if app_args.rename_ios:
        dealWithIos()

    if app_args.replace_src:
        dealWithSrc()

    if app_args.replace_icon:
        dealWithIcon()

    if app_args.replace_start:
        dealWithStartImg()
    print "all finished.\n"


#----------------------------------------------------main------------------------------------------------        
def parse_args():
    global script_path, proj_ios_path
    parser = argparse.ArgumentParser(description='马甲包初始化工具.\n')
    parser.add_argument('--rename', dest='rename_ios', required=False, help='重命名ios类名', action="store_true")
    parser.add_argument('--replace_src', dest='replace_src', required=False, help='替换src', action="store_true")
    parser.add_argument('--replace_icon', dest='replace_icon', required=False, help='替换icon', action="store_true")
    parser.add_argument('--replace_start', dest='replace_start', required=False, help='替换启动页', action="store_true")
    parser.add_argument('--name', dest='proj_name', type=str, required=False, help='马甲包前缀')

    args = parser.parse_args()
    return args

def main():
    app_args = parse_args()
    if not app_args.proj_name:
        print getTips()
        exit(0)
    initProject(app_args)
 

if __name__ == "__main__":
    main()