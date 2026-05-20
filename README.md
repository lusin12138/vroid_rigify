[vroid_rigify_README.md](https://github.com/user-attachments/files/28060703/vroid_rigify_README.md)
# VRoid Rigify

> Originally forked from [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify) (MIT license).  
> Adapted for **VRoid Studio** models (J_Bip_ bone naming) and **Blender 4.0+**.

Generates a Rigify armature from your VRoid Studio model imported via the [VRM Format](https://extensions.blender.org/add-ons/vrm/) addon.  
The generated rig follows your model's T-pose, preserves vertex group names (J_Bip_ / J_Adj_ / J_Sec_), and attaches secondary bones (hair, skirt, etc.) automatically.

---

## 📥 Download

Go to **[Releases](../../releases)** and download the latest `vroid_rigify.zip`.

---

## ⚙️ Prerequisites

1. Open Blender → **Edit → Preferences**
2. **Interface** tab → enable **Developer Extras**
3. **Save & Load** tab → enable **Auto Run Python Scripts**

4. Install & enable the **[VRM Format](https://extensions.blender.org/add-ons/vrm/)** addon (used to import `.vrm` files).
5. Make sure **Rigify** is enabled (it ships with Blender by default).

---

## 🚀 Usage

1. Import your VRoid `.vrm` model (File → Import → VRM).
2. In **Object Mode**, select the **original armature**.
3. Press **F3** and search: `Generate Rigify armature for VRoid model`  
   (or search `vroid`).
4. Wait a few seconds. A new object **`Armature.rig`** will appear in the Outliner.
5. For each mesh (Body, Face, Hair):
   - Select the mesh → go to **Modifiers** panel.
   - Replace the **Armature** modifier target from the original skeleton → **Armature.rig**.
6. Switch to **Pose Mode** and test — the rig should drive your model.

---

## ⚠️ Known Issues

- **Eye position may be slightly misaligned** after conversion.  
  In Pose Mode, select the eye bones and move them into the correct position in Pose Mode.

- **Expressions panel** (VRM blend shape controls) is not copied from the original armature.  
  You can manually re-assign blend shape proxies on the new rig if needed.

- Non-VRoid VRM models (other `J_Bip_` naming styles) are unlikely to work without modifying the bone mapping table in `__init__.py`.

---

## 📄 License

MIT — same as the original [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify).

---

## 🙏 Credits

Forked from [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify). Thank you for the original work!

---

# VRoid Rigify（中文说明）

> 基于 [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify)（MIT 许可）二次开发。  
> 专为 **VRoid Studio** 模型适配（J_Bip_ 骨骼命名），兼容 **Blender 4.0+**。

将 VRoid Studio 导出的 VRM 模型（通过 [VRM Format](https://extensions.blender.org/add-ons/vrm/) 插件导入）转换为 Rigify 骨架。  
生成的 rig 会匹配模型的 T-pose，保持顶点组命名（J_Bip_ / J_Adj_ / J_Sec_），并自动附加头发、裙子等次级骨骼。

---

## 📥 下载

前往 **[Releases](../../releases)** 下载最新版 `vroid_rigify.zip`。

---

## ⚙️ 前置设置

1. 打开 Blender → **编辑 → 偏好设置**
2. **界面** 选项卡 → 勾选 **开发选项**
3. **保存 & 加载** 选项卡 → 勾选 **自动运行 Python 脚本**

4. 安装并启用 **[VRM Format](https://extensions.blender.org/add-ons/vrm/)** 插件（用于导入 `.vrm` 文件）。
5. 确保 **Rigify** 已启用（Blender 自带，默认开启）。

---

## 🚀 使用方法

1. 导入 VRoid `.vrm` 模型（文件 → 导入 → VRM）。
2. 在 **物体模式** 下，选中 **原骨架**。
3. 按 **F3** 搜索：`Generate Rigify armature for VRoid model`  
   （也可搜 `vroid`）。
4. 等待几秒，大纲视图中会出现 **`Armature.rig`**。
5. 对每个网格（身体、脸部、头发等）：
   - 选中网格 → **修改器** 面板。
   - 将 **骨架** 修改器的目标从原骨架切换为 **Armature.rig**。
6. 切换到 **姿态模式** 测试——骨骼应该能驱动模型了。

---

## ⚠️ 已知问题

- **眼球位置可能会偏**。  
  在姿态模式下选中眼球骨骼，移动到正确位置即可。

- **表情面板**（VRM blend shape 控件）不会从原骨架复制过来。  
  如有需要，可在新 rig 上手动重新分配 blend shape proxy。

- 非 VRoid 导出的 VRM 模型（其他 J_Bip_ 命名风格）大概率不兼容，需手动修改 `__init__.py` 中的骨骼映射表。

---

## 📄 许可

MIT — 与原项目 [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify) 一致。

---

## 🙏 致谢

Fork 自 [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify)，感谢原作者！
