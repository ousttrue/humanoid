# blender Humanoid

- Armature の bone に HumanoidBone の割当をする
- 割当に基づいて `VRMC_vrm_pose` をクリップボードにコピーする

## VRMC_vrm_pose (案)

```json
{
  extensions: {
    VRMC_vrm_animation: {
      humanoid : {
        humanBones: {
        }
      },
      extensions: {
        VMRC_vrm_pose: {
          humanoid: {
            translation: [0, 1, 0],
            rotations: {
              hips: [0, 0.707, 0, 0.707],
              spine: [0, 0.707, 0, 0.707],
              // ...
            }
          },
          expressions: {
            preset: {
              happy: 1.0,
            },
          },
          lookAt: {
            position: [4, 5, 6],
           // yawPitchDegrees: [20, 30],
        }
      }
    }
  }
}
```
