# brain.py
# Contains the main Brain class that integrates all components.

import the_forebrain
import the_midbrain
import the_hindbrain

class Brain:
    def __init__(self):
        print("[Brain] Initializing all components...")
        self.is_running = True
        
        # 1. Initialize Forebrain (The Thinker)
        self.memory = forebrain.Hippocampus()
        # mongo DB or other vector DB could be integrated here
        self.cortex = forebrain.Cortex(memory_system=self.memory)
        # frontal_lobe  as decision_maker(the magi system),problem_solver(gemini),motor_cortex(conditional),speech_recognition(cv2),personality(gpt),impulse_control(it wont have impulses).
        # parietal_lobe as sensory_integration(two basic sences),spatial_awareness(visual_sences andd depth perception).
        # temporal_lobe as auditory_processing(speech recognition(pyaudio)),language_comprehension(gpt),memory_storage(hippocampus).
        # occipital_lobe as visual_processing(cv2),image_recognition(cv2).

        self.decision_maker = forebrain.DecisionMaker()
        # Could intigrate the magi system here for complex decision making

        # 2. Initialize Midbrain (The Sensor & Router)
        self.vision = midbrain.VisionSensor()
        # oif available, integrate cv2 for visual input
        self.audio = midbrain.AudioSensor()
        # integrate pyaudio for audio input if available
        self.attention = midbrain.AttentionGate()
        # integrate RAS logic here for attention filtering - Sensory Filtering: RAS filters incoming sensory data, allowing the brain to focus on relevant stimuli while ignoring distractions.

        """| Function                   | Description                                                                                                                                                                         |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Arousal & Wakefulness**  | The RAS acts as your brain’s “on/off switch.” It keeps the cerebral cortex alert and ready to process information. Damage here can cause deep sleep or even coma.                   |
| **Attention & Focus**      | It filters the massive amount of sensory information coming into your brain, deciding what’s important (e.g., you can tune out background noise but notice your name being called). |
| **Sleep–Wake Cycle**       | The RAS helps regulate transitions between sleep and wakefulness by interacting with other brain areas (like the hypothalamus).                                                     |
| **Muscle Tone & Reflexes** | It also helps maintain muscle tone and posture through its connections with motor neurons.                                                                                          |
"""


        # 3. Initialize Hindbrain (The Executor & Manager)
        self.motor_tuner = hindbrain.Cerebellum()
# Could integrate fine motor control logic here - The cerebellum fine-tunes motor commands from the motor cortex, ensuring smooth, coordinated movements. It also plays a role in motor learning and balance.
        self.vitals = hindbrain.AutonomicMonitor()
# Could integrate system health monitoring logic here - The medulla oblongata and pons manage autonomic functions like heart rate, breathing, and digestion, keeping the body’s vital systems running smoothly.
        
        print("[Brain] All components online. Brain is running.")












        

    def main_processing_loop(self):
        """
        This is the main "heartbeat" of the brain, running continuously.
        It follows the SENSE -> FILTER -> REFLEX/THINK -> ACT -> LIVE cycle.
        """
        
        # 1. SENSE (Midbrain)
        vision_input = self.vision.scan()
        audio_input = self.audio.listen()
        
        # 2. FILTER (Midbrain)
        # Attention gate decides what's important and if a reflex is needed
        stimulus, reflex_action = self.attention.filter(vision_input, audio_input)

        # 3. REFLEX (Midbrain -> Hindbrain)
        if reflex_action:
            print(f"[REFLEX] {reflex_action}")
            self.motor_tuner.execute_reflex(reflex_action)
            return  # Skip cognitive loop for this tick

        # 4. PERCEIVE & THINK (Forebrain)
        if stimulus:
            print(f"[COGNITION] Processing new stimulus...")
            
            # Cortex (LLM) processes the stimulus, using memory
            thought = self.cortex.process_stimulus(stimulus)
            
            # DecisionMaker (RL) decides what to do
            goal = self.decision_maker.choose_goal(thought)
            
            # Cortex (LLM) generates a high-level plan
            high_level_plan = self.cortex.generate_plan(goal)

            # 5. ACT (Hindbrain)
            if high_level_plan:
                print(f"[ACTION] Executing: {high_level_plan}")
                self.motor_tuner.execute_plan(high_level_plan)

        # 6. LIVE (Hindbrain)
        # Autonomic functions run in the background
        self.vitals.check_system_status()
        if self.vitals.needs_shutdown():
            self.shutdown()

    def shutdown(self):
        print("[Brain] Initiating shutdown procedure...")
        self.is_running = False
        # Add any cleanup logic here (e.g., save memory)
        self.memory.save_to_disk()























# forebrain.py
# Contains components for higher-order cognition.

class Hippocampus:
    """Simulates long-term memory (a vector database)."""
    def __init__(self):
        self.memory_vectors = {}
        print("[Forebrain] Hippocampus (Memory) initialized.")
        
    def store(self, thought, vector):
        """Stores a new memory."""
        print(f"[Memory] Storing: {thought[:20]}...")
        self.memory_vectors[thought] = vector
        
    def recall(self, query_vector):
        """Recalls relevant memories."""
        print(f"[Memory] Recalling based on query...")
        # In a real system, this would be a K-NN or ANN search
        if not self.memory_vectors:
            return None
        return "A relevant past memory."

    def save_to_disk(self):
        print("[Memory] Saving memories to disk...")
        # Logic to save self.memory_vectors

class Cortex:
    """Simulates the Cerebrum/Cortex (an LLM)."""
    def __init__(self, memory_system):
        self.memory = memory_system
        print("[Forebrain] Cortex (LLM) initialized.")
        
    def process_stimulus(self, stimulus):
        """Analyzes a stimulus using context from memory."""
        context = self.memory.recall(stimulus)
        print(f"[Cortex] Thinking about {stimulus} with context: {context}")
        # --- API CALL TO LLM ---
        # thought = llm.generate(f"Stimulus: {stimulus}, Context: {context}")
        thought = f"Analyzed thought about {stimulus}"
        
        # Store the new thought as a memory
        self.memory.store(thought, f"vector_for_{thought}")
        return thought
        
    def generate_plan(self, goal):
        """Generates a high-level plan to achieve a goal."""
        print(f"[Cortex] Generating plan for goal: {goal}")
        # --- API CALL TO LLM ---
        # plan = llm.generate(f"Create a step-by-step plan for: {goal}")
        plan = f"Plan for {goal}"
        return plan

class DecisionMaker:
    """Simulates the Prefrontal Cortex (an RL Agent)."""
    def __init__(self):
        print("[Forebrain] DecisionMaker (RL Agent) initialized.")
        
    def choose_goal(self, thought):
        """Uses a policy to select the best goal."""
        print(f"[DecisionMaker] Choosing goal based on: {thought}")
        # --- RL MODEL LOGIC ---
        # state = self.process_thought(thought)
        # goal = self.rl_policy(state)
        goal = "A chosen goal"
        return goal



































   # midbrain.py
# Contains components for sensory input and attention.

class VisionSensor:
    """Simulates the eyes and visual cortex."""
    def __init__(self):
        print("[Midbrain] VisionSensor initialized.")
            
    def scan(self):
        """Scans the environment. Placeholder."""
        # In a real app, this could be a camera feed.
        return None # "image_data_placeholder"
        
class AudioSensor:
    """Simulates the ears and auditory cortex."""
    def __init__(self):
        print("[Midbrain] AudioSensor initialized.")
        
    def listen(self):
        """Listens to the environment. Placeholder."""
        # In a real app, this could be a microphone stream.
        # For a chatbot, this is where we'd get user input.
        print("[AudioSensor] Listening...")
        # Simple simulation:
        # return input("USER: ")
        return None # "user_speech_placeholder"

class AttentionGate:
    """Simulates the reticular activating system (RAS)."""
    def __init__(self):
        print("[Midbrain] AttentionGate (RAS) initialized.")
        self.name_trigger = "gemini" # Example trigger
        
    def filter(self, vision_input, audio_input):
        """
        Decides what's important.
        Returns (stimulus, reflex_action)
        """
        # 1. Check for reflex-level triggers
        if vision_input == "fast_moving_object":
            return (None, "FLINCH")
        if audio_input == "loud_bang":
            return (None, "STARTLE")
            
        # 2. Check for important stimuli to pass to forebrain
        if audio_input and (self.name_trigger in audio_input.lower()):
            print("[Attention] Detected trigger word!")
            return (audio_input, None)
            
        if vision_input:
            # Simple logic: always pass visual info if it exists
            return (vision_input, None)

        # 3. If nothing important, return None
        return (None, None)  













































        # hindbrain.py
# Contains components for autonomic functions and motor control.

class Cerebellum:
    """Simulates the cerebellum (fine motor control)."""
    def __init__(self):
        print("[Hindbrain] Cerebellum (MotorTuner) initialized.")
        
    def execute_plan(self, high_level_plan):
        """Converts a high-level plan into fine motor actions."""
        print(f"[Cerebellum] Executing plan: {high_level_plan}")
        # In a real app, this would send commands to actuators,
        # or type text to a screen.
        # for step in plan.steps:
        #    self.execute_micro_action(step)
        pass

    def execute_reflex(self, reflex_action):
        """Executes an immediate, pre-programmed reflex."""
        print(f"[Cerebellum] EXECUTING REFLEX: {reflex_action}!")
        # e.g., self.motor_controller.flinch()
        pass

class AutonomicMonitor:
    """Simulates the medulla/pons (autonomic functions)."""
    def __init__(self):
        self.cpu_load = 0
        self.memory_usage = 0
        self.shutdown_threshold = 95 # e.g., 95% CPU
        print("[Hindbrain] AutonomicMonitor (Vitals) initialized.")

    def check_system_status(self):
        """Monitors system health."""
        # Placeholder for real system checks
        # self.cpu_load = psutil.cpu_percent()
        # self.memory_usage = psutil.virtual_memory().percent
        
        # Simulating a check
        self.cpu_load = 0 # (self.cpu_load + 1) % 100
        
        if self.cpu_load > self.shutdown_threshold:
            print(f"[Vitals] CRITICAL: CPU load at {self.cpu_load}%")
            return True # Signals a need to shut down
        
        # print(f"[Vitals] System OK (CPU: {self.cpu_load}%)")
        return False
        
    def needs_shutdown(self):
        """Public method to check if a shutdown is needed."""
        return self.check_system_status()   








































# main.py
# This is the "brainstem" - the entry point that initializes 
# and runs the entire brain.

import time
from brain import Brain

# ==========================================================
# The "Brainstem" - This is the script's main entry point
# ==========================================================
if __name__ == "__main__":
    
    # 1. Create the single instance of our brain
    my_brain = Brain()
    
    # 2. Run the main loop
    while my_brain.is_running:
        try:
            # Call the brain's main "heartbeat"
            my_brain.main_processing_loop()
            
            # Prevent the loop from running too fast 
            # (e.g., 10 "ticks" per second)
            time.sleep(0.1) 
            
        except KeyboardInterrupt:
            print("\n[Brainstem] Manual shutdown initiated (KeyboardInterrupt).")
            my_brain.shutdown()
            
        except Exception as e:
            print(f"[FATAL ERROR in main loop] {e}")
            my_brain.shutdown()
    
    print("[Brainstem] Brain has shut down.")








































# vishu:
    # magi system for decision making. three tier system
    # gemini system for problem solving. api calls
    # cv2 for visual processing. 
    # pyaudio for audio processing.

    # rl agent for decision making. needs training time and data . can be replaced with magi system for now.

    # cortex as llm for higher order thinking(OLLAMA for planning, reasoning)
    
    # cerebellum for fine motor control. bitch is too stupid and complex 


# avi:
# databases
    # hippocampus(remembers facts and events)
    # amygdala(emotional memories)
    # Cerebral Cortex(long - term memory storage)
    
    # Prefrontal Cortex(similar to ram Short termm memory)

    # Cerebellum / Basal Ganglia(motor skills memory) out of the scope for now



"""

| Hemisphere | General Specialization                                  |
| ---------- | ------------------------------------------------------- |
| **Left**   | Logical thinking, language, math, analytical tasks      |
| **Right**  | Creativity, spatial ability, intuition, artistic skills |

"""