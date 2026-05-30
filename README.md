# VRoid Rigify

> 基于 [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify)（MIT 许可）二次开发。  
> 专为 **VRoid Studio** 模型适配（J_Bip_ 骨骼命名），兼容 **Blender 4.0+**。

将 VRoid Studio 导出的 VRM 模型（通过 [VRM Format](https://extensions.blender.org/add-ons/vrm/) 插件导入）转换为 Rigify 骨架。  
生成的 rig 匹配模型 T-pose，保持顶点组命名（J_Bip_ / J_Adj_ / J_Sec_），并自动替换所有网格的骨架修改器。

---

## 📥 下载

前往 **[Releases](../../releases)** 下载最新版 `vroid_rigify.zip`。

---

## ⚙️ 前置设置

1. 打开 Blender → **编辑 → 偏好设置**
2. **界面** 选项卡 → 勾选 **开发选项**
3. **保存 & 加载** 选项卡 → 勾选 **自动运行 Python 脚本**
4. 安装并启用 **[VRM Format](https://extensions.blender.org/add-ons/vrm/)** 插件（用于导入 `.vrm` 文件）
5. 确保 **Rigify** 已启用（Blender 自带）

---

## 🚀 使用方法

1. 导入 VRoid `.vrm` 模型（文件 → 导入 → VRM）
2. 在**物体模式**下，选中原骨架
3. 方式一：右侧 **VRoid 侧边栏** → 点击「生成 Rigify 控制器」
4. 方式二：按 **F3** 搜索 `vroid` → 选「Generate Rigify armature for VRoid model」
5. 顶部状态栏显示进度，完成后大纲视图出现 **`Armature.rig`**
6. 所有网格骨架修改器已自动切换，无需手动操作
7. 切换到**姿态模式**测试

---

## ⚠️ 已知问题

- **眼球位置可能偏移**：姿态模式下选中眼球骨骼，移动到正确位置即可。
- **表情面板**（VRM blend shape）不会从原骨架复制，需手动重配。
- 非 VRoid 导出的 VRM 模型（其他骨骼命名风格）大概率不兼容。

---

## 📄 许可

MIT — 与原项目 [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify) 一致。

---

## 🙏 致谢

Fork 自 [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify)，感谢原作者！

---

# VRoid Rigify

> Originally forked from [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify) (MIT license).  
> Adapted for **VRoid Studio** models (J_Bip_ bone naming) and **Blender 4.0+**.

Converts VRoid Studio `.vrm` models (imported via the [VRM Format](https://extensions.blender.org/add-ons/vrm/) addon) into Rigify armatures.  
The generated rig matches T-pose, preserves vertex group names (J_Bip_ / J_Adj_ / J_Sec_), and auto-reassigns all mesh Armature modifiers.

---

## 📥 Download

Go to **[Releases](../../releases)** → download `vroid_rigify.zip`.

---

## ⚙️ Prerequisites

1. Blender → **Edit → Preferences**
2. **Interface** → enable **Developer Extras**
3. **Save & Load** → enable **Auto Run Python Scripts**
4. Install & enable **[VRM Format](https://extensions.blender.org/add-ons/vrm/)**
5. Make sure **Rigify** is enabled (built-in)

---

## 🚀 Usage

1. Import your VRoid `.vrm` model (File → Import → VRM)
2. In **Object Mode**, select the original armature
3. Method A: **VRoid sidebar** (N panel) → click **生成 Rigify 控制器**
4. Method B: Press **F3** → search `vroid`
5. A progress bar appears in the status bar. When done, **`Armature.rig`** appears in the Outliner
6. All mesh Armature modifiers are auto-reassigned
7. Switch to **Pose Mode** to test

---

## ⚠️ Known Issues

- **Eye position** may shift slightly → adjust in Pose Mode.
- **Expressions panel** (VRM blend shapes) is not copied.
- Non-VRoid VRM models will likely not work.

---

## 📄 License

MIT — same as [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify).

---

## 🙏 Credits

Forked from [Nanoskript/vrm-rigify](https://github.com/nanoskript/vrm-rigify). Thank you!