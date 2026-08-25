# -*- coding: utf-8 -*-
"""把器械透明 PNG 按鼻部关键点贴到真实人脸照片上，生成模拟照。

关键点定位：OpenCV 人脸 + 双眼检测 → 推算鼻根(nasion)、鼻下点(subnasale)、鼻翼宽度。
器械前端槽位与 nose-base 参考图同坐标系（中心 x=100，nasion y=96，subnasale y=282，鼻翼宽 60）。
"""
import cv2
import numpy as np
from PIL import Image
import pathlib

ROOT = pathlib.Path(r"C:\Users\86158\rhinoplasty-recovery-assets")
DEMO = ROOT / "demo"
PNG = ROOT / "png"

# 参考坐标系常量（与 nose-base-front.svg 一致）
REF_NASION = (100.0, 96.0)
REF_SUBNASALE = (100.0, 282.0)
REF_ALAR_W = 60.0           # 鼻翼宽度（单位）
REF_SPAN = REF_SUBNASALE[1] - REF_NASION[1]   # 186


def detect(img_path):
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape
    face_c = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
    eye_c = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    faces = face_c.detectMultiScale(gray, 1.08, 5, minSize=(100, 100))
    if len(faces) == 0:
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml").detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
    if len(faces) == 0:
        raise RuntimeError("未检测到人脸")
    fx, fy, fw, fh = max(faces, key=lambda r: r[2] * r[3])

    roi = gray[fy:fy + fh, fx:fx + fw]
    eyes = eye_c.detectMultiScale(roi, 1.1, 6, minSize=(int(0.07 * fw), int(0.07 * fw)))
    centers = sorted((fx + ex + ew // 2, fy + ey + eh // 2) for (ex, ey, ew, eh) in eyes)

    if len(centers) >= 2:
        l, r = centers[0], centers[-1]
        ipd = float(np.hypot(r[0] - l[0], r[1] - l[1]))
        nasion = ((l[0] + r[0]) / 2.0, (l[1] + r[1]) / 2.0)
        use_eyes = True
    else:
        ipd = 0.40 * fw
        nasion = (fx + 0.5 * fw, fy + 0.40 * fh)
        use_eyes = False

    subnasale = (nasion[0], nasion[1] + 1.05 * ipd)
    tip = (nasion[0], nasion[1] + 0.84 * ipd)
    alar_half = 0.30 * ipd

    L = dict(W=W, H=H, face=(fx, fy, fw, fh), nasion=nasion, subnasale=subnasale,
             tip=tip, alar_half=alar_half, ipd=ipd, eyes=use_eyes, centers=centers)
    print(f"  图片 {W}x{H} | 人脸框 {L['face']} | 用双眼={use_eyes} | 眼数={len(centers)}")
    print(f"  IPD={ipd:.1f}px | nasion=({nasion[0]:.0f},{nasion[1]:.0f}) | subnasale=({subnasale[0]:.0f},{subnasale[1]:.0f}) | 鼻翼半宽={alar_half:.0f}px")
    return L


def blend(base, layer, pos, mode="normal"):
    """把带 alpha 的 layer 以 mode 方式贴到 base（RGBA）上，带越界裁剪。"""
    bx, by = pos
    lw, lh = layer.size
    src_x = max(0, -bx); src_y = max(0, -by)
    dst_x = max(0, bx);  dst_y = max(0, by)
    w = min(lw - src_x, base.size[0] - dst_x)
    h = min(lh - src_y, base.size[1] - dst_y)
    if w <= 0 or h <= 0:
        return base
    lcrop = layer.crop((src_x, src_y, src_x + w, src_y + h))
    base = base.convert("RGBA")
    bn = np.array(base).astype(np.float32)
    ln = np.array(lcrop).astype(np.float32)
    a = ln[..., 3:4] / 255.0
    lrgb = ln[..., :3] / 255.0
    reg = bn[dst_y:dst_y + h, dst_x:dst_x + w, :3] / 255.0
    if mode == "multiply":
        out = reg * (1 - a) + (reg * lrgb) * a
    else:
        out = reg * (1 - a) + lrgb * a
    bn[dst_y:dst_y + h, dst_x:dst_x + w, :3] = out * 255.0
    bn[dst_y:dst_y + h, dst_x:dst_x + w, 3] = 255.0
    return Image.fromarray(bn.astype(np.uint8), "RGBA")


def front_crop(png_name):
    """取器械 PNG 的「正面」槽位（左 1/3）。"""
    img = Image.open(PNG / png_name).convert("RGBA")
    W0, H0 = img.size
    crop = img.crop((0, 0, W0 // 3, H0))
    return crop


def place(face_rgba, png_name, L, mode="normal"):
    crop = front_crop(png_name)
    W0, H0 = crop.size
    Nf, Sf = L["nasion"], L["subnasale"]
    scale_y = (Sf[1] - Nf[1]) / REF_SPAN
    scale_x = (2 * L["alar_half"]) / REF_ALAR_W
    newW = max(1, round(W0 * scale_x)); newH = max(1, round(H0 * scale_y))
    crop = crop.resize((newW, newH), Image.LANCZOS)
    off_x = int(round(Nf[0] - (REF_NASION[0] / 220.0) * W0 * scale_x))
    off_y = int(round(Nf[1] - (REF_NASION[1] / 300.0) * H0 * scale_y))
    return blend(face_rgba, crop, (off_x, off_y), mode)


def main():
    src = DEMO / "face_1.jpg"
    print("检测关键点：", src.name)
    L = detect(src)
    face = Image.open(src).convert("RGBA")

    # ① 夹板期：胶带(正片叠底) + 热塑夹板(普通)
    r1 = place(face, "tape-micropore-standard.png", L, "multiply")
    r1 = place(r1, "splint-thermoplastic-standard.png", L, "normal")
    r1.convert("RGB").save(DEMO / "result_1_splint.jpg", quality=92)

    # ② 夜间胶带：仅胶带
    r2 = place(face, "tape-micropore-standard.png", L, "multiply")
    r2.convert("RGB").save(DEMO / "result_2_tape.jpg", quality=92)

    # ③ 术后当天：胡须敷料/滴液垫
    r3 = place(face, "dressing-drip-pad-standard.png", L, "normal")
    r3.convert("RGB").save(DEMO / "result_3_drip.jpg", quality=92)

    # 原图复制
    face.convert("RGB").save(DEMO / "original.jpg", quality=92)

    # 关键点调试图
    dbg = cv2.imread(str(src))
    for (x, y, name) in [(L["nasion"][0], L["nasion"][1], "nasion"),
                          (L["subnasale"][0], L["subnasale"][1], "subnasale"),
                          (L["tip"][0], L["tip"][1], "tip")]:
        cv2.circle(dbg, (int(x), int(y)), 6, (0, 0, 255), -1)
        cv2.putText(dbg, name, (int(x) + 8, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    (fx, fy, fw, fh) = L["face"]
    cv2.rectangle(dbg, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 3)
    cv2.imwrite(str(DEMO / "landmarks_debug.jpg"), dbg)

    print("完成 ->", DEMO)


if __name__ == "__main__":
    main()
