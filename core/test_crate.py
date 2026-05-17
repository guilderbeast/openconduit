import bpy

print("\n📦 Crate Generation Script Initiated...")

# 1. Add a primitive cube to the scene
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))

# 2. Grab the ACTUAL Object context (not just the mesh data)
crate_object = bpy.context.active_object
crate_object.name = "Production_Crate"

# 3. Apply the dimensions to the Object
crate_object.dimensions = (3.0, 2.0, 1.0)

print("✅ SUCCESS: Crate dimensions set to 3x2x1 perfectly!")