# iosMixTools
ios混淆脚本工具,顺便安利一波:  [IOS马甲包混淆](https://blog.csdn.net/lyzz0612/article/details/80390362)

### 1.  addNative.py 生成oc垃圾代码工具
此脚本会扫描指定目录，给OC文件添加垃圾函数，同时创建垃圾文件到/trash目录。
#### 参数说明

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


### 3. autoBornCode.py 添加lua和png，修改资源文件MD5
此脚本会扫描指定文件夹，在路径包含/res的目录创建png, 其他地方创建lua。根据目录下的文件和文件夹数随机添加文件和子文件夹。然后会给大部分类型资源文件添加一些无效内容来改变其MD5。

#### 参数说明

* `--res RESOURCE_DIR` 资源目录
* `--target TARGET_FOLDER` 可选参数，修改后的资源存放目录。不设置为脚本目录下的target_resource 

在代码的最前面有个匹配规则, path_exclude表示必须是不包含该字符串的路径才能创建该类型文件，path_include表示必须是包含该字符串的路径才要创建该类型文件
```
match_rule = {
    ".png": {
        "path_include": os.path.sep + "res",
    },
    ".lua": {
        # "path_include": "src",
        "path_exclude": os.path.sep + "res",
    },
}
```
**TODO**音效文件修改MD5值
