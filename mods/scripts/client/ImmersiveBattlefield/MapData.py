# Mapping of system map names (geometry names) to configuration presets
MAP_PRESETS = {
    '01_karelia': 'soviet_summer',
    '02_malinovka': 'soviet_summer',
    '04_himmelsdorf': 'german_urban',
    '05_prohorovka': 'soviet_summer',
    '07_lakeville': 'us_summer',
    '08_ruinberg': 'german_urban',
    '10_hills': 'soviet_summer', # Mines
    '13_erlenberg': 'german_winter',
    '18_cliff': 'brit_summer',
}

# Define what each preset implies (models, behaviors)
PRESET_CONFIGS = {
    'soviet_summer': {
        'nation': 'ussr',
        'voice_language': 'ru',
        'models': ['ussr_soldier_01.model', 'ussr_officer.model']
    },
    'german_urban': {
        'nation': 'germany',
        'voice_language': 'de',
        'models': ['ger_soldier_01.model', 'ger_soldier_mg.model']
    },
    'german_winter': {
        'nation': 'germany',
        'voice_language': 'de',
        'models': ['ger_winter_01.model']
    },
    'us_summer': {
        'nation': 'usa',
        'voice_language': 'en',
        'models': ['usa_paratrooper.model']
    },
    'brit_summer': {
        'nation': 'uk',
        'voice_language': 'en',
        'models': ['uk_soldier_01.model']
    },
    'test_cube': {
        'nation': 'debug',
        'voice_language': 'en',
        'models': ['cube.model']
    },
    'default': {
        'nation': 'unknown',
        'voice_language': 'en',
        'models': ['default_soldier.model']
    }
}

def get_map_config(map_name):
    """Returns the configuration dict for a given map name."""
    # For testing, we can force the test_cube preset if needed
    if map_name == 'debug_zone':
        return PRESET_CONFIGS['test_cube']
        
    preset_key = MAP_PRESETS.get(map_name, 'default')
    # fallback to use test_cube if model files are missing? 
    # For now, just return standard logic.
    return PRESET_CONFIGS.get(preset_key, PRESET_CONFIGS['default'])
