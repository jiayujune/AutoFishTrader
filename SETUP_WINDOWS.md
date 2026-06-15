# Windows 安装指南

在新的 Windows 电脑上从零跑起来,按顺序做。

## 1. 装 Python
- 去 https://www.python.org/downloads/ 下载 Python 3.12+
- 安装时**务必勾选「Add Python to PATH」**,否则后面命令找不到 python

## 2. 装 adb(platform-tools)
推荐用 winget(Win10/11 自带),打开 **cmd** 或 **PowerShell** 执行:
```cmd
winget install Google.PlatformTools
```
装完**关掉重开**一个新的 cmd 窗口(让 PATH 生效),验证:
```cmd
adb version
```
> 如果没有 winget:去 https://developer.android.com/tools/releases/platform-tools 下载
> `platform-tools` 压缩包,解压到比如 `C:\platform-tools`,再把这个路径加到
> 系统环境变量 PATH 里。

## 3. 装手机 USB 驱动(Windows 特有,最容易卡这一步)
Windows 经常认不出手机,需要装厂商驱动:
- **小米/红米**:装「小米助手」会自动带驱动
- **华为/荣耀**:装「华为手机助手 HiSuite」
- **OPPO/vivo/一加**:去官网下对应的 USB 驱动
- 通用兜底:Google USB Driver
- 装完在「设备管理器」里能看到手机、且没有黄色感叹号就对了

## 4. 手机开 USB 调试
- 设置 → 关于手机 → 连点 7 次「版本号」→ 开启开发者模式
- 设置 → 开发者选项 → 打开「USB 调试」
- USB 连电脑,手机弹「允许 USB 调试吗?」→ 点**允许**(勾选"一律允许")

## 5. 安装项目环境
把整个项目文件夹拷到这台电脑(**不要拷 `.venv` 文件夹**,它不跨机器/跨系统通用),
然后双击运行 `setup.bat`(或在 cmd 里执行)。它会自动建 venv、装依赖、检查 adb。

## 6. 验证
```cmd
adb devices
.venv\Scripts\python dump_ui.py
```
`adb devices` 能看到设备、dump_ui 能在 `dumps\` 里生成截图,就算成功。

---

### 拷贝注意
跨机器迁移时,带上这些就够了:
```
dump_ui.py  requirements.txt  setup.bat  SETUP_WINDOWS.md  README.md
（以及后续写的 main.py / config.py 等源码）
```
**不要带 `.venv\` 和 `dumps\`** —— venv 在新机器上由 setup.bat 重新生成。
