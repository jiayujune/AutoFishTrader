# 闲鱼 VIN 代购自动化

闲鱼买家拍下 → 自动去淘宝下单付款(免密)→ 从淘宝客服消息抓取查询链接 → 自动回发给闲鱼买家。

## 流程
```
闲鱼新订单(已付款)
  → 淘宝搜索商品并下单
  → 付款(试水期:人工确认;稳定后:小额免密全自动)
  → 等待淘宝客服自动发来"查询链接"消息
  → 复制链接,回到闲鱼回复买家 + 点发货
  → 落库标记完成
```

## 环境准备
1. 安装 adb(一次性):
   ```bash
   sudo apt-get install -y android-tools-adb android-tools-fastboot
   ```
2. Python 依赖已装在 `.venv/`:
   ```bash
   .venv/bin/pip install -r requirements.txt
   ```
3. 手机:开启「开发者选项 → USB 调试」,USB 连电脑,弹出授权时点「允许」。
4. 验证连接:
   ```bash
   adb devices          # 应能看到你的设备
   .venv/bin/python dump_ui.py    # 抓当前屏幕
   ```

## 文件
- `dump_ui.py` — UI 抓取工具,用于编写闲鱼/淘宝选择器(开发阶段用)
- `dumps/` — 抓取产物(截图 / XML / 精简列表)

> ⚠️ 自动化操控闲鱼/淘宝违反平台协议,有封号风险。试水期请开人工确认,小步验证。
