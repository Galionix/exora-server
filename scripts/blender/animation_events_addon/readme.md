# Animation Events System для Blender

Профессиональная система событий анимации с настраиваемыми полями, ENUM селекторами и маркерами таймлайна для Blender 3.0+.

---

## 🎯 Быстрый старт для аниматора

> **Для кого**: Аниматоры и моделлеры, работающие с готовыми шаблонами событий

### Установка аддона

1. **Скачайте файл** `animation_events_addon.py`
2. **В Blender**: `Edit → Preferences → Add-ons`
3. **Нажмите** `Install...` и выберите файл аддона
4. **Включите** аддон `Animation Events System` (поставьте галочку)
5. **Сохраните настройки**: `Save Preferences`

### Где найти интерфейс

📍 **Dope Sheet Editor** → боковая панель (**клавиша N**) → вкладка **"Events"**

### Рабочий процесс аниматора

#### 1️⃣ Загрузка готовой палетки событий

1. **Получите палетку** от разработчика - файл `.json` с готовыми шаблонами событий
2. В секции **"Template Tools"** нажмите **"Import Palette"**
3. **Дважды кликните** на файл `.json` (не выбирайте мышкой!)
4. **Опция импорта**: снимите галочку `Replace Existing Templates` если хотите добавить к существующим

✅ **Результат**: У вас появятся готовые шаблоны событий для вашего проекта

#### 2️⃣ Добавление событий на анимацию

1. **Выберите шаблон** в списке `Event Templates`
2. **Установите кадр** на нужную позицию анимации
3. **Нажмите большую кнопку** `Add '[Template Name]' to Frame [X]`

✅ **Результат**: На таймлайне появится цветной маркер, событие добавится в список

#### 3️⃣ Настройка параметров события

1. **Событие автоматически выделяется** при добавлении
2. В секции **"Edit Selected Event"** настройте параметры:
   - **ENUM поля** - выпадающие списки с готовыми вариантами
   - **Числовые поля** - урон, громкость, время, количество и т.д.
   - **Текстовые поля** - имена файлов, описания, идентификаторы
   - **Boolean поля** - флаги включения/выключения

**Пример настройки события:**
- Выпадающий список: option1 → option2 → option3
- Числовое поле: 100 → 150 → 200
- Текстовое поле: "default_file.wav" → "custom_file.wav"
- Флаг: false → true

#### 4️⃣ Навигация и управление

**Автоматическая навигация:**
- При перемещении по кадрам событие автоматически выделяется
- **"Go to Frame"** - быстрый переход на кадр события

**Копирование и перемещение:**
- **"Duplicate"** - копировать событие на текущий кадр
- **"Move to Current Frame"** - переместить событие
- **X** в списке - удалить событие

#### 5️⃣ Экспорт для игры

1. **"Export Events"** в секции `Timeline Tools`
2. **Сохраните как** `animation_events.json`
3. **Передайте программисту** - файл содержит только события с их параметрами

### Общие принципы работы с событиями

#### Типы полей в событиях

**🔽 Выпадающие списки (ENUM)** - предустановленные варианты
- Используются для выбора из ограниченного набора опций
- Примеры: тип оружия, материал поверхности, интенсивность эффекта
- Нельзя вводить произвольные значения

**🔢 Числовые поля (INT/FLOAT)** - точные значения
- Целые числа (INT): урон, количество, индексы
- Дробные числа (FLOAT): громкость, время, расстояния
- Можно вводить любые числа в допустимом диапазоне

**📝 Текстовые поля (STRING)** - произвольный текст
- Имена файлов, идентификаторы, описания
- Можно вводить любой текст

**☑️ Флаги (BOOL)** - включено/выключено
- Простые переключатели для опций
- Примеры: критический удар, зацикленная анимация, автоиспользование

**📋 Списки (ARRAY)** - набор значений
- Несколько элементов через запятую
- Примеры: эффекты, теги, компоненты

#### Цветовая кодировка шаблонов

Каждый шаблон имеет свой цвет для быстрой визуальной идентификации:
- **🔴 Красный** - боевые действия и урон
- **🔵 Синий** - звуковые эффекты
- **🟣 Фиолетовый** - магия и заклинания
- **🟡 Желтый** - движение и навигация
- **🟢 Зеленый** - окружение и природа
- **🟠 Оранжевый** - интерфейс и UI
- **⚫ Серый** - общие и служебные события

### Типичные рабочие сценарии

#### Работа с боевыми анимациями
```
1. Добавьте события подготовки (звуки, эффекты)
2. Разместите основное событие на момент контакта
3. Добавьте события последствий (отдача, эффекты)
4. Настройте параметры урона и типов атаки
```

#### Работа с анимациями передвижения
```
1. Разместите события шагов на контакт с поверхностью
2. Настройте тип поверхности и интенсивность
3. Добавьте звуковые события для шагов
4. При необходимости добавьте эффекты частиц
```

#### Работа с анимациями заклинаний
```
1. Событие начала каста в начале анимации
2. Звуковые и визуальные эффекты в процессе
3. Основное событие применения эффекта
4. События завершения и последствий
```

#### Работа с интерфейсными анимациями
```
1. События показа/скрытия элементов
2. Звуковые подтверждения действий
3. Анимационные переходы между состояниями
4. Обновления информации в UI
```

### Советы для эффективной работы

✅ **Планируйте заранее** - определите ключевые моменты анимации перед началом работы
✅ **Используйте цвета шаблонов** - для быстрого поиска нужного типа события
✅ **Дублируйте похожие события** - сэкономьте время на настройке параметров
✅ **Тестируйте в игре** - регулярно экспортируйте и проверяйте результат
✅ **Сохраняйте версии** - делайте бэкапы важных анимационных последовательностей
✅ **Изучите доступные шаблоны** - познакомьтесь с полным набором событий проекта
✅ **Следуйте конвенциям проекта** - используйте стандартные значения для схожих ситуаций

### Решение проблем

**🔴 Не видно аддона**
- Убедитесь что включен в Preferences → Add-ons
- Откройте Dope Sheet Editor (не Graph Editor!)
- Нажмите N для показа боковой панели

**🔴 Пустые выпадающие списки**
- Убедитесь что импортировали палетку с ENUM полями
- Проверьте что используете правильную версию палетки
- Пересоздайте событие если изменяли шаблон

**🔴 Импорт палетки не работает**
- Дважды кликните на файл, не выбирайте мышкой + кнопка
- Убедитесь что файл имеет расширение .json
- Проверьте что файл не поврежден и содержит правильную структуру

**🔴 События не экспортируются**
- Убедитесь что есть события на таймлайне
- Проверьте права записи в папку экспорта
- Попробуйте экспортировать в другую папку

**🔴 Значения полей сбрасываются**
- Не меняйте тип шаблона после создания события
- Убедитесь что сохраняете файл Blender после настройки
- При проблемах пересоздайте событие заново

**🔴 События не экспортируются**
- Убедитесь что есть события на таймлайне
- Проверьте права записи в папку экспорта
- Попробуйте экспортировать в другую папку

**🔴 Значения полей сбрасываются**
- Не меняйте тип шаблона после создания события
- Убедитесь что сохраняете файл Blender после настройки
- При проблемах пересоздайте событие заново

### Взаимодействие с командой

#### С разработчиком системы событий:
- **Запрашивайте обновленные палетки** при изменении игровой логики
- **Сообщайте о недостающих типах событий** для вашей работы
- **Предлагайте улучшения** в структуре существующих шаблонов

#### С программистами:
- **Предоставляйте файлы экспорта** в согласованном формате
- **Тестируйте совместно** корректность обработки событий в игре
- **Документируйте особенности** использования событий в анимациях

#### С другими аниматорами:
- **Используйте единые соглашения** по именованию и параметрам
- **Делитесь настроенными шаблонами** событий между проектами
- **Координируйте изменения** в общих палетках событий

---

## 🛠️ Подробное руководство для разработчика

> **Для кого**: Разработчики игр, создающие шаблоны событий и настраивающие систему

### Архитектура системы

#### Основные компоненты

**🎨 Event Templates (Шаблоны событий)**
- Переиспользуемые типы событий
- Настраиваемые поля с типами и значениями по умолчанию
- Цветовая кодировка для визуальной идентификации
- Экспорт/импорт как отдельная палетка

**📋 Event Instances (Экземпляры событий)**
- Конкретные события на таймлайне
- Привязаны к кадрам анимации
- Содержат актуальные значения полей
- Создают маркеры на таймлайне Blender

**🔧 Custom Fields (Настраиваемые поля)**
- 6 типов: Boolean, String, Integer, Float, Array, **Enum**
- Значения по умолчанию для быстрого создания
- Динамическая генерация UI на основе типов

#### Типы полей и их применение

**BOOL (Boolean)** - True/False
```python
# Примеры использования
is_critical_hit: bool = True
auto_use_item: bool = False
loop_animation: bool = True
```

**STRING (String)** - Текстовые значения
```python
# Примеры использования
audio_file: str = "sword_clash.wav"
dialogue_id: str = "npc_greeting_001"
animation_name: str = "attack_combo_1"
```

**INT (Integer)** - Целые числа
```python
# Примеры использования
damage: int = 150
mana_cost: int = 80
stamina_cost: int = 25
```

**FLOAT (Float)** - Дробные числа
```python
# Примеры использования
volume: float = 0.85
blend_time: float = 0.2
jump_height: float = 3.5
```

**ARRAY (Array)** - Списки через запятую
```python
# Примеры использования
hit_effects: list = ["spark", "blood", "screen_shake"]
spell_components: list = ["fire_essence", "sulfur"]
dialogue_tags: list = ["quest", "friendly", "important"]
```

**🆕 ENUM (Enumeration)** - Выбор из списка
```python
# Примеры использования
weapon_type: enum = "sword" # [sword, axe, mace, dagger]
surface_type: enum = "stone" # [grass, dirt, stone, wood, metal]
spell_element: enum = "fire" # [fire, water, earth, air, lightning]
```

### Создание профессиональных шаблонов

#### Планирование шаблона события

**1. Определите назначение**
```
Имя: Combat_WeaponHit
Назначение: Обработка попаданий оружием в бою
Цвет: Красный (#FF0000) - боевые действия
```

**2. Определите обязательные поля**
```
weapon_type (ENUM) - тип оружия [sword, axe, bow, magic]
damage (INT) - базовый урон [1-1000]
hit_location (ENUM) - место попадания [head, torso, limbs]
```

**3. Добавьте дополнительные поля**
```
damage_type (ENUM) - тип урона [physical, fire, ice, poison]
knockback_force (FLOAT) - сила отталкивания [0.0-10.0]
is_critical (BOOL) - критический удар [true/false]
hit_effects (ARRAY) - эффекты ["blood", "sparks", "screen_shake"]
```

#### Создание ENUM полей

**Рекомендации по ENUM значениям:**
```
✅ Хорошо: "sword", "axe", "mace", "dagger"
❌ Плохо: "wpn_01", "weapon1", "SWORD"

✅ Хорошо: "head", "torso", "left_arm", "right_leg"
❌ Плохо: "1", "target_a", "HitLoc_Head"

✅ Хорошо: "fire", "ice", "lightning", "poison"
❌ Плохо: "dmg_fire", "FIRE_DAMAGE", "burn"
```

**Пример настройки ENUM поля:**
```
Field Name: surface_type
Type: Enum
Description: Type of surface for footstep sounds
Enum Options: grass,dirt,stone,wood,metal,water,sand,snow,mud,gravel
Default Value: grass
```

#### Цветовая схема шаблонов

```python
# Рекомендуемые цвета для категорий
COMBAT_RED = [1.0, 0.2, 0.2]      # Боевые действия
AUDIO_BLUE = [0.2, 0.6, 1.0]      # Звуковые эффекты
MAGIC_PURPLE = [0.8, 0.3, 0.8]    # Магические заклинания
MOVEMENT_YELLOW = [1.0, 0.8, 0.2] # Движение персонажа
PICKUP_GOLD = [1.0, 1.0, 0.2]     # Подбор предметов
UI_CYAN = [0.2, 0.8, 0.8]         # Интерфейс
ENV_GREEN = [0.4, 0.7, 0.4]       # Окружение
NEUTRAL_GRAY = [0.5, 0.5, 0.5]    # Общие события
```

### Экспорт и импорт данных

#### Форматы файлов

**Палетка шаблонов** (`event_palette.json`)
```json
{
  "templates": [
    {
      "name": "Weapon_Hit",
      "description": "Weapon hit with damage calculation",
      "color": [1.0, 0.2, 0.2],
      "custom_fields": [
        {
          "name": "weapon_type",
          "type": "ENUM",
          "description": "Type of weapon used",
          "default_value": "sword",
          "enum_options": ["sword", "axe", "mace", "dagger"]
        },
        {
          "name": "damage",
          "type": "INT",
          "description": "Base damage amount",
          "default_value": 100
        }
      ]
    }
  ]
}
```

**События таймлайна** (`timeline_events.json`)
```json
{
  "events": [
    {
      "template_name": "Weapon_Hit",
      "frame": 25,
      "time": 1.041,
      "field_values": {
        "weapon_type": "sword",
        "damage": 150,
        "hit_location": "torso",
        "is_critical": false
      }
    }
  ]
}
```

#### Стратегии версионирования

**Вариант 1: Семантическое версионирование палеток**
```json
{
  "version": "1.2.0",
  "compatibility": "blender_3.0+",
  "templates": [...]
}
```

**Вариант 2: Хеширование для контроля изменений**
```python
import hashlib
palette_hash = hashlib.md5(json.dumps(palette_data).encode()).hexdigest()
```

**Вариант 3: Временные метки**
```json
{
  "created": "2024-01-15T10:30:00Z",
  "modified": "2024-01-20T15:45:00Z",
  "templates": [...]
}
```

### Интеграция с игровыми движками

#### Unity Integration

**C# структуры данных:**
```csharp
[System.Serializable]
public class AnimationEvent
{
    public string template_name;
    public float time;
    public Dictionary<string, object> field_values;

    public T GetFieldValue<T>(string fieldName, T defaultValue = default)
    {
        if (field_values.TryGetValue(fieldName, out var value))
        {
            return (T)Convert.ChangeType(value, typeof(T));
        }
        return defaultValue;
    }
}

[System.Serializable]
public class EventTimeline
{
    public List<AnimationEvent> events;

    public IEnumerable<AnimationEvent> GetEventsAtTime(float time, float tolerance = 0.1f)
    {
        return events.Where(e => Mathf.Abs(e.time - time) <= tolerance);
    }
}
```

**Обработка ENUM значений в Unity:**
```csharp
public enum WeaponType { Sword, Axe, Mace, Dagger }
public enum AttackType { Slash, Stab, Crush, Pierce }

public void ProcessCombatEvent(AnimationEvent evt)
{
    var weaponType = Enum.Parse<WeaponType>(
        evt.GetFieldValue<string>("weapon_type"), true);
    var attackType = Enum.Parse<AttackType>(
        evt.GetFieldValue<string>("attack_type"), true);
    var damage = evt.GetFieldValue<int>("damage", 100);

    // Обработка события...
}
```

#### Unreal Engine Integration

**Blueprint структуры:**
```cpp
USTRUCT(BlueprintType)
struct FAnimationEvent
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly)
    FString TemplateName;

    UPROPERTY(BlueprintReadOnly)
    float Time;

    UPROPERTY(BlueprintReadOnly)
    TMap<FString, FString> FieldValues;

    template<typename T>
    T GetFieldValue(const FString& FieldName, T DefaultValue) const;
};

UCLASS(BlueprintType)
class UEventProcessor : public UObject
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable)
    void ProcessWeaponHitEvent(const FAnimationEvent& Event);

    UFUNCTION(BlueprintCallable)
    void ProcessSpellCastEvent(const FAnimationEvent& Event);
};
```

#### Godot Integration

**GDScript обработка:**
```gdscript
extends Node
class_name EventProcessor

enum WeaponType { SWORD, AXE, MACE, DAGGER }
enum AttackType { SLASH, STAB, CRUSH, PIERCE }

func process_animation_event(event_data: Dictionary):
    var template_name = event_data.get("template_name", "")

    match template_name:
        "Weapon_Hit":
            process_weapon_hit(event_data)
        "Spell_Cast":
            process_spell_cast(event_data)
        "Audio_SFX":
            process_audio_sfx(event_data)

func process_weapon_hit(event_data: Dictionary):
    var field_values = event_data.get("field_values", {})

    var weapon_type = get_enum_value(WeaponType, field_values.get("weapon_type", "sword"))
    var attack_type = get_enum_value(AttackType, field_values.get("attack_type", "slash"))
    var damage = field_values.get("damage", 100)

    # Обработка удара...

func get_enum_value(enum_class, string_value: String):
    return enum_class.get(string_value.to_upper(), 0)
```

### Оптимизация производительности

#### Минимизация размера файлов

**Техника 1: Сжатие ENUM значений**
```python
# Вместо полных строк используйте сокращения
WEAPON_CODES = {
    "s": "sword", "a": "axe", "m": "mace", "d": "dagger"
}

SURFACE_CODES = {
    "g": "grass", "d": "dirt", "s": "stone", "w": "wood"
}
```

**Техника 2: Объединение повторяющихся событий**
```json
{
  "events": [
    {
      "template_name": "Footstep",
      "frames": [10, 25, 40, 55],
      "field_values": {
        "surface_type": "stone",
        "movement_type": "walk"
      }
    }
  ]
}
```

#### Кеширование для больших проектов

**Python скрипт для предварительной обработки:**
```python
import json
from typing import Dict, List, Any

class EventCache:
    def __init__(self):
        self.templates: Dict[str, Any] = {}
        self.events_by_frame: Dict[int, List[Any]] = {}
        self.events_by_template: Dict[str, List[Any]] = {}

    def load_timeline(self, filepath: str):
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Индексирование для быстрого поиска
        for event in data.get('events', []):
            frame = event['frame']
            template = event['template_name']

            if frame not in self.events_by_frame:
                self.events_by_frame[frame] = []
            self.events_by_frame[frame].append(event)

            if template not in self.events_by_template:
                self.events_by_template[template] = []
            self.events_by_template[template].append(event)

    def get_events_at_frame(self, frame: int) -> List[Any]:
        return self.events_by_frame.get(frame, [])

    def get_events_by_template(self, template_name: str) -> List[Any]:
        return self.events_by_template.get(template_name, [])
```

#### Расширенные возможности

#### Пользовательские валидаторы полей

```python
# Добавление в EventField класс
validation_rules: StringProperty(
    name="Validation Rules",
    default="",
    description="JSON string with validation rules"
)

# Пример правил валидации
validation_examples = {
    "damage": {
        "min": 1,
        "max": 1000,
        "step": 5
    },
    "volume": {
        "min": 0.0,
        "max": 2.0,
        "precision": 2
    },
    "weapon_type": {
        "allowed": ["sword", "axe", "mace"],
        "case_sensitive": false
    }
}
```

#### Условная логика в шаблонах

```python
# Поля которые показываются только при определенных условиях
conditional_fields = {
    "spell_components": {
        "show_when": {
            "spell_school": ["conjuration", "transmutation"],
            "spell_level": ["level_3", "level_4", "level_5"]
        }
    },
    "ammo_count": {
        "show_when": {
            "weapon_type": ["bow", "crossbow"]
        }
    }
}
```

#### Автоматическая генерация документации

```python
def generate_template_docs(events_system):
    """Генерация документации по шаблонам"""

    docs = {
        "templates": [],
        "generated": datetime.now().isoformat(),
        "total_templates": len(events_system.event_templates)
    }

    for template in events_system.event_templates:
        template_doc = {
            "name": template.name,
            "description": template.description,
            "color": list(template.color),
            "fields": []
        }

        for field in template.custom_fields:
            field_doc = {
                "name": field.name,
                "type": field.field_type,
                "description": field.description,
                "required": True,  # Можно добавить логику
                "default_value": get_default_value(field)
            }

            if field.field_type == 'ENUM':
                field_doc["options"] = field.enum_options.split(',')
                field_doc["total_options"] = len(field_doc["options"])

            template_doc["fields"].append(field_doc)

        docs["templates"].append(template_doc)

    return docs
```

### Лучшие практики разработки

#### Соглашения по именованию

**Шаблоны событий:**
```
✅ Хорошо: "Combat_WeaponHit", "Audio_Footstep", "Magic_SpellCast"
❌ Плохо: "event1", "hit", "sound_thing"
```

**Поля:**
```
✅ Хорошо: "weapon_type", "damage_amount", "spell_element"
❌ Плохо: "wpnType", "dmg", "elem"
```

**ENUM значения:**
```
✅ Хорошо: "fire", "ice", "lightning", "poison"
❌ Плохо: "Fire", "ICE", "Lightning_Element", "psn"
```

#### Тестирование и отладка

**Скрипт валидации палетки:**
```python
def validate_palette(filepath: str) -> List[str]:
    """Проверка палетки на ошибки"""

    errors = []

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {str(e)}"]

    if "templates" not in data:
        errors.append("Missing 'templates' section")
        return errors

    for i, template in enumerate(data["templates"]):
        # Проверка обязательных полей шаблона
        if "name" not in template:
            errors.append(f"Template {i}: missing 'name'")

        if "custom_fields" not in template:
            errors.append(f"Template {i}: missing 'custom_fields'")
            continue

        # Проверка полей
        for j, field in enumerate(template["custom_fields"]):
            if "name" not in field:
                errors.append(f"Template {i}, field {j}: missing 'name'")

            if "type" not in field:
                errors.append(f"Template {i}, field {j}: missing 'type'")

            if field.get("type") == "ENUM":
                if "enum_options" not in field:
                    errors.append(f"Template {i}, field {j}: ENUM missing 'enum_options'")
                elif not field["enum_options"]:
                    errors.append(f"Template {i}, field {j}: ENUM has empty 'enum_options'")

    return errors
```

**Автоматическое тестирование экспорта/импорта:**
```python
def test_export_import_cycle():
    """Тест полного цикла экспорт → импорт"""

    # 1. Создать тестовые данные
    # 2. Экспортировать
    # 3. Очистить сцену
    # 4. Импортировать
    # 5. Сравнить результаты

    original_events = get_current_events()
    export_events("/tmp/test_export.json")
    clear_all_events()
    import_events("/tmp/test_export.json")
    imported_events = get_current_events()

    assert compare_events(original_events, imported_events), "Export/Import cycle failed"
```

#### Контроль версий и совместная работа

**Git hooks для валидации палеток:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Проверка всех .json файлов палеток
for file in *.json; do
    if [[ $file == *"palette"* ]]; then
        python validate_palette.py "$file"
        if [ $? -ne 0 ]; then
            echo "❌ Palette validation failed: $file"
            exit 1
        fi
    fi
done

echo "✅ All palettes validated successfully"
```

**Автоматическая генерация changelog:**
```python
def generate_changelog(old_palette_path: str, new_palette_path: str) -> str:
    """Генерация changelog между версиями палеток"""

    with open(old_palette_path) as f:
        old_data = json.load(f)
    with open(new_palette_path) as f:
        new_data = json.load(f)

    old_templates = {t["name"]: t for t in old_data["templates"]}
    new_templates = {t["name"]: t for t in new_data["templates"]}

    changelog = []

    # Новые шаблоны
    for name in new_templates:
        if name not in old_templates:
            changelog.append(f"➕ Added template: {name}")

    # Удаленные шаблоны
    for name in old_templates:
        if name not in new_templates:
            changelog.append(f"➖ Removed template: {name}")

    # Измененные шаблоны
    for name in old_templates:
        if name in new_templates:
            old_fields = {f["name"]: f for f in old_templates[name].get("custom_fields", [])}
            new_fields = {f["name"]: f for f in new_templates[name].get("custom_fields", [])}

            for field_name in new_fields:
                if field_name not in old_fields:
                    changelog.append(f"🔧 {name}: Added field '{field_name}'")
                elif old_fields[field_name] != new_fields[field_name]:
                    changelog.append(f"🔧 {name}: Modified field '{field_name}'")

    return "\n".join(changelog)
```

### Заключение

Эта система событий анимации предоставляет полный контроль над интеграцией анимаций с игровой логикой. Следуя описанным принципам и практикам, вы сможете создать эффективный workflow для любого игрового проекта.

Для получения поддержки или предложения улучшений создавайте Issues в репозитории проекта.
