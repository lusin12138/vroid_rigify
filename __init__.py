import re

import bpy

# Originally forked from Nanoskript/vrm-rigify (MIT license).
# Adapted for VRoid Studio models with J_Bip_ bone naming and Blender 4.5+.
bl_info = {
    "name": "VRoid Rigify",
    "author": "lusin12138",
    "description": "Generates Rigify armatures for VRoid Studio models (J_Bip_ bone naming)",
    "version": (0, 3, 0),
    "blender": (4, 0, 0),
    "location": "Operator Search > VRoid Rigify",
    "doc_url": "https://github.com/lusin12138/vroid-rigify",
    "tracker_url": "https://github.com/lusin12138/vroid-rigify/issues",
    "category": "Rigging",
}


class ModeContext:
    def __init__(self, mode):
        self.mode = mode

    def __enter__(self):
        self.old_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode=self.mode)

    def __exit__(self, _type, _value, _trace):
        bpy.ops.object.mode_set(mode=self.old_mode)

    @staticmethod
    def editing(node: bpy.types.Object):
        node.select_set(True)
        return ModeContext("EDIT")


def objects_by_name_patterns(objects, patterns: list[str]):
    object_matches = []
    for node in objects:
        matches = False
        for pattern in patterns:
            matches |= bool(re.match(pattern, node.name))
        if matches:
            object_matches.append(node)
    return object_matches


def full_bone_path(bone: bpy.types.Bone | bpy.types.EditBone) -> str:
    bone_chain = list(reversed(bone.parent_recursive)) + [bone]
    return '/'.join([bone.name for bone in bone_chain])


# Rigify metarig 骨骼名 → VRoid 模型实际骨骼名
# 针对 VRoid Studio 导入的 J_Bip_ 命名体系，绕过 VRM 插件自动检测
RIGIFY_TO_VROID = {
    # 躯干
    "spine": "J_Bip_C_Hips",
    "spine.001": "J_Bip_C_Spine",
    "spine.002": "J_Bip_C_Chest",
    "spine.003": "J_Bip_C_UpperChest",
    "spine.004": "J_Bip_C_Neck",
    "spine.005": "J_Bip_C_Head",
    "spine.006": "J_Bip_C_Head",
    # 肩
    "shoulder.L": "J_Bip_L_Shoulder",
    "shoulder.R": "J_Bip_R_Shoulder",
    # 手臂
    "upper_arm.L": "J_Bip_L_UpperArm",
    "upper_arm.R": "J_Bip_R_UpperArm",
    "forearm.L": "J_Bip_L_LowerArm",
    "forearm.R": "J_Bip_R_LowerArm",
    "hand.L": "J_Bip_L_Hand",
    "hand.R": "J_Bip_R_Hand",
    # 腿
    "thigh.L": "J_Bip_L_UpperLeg",
    "thigh.R": "J_Bip_R_UpperLeg",
    "shin.L": "J_Bip_L_LowerLeg",
    "shin.R": "J_Bip_R_LowerLeg",
    "foot.L": "J_Bip_L_Foot",
    "foot.R": "J_Bip_R_Foot",
    "toe.L": "J_Bip_L_ToeBase",
    "toe.R": "J_Bip_R_ToeBase",
    # 眼睛
    "eye.L": "J_Adj_L_FaceEye",
    "eye.R": "J_Adj_R_FaceEye",
    # 拇指
    "thumb.01.L": "J_Bip_L_Thumb1",
    "thumb.02.L": "J_Bip_L_Thumb2",
    "thumb.03.L": "J_Bip_L_Thumb3",
    "thumb.01.R": "J_Bip_R_Thumb1",
    "thumb.02.R": "J_Bip_R_Thumb2",
    "thumb.03.R": "J_Bip_R_Thumb3",
    # 食指
    "f_index.01.L": "J_Bip_L_Index1",
    "f_index.02.L": "J_Bip_L_Index2",
    "f_index.03.L": "J_Bip_L_Index3",
    "f_index.01.R": "J_Bip_R_Index1",
    "f_index.02.R": "J_Bip_R_Index2",
    "f_index.03.R": "J_Bip_R_Index3",
    # 中指
    "f_middle.01.L": "J_Bip_L_Middle1",
    "f_middle.02.L": "J_Bip_L_Middle2",
    "f_middle.03.L": "J_Bip_L_Middle3",
    "f_middle.01.R": "J_Bip_R_Middle1",
    "f_middle.02.R": "J_Bip_R_Middle2",
    "f_middle.03.R": "J_Bip_R_Middle3",
    # 无名指
    "f_ring.01.L": "J_Bip_L_Ring1",
    "f_ring.02.L": "J_Bip_L_Ring2",
    "f_ring.03.L": "J_Bip_L_Ring3",
    "f_ring.01.R": "J_Bip_R_Ring1",
    "f_ring.02.R": "J_Bip_R_Ring2",
    "f_ring.03.R": "J_Bip_R_Ring3",
    # 小指
    "f_pinky.01.L": "J_Bip_L_Little1",
    "f_pinky.02.L": "J_Bip_L_Little2",
    "f_pinky.03.L": "J_Bip_L_Little3",
    "f_pinky.01.R": "J_Bip_R_Little1",
    "f_pinky.02.R": "J_Bip_R_Little2",
    "f_pinky.03.R": "J_Bip_R_Little3",
}


def generate_template_metarig(metarig_name: str) -> bpy.types.Object:
    try:
        bpy.ops.object.armature_human_metarig_add()
        metarig = bpy.context.view_layer.objects.active
        metarig.name = metarig_name
        metarig.data.name = metarig_name
        return metarig
    except AttributeError as e:
        raise Exception("Failed to spawn metarig. Is the Rigify addon enabled?") from e


def compute_metarig_and_vrm_model_bone_mapping(metarig: bpy.types.Object, vrm_object: bpy.types.Object):
    """使用固定映射表（RIGIFY_TO_VROID）直接建立 Rigify → VRoid 骨骼映射。
    完全绕过 VRM 插件的 human_bones 自动检测（VRoid 命名体系不兼容）。
    """
    armature_vrm: bpy.types.Armature = vrm_object.data
    armature_metarig: bpy.types.Armature = metarig.data

    bone_mapping = []
    for rigify_name, vroid_name in RIGIFY_TO_VROID.items():
        if rigify_name not in armature_metarig.bones:
            continue
        if vroid_name not in armature_vrm.bones:
            continue
        bone_mapping.append((rigify_name, vroid_name))

    return bone_mapping


def remove_or_log_unmapped_metarig_bones(metarig: bpy.types.Object, bone_mapping):
    mapped_metarig_bone_names = set([metarig_bone for metarig_bone, vrm_bone in bone_mapping])
    armature_metarig: bpy.types.Armature = metarig.data
    with ModeContext.editing(metarig):
        for metarig_bone in armature_metarig.edit_bones:
            if metarig_bone.name in mapped_metarig_bone_names:
                continue

            # spine.003 (Upper Chest) is an optional VRM bone. Remove it if it
            # cannot be mapped or else Rigify will fail to generate the rig due to
            # a disconnection between spine.003 and spine.004.
            # FIXME: Add heuristics for mapping breast bones.
            if metarig_bone.name not in ["spine.003", "breast.L", "breast.R"]:
                print(f"metarig bone is not mapped '{full_bone_path(metarig_bone)}'")
                continue

            print(f"removing unmapped metarig bone '{full_bone_path(metarig_bone)}'")
            armature_metarig.edit_bones.remove(metarig_bone)


def position_metarig_bones_to_vrm_model(metarig: bpy.types.Object, vrm_object: bpy.types.Object, bone_mapping):
    armature_metarig: bpy.types.Armature = metarig.data
    armature_vrm: bpy.types.Armature = vrm_object.data
    with ModeContext.editing(metarig):
        metarig.matrix_world = vrm_object.matrix_world
        for metarig_bone_name, vrm_bone_name in bone_mapping:
            metarig_bone = armature_metarig.edit_bones[metarig_bone_name]
            vrm_bone = armature_vrm.bones[vrm_bone_name]

            print(f"positioning '{full_bone_path(metarig_bone)}' to '{full_bone_path(vrm_bone)}'")
            metarig_bone.select = True
            metarig_bone.head = vrm_bone.head_local
            metarig_bone.tail = vrm_bone.tail_local


def fix_position_of_metarig_spine_bones(metarig: bpy.types.Object):
    armature_metarig: bpy.types.Armature = metarig.data
    with ModeContext.editing(metarig):
        # If spine.003 and spine.004 are present, ensure that they are connected
        # to each other, otherwise Rigify will fail to generate the rig.
        armature_metarig.edit_bones["spine.004"].use_connect = True
        armature_metarig.edit_bones["spine.004"].use_connect = False


def remove_metarig_palm_bones(metarig: bpy.types.Object):
    # There isn't a bone mapping for the palm bones so let's remove them.
    armature_metarig: bpy.types.Armature = metarig.data
    with ModeContext.editing(metarig):
        edit_bones = armature_metarig.edit_bones
        for bone in objects_by_name_patterns(edit_bones, [r"^palm.*$"]):
            print(f"deleting metarig palm bone '{bone.name}'")
            edit_bones.remove(bone)


def fix_metarig_limb_rotation_axes(metarig: bpy.types.Object):
    limb_bones = [
        r"^upper_arm\.(L|R)$",
        r"^thigh\.(L|R)$",
    ]

    finger_bones = [
        r"^f_pinky\.01\.(L|R)$",
        r"^f_ring\.01\.(L|R)$",
        r"^f_middle\.01\.(L|R)$",
        r"^f_index\.01\.(L|R)$",
        r"^thumb\.01\.(L|R)$",
    ]

    pose_bones = metarig.pose.bones
    for bone in objects_by_name_patterns(pose_bones, limb_bones):
        print(f"amending bone parameters for limb '{bone.name}'")
        # Ensure local bend direction is correct.
        bone.rigify_parameters.rotation_axis = 'x'

    # Amend armature fingers.
    for bone in objects_by_name_patterns(pose_bones, finger_bones):
        print(f"amending bone parameters for finger '{bone.name}'")
        # Ensure primary bend direction is correct.
        axis = 'Z' if bone.name.endswith('L') else '-Z'
        bone.rigify_parameters.primary_rotation_axis = axis


def invoke_rigify_generate(metarig: bpy.types.Object) -> bpy.types.Object:
    bpy.context.view_layer.objects.active = metarig
    bpy.ops.pose.rigify_generate()
    return bpy.context.view_layer.objects.active


def removed_generated_rig_facial_bones(rig_object: bpy.types.Object):
    rig_bones_to_delete_by_name_pattern = [
        # Facial expressions and features are managed by shape keys,
        # so we remove all facial bones except for eyes.
        r"^(ORG|DEF)-forehead.*$",
        r"^(ORG|DEF)-temple.*$",
        r"^((ORG|DEF)-)?brow.*$",
        r"^((MCH|ORG|DEF)-)?lid\.(B|T).*$",
        r"^((ORG|DEF)-)?ear\.(L|R).*$",
        r"^((MCH|ORG|DEF)-)?tongue.*$",
        r"^((ORG|DEF)-)?chin.*$",
        r"^((ORG|DEF)-)?cheek\.(B|T).*$",
        r"^(ORG-)?teeth\.(B|T)$",
        r"^((ORG|DEF)-)?nose.*$",
        r"^((ORG|DEF)-)?lip.*$",
        r"^((MCH|ORG|DEF)-)?jaw.*$",
        r"^MCH-mouth_lock$",
    ]

    armature_rig: bpy.types.Armature = rig_object.data
    with ModeContext.editing(rig_object):
        bones_to_remove = []
        for bone_root in objects_by_name_patterns(armature_rig.edit_bones, rig_bones_to_delete_by_name_pattern):
            for bone in bone_root.children_recursive + [bone_root]:
                if bone not in bones_to_remove:
                    bones_to_remove.append(bone)

        for bone in bones_to_remove:
            print(f"deleting facial bone '{full_bone_path(bone)}'")
            armature_rig.edit_bones.remove(bone)


def rename_rig_bones_to_match_vrm_model_vertex_groups(rig_object: bpy.types.Object, bone_mapping):
    armature_rig: bpy.types.Armature = rig_object.data
    with ModeContext.editing(rig_object):
        for metarig_bone_name, vrm_bone_name in bone_mapping:
            prefix = "ORG-" if metarig_bone_name in ("eye.L", "eye.R") else "DEF-"
            try:
                rig_bone = armature_rig.edit_bones[f"{prefix}{metarig_bone_name}"]
            except KeyError:
                print(f"warning: rig bone '{prefix}{metarig_bone_name}' not found, skipping rename")
                continue

            if prefix == "ORG-":
                rig_bone.use_deform = True
            else:
                assert rig_bone.use_deform

            print(f"renaming bone '{full_bone_path(rig_bone)}' to '{vrm_bone_name}'")
            rig_bone.name = vrm_bone_name


def attach_unmapped_vrm_model_bones_to_rig(rig_object: bpy.types.Object, vrm_object: bpy.types.Object):
    armature_rig: bpy.types.Armature = rig_object.data
    armature_vrm: bpy.types.Armature = vrm_object.data

    # 创建或获取「头发衣服」骨骼集合
    sec_collection_name = "Hair & Cloth"
    sec_collection = armature_rig.collections.get(sec_collection_name)
    if sec_collection is None:
        sec_collection = armature_rig.collections.new(name=sec_collection_name)

    # 预先读取 VRM 骨架的骨骼 roll 值（EditBone 才有的属性）
    prev_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
    bpy.context.view_layer.objects.active = vrm_object
    bpy.ops.object.mode_set(mode='EDIT')
    vrm_rolls = {b.name: b.roll for b in armature_vrm.edit_bones}
    bpy.ops.object.mode_set(mode=prev_mode)

    with ModeContext.editing(rig_object):
        pending = []
        for vrm_bone in armature_vrm.bones:
            if vrm_bone.name in armature_rig.edit_bones or not vrm_bone.parent:
                continue
            pending.append(vrm_bone)

        copied_this_pass = True
        while pending and copied_this_pass:
            copied_this_pass = False
            still_pending = []
            for vrm_bone in pending:
                parent_name = vrm_bone.parent.name
                if parent_name not in armature_rig.edit_bones:
                    still_pending.append(vrm_bone)
                    continue

                parent_bone_in_rig = armature_rig.edit_bones[parent_name]
                print(f"generating bone '{full_bone_path(parent_bone_in_rig)}/{vrm_bone.name}'")

                bone_in_rig = armature_rig.edit_bones.new(vrm_bone.name)
                bone_in_rig.tail = vrm_bone.tail_local
                bone_in_rig.roll = vrm_rolls.get(vrm_bone.name, 0.0)
                bone_in_rig.parent = parent_bone_in_rig

                # J_Sec_ 骨骼强制 head = parent.tail，保证连续链（不断开）
                if vrm_bone.name.startswith("J_Sec_"):
                    bone_in_rig.head = parent_bone_in_rig.tail.copy()
                    sec_collection.assign(bone_in_rig)
                else:
                    bone_in_rig.head = vrm_bone.head_local

                for collection in parent_bone_in_rig.collections:
                    collection.assign(bone_in_rig)

                copied_this_pass = True
            pending = still_pending


# Enables use of the blend shape proxy and expressions panel from the VRM addon.
def copy_shape_key_controls_from_vrm_armature(rig_object: bpy.types.Object, vrm_object: bpy.types.Object):
    armature_rig: bpy.types.Armature = rig_object.data
    armature_vrm: bpy.types.Armature = vrm_object.data
    blend_shape_master = armature_vrm.vrm_addon_extension.vrm0["blend_shape_master"]
    armature_rig.vrm_addon_extension.vrm0["blend_shape_master"] = blend_shape_master

    # 新版 VRM 插件的 expressions 改用 PropertyGroup 结构，无法逐条复制。
    # 跳过 expressions，不影响骨骼绑定和蒙皮（expression 仅用于 VRM 表情面板预览）


def disable_ik_stretching(rig_object: bpy.types.Object):
    for bone in rig_object.pose.bones:
        stretch_key = "IK_Stretch"
        if stretch_key in bone:
            bone[stretch_key] = 0.0


def reassign_mesh_armatures(old_armature: bpy.types.Object, new_armature: bpy.types.Object):
    """自动将场景中所有 mesh 的 Armature 修改器目标从旧骨架替换为新 rig"""
    count = 0
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        for mod in obj.modifiers:
            if mod.type == 'ARMATURE' and mod.object == old_armature:
                mod.object = new_armature
                count += 1
                print(f"reassigned '{obj.name}' Armature modifier → {new_armature.name}")
    if count:
        print(f"Reassigned {count} mesh Armature modifier(s) to {new_armature.name}")


def fix_eye_bone_positions(rig_object: bpy.types.Object, vrm_object: bpy.types.Object):
    """删除 Rigify 生成的眼骨，在 VRM 眼骨末端重新创建——彻底解决斗鸡眼"""
    armature_rig = rig_object.data
    armature_vrm = vrm_object.data
    eye_names = ["J_Adj_L_FaceEye", "J_Adj_R_FaceEye"]
    head_bone_name = "J_Bip_C_Head"

    rig_original_matrix = rig_object.matrix_world.copy()
    rig_object.matrix_world = vrm_object.matrix_world

    prev_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'

    # 读 VRM 眼骨数据
    bpy.context.view_layer.objects.active = vrm_object
    bpy.ops.object.mode_set(mode='EDIT')
    vrm_eye_data = {}
    for eye_name in eye_names:
        if eye_name in armature_vrm.edit_bones:
            vrm_bone = armature_vrm.edit_bones[eye_name]
            vrm_eye_data[eye_name] = {
                'head': vrm_bone.head.copy(),
                'tail': vrm_bone.tail.copy(),
                'roll': vrm_bone.roll,
            }
    bpy.ops.object.mode_set(mode='OBJECT')

    # 在 rig 中删除旧眼骨，创建新眼骨
    bpy.context.view_layer.objects.active = rig_object
    bpy.ops.object.mode_set(mode='EDIT')
    head_bone = armature_rig.edit_bones.get(head_bone_name)

    for eye_name, data in vrm_eye_data.items():
        # 删除旧的 rigify 眼骨
        old_bone = armature_rig.edit_bones.get(eye_name)
        if old_bone:
            armature_rig.edit_bones.remove(old_bone)

        if head_bone is None:
            continue

        new_bone = armature_rig.edit_bones.new(eye_name)
        new_bone.head = data['head']
        new_bone.tail = data['tail']
        new_bone.roll = data['roll']
        new_bone.parent = head_bone
        new_bone.use_deform = True

        for collection in head_bone.collections:
            collection.assign(new_bone)
        print(f"rebuilt eye bone '{eye_name}' from VRM original")

    bpy.ops.object.mode_set(mode=prev_mode)
    rig_object.matrix_world = rig_original_matrix


def hide_fk_collections(rig_object: bpy.types.Object):
    """默认隐藏 FK 骨骼集合，只显示 IK"""
    for col in rig_object.data.collections:
        if 'FK' in col.name or 'fk' in col.name:
            col.is_visible = False
    print("FK bone collections hidden (IK only)")


def add_damped_track_to_sec_bones(rig_object: bpy.types.Object):
    """给 J_Sec_ 骨骼添加阻尼追踪——每节指向子骨骼（往尖端），跳过根级。
    手动成功示范：Hair2→Hair4→Hair5→Hair5_end，目标为子骨骼。
    """
    prev_mode = bpy.context.object.mode if bpy.context.object else 'OBJECT'
    bpy.context.view_layer.objects.active = rig_object
    bpy.ops.object.mode_set(mode='POSE')
    count = 0
    for bone in rig_object.pose.bones:
        if not bone.name.startswith("J_Sec_"):
            continue
        if not bone.parent or not bone.parent.name.startswith("J_Sec_"):
            continue  # 根级不加
        if not bone.children:
            continue  # 无子级不加
        constraint = bone.constraints.new('DAMPED_TRACK')
        constraint.target = rig_object
        constraint.subtarget = bone.children[0].name
        constraint.track_axis = 'TRACK_Y'
        constraint.influence = 0.3
        count += 1
    bpy.ops.object.mode_set(mode=prev_mode)
    print(f"Damped Track on {count} J_Sec_ bones (child target, influence=0.3)")


def hide_collider_objects():
    """隐藏 Colliders 集合"""
    coll = bpy.data.collections.get("Colliders")
    if coll:
        coll.hide_viewport = True
        coll.hide_render = True
        print("Hidden 'Colliders' collection")


def remove_all_gn_outlines():
    """移除所有网格上的几何节点描边修改器"""
    count = 0
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        to_remove = [m for m in obj.modifiers if m.type == 'NODES']
        for mod in to_remove:
            obj.modifiers.remove(mod)
            count += 1
    if count:
        print(f"Removed {count} Geometry Nodes outline modifiers")


def parent_meshes_to_rig(rig_object: bpy.types.Object):
    """将所有使用了新 rig 作为骨架修改器的 mesh 父级到 rig 下"""
    count = 0
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        for mod in obj.modifiers:
            if mod.type == 'ARMATURE' and mod.object == rig_object:
                obj.parent = rig_object
                count += 1
                break
    if count:
        print(f"Parented {count} mesh(es) to {rig_object.name}")


class GenerateVRoidRig(bpy.types.Operator):
    bl_idname = "vroid_rigify.create_rig"
    bl_label = "Generate Rigify armature for VRoid model"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj is None or obj.type != 'ARMATURE':
            return False
        # 额外确认：骨架必须在选中列表中
        return obj in context.selected_objects

    def execute(self, context):
        vrm_object = context.active_object
        if not vrm_object or vrm_object.type != 'ARMATURE':
            self.report({'ERROR'}, "请选中 VRoid 骨架 / Select a VRoid armature first")
            return {'CANCELLED'}
        if vrm_object not in context.selected_objects:
            self.report({'ERROR'}, "请选中 VRoid 骨架 / Select a VRoid armature first")
            return {'CANCELLED'}

        # 确认是 VRoid 导入的骨架（有 vrm_addon_extension）
        try:
            _ = vrm_object.data.vrm_addon_extension
        except AttributeError:
            self.report({'ERROR'}, "不是 VRoid 骨架，缺少 VRM 扩展数据 / Not a VRoid armature")
            return {'CANCELLED'}

        wm = context.window_manager
        steps = 12
        wm.progress_begin(0, steps)

        metarig = generate_template_metarig(f"{vrm_object.name}.metarig")
        wm.progress_update(1)

        bone_mapping = compute_metarig_and_vrm_model_bone_mapping(metarig, vrm_object)
        wm.progress_update(2)

        remove_metarig_palm_bones(metarig)
        wm.progress_update(3)

        remove_or_log_unmapped_metarig_bones(metarig, bone_mapping)
        wm.progress_update(4)

        position_metarig_bones_to_vrm_model(metarig, vrm_object, bone_mapping)
        wm.progress_update(5)

        fix_position_of_metarig_spine_bones(metarig)
        wm.progress_update(6)

        fix_metarig_limb_rotation_axes(metarig)
        wm.progress_update(7)

        rig_object = invoke_rigify_generate(metarig)
        wm.progress_update(8)

        removed_generated_rig_facial_bones(rig_object)
        rename_rig_bones_to_match_vrm_model_vertex_groups(rig_object, bone_mapping)
        fix_eye_bone_positions(rig_object, vrm_object)
        wm.progress_update(9)

        attach_unmapped_vrm_model_bones_to_rig(rig_object, vrm_object)
        wm.progress_update(10)

        copy_shape_key_controls_from_vrm_armature(rig_object, vrm_object)
        disable_ik_stretching(rig_object)
        reassign_mesh_armatures(vrm_object, rig_object)
        parent_meshes_to_rig(rig_object)
        hide_fk_collections(rig_object)
        wm.progress_update(11)

        metarig.hide_set(True)
        vrm_object.hide_set(True)
        wm.progress_end()

        # 根据面板勾选执行可选功能
        if context.scene.vroid_rigify_damped_track:
            add_damped_track_to_sec_bones(rig_object)
        if context.scene.vroid_rigify_hide_colliders:
            hide_collider_objects()
        if context.scene.vroid_rigify_clear_gn:
            remove_all_gn_outlines()

        self.report({'INFO'}, f"Rigify 生成完成 → {rig_object.name}")
        return {"FINISHED"}


class VRoidPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_vroid_rigify"
    bl_label = "VRoid"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRoid"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        is_armature = obj and obj.type == 'ARMATURE' and obj in context.selected_objects
        scene = context.scene

        if is_armature:
            layout.label(text=f"选中: {obj.name}", icon='ARMATURE_DATA')
            layout.operator("vroid_rigify.create_rig", text="生成 Rigify / Generate Rigify", icon='OUTLINER_OB_ARMATURE')

        layout.separator()
        layout.prop(scene, "vroid_rigify_damped_track", text="头发衣服阻尼追踪")
        layout.prop(scene, "vroid_rigify_hide_colliders", text="隐藏碰撞体")
        layout.prop(scene, "vroid_rigify_clear_gn", text="清除全部描边节点")

        if not is_armature:
            layout.label(text="Select a VRoid armature", icon='INFO')
            layout.label(text="请选中 VRoid 骨架", icon='BLANK1')


CLASSES = [
    GenerateVRoidRig,
    VRoidPanel,
]


def register():
    for clazz in CLASSES:
        bpy.utils.register_class(clazz)
    bpy.types.Scene.vroid_rigify_damped_track = bpy.props.BoolProperty(
        name="Damped Track",
        description="Add Damped Track constraint to Hair & Cloth bones",
        default=True,
    )
    bpy.types.Scene.vroid_rigify_hide_colliders = bpy.props.BoolProperty(
        name="Hide Colliders",
        description="Hide VRoid collision objects after conversion",
        default=True,
    )
    bpy.types.Scene.vroid_rigify_clear_gn = bpy.props.BoolProperty(
        name="Clear Outline GN",
        description="Remove ALL outline Geometry Nodes modifiers from meshes",
        default=True,
    )


def unregister():
    for clazz in CLASSES:
        bpy.utils.unregister_class(clazz)
    del bpy.types.Scene.vroid_rigify_damped_track
    del bpy.types.Scene.vroid_rigify_hide_colliders
    del bpy.types.Scene.vroid_rigify_clear_gn


if __name__ == "__main__":
    register()
