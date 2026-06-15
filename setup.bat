@echo off
chcp 65001 >nul
REM ============================================================
REM  Windows 一键环境安装脚本
REM  双击运行,或在 cmd 里执行: setup.bat
REM ============================================================
setlocal

echo.
echo === [1/4] 检查 Python ===
where python >nul 2>nul
if errorlevel 1 (
    echo [错误] 没找到 python。请先去 https://www.python.org/downloads/ 安装,
    echo        安装时务必勾选 "Add Python to PATH"。
    pause
    exit /b 1
)
python --version

echo.
echo === [2/4] 创建虚拟环境 .venv ===
if not exist .venv (
    python -m venv .venv
    echo 已创建 .venv
) else (
    echo .venv 已存在,跳过
)

echo.
echo === [3/4] 安装 Python 依赖 ===
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败,请把上面的报错发给我。
    pause
    exit /b 1
)

echo.
echo === [4/4] 检查 adb ===
where adb >nul 2>nul
if errorlevel 1 (
    echo [警告] 没找到 adb。请按 SETUP_WINDOWS.md 安装 platform-tools,
    echo        最简单: 在 cmd 里执行  winget install Google.PlatformTools
    echo        装完关掉这个窗口重新运行本脚本。
) else (
    echo adb 已安装:
    adb version
    echo.
    echo 当前连接的设备(手机插上 USB 并开启调试后应能看到):
    adb devices
)

echo.
echo === 完成 ===
echo 测试抓屏:  .venv\Scripts\python dump_ui.py
echo.
pause
endlocal
