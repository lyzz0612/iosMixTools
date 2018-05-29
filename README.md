# iosMixTools
ios混淆脚本工具

### 1.  addNative.py 生成oc垃圾代码工具
此脚本会扫描指定proj.ios_mac下的ios目录，给OC文件添加垃圾函数，同时创建垃圾文件到ios/trash目录。它有以下参数可选：

* ` --oc_folder OC_FOLDER` OC_FOLDER为OC代码所在目录
* `--replace`替换OC_FOLDER下的原文件，同时原代码会备份到脚本目录下的backup_ios目录。不指定此项垃圾代码只会放到脚本目录下的target_ios/

addNative.py里还有一些配置可以看需求手动修改，如生成垃圾文件的数量，垃圾函数的数量，忽略文件列表等，具体请查看代码顶部相关注释

### 2. renameNative.py 修改类名前缀工具
类名是引用可能较为复杂的东西，工具批量替换的限制要求会比较多。如果你的项目满足以下条件，那么这个工具会比较适合你：

* 大部分类名都带相同的前缀，也只准备替换前缀；
* 大部分类都只在一个大文件夹下，它们之间相互引用，外部调用的情况较少并且你能很有把握的排除或手动替换它们；
* 类名和文件名一致；

本工具的流程是扫描指定文件夹，找到名称（或者说类名，工具假设两者是一致的）以指定前缀开始的文件；修改替换文件名前缀；并再次遍历此文件夹所有文件，将文件内容中的所有该名称也替换掉；替换xx.xcodeproj/project.pbxproj下的路径，省去在Xcode中手动添加文件（因为文件名修改了，不替换的话Xcode上还保持原来的名称会提示找不到文件）；同时为了防止文件夹名称跟文件名相同而导致替换project.pbxproj时将目录名也替换掉的情况，对文件夹名称也进行相同的流程。

#### 参数说明：

* `--old_prefix OLD_PREFIX` 替换前的类名前缀
* `--new_prefix NEW_PREFIX` 替换后的类名前缀
* `--ios_path IOS_PATH` OC文件目录
* `--proj_path PROJ_PATH ` xx.xcodeproj路径

运行示例：`python renameNative.py --old_prefix ANDROID --new_prefix IOS --ios_path xx/xx/xx/ --proj_path xx/xx/xx.xcodeproj`


