import json
import os

CONFIG_PATH = "./mods/configs/ImmersiveBattlefield/config.json"

class ModSettings(object):
    def __init__(self):
        self.config = {}
        self.load()

    def load(self):
        if not os.path.exists(CONFIG_PATH):
            print("[ModSettings] Config not found, using defaults.")
            self.defaults()
            return

        try:
            with open(CONFIG_PATH, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print("[ModSettings] Error loading config: %s" % str(e))
            self.defaults()

    def defaults(self):
        self.config = {
            "interactionLevel": "interactive",
            "soldierDensity": "medium",
            "maxSoldiers": 20,
            "enableExplosions": True,
            "performanceMode": "balanced"
        }
        self.save()

    def save(self):
        try:
            config_dir = os.path.dirname(CONFIG_PATH)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            with open(CONFIG_PATH, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print("[ModSettings] Error saving config: %s" % str(e))

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()
