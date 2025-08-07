# Animation Events System для Blender

Полнофункциональная система событий анимации с настраиваемыми полями, ENUM селекторами и маркерами таймлайна для Blender 3.0+.

## Ключевые возможности

✅ **Настраиваемые шаблоны событий** с цветовой кодировкой
✅ **6 типов полей**: Boolean, String, Integer, Float, Array, **ENUM**
✅ **ENUM поля** с выпадающими списками для точного выбора
✅ **Визуальные маркеры** на таймлайне Blender
✅ **Автоматическое выделение** событий при навигации
✅ **Экспорт/импорт** палеток и проектов
✅ **Готовые шаблоны** для игровых событий

## Визуальная документация

> **Примечание**: Для лучшего понимания рекомендуется добавить скриншоты следующих элементов:

### Рекомендуемые иллюстрации:
1. **`screenshot_01_installation.png`** - Процесс установки аддона в Preferences
2. **`screenshot_02_interface_overview.png`** - Общий вид интерфейса в Dope Sheet Editor
3. **`screenshot_03_template_creation.png`** - Создание шаблона события
4. **`screenshot_04_enum_fields.png`** - Настройка ENUM полей с опциями
5. **`screenshot_05_timeline_events.png`** - События на таймлайне с маркерами
6. **`screenshot_06_event_editing.png`** - Панель редактирования с ENUM селекторами
7. **`screenshot_07_export_import.png`** - Диалоги экспорта/импорта

### Альтернативные способы документации:
- **Создайте скриншоты самостоятельно** используя Blender
- **Запишите короткое видео** демонстрирующее workflow
- **Создайте GIF анимации** ключевых операций
- **Нарисуйте схемы** в любом графическом редакторе

### Инструкция для создания скриншотов:

```
Настройки для скриншотов:
- Разрешение: 1920x1080 или больше
- Формат: PNG для четкости интерфейса
- Выделите активные элементы красными рамками
- Используйте стрелки для указания важных кнопок
- Добавьте подписи к ключевым элементам
```

## Установка

<!-- ![Установка аддона](screenshots/screenshot_01_installation.png) -->

1. Скачайте файл `animation_events_addon.py`
2. В Blender откройте: **Edit → Preferences → Add-ons**
3. Нажмите **"Install..."** и выберите файл аддона
4. Включите аддон **"Animation Events System"** в списке (поставьте галочку)
5. Нажмите **"Save Preferences"**

## Расположение интерфейса

<!-- ![Обзор интерфейса](screenshots/screenshot_02_interface_overview.png) -->

После установки аддон доступен в:
- **Dope Sheet Editor** → боковая панель (клавиша **N**) → вкладка **"Events"**

## Подробное руководство

### 1. Создание шаблонов событий

<!-- ![Создание шаблона](screenshots/screenshot_03_template_creation.png) -->

Шаблоны - это переиспользуемые типы событий с настраиваемыми полями.

#### Создание базового шаблона:
1. В секции **"Event Templates"** нажмите кнопку **"+"**
2. Настройте основные свойства:
   - **Name** - название события (например, "Footstep", "Attack", "SwordHit")
   - **Description** - подробное описание события
   - **Color** - цвет для визуальной идентификации

#### Добавление настраиваемых полей:

<!-- ![ENUM поля](screenshots/screenshot_04_enum_fields.png) -->

1. Выберите шаблон в списке
2. В секции **"Custom Fields"** нажмите **"+"**
3. Настройте поле:
   - **Field Name** - название поля (например, "weapon_type", "surface_type")
   - **Type** - тип поля:
     - **Boolean** - True/False (например, "is_critical_hit")
     - **String** - текст (например, "sound_file_name")
     - **Integer** - целое число (например, "damage_amount")
     - **Float** - дробное число (например, "volume_level")
     - **Array** - список через запятую (например, "particle_effects")
     - **🆕 Enum** - выбор из списка (например, "weapon_type")
   - **Description** - описание поля
   - **Default** - значение по умолчанию

#### 🆕 Настройка ENUM полей:
1. Выберите тип **"Enum"**
2. В поле **"Enum Options"** введите варианты через запятую:
   ```
   sword,axe,mace,dagger,bow,staff
   ```
3. В поле **"Default"** укажите значение по умолчанию:
   ```
   sword
   ```
4. Система покажет превью: **"Options: sword, axe, mace, dagger, bow, staff"**

#### Примеры готовых шаблонов с ENUM:

**Footstep (Улучшенный)**
- Поля:
  - `foot_type` (Enum) = "left" [left, right, both]
  - `surface_type` (Enum) = "grass" [grass, dirt, stone, wood, metal, water, sand, snow]
  - `movement_type` (Enum) = "walk" [walk, run, sneak, sprint, crouch, backwards]
  - `volume` (Float) = 0.8
  - `pitch_variation` (Enum) = "normal" [low, normal, high, random]

**Attack (Расширенный)**
- Поля:
  - `weapon_type` (Enum) = "sword" [sword, axe, mace, dagger, bow, crossbow, staff]
  - `attack_type` (Enum) = "slash" [slash, stab, crush, pierce, ranged, magic]
  - `hit_location` (Enum) = "torso" [head, torso, arms, legs, shield, armor]
  - `damage` (Integer) = 100
  - `damage_type` (Enum) = "physical" [physical, fire, ice, lightning, poison, holy]
  - `hit_intensity` (Enum) = "medium" [light, medium, heavy, devastating]

**Spell Cast (Магические заклинания)**
- Поля:
  - `spell_school` (Enum) = "evocation" [evocation, conjuration, transmutation, illusion]
  - `spell_element` (Enum) = "fire" [fire, water, earth, air, lightning, ice, arcane]
  - `spell_level` (Enum) = "level_1" [cantrip, level_1, level_2, level_3, epic]
  - `casting_style` (Enum) = "verbal" [verbal, somatic, material, focus, instant]
  - `target_type` (Enum) = "single" [self, single, area, cone, line, chain]

### 2. Работа с палеткой шаблонов

#### Импорт готовой палетки:
1. Скачайте `event_palette_example.json` (содержит 10 готовых шаблонов с ENUM)
2. В секции **"Template Tools"** нажмите **"Import Palette"**
3. **Важно**: Дважды кликните на файл `.json` (не выбирайте мышкой + кнопка!)
4. Выберите опцию:
   - **Replace Existing Templates** ☐ - добавить к существующим
   - **Replace Existing Templates** ☑ - заменить все шаблоны

#### Экспорт палетки:
1. В секции **"Template Tools"** нажмите **"Export Palette"**
2. Выберите место сохранения и имя файла
3. **Важно**: Дважды кликните или введите имя и нажмите Enter

### 3. Добавление событий на таймлайн

<!-- ![События на таймлайне](screenshots/screenshot_05_timeline_events.png) -->

#### Процесс добавления:
1. Выберите нужный шаблон в списке **"Event Templates"**
2. Установите текущий кадр (Current Frame) на нужную позицию
3. Нажмите большую кнопку **"Add '[Template Name]' to Frame [X]"**

#### 🆕 Автоматические улучшения:
- **Автоматическое выделение**: новое событие сразу выделяется в списке
- **Готовые значения**: все поля заполняются значениями по умолчанию
- **Визуальные маркеры**: на таймлайне появляется цветной маркер

### 4. Редактирование событий на таймлайне

<!-- ![Редактирование с ENUM](screenshots/screenshot_06_event_editing.png) -->

#### Автоматический выбор:
- При перемещении по кадрам событие автоматически выделяется в списке
- В панели **"Edit Selected Event"** отображаются его настройки

#### 🆕 Редактирование ENUM полей:
1. **ENUM поля** отображаются как **выпадающие списки**
2. **Клик на поле** открывает список доступных вариантов
3. **Выбор значения** мгновенно сохраняется
4. **Только валидные варианты** - невозможно ввести неправильное значение

#### Редактирование других типов полей:
- **Boolean поля** - checkbox (☑/☐)
- **String поля** - текстовое поле
- **Integer/Float поля** - числовые поля с валидацией
- **Array поля** - текст через запятую

#### Важные особенности:
- **Изменения сохраняются мгновенно** - не нужно нажимать "Сохранить"
- **Независимость от шаблонов** - изменения в событиях НЕ влияют на шаблоны
- **Умная валидация** - ENUM поля принимают только допустимые значения
- **Предотвращение дублей** - нельзя добавить два одинаковых события на один кадр

### 5. Управление событиями

#### Навигация:
- **Go to Frame** - перейти на кадр выбранного события
- **Duplicate** - создать копию события на текущем кадре (со всеми настройками)
- **Move to Current Frame** - переместить событие на текущий кадр

#### Удаление:
- **X** в списке событий - удалить конкретное событие
- **Clear All Events** - удалить все события (с подтверждением)

### 6. Экспорт и импорт проектов

<!-- ![Экспорт и импорт](screenshots/screenshot_07_export_import.png) -->

#### 🆕 Раздельный экспорт:

**Экспорт только событий (новое):**
1. В секции **"Timeline Tools"** нажмите **"Export Events"**
2. Сохраняются: **только события** с таймлайна + значения полей
3. **Файл меньше** и содержит только нужные данные для игры

**Экспорт палетки шаблонов:**
1. В секции **"Template Tools"** нажмите **"Export Palette"**
2. Сохраняются: **только шаблоны** с настройками полей
3. **Можно переиспользовать** в других проектах

#### Импорт проекта:
1. Нажмите **"Import Events"** (импортирует шаблоны + события)
2. **Дважды кликните** на файл проекта
3. **Внимание**: Все текущие данные будут заменены!

#### 🆕 Форматы файлов:

**Экспорт только событий** (`timeline_events.json`):
```json
{
  "events": [
    {
      "template_name": "Attack_Hit",
      "frame": 25,
      "time": 1.041,
      "field_values": {
        "weapon_type": "sword",
        "attack_type": "slash",
        "hit_location": "torso",
        "damage": 150,
        "damage_type": "fire",
        "hit_intensity": "heavy"
      }
    }
  ]
}
```

**Палетка шаблонов** (`event_palette.json`):
```json
{
  "templates": [
    {
      "name": "Attack_Hit",
      "description": "Weapon hit event",
      "color": [1.0, 0.2, 0.2],
      "custom_fields": [
        {
          "name": "weapon_type",
          "type": "ENUM",
          "description": "Type of weapon used",
          "default_value": "sword",
          "enum_options": ["sword", "axe", "mace", "dagger"]
        }
      ]
    }
  ]
}
```

## Практические примеры с ENUM

### Пример 1: Боевая анимация (RPG)
1. **Импортируйте готовую палетку** `event_palette_example.json`
2. **Используйте шаблон "Attack_Hit"** с ENUM полями:
   - `weapon_type`: sword → axe → dagger
   - `attack_type`: slash → stab → crush
   - `hit_location`: head → torso → legs
   - `damage_type`: physical → fire → ice
3. **Расставьте события** по кадрам атаки
4. **Настройте каждое попадание** через выпадающие списки

### Пример 2: Система звуков окружения
1. **Создайте шаблон "Environmental_Sound"**:
   - `sound_category` (Enum): [ambient, nature, mechanical, magical]
   - `weather_condition` (Enum): [clear, rain, storm, snow, fog]
   - `time_of_day` (Enum): [dawn, morning, noon, evening, night]
   - `intensity` (Enum): [subtle, normal, prominent, overwhelming]
2. **Добавляйте звуки** на разные кадры анимации
3. **Быстро меняйте настройки** через ENUM селекторы

### Пример 3: Интерактивные UI события
1. **Шаблон "UI_Interaction"**:
   - `ui_element` (Enum): [button, menu, popup, notification]
   - `interaction_type` (Enum): [click, hover, drag, swipe]
   - `feedback_type` (Enum): [visual, audio, haptic, combined]
   - `animation_style` (Enum): [fade, slide, scale, bounce]
2. **Синхронизируйте** с анимацией интерфейса
3. **Точно контролируйте** поведение UI

### Пример 4: Магические заклинания
1. **Шаблон "Spell_Cast"** (уже в палетке):
   - `spell_school`: evocation → conjuration → transmutation
   - `spell_element`: fire → ice → lightning → arcane
   - `spell_level`: cantrip → level_1 → level_3 → epic
   - `target_type`: self → single → area → chain
2. **Создавайте комбинации** заклинаний
3. **Легко балансируйте** магическую систему

## Интеграция с игровыми движками

### Unity (C#)
```csharp
[System.Serializable]
public class AnimationEvent {
    public string template_name;
    public float time;
    public Dictionary<string, object> field_values;
}

// Загрузка ENUM значений
var weaponType = eventData.field_values["weapon_type"] as string;
switch(weaponType) {
    case "sword": PlaySwordSound(); break;
    case "axe": PlayAxeSound(); break;
    case "mace": PlayMaceSound(); break;
}
```

### Unreal Engine (Blueprint)
1. **Создайте Enum** для каждого ENUM поля из Blender
2. **Используйте Select node** для обработки ENUM значений
3. **Привяжите к Animation Notifies** для автоматического вызова

### Godot (GDScript)
```gdscript
# Загрузка и обработка ENUM событий
func process_animation_event(event_data):
    var weapon_type = event_data.field_values.weapon_type

    match weapon_type:
        "sword": play_sword_effects()
        "axe": play_axe_effects()
        "mace": play_mace_effects()
        _: print("Unknown weapon type: ", weapon_type)
```

### Custom Game Engine (C++)
```cpp
// Строгая типизация для ENUM значений
enum class WeaponType { Sword, Axe, Mace, Dagger };
enum class AttackType { Slash, Stab, Crush, Pierce };

WeaponType ParseWeaponType(const std::string& value) {
    if (value == "sword") return WeaponType::Sword;
    if (value == "axe") return WeaponType::Axe;
    // ...
}
```

## Советы по работе с ENUM

### Планирование ENUM значений:
- **Используйте понятные имена**: "sword" вместо "wpn_01"
- **Группируйте логически**: все оружие, все поверхности, все эмоции
- **Предусматривайте расширение**: добавляйте "custom" или "other"
- **Соблюдайте единообразие**: "magic_missile" везде, не "magic_missile" и "magicMissile"

### Организация шаблонов:
- **Цветовое кодирование**: красные - атаки, зеленые - звуки, синие - UI
- **Префиксы в названиях**: "Combat_", "Audio_", "UI_", "Magic_"
- **Группировка полей**: сначала основные ENUM, потом числовые значения
- **Документирование**: заполняйте Description для каждого поля

### Эффективный workflow:
1. **Планирование** - определите все возможные значения ENUM заранее
2. **Создание палетки** - настройте все шаблоны с ENUM полями
3. **Тестирование** - проверьте все комбинации значений
4. **Расстановка событий** - добавьте события на анимацию
5. **Тонкая настройка** - используйте ENUM селекторы для быстрой настройки
6. **Экспорт** - сохраните только события для использования в движке

### Отладка и валидация:
```python
# Скрипт для проверки всех ENUM значений
def validate_enum_values():
    events = bpy.context.scene.event_system

    for instance in events.event_instances:
        for field_value in instance.field_values:
            if field_value.field_type == 'ENUM':
                # Найти шаблон и проверить допустимые значения
                template = find_template(instance.template_name)
                field_def = find_field_definition(template, field_value.name)

                valid_options = field_def.enum_options.split(',')
                if field_value.enum_value not in valid_options:
                    print(f"ОШИБКА: {field_value.enum_value} не входит в {valid_options}")
```

## Решение проблем

### ENUM поля не работают:
- **Проверьте версию аддона** - ENUM добавлены в последней версии
- **Переустановите аддон** если обновляли с предыдущей версии
- **Перезапустите Blender** после установки

### Выпадающий список пустой:
- **Убедитесь**, что в шаблоне заполнено поле "Enum Options"
- **Проверьте формат**: варианты через запятую без пробелов
- **Пересоздайте событие** если изменяли опции шаблона

### Импорт палетки не работает:
- **Дважды кликните** на файл вместо выбора мышкой
- **Проверьте JSON формат** - файл должен содержать "enum_options"
- **Убедитесь**, что файл имеет расширение `.json`

### Экспорт содержит неправильные значения:
- **Используйте новую версию** - в старых версиях была проблема с дубликатами
- **Сохраните проект** и перезапустите Blender если проблема остается

## 🆕 Новые возможности в последней версии

✅ **ENUM поля** с выпадающими списками
✅ **Автоматическое выделение** новых событий
✅ **Раздельный экспорт** событий и палеток
✅ **Исправлен экспорт** - сохраняются измененные значения
✅ **Готовая палетка** с 10 шаблонами и множеством ENUM полей
✅ **Улучшенная валидация** ENUM значений

## Готовые ресурсы

### Файлы для скачивания:
- **`animation_events_addon.py`** - основной файл аддона
- **`event_palette_example.json`** - готовая палетка с 10 шаблонами
- **`readme.md`** - подробная документация

### Шаблоны в готовой палетке:
1. **Footstep** - шаги персонажа (5 ENUM полей)
2. **Attack_Hit** - попадания оружием (6 ENUM полей)
3. **Audio_SFX** - звуковые эффекты (5 ENUM полей)
4. **Spell_Cast** - магические заклинания (8 ENUM полей)
5. **Movement_Jump** - прыжки персонажа (4 ENUM поля)
6. **Pickup_Item** - подбор предметов (5 ENUM полей)
7. **Animation_Trigger** - триггеры анимации (6 ENUM полей)
8. **Dialogue_Start** - начало диалогов (6 ENUM полей)
9. **Environmental_Effect** - эффекты окружения (6 ENUM полей)
10. **UI_Interaction** - взаимодействие с интерфейсом (5 ENUM полей)

**Всего: 56 ENUM полей с 400+ предустановленными вариантами!**

## Обновления и поддержка

Для получения обновлений и сообщения об ошибках:
- Проверяйте репозиторий проекта
- Создавайте Issues для багов и предложений
- Делитесь своими палетками с сообществом

## Создание собственной документации

### Для разработчиков аддонов:
```python
# Пример автоматических скриншотов с ENUM полями
import bpy

def create_enum_demo():
    # Создать шаблон с ENUM полями
    events = bpy.context.scene.event_system
    template = events.event_templates.add()
    template.name = "Demo_Template"

    # ENUM поле
    field = template.custom_fields.add()
    field.name = "demo_enum"
    field.field_type = 'ENUM'
    field.enum_options = "option1,option2,option3"
    field.default_enum = "option1"

    # Добавить событие
    bpy.ops.event.add_to_timeline()

    # Сделать скриншот
    bpy.ops.screen.screenshot(filepath="/path/to/enum_demo.png")
```

### Для пользователей:
1. **Встроенная функция Blender**: `Window → Save Screenshot`
2. **Внешние инструменты**:
   - Windows: Snipping Tool, ShareX
   - Mac: Command+Shift+4
   - Linux: GNOME Screenshot, Flameshot

### Создание собственных палеток:
```json
{
  "templates": [
    {
      "name": "Your_Custom_Event",
      "description": "Description of your event",
      "color": [1.0, 5.0, 0.0],
      "custom_fields": [
        {
          "name": "your_enum_field",
          "type": "ENUM",
          "description": "Your ENUM field",
          "default_value": "option1",
          "enum_options": ["option1", "option2", "option3"]
        }
      ]
    }
  ]
}
```

### Рекомендации по оформлению:
- **Стрелки и выноски**: Красный цвет (#FF0000)
- **Выделение ENUM полей**: Синие рамки (#0066FF)
- **Выпадающие списки**: Зеленые рамки (#00AA00)
- **Нумерация шагов**: Желтые кружки с черными цифрами
- **Размер изображений**: Максимум 1200px по ширине

### Инструменты для создания схем:
- **Draw.io** (diagrams.net) - бесплатный онлайн редактор
- **Figma** - для UI mockups и схем ENUM взаимодействий
- **Canva** - для простых иллюстраций с ENUM полями
- **GIMP/Photoshop** - для редактирования скриншотов интерфейса
