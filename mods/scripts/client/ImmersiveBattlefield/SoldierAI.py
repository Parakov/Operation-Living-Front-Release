import BigWorld
import Math
import random
import time

class AIState:
    IDLE = 0
    ALERT = 1
    COMBAT = 2
    TAKE_COVER = 3
    RETREAT = 4
    DEAD = 5

class ThreatType:
    NONE = 0
    TANK = 1
    EXPLOSION = 2
    SHOT = 3

class SoldierAI(object):
    def __init__(self, entity_id, position):
        self.entity_id = entity_id
        self.position = position
        self.state = AIState.IDLE
        self.last_state_change = time.time()
        self.target_id = None
        self.health = 100
        
        # Perception Config
        self.vision_radius = 40.0
        self.hearing_radius = 60.0
        self.danger_radius = 20.0
        
        # Timers
        self.next_tick = 0
        self.tick_interval = 0.2 + random.random() * 0.3 # Randomize tick to prevent spikes
        self.cover_timer = 0
        
        print("[SoldierAI-%d] Initialized at %s" % (self.entity_id, str(self.position)))

    def update(self, current_time):
        """Called by Manager every frame, but we throttle logic execution."""
        if current_time < self.next_tick:
            return
            
        self.next_tick = current_time + self.tick_interval
        
        if self.state == AIState.DEAD:
            return

        threat = self.sense_threats()
        self.handle_state_logic(threat)

    def change_state(self, new_state):
        if self.state == new_state:
            return
            
        print("[SoldierAI-%d] State Change: %s -> %s" % (self.entity_id, self.get_state_name(self.state), self.get_state_name(new_state)))
        self.state = new_state
        self.last_state_change = time.time()
        
        # Trigger entry actions
        if new_state == AIState.ALERT:
            self.play_animation("weapon_up")
        elif new_state == AIState.COMBAT:
            self.play_animation("combat_idle")
        elif new_state == AIState.TAKE_COVER:
            self.play_animation("crouch_hide")
        elif new_state == AIState.RETREAT:
            self.play_animation("run_panic")

    def sense_threats(self):
        """
        Scans BigWorld entities to find threats (Vehicles).
        """
        # Debug: Log what we see occasionally (not every tick to avoid spam)
        # We use a simple counter or timer in real app, but for now we'll just check if we have a target
        
        threat = None
        min_dist = self.vision_radius
        
        # Iterate over all entities in the game client
        for eid, entity in BigWorld.entities.items():
            if eid == self.entity_id:
                continue

            # Calculate distance
            try:
                # Entities usually have .position (Math.Vector3)
                dist = (entity.position - self.position).length
            except Exception:
                continue
                
            if dist > self.vision_radius:
                continue

            # Identify Entity Type
            # We look for 'Vehicle' in the class name or type
            class_name = entity.__class__.__name__
            
            # LOGGING FOR DEBUGGING
            # Print everything close by so we know what 'Tanks' are called
            # print(f"[SoldierAI-{self.entity_id}] Saw {class_name} (ID: {eid}) at {dist:.1f}m")

            if 'Vehicle' in class_name or 'Avatar' in class_name:
                # It's a tank!
                if dist < min_dist:
                    min_dist = dist
                    threat = {
                        'type': ThreatType.TANK,
                        'entity': entity,
                        'dist': dist,
                        'is_heavy': 'heavy' in class_name.lower(), # Guessing
                        'close_proximity': dist < self.danger_radius
                    }
                    print(f"[SoldierAI-{self.entity_id}] THREAT DETECTED: {class_name} at {dist:.1f}m")

        return threat

    def handle_state_logic(self, threat):
        current_time = time.time()
        
        if self.state == AIState.IDLE:
            if threat:
                self.change_state(AIState.ALERT)
            else:
                # Random ambient behavior
                if random.random() < 0.05:
                    self.play_animation("look_around")

        elif self.state == AIState.ALERT:
            if not threat:
                # Cooldown to idle
                if current_time - self.last_state_change > 5.0:
                    self.change_state(AIState.IDLE)
            elif threat['type'] == ThreatType.TANK:
                self.change_state(AIState.COMBAT)
            elif threat['type'] == ThreatType.EXPLOSION:
                self.change_state(AIState.TAKE_COVER)

        elif self.state == AIState.COMBAT:
            self.fire_fake_weapon()
            
            if threat and threat.get('close_proximity', False):
                 self.change_state(AIState.RETREAT)
            elif threat and threat.get('is_heavy', False):
                 self.change_state(AIState.TAKE_COVER)
            elif not threat:
                self.change_state(AIState.ALERT)

        elif self.state == AIState.TAKE_COVER:
            # Check safety
            if current_time - self.last_state_change > 3.0:
                 # Peak out
                 self.change_state(AIState.COMBAT) # Or Alert

        elif self.state == AIState.RETREAT:
            # Run away logic
            pass

    def fire_fake_weapon(self):
        # Visuals only
        # print("Pew pew")
        pass

    def play_animation(self, anim_name):
        # Mock animation trigger
        # print("[SoldierAI-%d] Playing anim: %s" % (self.entity_id, anim_name))
        pass

    def get_state_name(self, state_id):
        names = ["IDLE", "ALERT", "COMBAT", "TAKE_COVER", "RETREAT", "DEAD"]
        return names[state_id] if 0 <= state_id < len(names) else "UNKNOWN"

    # External Event Triggers
    def on_explosion_nearby(self):
        print("[SoldierAI-%d] Event: Explosion Nearby!" % self.entity_id)
        threat = {'type': ThreatType.EXPLOSION}
        self.handle_state_logic(threat)

    def on_tank_shot_nearby(self):
        print("[SoldierAI-%d] Event: Tank Shot Nearby!" % self.entity_id)
        if self.state in [AIState.IDLE, AIState.ALERT]:
             self.change_state(AIState.TAKE_COVER)

