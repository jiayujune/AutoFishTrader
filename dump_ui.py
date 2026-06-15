#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI 抓取工具
------------
连接安卓手机,把"当前屏幕"的信息抓下来,用于编写闲鱼/淘宝的自动化选择器。

用法:
    .venv/bin/python dump_ui.py            # 抓一次当前屏幕
    .venv/bin/python dump_ui.py watch      # 每隔 2 秒抓一次当前前台 App(用于探查)

抓取产物保存在 ./dumps/ 目录:
    - screen_<时间戳>.png   截图
    - screen_<时间戳>.xml   完整 UI 层级(含每个控件的 resourceId / text / bounds)
    - screen_<时间戳>.txt   精简版:只列出有文字或可点击的控件,方便人快速看
"""
import sys
import time
import os
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

import uiautomator2 as u2

DUMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dumps")


def connect():
    """连接 USB 上的手机(只连一台时无需指定序列号)。"""
    print("正在连接手机... (确保已开启 USB 调试并授权)")
    d = u2.connect()
    info = d.info
    print(f"已连接: {d.serial}")
    print(f"  分辨率: {info.get('displayWidth')}x{info.get('displayHeight')}")
    print(f"  当前前台 App: {d.app_current()}")
    return d


def dump_once(d, tag=""):
    os.makedirs(DUMP_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    name = f"screen_{ts}" + (f"_{tag}" if tag else "")

    cur = d.app_current()
    pkg = cur.get("package", "?")
    act = cur.get("activity", "?")

    # 截图
    png_path = os.path.join(DUMP_DIR, name + ".png")
    d.screenshot(png_path)

    # 完整层级 XML
    xml_str = d.dump_hierarchy()
    xml_path = os.path.join(DUMP_DIR, name + ".xml")
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(minidom.parseString(xml_str).toprettyxml(indent="  "))

    # 精简版:列出有 text / resource-id / 可点击 的控件
    txt_path = os.path.join(DUMP_DIR, name + ".txt")
    lines = [f"# 前台 App: {pkg} / {act}", ""]
    root = ET.fromstring(xml_str)
    for node in root.iter("node"):
        text = node.get("text", "").strip()
        rid = node.get("resource-id", "")
        desc = node.get("content-desc", "").strip()
        clickable = node.get("clickable") == "true"
        if text or desc or (rid and clickable):
            lines.append(
                f"text={text!r:30} desc={desc!r:20} id={rid:50} "
                f"clickable={clickable} bounds={node.get('bounds')}"
            )
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[{ts}] 前台: {pkg}")
    print(f"  截图:   {png_path}")
    print(f"  完整XML: {xml_path}")
    print(f"  精简版:  {txt_path}  ({len(lines)-2} 个有用控件)")
    return pkg


def main():
    d = connect()
    mode = sys.argv[1] if len(sys.argv) > 1 else "once"
    if mode == "watch":
        print("\n进入 watch 模式,每 2 秒抓一次。按 Ctrl+C 停止。")
        print("现在请在手机上手动操作到你想抓的界面(闲鱼订单页 / 淘宝下单页 / 客服消息页)。\n")
        try:
            while True:
                dump_once(d, tag="watch")
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n已停止。")
    else:
        dump_once(d)


if __name__ == "__main__":
    main()
