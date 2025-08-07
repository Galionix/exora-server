import bpy
import json
from bpy.props import StringProperty, IntProperty, CollectionProperty, FloatVectorProperty, PointerProperty, BoolProperty, FloatProperty, EnumProperty
from bpy.types import PropertyGroup, Panel, Operator, UIList
from bpy.app.handlers import persistent

bl_info = {
    "name": "Animation Events System",
    "author": "GitHub Copilot",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Dope Sheet > Sidebar > Events",
    "description": "Visual animation events system with timeline markers",
    "category": "Animation",
}

# Custom Field System
class EventField(PropertyGroup):
    name: StringProperty(
        name="Field Name",
        default="new_field",
        description="Name of the custom field"
    )
    field_type: EnumProperty(
        name="Type",
        items=[
            ('BOOL', "Boolean", "True/False value"),
            ('STRING', "String", "Text value"),
            ('INT', "Integer", "Whole number"),
            ('FLOAT', "Float", "Decimal number"),
            ('ARRAY', "Array", "List of strings (comma-separated)"),
        ],
        default='STRING',
        description="Type of the field"
    )
    # Default values for different types
    default_bool: BoolProperty(name="Default", default=False)
    default_string: StringProperty(name="Default", default="")
    default_int: IntProperty(name="Default", default=0)
    default_float: FloatProperty(name="Default", default=0.0)
    default_array: StringProperty(name="Default", default="", description="Comma-separated values")
    description: StringProperty(name="Description", default="")

class EventFieldValue(PropertyGroup):
    name: StringProperty(name="Field Name")
    field_type: StringProperty(name="Type")
    # Actual values
    bool_value: BoolProperty(name="Value")
    string_value: StringProperty(name="Value")
    int_value: IntProperty(name="Value")
    float_value: FloatProperty(name="Value")
    array_value: StringProperty(name="Value", description="Comma-separated values")

class EventTemplate(PropertyGroup):
    name: StringProperty(
        name="Event Name",
        default="New Event",
        description="Name of the event template"
    )
    color: FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 0.0, 0.0),
        min=0.0, max=1.0,
        description="Color for visual identification"
    )
    description: StringProperty(
        name="Description",
        default="",
        description="Event description"
    )
    custom_fields: CollectionProperty(type=EventField)
    active_field_index: IntProperty(default=0)

class EventInstance(PropertyGroup):
    template_name: StringProperty(
        name="Template",
        description="Name of the template this instance uses",
        update=lambda self, context: update_event_instance(self, context)
    )
    frame: IntProperty(
        name="Frame",
        description="Frame where the event occurs",
        update=lambda self, context: update_event_frame(self, context)
    )
    marker_name: StringProperty(
        name="Marker Name",
        description="Name of the timeline marker"
    )
    field_values: CollectionProperty(type=EventFieldValue)

class EventSystemProperties(PropertyGroup):
    event_templates: CollectionProperty(type=EventTemplate)
    event_instances: CollectionProperty(type=EventInstance)
    active_template_index: IntProperty(default=0)
    active_instance_index: IntProperty(default=0)

# UI Lists for custom fields
class EVENT_UL_fields(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "name", text="", emboss=False)
            row.label(text=f"({item.field_type})")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='PROPERTIES')

class EVENT_UL_templates(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "name", text="", emboss=False)
            row.prop(item, "color", text="")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='EVENT')

class EVENT_UL_instances(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=f"{item.template_name} @ Frame {item.frame}")
            op = layout.operator("event.remove_from_timeline", text="", icon='X')
            op.frame = item.frame
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='MARKER')

class EVENT_PT_panel(Panel):
    bl_label = "Animation Events"
    bl_idname = "EVENT_PT_panel"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Events"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        events = scene.event_system

        # Event Templates Section
        layout.label(text="Event Templates:", icon='PRESET')

        row = layout.row()
        row.template_list("EVENT_UL_templates", "", events, "event_templates",
                         events, "active_template_index")

        col = row.column(align=True)
        col.operator("event.add_template", icon='ADD', text="")
        col.operator("event.remove_template", icon='REMOVE', text="")

        # Template properties
        if events.event_templates and events.active_template_index < len(events.event_templates):
            template = events.event_templates[events.active_template_index]
            box = layout.box()
            box.prop(template, "name")
            box.prop(template, "description")
            box.prop(template, "color")

            # Custom Fields for Template
            box.separator()
            box.label(text="Custom Fields:", icon='PROPERTIES')

            field_row = box.row()
            field_row.template_list("EVENT_UL_fields", "", template, "custom_fields",
                                   template, "active_field_index")

            field_col = field_row.column(align=True)
            field_col.operator("event.add_field", icon='ADD', text="")
            field_col.operator("event.remove_field", icon='REMOVE', text="")

            # Field properties
            if template.custom_fields and template.active_field_index < len(template.custom_fields):
                field = template.custom_fields[template.active_field_index]
                field_box = box.box()
                field_box.prop(field, "name")
                field_box.prop(field, "field_type")
                field_box.prop(field, "description")

                # Default value based on type
                if field.field_type == 'BOOL':
                    field_box.prop(field, "default_bool")
                elif field.field_type == 'STRING':
                    field_box.prop(field, "default_string")
                elif field.field_type == 'INT':
                    field_box.prop(field, "default_int")
                elif field.field_type == 'FLOAT':
                    field_box.prop(field, "default_float")
                elif field.field_type == 'ARRAY':
                    field_box.prop(field, "default_array")

        # Template Tools Section
        if events.event_templates:
            layout.separator()
            template_tools = layout.box()
            template_tools.label(text="Template Tools:", icon='TOOL_SETTINGS')
            template_row = template_tools.row(align=True)
            template_row.operator("event.export_palette", text="Export Palette", icon='EXPORT')
            template_row.operator("event.import_palette", text="Import Palette", icon='IMPORT')

        layout.separator()

        # Add to Timeline Section
        if events.event_templates:
            if events.active_template_index < len(events.event_templates):
                template = events.event_templates[events.active_template_index]
                col = layout.column()
                col.scale_y = 1.5
                op = col.operator("event.add_to_timeline",
                                text=f"Add '{template.name}' to Frame {scene.frame_current}",
                                icon='MARKER_HLT')

        layout.separator()

        # Timeline Events Section
        layout.label(text="Timeline Events:", icon='MARKER')

        if events.event_instances:
            layout.template_list("EVENT_UL_instances", "", events, "event_instances",
                               events, "active_instance_index")

            # Edit selected event instance
            if events.active_instance_index < len(events.event_instances):
                instance = events.event_instances[events.active_instance_index]
                box = layout.box()
                box.label(text="Edit Selected Event:", icon='PROPERTIES')

                # Template selector with available templates
                row = box.row()
                row.label(text="Template:")
                if events.event_templates:
                    row.prop_search(instance, "template_name", events, "event_templates", text="")
                else:
                    row.label(text="No templates available", icon='ERROR')

                # Frame editor
                row = box.row()
                row.label(text="Frame:")
                row.prop(instance, "frame", text="")

                # Custom field values for this instance - ИСПРАВЛЕНО: убрано дублирование
                if instance.field_values:
                    box.separator()
                    box.label(text="Field Values:", icon='PROPERTIES')

                    # Создаем множество уже показанных полей чтобы избежать дублирования
                    shown_fields = set()

                    for field_value in instance.field_values:
                        # Проверяем, не показывали ли мы уже это поле
                        if field_value.name in shown_fields:
                            continue
                        shown_fields.add(field_value.name)

                        field_row = box.row()
                        field_row.label(text=f"{field_value.name}:")

                        if field_value.field_type == 'BOOL':
                            field_row.prop(field_value, "bool_value", text="")
                        elif field_value.field_type == 'STRING':
                            field_row.prop(field_value, "string_value", text="")
                        elif field_value.field_type == 'INT':
                            field_row.prop(field_value, "int_value", text="")
                        elif field_value.field_type == 'FLOAT':
                            field_row.prop(field_value, "float_value", text="")
                        elif field_value.field_type == 'ARRAY':
                            field_row.prop(field_value, "array_value", text="")

                # Show template info if valid template is selected
                selected_template = None
                for template in events.event_templates:
                    if template.name == instance.template_name:
                        selected_template = template
                        break

                if selected_template:
                    info_box = box.box()
                    info_box.label(text=f"Template: {selected_template.name}", icon='INFO')
                    if selected_template.description:
                        info_box.label(text=f"Description: {selected_template.description}")
                    color_row = info_box.row()
                    color_row.label(text="Color:")
                    color_row.prop(selected_template, "color", text="")

                # Quick actions
                row = box.row(align=True)
                row.operator("event.go_to_event", text="Go to Frame", icon='PLAY')
                row.operator("event.duplicate_event", text="Duplicate", icon='DUPLICATE')

                # Additional editing options
                edit_row = box.row(align=True)
                edit_row.operator("event.move_event_to_current", text="Move to Current Frame", icon='MARKER_HLT')

        else:
            layout.label(text="No events on timeline", icon='INFO')

        layout.separator()

        # Tools Section
        layout.label(text="Timeline Tools:", icon='TOOL_SETTINGS')
        row = layout.row(align=True)
        row.operator("event.export_events", icon='EXPORT')
        row.operator("event.import_events", icon='IMPORT')
        row.operator("event.clear_all_events", icon='TRASH')

# Field management operators
class EVENT_OT_add_field(Operator):
    bl_idname = "event.add_field"
    bl_label = "Add Custom Field"
    bl_description = "Add a new custom field to the event template"

    def execute(self, context):
        events = context.scene.event_system
        if events.event_templates and events.active_template_index < len(events.event_templates):
            template = events.event_templates[events.active_template_index]
            field = template.custom_fields.add()
            field.name = f"field_{len(template.custom_fields)}"
            template.active_field_index = len(template.custom_fields) - 1
        return {'FINISHED'}

class EVENT_OT_remove_field(Operator):
    bl_idname = "event.remove_field"
    bl_label = "Remove Custom Field"
    bl_description = "Remove selected custom field from the event template"

    def execute(self, context):
        events = context.scene.event_system
        if events.event_templates and events.active_template_index < len(events.event_templates):
            template = events.event_templates[events.active_template_index]
            if template.custom_fields and template.active_field_index < len(template.custom_fields):
                template.custom_fields.remove(template.active_field_index)
                if template.active_field_index > 0:
                    template.active_field_index -= 1
        return {'FINISHED'}

class EVENT_OT_add_to_timeline(Operator):
    bl_idname = "event.add_to_timeline"
    bl_label = "Add Event to Timeline"
    bl_description = "Add selected event template to current frame"

    def execute(self, context):
        scene = context.scene
        events = scene.event_system
        current_frame = scene.frame_current

        if events.event_templates and events.active_template_index < len(events.event_templates):
            template = events.event_templates[events.active_template_index]

            # Check if event already exists on this frame
            for instance in events.event_instances:
                if instance.frame == current_frame and instance.template_name == template.name:
                    self.report({'WARNING'}, f"Event '{template.name}' already exists on frame {current_frame}")
                    return {'CANCELLED'}

            # Create marker
            marker_name = f"{template.name}_{current_frame}"
            marker = scene.timeline_markers.new(marker_name, frame=current_frame)

            # Store event instance
            instance = events.event_instances.add()
            instance.template_name = template.name
            instance.frame = current_frame
            instance.marker_name = marker_name

            # Copy custom field values from template
            for field in template.custom_fields:
                field_value = instance.field_values.add()
                field_value.name = field.name
                field_value.field_type = field.field_type

                # Set default values
                if field.field_type == 'BOOL':
                    field_value.bool_value = field.default_bool
                elif field.field_type == 'STRING':
                    field_value.string_value = field.default_string
                elif field.field_type == 'INT':
                    field_value.int_value = field.default_int
                elif field.field_type == 'FLOAT':
                    field_value.float_value = field.default_float
                elif field.field_type == 'ARRAY':
                    field_value.array_value = field.default_array

            self.report({'INFO'}, f"Added event '{template.name}' to frame {current_frame}")
        else:
            self.report({'ERROR'}, "No event template selected")

        return {'FINISHED'}

class EVENT_OT_add_template(Operator):
    bl_idname = "event.add_template"
    bl_label = "Add Event Template"
    bl_description = "Add a new event template"

    def execute(self, context):
        events = context.scene.event_system
        template = events.event_templates.add()
        template.name = f"Event_{len(events.event_templates)}"
        template.color = (1.0, 0.5, 0.0)  # Default orange color
        events.active_template_index = len(events.event_templates) - 1
        return {'FINISHED'}

class EVENT_OT_remove_template(Operator):
    bl_idname = "event.remove_template"
    bl_label = "Remove Event Template"
    bl_description = "Remove selected event template"

    def execute(self, context):
        events = context.scene.event_system
        if events.event_templates and events.active_template_index < len(events.event_templates):
            events.event_templates.remove(events.active_template_index)
            if events.active_template_index > 0:
                events.active_template_index -= 1
        return {'FINISHED'}

class EVENT_OT_remove_from_timeline(Operator):
    bl_idname = "event.remove_from_timeline"
    bl_label = "Remove Event from Timeline"
    bl_description = "Remove event from timeline"

    frame: IntProperty()

    def execute(self, context):
        scene = context.scene
        events = scene.event_system

        # Find and remove marker
        marker_to_remove = None
        for marker in scene.timeline_markers:
            if marker.frame == self.frame:
                marker_to_remove = marker
                break

        if marker_to_remove:
            scene.timeline_markers.remove(marker_to_remove)

        # Remove event instance
        instance_to_remove = None
        for i, instance in enumerate(events.event_instances):
            if instance.frame == self.frame:
                instance_to_remove = i
                break

        if instance_to_remove is not None:
            events.event_instances.remove(instance_to_remove)
            self.report({'INFO'}, f"Removed event from frame {self.frame}")

        return {'FINISHED'}

class EVENT_OT_go_to_event(Operator):
    bl_idname = "event.go_to_event"
    bl_label = "Go to Event Frame"
    bl_description = "Jump to the frame of the selected event"

    def execute(self, context):
        events = context.scene.event_system
        if events.event_instances and events.active_instance_index < len(events.event_instances):
            instance = events.event_instances[events.active_instance_index]
            context.scene.frame_set(instance.frame)
            self.report({'INFO'}, f"Jumped to frame {instance.frame}")
        return {'FINISHED'}

class EVENT_OT_duplicate_event(Operator):
    bl_idname = "event.duplicate_event"
    bl_label = "Duplicate Event"
    bl_description = "Duplicate the selected event to current frame"

    def execute(self, context):
        scene = context.scene
        events = scene.event_system
        current_frame = scene.frame_current

        if events.event_instances and events.active_instance_index < len(events.event_instances):
            source_instance = events.event_instances[events.active_instance_index]

            # Check if event already exists on current frame
            for instance in events.event_instances:
                if instance.frame == current_frame and instance.template_name == source_instance.template_name:
                    self.report({'WARNING'}, f"Event '{source_instance.template_name}' already exists on frame {current_frame}")
                    return {'CANCELLED'}

            # Create marker
            marker_name = f"{source_instance.template_name}_{current_frame}"
            marker = scene.timeline_markers.new(marker_name, frame=current_frame)

            # Create new instance
            new_instance = events.event_instances.add()
            new_instance.template_name = source_instance.template_name
            new_instance.frame = current_frame
            new_instance.marker_name = marker_name

            # Copy field values
            for field_value in source_instance.field_values:
                new_field_value = new_instance.field_values.add()
                new_field_value.name = field_value.name
                new_field_value.field_type = field_value.field_type
                new_field_value.bool_value = field_value.bool_value
                new_field_value.string_value = field_value.string_value
                new_field_value.int_value = field_value.int_value
                new_field_value.float_value = field_value.float_value
                new_field_value.array_value = field_value.array_value

            self.report({'INFO'}, f"Duplicated event '{source_instance.template_name}' to frame {current_frame}")
        else:
            self.report({'ERROR'}, "No event selected")

        return {'FINISHED'}

class EVENT_OT_move_event_to_current(Operator):
    bl_idname = "event.move_event_to_current"
    bl_label = "Move Event to Current Frame"
    bl_description = "Move the selected event to the current frame"

    def execute(self, context):
        scene = context.scene
        events = scene.event_system
        current_frame = scene.frame_current

        if events.event_instances and events.active_instance_index < len(events.event_instances):
            instance = events.event_instances[events.active_instance_index]
            old_frame = instance.frame

            # Check if another event already exists on current frame with same template
            for other_instance in events.event_instances:
                if (other_instance != instance and
                    other_instance.frame == current_frame and
                    other_instance.template_name == instance.template_name):
                    self.report({'WARNING'}, f"Event '{instance.template_name}' already exists on frame {current_frame}")
                    return {'CANCELLED'}

            # Update the frame (this will trigger the update function)
            instance.frame = current_frame

            self.report({'INFO'}, f"Moved event from frame {old_frame} to frame {current_frame}")
        else:
            self.report({'ERROR'}, "No event selected")

        return {'FINISHED'}

class EVENT_OT_clear_all_events(Operator):
    bl_idname = "event.clear_all_events"
    bl_label = "Clear All Events"
    bl_description = "Clear all events from timeline"

    def execute(self, context):
        scene = context.scene
        events = scene.event_system

        # Remove all markers created by this addon
        markers_to_remove = []
        for marker in scene.timeline_markers:
            for instance in events.event_instances:
                if marker.name == instance.marker_name:
                    markers_to_remove.append(marker)
                    break

        for marker in markers_to_remove:
            scene.timeline_markers.remove(marker)

        # Clear event instances
        events.event_instances.clear()

        self.report({'INFO'}, "All events cleared from timeline")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

def update_event_instance(self, context):
    """Called when template_name is changed"""
    scene = context.scene
    events = scene.event_system

    # Validate that the template exists
    template_exists = False
    selected_template = None
    for template in events.event_templates:
        if template.name == self.template_name:
            template_exists = True
            selected_template = template
            break

    if not template_exists and self.template_name:
        # If template doesn't exist, revert to first available template
        if events.event_templates:
            self.template_name = events.event_templates[0].name
            selected_template = events.event_templates[0]
        else:
            self.template_name = ""
            return

    # Update field values to match template
    if selected_template:
        # Clear existing field values
        self.field_values.clear()

        # Add field values from new template
        for field in selected_template.custom_fields:
            field_value = self.field_values.add()
            field_value.name = field.name
            field_value.field_type = field.field_type

            # Set default values
            if field.field_type == 'BOOL':
                field_value.bool_value = field.default_bool
            elif field.field_type == 'STRING':
                field_value.string_value = field.default_string
            elif field.field_type == 'INT':
                field_value.int_value = field.default_int
            elif field.field_type == 'FLOAT':
                field_value.float_value = field.default_float
            elif field.field_type == 'ARRAY':
                field_value.array_value = field.default_array

    # Find and update the marker name
    for marker in scene.timeline_markers:
        if marker.name == self.marker_name:
            new_name = f"{self.template_name}_{self.frame}"
            marker.name = new_name
            self.marker_name = new_name
            break

def update_event_frame(self, context):
    """Called when frame is changed"""
    scene = context.scene
    events = scene.event_system

    # Check for conflicts with other events
    for other_instance in events.event_instances:
        if (other_instance != self and
            other_instance.frame == self.frame and
            other_instance.template_name == self.template_name):
            # Revert the change
            for marker in scene.timeline_markers:
                if marker.name == self.marker_name:
                    self.frame = marker.frame
                    break
            return

    # Update marker frame and name
    for marker in scene.timeline_markers:
        if marker.name == self.marker_name:
            marker.frame = self.frame
            new_name = f"{self.template_name}_{self.frame}"
            marker.name = new_name
            self.marker_name = new_name
            break

@persistent
def frame_change_handler(scene):
    """Handler for frame changes to auto-select events"""
    if not hasattr(scene, 'event_system'):
        return

    events = scene.event_system
    current_frame = scene.frame_current

    # Find event on current frame
    for i, instance in enumerate(events.event_instances):
        if instance.frame == current_frame:
            events.active_instance_index = i
            break

class EVENT_OT_export_events(Operator):
    bl_idname = "event.export_events"
    bl_label = "Export Events"
    bl_description = "Export events to JSON file"

    filepath: StringProperty(
        name="File Path",
        description="Filepath used for exporting the events file",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    def execute(self, context):
        events_data = {
            "templates": [],
            "events": []
        }

        # Export templates with custom fields
        for template in context.scene.event_system.event_templates:
            template_data = {
                "name": template.name,
                "description": template.description,
                "color": list(template.color),
                "custom_fields": []
            }

            for field in template.custom_fields:
                field_data = {
                    "name": field.name,
                    "type": field.field_type,
                    "description": field.description,
                    "default_value": None
                }

                if field.field_type == 'BOOL':
                    field_data["default_value"] = field.default_bool
                elif field.field_type == 'STRING':
                    field_data["default_value"] = field.default_string
                elif field.field_type == 'INT':
                    field_data["default_value"] = field.default_int
                elif field.field_type == 'FLOAT':
                    field_data["default_value"] = field.default_float
                elif field.field_type == 'ARRAY':
                    field_data["default_value"] = field.default_array.split(',') if field.default_array else []

                template_data["custom_fields"].append(field_data)

            events_data["templates"].append(template_data)

        # Export event instances with field values
        for instance in context.scene.event_system.event_instances:
            event_data = {
                "template_name": instance.template_name,
                "frame": instance.frame,
                "time": instance.frame / context.scene.render.fps,
                "field_values": {}
            }

            for field_value in instance.field_values:
                if field_value.field_type == 'BOOL':
                    event_data["field_values"][field_value.name] = field_value.bool_value
                elif field_value.field_type == 'STRING':
                    event_data["field_values"][field_value.name] = field_value.string_value
                elif field_value.field_type == 'INT':
                    event_data["field_values"][field_value.name] = field_value.int_value
                elif field_value.field_type == 'FLOAT':
                    event_data["field_values"][field_value.name] = field_value.float_value
                elif field_value.field_type == 'ARRAY':
                    event_data["field_values"][field_value.name] = field_value.array_value.split(',') if field_value.array_value else []

            events_data["events"].append(event_data)

        try:
            with open(self.filepath, "w") as f:
                json.dump(events_data, f, indent=2)
            self.report({'INFO'}, f"Events exported to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class EVENT_OT_import_events(Operator):
    bl_idname = "event.import_events"
    bl_label = "Import Events"
    bl_description = "Import events from JSON file"

    filepath: StringProperty(
        name="File Path",
        description="Filepath used for importing the events file",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255
    )

    def execute(self, context):
        import os

        # Проверяем, что путь не пустой и файл существует
        if not self.filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}

        if not os.path.exists(self.filepath):
            self.report({'ERROR'}, f"File does not exist: {self.filepath}")
            return {'CANCELLED'}

        if not self.filepath.lower().endswith('.json'):
            self.report({'ERROR'}, "Selected file is not a JSON file")
            return {'CANCELLED'}

        try:
            with open(self.filepath, "r", encoding='utf-8') as f:
                events_data = json.load(f)

            # Проверяем структуру файла
            if "templates" not in events_data and "events" not in events_data:
                self.report({'ERROR'}, "Invalid events file format")
                return {'CANCELLED'}

            events = context.scene.event_system
            scene = context.scene

            # Clear existing data
            events.event_templates.clear()
            events.event_instances.clear()

            # Clear existing markers
            markers_to_remove = []
            for marker in scene.timeline_markers:
                for instance in events.event_instances:
                    if marker.name == instance.marker_name:
                        markers_to_remove.append(marker)
                        break

            for marker in markers_to_remove:
                scene.timeline_markers.remove(marker)

            # Import templates with custom fields
            for template_data in events_data.get("templates", []):
                if "name" not in template_data:
                    continue

                template = events.event_templates.add()
                template.name = template_data["name"]
                template.description = template_data.get("description", "")
                template.color = template_data.get("color", [1.0, 0.0, 0.0])

                # Import custom fields
                for field_data in template_data.get("custom_fields", []):
                    if "name" not in field_data or "type" not in field_data:
                        continue

                    field = template.custom_fields.add()
                    field.name = field_data["name"]
                    field.field_type = field_data["type"]
                    field.description = field_data.get("description", "")

                    default_value = field_data.get("default_value")
                    if field.field_type == 'BOOL' and default_value is not None:
                        field.default_bool = bool(default_value)
                    elif field.field_type == 'STRING' and default_value is not None:
                        field.default_string = str(default_value)
                    elif field.field_type == 'INT' and default_value is not None:
                        field.default_int = int(default_value)
                    elif field.field_type == 'FLOAT' and default_value is not None:
                        field.default_float = float(default_value)
                    elif field.field_type == 'ARRAY' and default_value is not None:
                        if isinstance(default_value, list):
                            field.default_array = ','.join(str(x) for x in default_value)
                        else:
                            field.default_array = str(default_value)

            # Import events with field values
            for event_data in events_data.get("events", []):
                if "frame" not in event_data or "template_name" not in event_data:
                    continue

                frame = event_data["frame"]
                template_name = event_data["template_name"]

                # Create marker
                marker_name = f"{template_name}_{frame}"
                marker = scene.timeline_markers.new(marker_name, frame=frame)

                # Create instance
                instance = events.event_instances.add()
                instance.template_name = template_name
                instance.frame = frame
                instance.marker_name = marker_name

                # Import field values
                field_values_data = event_data.get("field_values", {})
                for field_name, field_value in field_values_data.items():
                    field_val = instance.field_values.add()
                    field_val.name = field_name

                    # Determine field type from template
                    field_type = 'STRING'  # default
                    for template in events.event_templates:
                        if template.name == template_name:
                            for field in template.custom_fields:
                                if field.name == field_name:
                                    field_type = field.field_type
                                    break
                            break

                    field_val.field_type = field_type

                    try:
                        if field_type == 'BOOL':
                            field_val.bool_value = bool(field_value)
                        elif field_type == 'STRING':
                            field_val.string_value = str(field_value)
                        elif field_type == 'INT':
                            field_val.int_value = int(field_value)
                        elif field_type == 'FLOAT':
                            field_val.float_value = float(field_value)
                        elif field_type == 'ARRAY':
                            if isinstance(field_value, list):
                                field_val.array_value = ','.join(str(x) for x in field_value)
                            else:
                                field_val.array_value = str(field_value)
                    except (ValueError, TypeError):
                        # Если не удается конвертировать, используем строковое представление
                        field_val.string_value = str(field_value)

            self.report({'INFO'}, f"Events imported from {os.path.basename(self.filepath)}")

        except json.JSONDecodeError as e:
            self.report({'ERROR'}, f"Invalid JSON file: {str(e)}")
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {str(e)}")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class EVENT_OT_export_palette(Operator):
    bl_idname = "event.export_palette"
    bl_label = "Export Event Palette"
    bl_description = "Export event templates (palette) to JSON file"

    filepath: StringProperty(
        name="File Path",
        description="Filepath used for exporting the palette file",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    def execute(self, context):
        palette_data = {
            "templates": []
        }

        # Export only templates with custom fields
        for template in context.scene.event_system.event_templates:
            template_data = {
                "name": template.name,
                "description": template.description,
                "color": list(template.color),
                "custom_fields": []
            }

            for field in template.custom_fields:
                field_data = {
                    "name": field.name,
                    "type": field.field_type,
                    "description": field.description,
                    "default_value": None
                }

                if field.field_type == 'BOOL':
                    field_data["default_value"] = field.default_bool
                elif field.field_type == 'STRING':
                    field_data["default_value"] = field.default_string
                elif field.field_type == 'INT':
                    field_data["default_value"] = field.default_int
                elif field.field_type == 'FLOAT':
                    field_data["default_value"] = field.default_float
                elif field.field_type == 'ARRAY':
                    field_data["default_value"] = field.default_array.split(',') if field.default_array else []

                template_data["custom_fields"].append(field_data)

            palette_data["templates"].append(template_data)

        try:
            with open(self.filepath, "w") as f:
                json.dump(palette_data, f, indent=2)
            self.report({'INFO'}, f"Palette exported to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Palette export failed: {str(e)}")

        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = "event_palette.json"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class EVENT_OT_import_palette(Operator):
    bl_idname = "event.import_palette"
    bl_label = "Import Event Palette"
    bl_description = "Import event templates (palette) from JSON file"

    filepath: StringProperty(
        name="File Path",
        description="Filepath used for importing the palette file",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255
    )

    replace_existing: BoolProperty(
        name="Replace Existing Templates",
        description="Replace all existing templates or merge with current ones",
        default=False
    )

    def execute(self, context):
        import os

        # Проверяем, что путь не пустой и файл существует
        if not self.filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}

        if not os.path.exists(self.filepath):
            self.report({'ERROR'}, f"File does not exist: {self.filepath}")
            return {'CANCELLED'}

        if not self.filepath.lower().endswith('.json'):
            self.report({'ERROR'}, "Selected file is not a JSON file")
            return {'CANCELLED'}

        try:
            with open(self.filepath, "r", encoding='utf-8') as f:
                palette_data = json.load(f)

            # Проверяем структуру файла
            if "templates" not in palette_data:
                self.report({'ERROR'}, "Invalid palette file format - missing 'templates' section")
                return {'CANCELLED'}

            events = context.scene.event_system

            # Clear existing templates if replacing
            if self.replace_existing:
                events.event_templates.clear()

            # Import templates with custom fields
            imported_count = 0
            for template_data in palette_data.get("templates", []):
                # Проверяем обязательные поля
                if "name" not in template_data:
                    continue

                # Check if template with same name already exists
                existing_template = None
                for template in events.event_templates:
                    if template.name == template_data["name"]:
                        existing_template = template
                        break

                if existing_template and not self.replace_existing:
                    # Skip if template exists and we're not replacing
                    continue

                # Create new template or use existing
                if existing_template:
                    template = existing_template
                    # Clear existing fields
                    template.custom_fields.clear()
                else:
                    template = events.event_templates.add()

                template.name = template_data["name"]
                template.description = template_data.get("description", "")
                template.color = template_data.get("color", [1.0, 0.0, 0.0])

                # Import custom fields
                for field_data in template_data.get("custom_fields", []):
                    if "name" not in field_data or "type" not in field_data:
                        continue

                    field = template.custom_fields.add()
                    field.name = field_data["name"]
                    field.field_type = field_data["type"]
                    field.description = field_data.get("description", "")

                    default_value = field_data.get("default_value")
                    if field.field_type == 'BOOL' and default_value is not None:
                        field.default_bool = bool(default_value)
                    elif field.field_type == 'STRING' and default_value is not None:
                        field.default_string = str(default_value)
                    elif field.field_type == 'INT' and default_value is not None:
                        field.default_int = int(default_value)
                    elif field.field_type == 'FLOAT' and default_value is not None:
                        field.default_float = float(default_value)
                    elif field.field_type == 'ARRAY' and default_value is not None:
                        if isinstance(default_value, list):
                            field.default_array = ','.join(str(x) for x in default_value)
                        else:
                            field.default_array = str(default_value)

                imported_count += 1

            action = "replaced" if self.replace_existing else "imported"
            self.report({'INFO'}, f"Palette {action}: {imported_count} templates from {os.path.basename(self.filepath)}")

        except json.JSONDecodeError as e:
            self.report({'ERROR'}, f"Invalid JSON file: {str(e)}")
        except Exception as e:
            self.report({'ERROR'}, f"Palette import failed: {str(e)}")

        return {'FINISHED'}

    def invoke(self, context, event):
        # Показываем диалог выбора файла с опциями
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "replace_existing")

# Registration
classes = [
    EventField,
    EventFieldValue,
    EventTemplate,
    EventInstance,
    EventSystemProperties,
    EVENT_UL_templates,
    EVENT_UL_instances,
    EVENT_UL_fields,
    EVENT_PT_panel,
    EVENT_OT_add_template,
    EVENT_OT_remove_template,
    EVENT_OT_add_field,
    EVENT_OT_remove_field,
    EVENT_OT_add_to_timeline,
    EVENT_OT_remove_from_timeline,
    EVENT_OT_go_to_event,
    EVENT_OT_duplicate_event,
    EVENT_OT_move_event_to_current,
    EVENT_OT_export_palette,
    EVENT_OT_import_palette,
    EVENT_OT_export_events,
    EVENT_OT_import_events,
    EVENT_OT_clear_all_events,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.event_system = PointerProperty(type=EventSystemProperties)

    # Add frame change handler
    if frame_change_handler not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(frame_change_handler)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    if hasattr(bpy.types.Scene, 'event_system'):
        del bpy.types.Scene.event_system

    # Remove frame change handler
    if frame_change_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(frame_change_handler)

if __name__ == "__main__":
    register()
