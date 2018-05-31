import bpy


class SmartSnap(bpy.types.Operator):
    """
    Trims, extends and snaps selected strips to cursor
    """
    bl_idname = "power_sequencer.smart_snap"
    bl_label = "Smart Snap Strip Handles"
    bl_description = "Trims, extends, and snaps selected strips to cursor"
    bl_options = {'REGISTER', 'UNDO'}

    side = bpy.props.EnumProperty(
        items=[('left', 'Left', 'Left side'), ('right', 'Right', 'Right side'),
               ('auto', 'Auto', 'Use the side closest to the time cursor')],
        name="Snap side",
        description="Handle side to use for the snap",
        default='auto')

    function = bpy.props.StringProperty("")

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        if context.selected_sequences:
            return self.execute(context)

        frame_current = context.scene.frame_current
        for s in context.sequences:
            if s.frame_final_start <= frame_current < s.frame_final_end:
                s.select = True
        return self.execute(context)

    def execute(self, context):
        frame_current = bpy.context.scene.frame_current

        self.select_strip_handle(bpy.context.selected_sequences, self.side, frame_current)
        bpy.ops.sequencer.snap(frame=frame_current)

        for s in context.selected_sequences:
            s.select_right_handle = False
            s.select_left_handle = False
        return {"FINISHED"}

    def select_strip_handle(self, sequences, side, frame):
        """
        Select the left or right handles of the strips based on the frame number
        """
        side = side.upper()

        for s in sequences:
            s.select_left_handle = False
            s.select_right_handle = False

            handle_side = ''
            start, end = s.frame_final_start, s.frame_final_end
            if side == 'AUTO' and start <= frame <= end:
                handle_side = 'LEFT' if abs(
                    frame - start) < s.frame_final_duration / 2 else 'RIGHT'
            elif side == 'LEFT' and frame < end or side == 'RIGHT' and frame > start:
                handle_side = side
            else:
                s.select = False
            if handle_side:
                bpy.ops.sequencer.select_handles(side=handle_side)
