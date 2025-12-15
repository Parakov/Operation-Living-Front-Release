import BigWorld
import ResMgr
import json
import os
import glob

# Import our package
from ImmersiveBattlefield.SoldierManager import SoldierManager
from ImmersiveBattlefield.ModSettings import ModSettings
from ImmersiveBattlefield.InputController import InputController
import Keys

# Mod Constants
MOD_NAME = "ImmersiveBattlefield"

class ModLogger:
    @staticmethod
    def log(message):
        print("[%s] %s" % (MOD_NAME, message))

class ImmersiveBattlefield(object):
    def __init__(self):
        ModLogger.log("Initializing...")
        self.settings = ModSettings()
        self.soldier_manager = SoldierManager(self.settings.config)
        self.input_controller = InputController(self.settings, self.soldier_manager)

    def start(self):
        """Called when the mod is ready to start (e.g. after login)."""
        ModLogger.log("Mod started. Interaction Level: %s" % self.settings.get('interactionLevel'))
        
        # Register Input Handler
        # BigWorld.callback(0.1, self.register_input) # specific to version
        # For this prototype we assume standard python hook capability or generic InputHandler
        
        # In a real mod, we would hook PlayerAvatar.onEnterWorld.
        # Check if we can access BigWorld.player() to get the arena name.
        try:
            player = BigWorld.player()
            if player and hasattr(player, 'arena') and player.arena:
                map_name = player.arena.arenaType.geometryName
                self.soldier_manager.on_enter_map(map_name)
            else:
                # If we are somehow started before the player is ready, 
                # we might need to listen for an event.
                ModLogger.log("Waiting for PlayerAvatar...")
        except Exception:
             # Basic fallback for testing simply implies a default map
             ModLogger.log("Could not detect map (not in-game?). Using test map 'debug_zone' for simulation.")
             self.soldier_manager.on_enter_map('debug_zone')

_mod_instance = None

def init():
    """Entry point called by WoT mod loader."""
    global _mod_instance
    try:
        _mod_instance = ImmersiveBattlefield()
        _mod_instance.start()
    except Exception as e:
        print("[%s] CRITICAL ERROR IN INIT: %s" % (MOD_NAME, str(e)))

def fini():
    """Cleanup called by WoT mod loader."""
    global _mod_instance
    if _mod_instance:
        if _mod_instance.soldier_manager:
            _mod_instance.soldier_manager.clear_all()
    _mod_instance = None

def handleKeyEvent(event):
    """Global hook for key events in some WoT mod loaders."""
    if _mod_instance and _mod_instance.input_controller:
        _mod_instance.input_controller.handle_key_event(event)

