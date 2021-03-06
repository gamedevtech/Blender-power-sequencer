import bpy
from .utils.get_frame_range import get_frame_range
from .utils.set_preview_range import set_preview_range


class PreviewToSelection(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/EV1sUrn.gif)
    
    Sets the scene frame start to the earliest frame start of selected 
    sequences and the scene frame end to the last frame of selected sequences.
    """
    bl_idname = "power_sequencer.preview_to_selection"
    bl_label = "Preview To Selection"
    bl_description = "Sets the timeline preview range to that of the selected sequences."
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = bpy.context.scene
        selection = bpy.context.selected_sequences
        if not selection:
            return {'CANCELLED'}
        frame_start, frame_end = get_frame_range(
            sequences=bpy.context.selected_sequences, get_from_start=False)

        if scene.frame_start == frame_start and scene.frame_end == frame_end:
            frame_start, frame_end = get_frame_range(get_from_start=True)

        set_preview_range(frame_start, frame_end - 1)
        return {'FINISHED'}
