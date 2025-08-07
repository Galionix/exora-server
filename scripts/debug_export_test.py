import bpy

def debug_event_values():
    """Отладочная функция для проверки значений полей событий"""

    if not hasattr(bpy.context.scene, 'event_system'):
        print("❌ Event system не найден!")
        return

    events = bpy.context.scene.event_system

    print("\n" + "="*60)
    print("🔍 ОТЛАДКА ЗНАЧЕНИЙ ПОЛЕЙ СОБЫТИЙ")
    print("="*60)

    # Проверяем шаблоны
    print(f"\n📋 ШАБЛОНЫ ({len(events.event_templates)}):")
    for i, template in enumerate(events.event_templates):
        print(f"  [{i}] {template.name}")
        for field in template.custom_fields:
            default_val = "НЕИЗВЕСТНО"
            if field.field_type == 'BOOL':
                default_val = field.default_bool
            elif field.field_type == 'STRING':
                default_val = f"'{field.default_string}'"
            elif field.field_type == 'INT':
                default_val = field.default_int
            elif field.field_type == 'FLOAT':
                default_val = field.default_float
            elif field.field_type == 'ARRAY':
                default_val = f"'{field.default_array}'"

            print(f"    - {field.name} ({field.field_type}): default = {default_val}")

    # Проверяем события на таймлайне
    print(f"\n🎬 СОБЫТИЯ НА ТАЙМЛАЙНЕ ({len(events.event_instances)}):")
    for i, instance in enumerate(events.event_instances):
        is_active = "⭐ АКТИВНОЕ" if i == events.active_instance_index else ""
        print(f"  [{i}] {instance.template_name} @ кадр {instance.frame} {is_active}")
        print(f"      Маркер: {instance.marker_name}")
        print(f"      Полей значений: {len(instance.field_values)}")

        for field_value in instance.field_values:
            actual_val = "НЕИЗВЕСТНО"
            if field_value.field_type == 'BOOL':
                actual_val = field_value.bool_value
            elif field_value.field_type == 'STRING':
                actual_val = f"'{field_value.string_value}'"
            elif field_value.field_type == 'INT':
                actual_val = field_value.int_value
            elif field_value.field_type == 'FLOAT':
                actual_val = field_value.float_value
            elif field_value.field_type == 'ARRAY':
                actual_val = f"'{field_value.array_value}'"

            print(f"        - {field_value.name} ({field_value.field_type}): {actual_val}")

    print("\n" + "="*60)
    print("✅ Отладка завершена")
    print("="*60)

# Запуск отладки
if __name__ == "__main__":
    debug_event_values()
