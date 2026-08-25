# 鼻部整形 · 术后恢复期器械资产库

一套用于「鼻部整形术后恢复期模拟」的可复用矢量资产库。所有资产均为原创 SVG 矢量图，
透明背景、可无损缩放，可按需导出为透明 PNG。

## 目录结构

```
rhinoplasty-recovery-assets/
├── index.html                 # 交互式画廊（双击打开浏览全部资产）
├── keypoints/
│   └── landmarks.json         # 鼻部解剖关键点 + 各器械配准关键点坐标
└── assets/
    ├── nose-base-front.svg    # 鼻部解剖参考 · 正面（关键点标注）
    ├── nose-base-profile.svg  # 鼻部解剖参考 · 侧面（关键点标注）
    ├── splint-thermoplastic.svg   # 热塑鼻夹板
    ├── splint-aluminum.svg        # 铝制鼻夹板（Denver 型）
    ├── splint-plaster.svg         # 石膏鼻夹板
    ├── tape-micropore.svg         # 医用胶带 / 免缝胶带（Micropore）
    ├── tape-steristrip.svg        # 免缝胶条（Steri-Strip）
    ├── dressing-gauze.svg         # 纱布敷料
    ├── dressing-drip-pad.svg      # 胡须敷料 / 滴液垫（mustache dressing）
    ├── packing-doyle.svg          # 鼻内填塞 / Doyle 硅胶鼻栓
    └── cold-gel-mask.svg          # 冷敷凝胶面罩 / 冰袋
```

## 每个器械 SVG 的内部结构

每个 SVG 含三个视角槽位（`viewBox="0 0 660 300"`）：

| 槽位 | X 范围 | 视图 |
|------|--------|------|
| A    | 0–220  | 正面（front） |
| B    | 220–440| 侧面（profile） |
| C    | 440–660| 模板 / 俯视 / 平铺（flat template） |

每个视角内部含三个可切换图层：

- `g.fill`     — 标准图（填色 + 描边）
- `g.outline`  — 轮廓（仅描边，无填充）
- `g.keypoints`— 关键点（红色圆点 + 标签）

默认只显示 `fill`。画廊页提供「标准图 / 轮廓 / 关键点」切换按钮。
若需单独导出某一视图，删除另外两个槽位的 `<g>` 即可。

## 关键点（landmarks）

鼻部配准关键点见 `keypoints/landmarks.json`，坐标分别对应
`nose-base-front.svg`（200×320）与 `nose-base-profile.svg`（240×320）坐标系。
器械卡中的关键点坐标为器械自身配准点（如夹板上下端点、胶带两端、敷料中心等），
用于把器械贴合到鼻部参考图上。

## 恢复期时间线（研究摘要）

| 时间 | 器械状态 |
|------|----------|
| 术后 0–2 天 | 鼻夹板 + 胡须敷料/滴液垫 + 鼻内填塞 + 冷敷（肿胀淤青高峰） |
| 术后 3–7 天 | 夹板在位；敷料/鼻栓拆除；胶带保留；拆线（4–7 天） |
| 术后 7–10 天 | 拆除鼻夹板 → 转夜间胶带固定 |
| 术后 2–4 周 | 夜间胶带（supratip → radix），减轻水肿、帮助皮肤回贴 |
| 术后 1–3 月 | 大部分肿胀消退；个别夜间胶带 |
| 术后 6–12 月 | 最终形态；鼻尖最后定型（可达 12–18 个月） |

> 夹板类型：热塑（Thermoplastic/Aquaplast）、铝制（Aluminum/Denver）、石膏（POP）。
> 仅当骨性结构被改动时才需刚性夹板；纯软骨矫正可只用胶带。
> 以上为通用参考，具体遵手术医生医嘱。

## 使用许可

本库为原创示意图，仅用于教学 / 产品原型 / 术前术后沟通演示。
真实「标准照片」请以器械厂商产品页与教科书影像为准（见 index.html 底部来源）。
