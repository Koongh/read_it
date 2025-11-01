# from algopy import ARC4Contract, String
# from algopy.arc4 import abimethod


# class ReadIt(ARC4Contract):
#     @abimethod()
#     def hello(self, name: String) -> String:
#         return "Hello, " + name


from algopy import ARC4Contract, abimethod, UInt64, String, GlobalState

class BookCompetitionWithRedeem(ARC4Contract):
    # Global states
    user_points: GlobalState[String, UInt64]     # name -> points
    user_redeem_code: GlobalState[String, String] # name -> redeem code (if earned)
    redeem_codes: GlobalState[UInt64, String]     # index -> redeem code (5 total)
    redeemed_codes: GlobalState[String, UInt64]   # code -> 1 if used, else 0

    # Initialize redeem codes (for example)
    def __init__(self) -> None:
        self.redeem_codes[UInt64(0)] = "BOOK100A"
        self.redeem_codes[UInt64(1)] = "BOOK100B"
        self.redeem_codes[UInt64(2)] = "BOOK100C"
        self.redeem_codes[UInt64(3)] = "BOOK100D"
        self.redeem_codes[UInt64(4)] = "BOOK100E"

    # ---------- Join ----------
    @abimethod()
    def join_competition(self, name: String) -> String:
        if not self.user_points.contains(name):
            self.user_points[name] = UInt64(0)
            return "Welcome " + name + "! You joined the book competition."
        else:
            return "User " + name + " already joined."

    # ---------- Add Points ----------
    @abimethod()
    def add_points(self, name: String, points: UInt64) -> String:
        if not self.user_points.contains(name):
            self.user_points[name] = UInt64(0)

        new_total = self.user_points[name] + points
        self.user_points[name] = new_total

        # If reach 100 points, assign redeem code (if available)
        if new_total >= 100 and not self.user_redeem_code.contains(name):
            code = self._get_available_code()
            if code != "":
                self.user_redeem_code[name] = code
                self.redeemed_codes[code] = UInt64(1)
                return (
                    "Congrats " + name +
                    "! You reached 100 points and earned redeem code: " + code
                )
            else:
                return (
                    name + " reached 100 points, but no redeem code left!"
                )

        return (
            "Added " + str(points) +
            " points for " + name +
            ". Total: " + str(new_total)
        )

    # ---------- Get Points ----------
    @abimethod()
    def get_points(self, name: String) -> UInt64:
        return self.user_points.get(name, UInt64(0))

    # ---------- Redeem Reward ----------
    @abimethod()
    def redeem_code(self, name: String, code: String) -> String:
        """
        Redeem the earned code for a deposit reward.
        """
        # Validate code ownership
        if not self.user_redeem_code.contains(name):
            return "No redeem code found for " + name

        stored_code = self.user_redeem_code[name]
        if stored_code != code:
            return "Invalid code for " + name

        # Simulate deposit reward (just a text in this simple example)
        reward_amount = 1000  # example "deposit" reward
        # Reset user's redeem code so they can't use it again
        del self.user_redeem_code[name]

        return (
            name + " redeemed code " + code +
            " and received deposit reward of " + str(reward_amount) + " microAlgos!"
        )

    # ---------- Helper ----------
    def _get_available_code(self) -> String:
        """
        Find first unused redeem code
        """
        for i in range(5):
            code = self.redeem_codes[UInt64(i)]
            if not self.redeemed_codes.contains(code):
                return code
        return ""

    @abimethod()
    def hello(self, name: String) -> String:
        return "Hello, " + name
