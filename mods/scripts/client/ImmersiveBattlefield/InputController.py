import BigWorld
import Keys
from ImmersiveBattlefield import ModLogger

class InputController(object):
    def __init__(self, settings, soldier_manager):
        self.settings = settings
        self.soldier_manager = soldier_manager
        self.enabled = True
        print("[InputController] Initialized.")

    def handle_key_event(self, event):
        """Called by the main mod loop on key press."""
        if not event.isKeyDown() or event.isRepeatedEvent():
            return

        key = event.key
        
        # Toggle RP / Interactive Mode (F9)
        if key == Keys.KEY_F9:
            self.toggle_interaction_mode()
            
        # Increase Soldier Count (Numpad +)
        elif key == Keys.KEY_ADD or key == Keys.KEY_NUMPADPLUS:
            self.adjust_soldier_count(5)
            
        # Decrease Soldier Count (Numpad -)
        elif key == Keys.KEY_MINUS or key == Keys.KEY_NUMPADMINUS:
            self.adjust_soldier_count(-5)
            
        # Spawn Test Squad (F10) - Debug
        elif key == Keys.KEY_F10:
            self.soldier_manager.spawn_test_squad()

    def toggle_interaction_mode(self):
        current = self.settings.get('interactionLevel')
        new_mode = "visual" if current == "interactive" else "interactive"
        self.settings.set('interactionLevel', new_mode)
        
        # Notify user (Console/Screen)
        msg = "ImmersiveBattlefield: Interaction Mode set to %s" % new_mode.upper()
        print(msg)
        self.show_screen_message(msg)

    def adjust_soldier_count(self, amount):
        current = self.settings.get('maxSoldiers', 20)
        new_count = max(0, min(100, current + amount))
        self.settings.set('maxSoldiers', new_count)
        self.soldier_manager.max_soldiers = new_count
        
        msg = "ImmersiveBattlefield: Max Soldiers set to %d" % new_count
        print(msg)
        self.show_screen_message(msg)

    def show_screen_message(self, message):
        """Displays a message on the player's screen."""
        try:
            import GUI
            # Simple text message via standard GUI, if available
            # This logic depends highly on WoT version, falling back to print if fails
            # BigWorld.target().gui.addMessage(message) # Pseudocode for some versions
            pass 
        except:
            pass
        
        # Ensure it's in the python log at least
        ModLogger.log(message)
