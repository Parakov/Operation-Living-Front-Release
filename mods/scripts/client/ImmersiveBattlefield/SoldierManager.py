import BigWorld
import Math
import random
import time
from ImmersiveBattlefield import MapData
from ImmersiveBattlefield.SoldierAI import SoldierAI

class SoldierManager(object):
    def __init__(self, config):
        self.config = config
        self.soldiers = [] # List of SoldierAI instances
        self.max_soldiers = config.get('maxSoldiers', 20)
        self.current_map_config = None
        self.model_pool = []
        self.next_id = 1
        print("[ImmersiveBattlefield] SoldierManager initialized. Max soldiers: %d" % self.max_soldiers)

    def on_enter_map(self, map_name):
        """Called when entering a map to load appropriate resources."""
        self.current_map_config = MapData.get_map_config(map_name)
        self.model_pool = self.current_map_config.get('models', [])
        print("[ImmersiveBattlefield] Entering map '%s'. Selected preset (Nation: %s)" % 
              (map_name, self.current_map_config.get('nation')))
        
        # Test Spawning
        self.spawn_test_squad()

    def update(self, dt):
        """Called every frame/tick to update soldier logic."""
        current_time = time.time()
        for soldier in self.soldiers:
            soldier.update(current_time)

    def spawn_soldier(self, position):
        if len(self.soldiers) >= self.max_soldiers:
            return None

        if not self.model_pool:
            return None
        
        # Pick a random model (e.g. cube.model for testing)
        model_name = random.choice(self.model_pool)

        # Create AI Instance
        soldier = SoldierAI(self.next_id, position)
        
        # Assign the model to the AI (metadata only for now)
        soldier.model_name = model_name
        
        self.soldiers.append(soldier)
        self.next_id += 1
        
        print("[ImmersiveBattlefield] Spawned Soldier-%d (%s) at %s" % (soldier.entity_id, model_name, str(position)))
        return soldier

    def spawn_test_squad(self):
        """Spawns a few soldiers around the player's potential position."""
        # Assuming player is at (0,0,0) for this blind test, or use random area
        print("[ImmersiveBattlefield] Spawning Test Squad (Cube Prototypes)...")
        center_x, center_z = 0, 0
        
        for i in range(5):
            # Spawn in a circle
            angle = (i / 5.0) * 6.28
            radius = 10.0
            x = center_x + Math.sin(angle) * radius
            z = center_z + Math.cos(angle) * radius
            # Y is usually terrain height, defaulting to 100 for safety or 0 if flat
            self.spawn_soldier((x, 0, z))


    # Global Event Handlers
    def handle_explosion(self, position, radius):
        """Called when an explosion occurs."""
        print("[ImmersiveBattlefield] Explosion at %s" % str(position))
        for soldier in self.soldiers:
             # In real impl, check distance
             soldier.on_explosion_nearby()

    def handle_gunfire(self, attacker_id, position):
        """Called when a tank fires."""
        print("[ImmersiveBattlefield] Gunfire detected from %s" % str(attacker_id))
        for soldier in self.soldiers:
            soldier.on_tank_shot_nearby()

    def clear_all(self):
        print("[ImmersiveBattlefield] Clearing all soldiers...")
        self.soldiers = []
