# blender Humanoid

- Armature にカスタムプロパティ `bpy.types.Armature.humanoid` を追加
- Armature の bone に HumanoidBone の割当をする
- 割当に基づいて `VRMC_vrm_pose` をクリップボードにコピーする

## Armature Humanoid を新規に作成する

`Add - Armature - Create Humanoid`

### property

- rig: true にするとポージング用の Rig を追加します。
  - InvertedPelvis( hips が隠蔽されて下向きの pelvis に置き換わり、 その親に COG が追加されます)
  - LegIk
  - ArmIk
  - HandConroler
    - finger bend(rot, scale)
    - finger spread(rot)

![humanoid_rig](./humanoid_rig.jpg)

`boneWidget` で一部をカスタムシェイプ化。

## Humanoid Panel

`VIEW_3D` - `UI(右側)`  - `Humanod(tab)`

### Humanoid Bone の Bone への割当

- `Guess Humanoid Bones` で空欄に名前ベースの簡単なマッチングによる割当を試行します
  - `Rigify` デフォルトの `Humanoid` Rig の割当がハードコーティングされています
  - `VRM-Addon-for-Blender` によって import された vrm0 の割り当てを読めます
  - `VRM-Addon-for-Blender` によって import された vrm1 の割り当てを読めます
- `clear` Humanoid 割当をクリアします

### ポーズ(テキスト)のコピー

前提として、 レストポーズが TPose であることが必要です。

- `Copy Pose To Humanoid` で `VRMC_vrm_pose` 形式のポーズをクリップボードにコピーします。

## VRMC_vrm_pose (案)

```json5
extensions: {
  VRMC_vrm_animation: {
    humanoid : {
      humanBones: {}
    },
    extensions: {
      VMRC_vrm_pose: {
        humanoid: {
          translation: [
            0,
            1,
            0
          ],
          rotations: {
            hips: [
              0,
              0.707,
              0,
              0.707
            ],
            spine: [
              0,
              0.707,
              0,
              0.707
            ],
            // ...
          }
        },
        expressions: {
          preset: {
            happy: 1.0,
          },
        },
        lookAt: {
          position: [
            4,
            5,
            6
          ],
          // yawPitchDegrees: [20, 30],
        }
      }
    }
  }
}
```
