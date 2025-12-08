"""
Demo Grok API integration for BeatSync Pro
DEFINITIVE CORRECT VERSION
"""

class GrokBeatSyncAPI:
    """A mock API that simulates generating a detailed Edit Plan."""
    
    def __init__(self, credits_manager):
        """Initializes the API with a credits manager."""
        if credits_manager is None:
            raise ValueError("GrokBeatSyncAPI requires a valid CreditsManager instance.")
        self.credits_manager = credits_manager
        print("[GrokAPI] Initialized and connected to Credits Manager.")

    def generate_prompt(self, user_text):
        """Generates a detailed Edit Plan, deducting credits."""
        cost = 1
        if self.credits_manager.deduct_credits(cost):
            print(f"[GrokAPI] Generating Edit Plan based on: '{user_text}'")
            
            edit_plan = (
                "// AI EDIT PLAN\n"
                f"// User Concept: '{user_text}'\n"
                "//----------------------------------------------------\n\n"
                "INTRO (0:00 - 0:15):\n"
                "- Music Profile: Low energy, atmospheric pads.\n"
                "- Clip Selection: Prioritize clips tagged as 'Scenery' or 'Abstract'.\n"
                "- Editing Style: Slow, 5-second dissolves between clips.\n"
                "- Effects Preset: Apply 'Vintage Film Grain'.\n\n"
                
                "CHORUS (0:45 - 1:15):\n"
                "- Music Profile: High energy, main melody/vocal.\n"
                "- Clip Selection: Use intense clips tagged as 'Action' and 'People (Close-ups)'.\n"
                "- Editing Style: Hyper-cuts synced to every snare hit. Use 'Glitch' transitions.\n"
                "- Effects Preset: Apply 'Chromatic Aberration' and 'Lens Flare' on strong impacts."
            )
            return edit_plan
        else:
            return "Error: Insufficient credits to generate Edit Plan."