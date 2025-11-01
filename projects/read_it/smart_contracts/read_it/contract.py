# from algopy import ARC4Contract, String
# from algopy.arc4 import abimethod


# class ReadIt(ARC4Contract):
#     @abimethod()
#     def hello(self, name: String) -> String:
#         return "Hello, " + name


# from algopy import ARC4Contract, UInt64, String, GlobalState
# from algopy.arc4 import abimethod

# class ReadIt(ARC4Contract):
#     # Global states
#     user_points: GlobalState[String, UInt64]     # name -> points
#     user_redeem_code: GlobalState[String, String] # name -> redeem code (if earned)
#     redeem_codes: GlobalState[UInt64, String]     # index -> redeem code (5 total)
#     redeemed_codes: GlobalState[String, UInt64]   # code -> 1 if used, else 0

#     # Initialize redeem codes (for example)
#     def __init__(self) -> None:
#         self.redeem_codes[UInt64(0)] = "BOOK100A"
#         self.redeem_codes[UInt64(1)] = "BOOK100B"
#         self.redeem_codes[UInt64(2)] = "BOOK100C"
#         self.redeem_codes[UInt64(3)] = "BOOK100D"
#         self.redeem_codes[UInt64(4)] = "BOOK100E"

#     # ---------- Join ----------
#     @abimethod()
#     def join_competition(self, name: String) -> String:
#         if not self.user_points.contains(name):
#             self.user_points[name] = UInt64(0)
#             return "Welcome " + name + "! You joined the book competition."
#         else:
#             return "User " + name + " already joined."

#     # ---------- Add Points ----------
#     @abimethod()
#     def add_points(self, name: String, points: UInt64) -> String:
#         if not self.user_points.contains(name):
#             self.user_points[name] = UInt64(0)

#         new_total = self.user_points[name] + points
#         self.user_points[name] = new_total

#         # If reach 100 points, assign redeem code (if available)
#         if new_total >= 100 and not self.user_redeem_code.contains(name):
#             code = self._get_available_code()
#             if code != "":
#                 self.user_redeem_code[name] = code
#                 self.redeemed_codes[code] = UInt64(1)
#                 return (
#                     "Congrats " + name +
#                     "! You reached 100 points and earned redeem code: " + code
#                 )
#             else:
#                 return (
#                     name + " reached 100 points, but no redeem code left!"
#                 )

#         return (
#             "Added " + str(points) +
#             " points for " + name +
#             ". Total: " + str(new_total)
#         )

#     # ---------- Get Points ----------
#     @abimethod()
#     def get_points(self, name: String) -> UInt64:
#         return self.user_points.get(name, UInt64(0))

    # ---------- Redeem Reward ----------
    # @abimethod()
    # def redeem_code(self, name: String, code: String) -> String:
    #     """
    #     Redeem the earned code for a deposit reward.
    #     """
    #     # Validate code ownership
    #     if not self.user_redeem_code.contains(name):
    #         return "No redeem code found for " + name

    #     stored_code = self.user_redeem_code[name]
    #     if stored_code != code:
    #         return "Invalid code for " + name

    #     # Simulate deposit reward (just a text in this simple example)
    #     reward_amount = 1000  # example "deposit" reward
    #     # Reset user's redeem code so they can't use it again
    #     del self.user_redeem_code[name]

    #     return (
    #         name + " redeemed code " + code +
    #         " and received deposit reward of " + str(reward_amount) + " microAlgos!"
    #     )

    # # ---------- Helper ----------
    # def _get_available_code(self) -> String:
    #     """
    #     Find first unused redeem code
    #     """
    #     for i in range(5):
    #         code = self.redeem_codes[UInt64(i)]
    #         if not self.redeemed_codes.contains(code):
    #             return code
    #     return ""

    # @abimethod()
    # def hello(self, name: String) -> String:
    #     return "Hello, " + name

# from algopy import ARC4Contract, UInt64, String, BoxMap, subroutine, urange
# from algopy.arc4 import abimethod

# class ReadIt(ARC4Contract):
#     def __init__(self) -> None:
#         # Initialize BoxMaps
#         self.user_points = BoxMap(String, UInt64)
#         self.user_code = BoxMap(String, String)
#         self.redeemed = BoxMap(String, UInt64)
#         self.redeem_codes = BoxMap(UInt64, String)
        
#         # Initialize redeem codes with String() constructor
#         self.redeem_codes[UInt64(0)] = String("BOOK100A")
#         self.redeem_codes[UInt64(1)] = String("BOOK100B")
#         self.redeem_codes[UInt64(2)] = String("BOOK100C")
#         self.redeem_codes[UInt64(3)] = String("BOOK100D")
#         self.redeem_codes[UInt64(4)] = String("BOOK100E")

#     @subroutine
#     def _get_available_code(self) -> String:
#         for i in urange(5):  # Use urange instead of range
#             code = self.redeem_codes[i]  # i is already UInt64
#             # Check if code exists in redeemed
#             if code in self.redeemed:
#                 if self.redeemed[code] == UInt64(0):
#                     return code
#             else:
#                 # Code not redeemed yet
#                 return code
#         return String("")

#     @abimethod()
#     def join_competition(self, name: String) -> String:
#         if name not in self.user_points:
#             self.user_points[name] = UInt64(0)
#             return String("Welcome ") + name + String("! You joined the book competition.")
#         else:
#             return String("User ") + name + String(" already joined.")

#     @abimethod()
#     def add_points(self, name: String, points: UInt64) -> String:
#         # Get current points
#         if name in self.user_points:
#             current_points = self.user_points[name]
#         else:
#             current_points = UInt64(0)
        
#         total = current_points + points
#         self.user_points[name] = total

#         if total >= UInt64(100) and name not in self.user_code:
#             code = self._get_available_code()
#             if code != String(""):
#                 self.user_code[name] = code
#                 self.redeemed[code] = UInt64(1)
#                 return (
#                     String("Congrats ") + name +
#                     String("! You reached 100 points and earned redeem code: ") + code
#                 )
#             else:
#                 return name + String(" reached 100 points, but no redeem code left!")

#         return String("Points added for ") + name

#     @abimethod()
#     def get_points(self, name: String) -> UInt64:
#         if name in self.user_points:
#             return self.user_points[name]
#         else:
#             return UInt64(0)


# from algopy import ARC4Contract, UInt64, String, BoxMap, subroutine, urange, Txn, Global, gtxn
# from algopy.arc4 import abimethod

# class ReadIt(ARC4Contract):
#     def __init__(self) -> None:
#         # Initialize BoxMaps
#         self.user_points = BoxMap(String, UInt64)
#         self.user_code = BoxMap(String, String)
#         self.redeemed = BoxMap(String, UInt64)
#         self.redeem_codes = BoxMap(UInt64, String)
#         self.user_balances = BoxMap(String, UInt64)
        
#         # Initialize redeem codes with String() constructor
#         self.redeem_codes[UInt64(0)] = String("BOOK100A")
#         self.redeem_codes[UInt64(1)] = String("BOOK100B")
#         self.redeem_codes[UInt64(2)] = String("BOOK100C")
#         self.redeem_codes[UInt64(3)] = String("BOOK100D")
#         self.redeem_codes[UInt64(4)] = String("BOOK100E")

#     @subroutine
#     def _get_available_code(self) -> String:
#         for i in urange(5):  # Use urange instead of range
#             code = self.redeem_codes[i]  # i is already UInt64
#             # Check if code exists in redeemed
#             if code in self.redeemed:
#                 if self.redeemed[code] == UInt64(0):
#                     return code
#             else:
#                 # Code not redeemed yet
#                 return code
#         return String("")

#     @abimethod()
#     def join_competition(self, name: String) -> String:
#         if name not in self.user_points:
#             self.user_points[name] = UInt64(0)
#             return String("Welcome ") + name + String("! You joined the book competition.")
#         else:
#             return String("User ") + name + String(" already joined.")

#     @abimethod()
#     def add_points(self, name: String, points: UInt64) -> String:
#         # Get current points
#         if name in self.user_points:
#             current_points = self.user_points[name]
#         else:
#             current_points = UInt64(0)
        
#         total = current_points + points
#         self.user_points[name] = total

#         if total >= UInt64(100) and name not in self.user_code:
#             code = self._get_available_code()
#             if code != String(""):
#                 self.user_code[name] = code
#                 self.redeemed[code] = UInt64(1)
#                 return (
#                     String("Congrats ") + name +
#                     String("! You reached 100 points and earned redeem code: ") + code
#                 )
#             else:
#                 return name + String(" reached 100 points, but no redeem code left!")

#         return String("Points added for ") + name

#     @abimethod()
#     def get_points(self, name: String) -> UInt64:
#         if name in self.user_points:
#             return self.user_points[name]
#         else:
#             return UInt64(0)

#     @abimethod()
#     def redeem_code(self, name: String, code: String, mbrPay: gtxn.PaymentTransaction) -> String:
#         # Payment Check
#         assert mbrPay.sender == Txn.sender, "Sender mismatch"
#         assert mbrPay.receiver == Global.current_application_address, "Invalid receiver"
#         assert mbrPay.amount > 0, "Zero Amount"
        
#         # Check if user has this code assigned to them
#         if name not in self.user_code:
#             return String("Error: No redeem code assigned to ") + name
        
#         user_assigned_code = self.user_code[name]
        
#         # Verify the code matches
#         if user_assigned_code != code:
#             return String("Error: Invalid redeem code")
        
#         # Check if code is valid and not already fully redeemed
#         if code not in self.redeemed:
#             return String("Error: Code does not exist")
        
#         if self.redeemed[code] != UInt64(1):
#             return String("Error: Code already redeemed or invalid")
        
#         # Mark code as fully redeemed (2 = used)
#         self.redeemed[code] = UInt64(2)
        
#         # Process deposit
#         if name in self.user_balances:
#             self.user_balances[name] += mbrPay.amount
#         else:
#             self.user_balances[name] = mbrPay.amount
        
#         return String("Success! Code redeemed and ") + String(" deposited for ") + name

#     @abimethod()
#     def get_balance(self, name: String) -> UInt64:
#         if name in self.user_balances:
#             return self.user_balances[name]
#         else:
#             return UInt64(0)

#     @abimethod()
#     def getMyBalance(self) -> UInt64:
#         sender_str = String(Txn.sender.bytes)
#         if sender_str in self.user_balances:
#             return self.user_balances[sender_str]
#         else:
#             assert False, "You've not been deposited before"


from algopy import ARC4Contract, UInt64, String, BoxMap, subroutine, urange, Txn, Global, gtxn, Account
from algopy.arc4 import abimethod

class ReadIt(ARC4Contract):
    def __init__(self) -> None:
        # Initialize BoxMaps
        self.user_points = BoxMap(String, UInt64)
        self.user_code = BoxMap(String, String)
        self.redeemed = BoxMap(String, UInt64)
        self.redeem_codes = BoxMap(UInt64, String)
        self.user_balances = BoxMap(String, UInt64)
        self.name_to_address = BoxMap(String, Account)  # Map name to address
        
        # Initialize redeem codes with String() constructor
        self.redeem_codes[UInt64(0)] = String("BOOK100A")
        self.redeem_codes[UInt64(1)] = String("BOOK100B")
        self.redeem_codes[UInt64(2)] = String("BOOK100C")
        self.redeem_codes[UInt64(3)] = String("BOOK100D")
        self.redeem_codes[UInt64(4)] = String("BOOK100E")

    @subroutine
    def _get_available_code(self) -> String:
        for i in urange(5):  # Use urange instead of range
            code = self.redeem_codes[i]  # i is already UInt64
            # Check if code exists in redeemed
            if code in self.redeemed:
                if self.redeemed[code] == UInt64(0):
                    return code
            else:
                # Code not redeemed yet
                return code
        return String("")

    @abimethod()
    def join_competition(self, name: String) -> String:
        if name not in self.user_points:
            self.user_points[name] = UInt64(0)
            self.name_to_address[name] = Txn.sender  # Save address mapping
            return String("Welcome ") + name + String("! You joined the book competition.")
        else:
            return String("User ") + name + String(" already joined.")

    @abimethod()
    def add_points(self, name: String, points: UInt64) -> String:
        # Get current points
        if name in self.user_points:
            current_points = self.user_points[name]
        else:
            current_points = UInt64(0)
        
        total = current_points + points
        self.user_points[name] = total

        if total >= UInt64(100) and name not in self.user_code:
            code = self._get_available_code()
            if code != String(""):
                self.user_code[name] = code
                self.redeemed[code] = UInt64(1)
                return (
                    String("Congrats ") + name +
                    String("! You reached 100 points and earned redeem code: ") + code
                )
            else:
                return name + String(" reached 100 points, but no redeem code left!")

        return String("Points added for ") + name

    @abimethod()
    def get_points(self, name: String) -> UInt64:
        if name in self.user_points:
            return self.user_points[name]
        else:
            return UInt64(0)

    @abimethod()
    def redeem_code(self, name: String, code: String, mbrPay: gtxn.PaymentTransaction) -> String:
        # Payment Check
        assert mbrPay.sender == Txn.sender, "Sender mismatch"
        assert mbrPay.receiver == Global.current_application_address, "Invalid receiver"
        assert mbrPay.amount > 0, "Zero Amount"
        
        # Verify caller is the registered user
        if name in self.name_to_address:
            assert self.name_to_address[name] == Txn.sender, "Not authorized for this name"
        
        # Check if user has this code assigned to them
        if name not in self.user_code:
            return String("Error: No redeem code assigned to ") + name
        
        user_assigned_code = self.user_code[name]
        
        # Verify the code matches
        if user_assigned_code != code:
            return String("Error: Invalid redeem code")
        
        # Check if code is valid and not already fully redeemed
        if code not in self.redeemed:
            return String("Error: Code does not exist")
        
        if self.redeemed[code] != UInt64(1):
            return String("Error: Code already redeemed or invalid")
        
        # Mark code as fully redeemed (2 = used)
        self.redeemed[code] = UInt64(2)
        
        # Process deposit
        if name in self.user_balances:
            self.user_balances[name] += mbrPay.amount
        else:
            self.user_balances[name] = mbrPay.amount
        
        return String("Success! Code redeemed and ") + String(" deposited for ") + name

    @abimethod()
    def get_balance(self, name: String) -> UInt64:
        if name in self.user_balances:
            return self.user_balances[name]
        else:
            return UInt64(0)

    @abimethod()
    def getMyBalance(self, my_name: String) -> UInt64:
        # Verify caller owns this name
        if my_name not in self.name_to_address:
            assert False, "Name not registered"
        
        assert self.name_to_address[my_name] == Txn.sender, "Not your name"
        
        if my_name in self.user_balances:
            return self.user_balances[my_name]
        else:
            assert False, "You've not been deposited before"