# iosMixTools
ios混淆脚本工具

### 1.  addNative.py 生成oc垃圾代码工具
此脚本会扫描指定proj.ios_mac下的ios目录，给OC文件添加垃圾函数，同时创建垃圾文件到ios/trash目录。它有以下参数可选：

* ` --oc_folder OC_FOLDER` OC_FOLDER为OC代码所在目录
* `--replace`替换OC_FOLDER下的原文件，同时备份原代码会备份到脚本目录下的backup_ios目录。不指定此项垃圾代码只会放到脚本目录下的target_ios/

addNative.py里还有一些配置可以看需求手动修改，如生成垃圾文件的数量，垃圾函数的数量，忽略文件列表等，具体请查看代码顶部相关注释