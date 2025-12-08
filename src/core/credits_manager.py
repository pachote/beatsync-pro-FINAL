"""
Demo Credits System for BeatSync Pro
FIXED: Added the missing 'deduct_credits' method.
"""

class CreditsManager:
    """Manages the user's credit balance in demo mode."""
    def __init__(self):
        self.balance = 100
        print(f"[CreditsManager] Initialized with {self.balance} credits (Demo Mode)")

    def get_balance(self):
        """Returns the current credit balance."""
        return self.balance

    def deduct_credits(self, amount):
        """Deducts credits if the balance is sufficient."""
        if self.balance >= amount:
            self.balance -= amount
            print(f"[CreditsManager] Deducted {amount} credits. New balance: {self.balance}")
            return True
        print(f"[CreditsManager] Credit deduction failed. Insufficient balance.")
        return False