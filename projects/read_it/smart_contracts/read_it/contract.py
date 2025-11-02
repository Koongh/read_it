# from algopy import ARC4Contract, UInt64, String, BoxMap, subroutine, urange, Txn, Global, gtxn, Account
# from algopy.arc4 import abimethod

# class ReadIt(ARC4Contract):
#     def __init__(self) -> None:
#         # Initialize BoxMaps
#         self.user_points = BoxMap(String, UInt64)
#         self.user_code = BoxMap(String, String)
#         self.redeemed = BoxMap(String, UInt64)
#         self.redeem_codes = BoxMap(UInt64, String)
#         self.user_balances = BoxMap(String, UInt64)
#         self.name_to_address = BoxMap(String, Account)  
        
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
#             self.name_to_address[name] = Txn.sender  # Save address mapping
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
        
#         # Verify caller is the registered user
#         if name in self.name_to_address:
#             assert self.name_to_address[name] == Txn.sender, "Not authorized for this name"
        
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
#     def getMyBalance(self, my_name: String) -> UInt64:
#         if my_name not in self.name_to_address:
#             assert False, "Name not registered"
        
#         assert self.name_to_address[my_name] == Txn.sender, "Not your name"
        
#         if my_name in self.user_balances:
#             return self.user_balances[my_name]
#         else:
#             return UInt64(0)  # ✅ Return 0 instead of 


# from algopy import ARC4Contract, UInt64, String, BoxMap, subroutine, urange, Txn, Global, gtxn, Account, GlobalState
# from algopy.arc4 import abimethod, UInt64 as Arc4UInt64

# class ReadIt(ARC4Contract):
#     def __init__(self) -> None:
#         # Store owner address (deployer)
#         self.owner = GlobalState(Txn.sender)
        
#         # Initialize BoxMaps
#         self.user_points = BoxMap(String, UInt64)
#         self.user_code = BoxMap(String, String)
#         self.redeemed = BoxMap(String, UInt64)
#         self.redeem_codes = BoxMap(UInt64, String)
#         self.user_balances = BoxMap(String, UInt64)
#         self.name_to_address = BoxMap(String, Account)  
        
#         # Initialize redeem codes
#         self.redeem_codes[UInt64(0)] = String("BOOK100A")
#         self.redeem_codes[UInt64(1)] = String("BOOK100B")
#         self.redeem_codes[UInt64(2)] = String("BOOK100C")
#         self.redeem_codes[UInt64(3)] = String("BOOK100D")
#         self.redeem_codes[UInt64(4)] = String("BOOK100E")

#     @subroutine
#     def _get_available_code(self) -> String:
#         """Mencari kode redeem yang belum digunakan"""
#         for i in urange(5):
#             code = self.redeem_codes[i]
#             if code in self.redeemed:
#                 if self.redeemed[code] == UInt64(0):
#                     return code
#             else:
#                 return code
#         return String("")

#     @abimethod()
#     def join_competition(self, name: String, mbrPay: gtxn.PaymentTransaction) -> String:
#         """
#         User join kompetisi dengan membayar MBR (untuk SDK/AlgoKit)
#         Payment: Minimal 50,000 microAlgo untuk box storage (buffer untuk nama panjang)
        
#         Atomic Group:
#         - Txn 0: Payment (user → contract, 50000 microAlgo)
#         - Txn 1: App call join_competition
#         """
#         # Validasi payment
#         assert mbrPay.sender == Txn.sender, "Sender mismatch"
#         assert mbrPay.receiver == Global.current_application_address, "Must pay to contract"
#         assert mbrPay.amount >= UInt64(50000), "Insufficient MBR payment (need 50000 microAlgo)"
        
#         # Cek apakah user sudah join
#         if name in self.user_points:
#             return String("Error: User ") + name + String(" already joined")
        
#         # Register user
#         self.user_points[name] = UInt64(0)
#         self.name_to_address[name] = Txn.sender
        
#         return String("Welcome ") + name + String("! You joined the book competition")
    
#     @abimethod(allow_actions=["OptIn"])
#     def join_simple(self, name: String) -> String:
#         """
#         Versi sederhana untuk Lora/UI wallet
#         User harus kirim 50,000 microAlgo ke contract address SEBELUM memanggil method ini
        
#         Cara pakai:
#         1. Kirim 50,000 microAlgo (0.05 ALGO) ke contract address
#         2. Call method ini dengan nama Anda
#         """
#         # Cek apakah user sudah join
#         if name in self.user_points:
#             return String("Error: User ") + name + String(" already joined")
        
#         # Register user
#         self.user_points[name] = UInt64(0)
#         self.name_to_address[name] = Txn.sender
        
#         return String("Welcome ") + name + String("! You joined the book competition")

#     @abimethod()
#     def add_points(self, name: String, points: UInt64, mbrPay: gtxn.PaymentTransaction) -> String:
#         """
#         Menambah poin untuk user (untuk SDK/AlgoKit dengan grouped transactions)
#         - Jika mencapai 100 poin pertama kali: bayar 35,000 microAlgo
#         - Jika hanya update poin: bayar minimal 1,000 microAlgo
        
#         Atomic Group:
#         - Txn 0: Payment (user → contract)
#         - Txn 1: App call add_points
#         """
#         # Validasi payment
#         assert mbrPay.sender == Txn.sender, "Sender mismatch"
#         assert mbrPay.receiver == Global.current_application_address, "Must pay to contract"
        
#         # Cek apakah user terdaftar
#         if name not in self.user_points:
#             return String("Error: User ") + name + String(" not registered. Please join first")
        
#         # Validasi kepemilikan nama
#         assert self.name_to_address[name] == Txn.sender, "Not authorized for this name"
        
#         # Get current points
#         current_points = self.user_points[name]
#         total = current_points + points
#         self.user_points[name] = total

#         # Cek apakah mencapai 100 poin dan belum dapat code
#         if total >= UInt64(100) and name not in self.user_code:
#             # Butuh MBR untuk 2 box baru (user_code dan redeemed)
#             assert mbrPay.amount >= UInt64(35000), "Insufficient MBR (need 35000 microAlgo for code assignment)"
            
#             code = self._get_available_code()
#             if code != String(""):
#                 self.user_code[name] = code
#                 self.redeemed[code] = UInt64(1)  # 1 = assigned but not redeemed
#                 return (
#                     String("Congrats ") + name +
#                     String("! You reached ") + String.from_bytes(Arc4UInt64(total).bytes) +
#                     String(" points and earned redeem code: ") + code
#                 )
#             else:
#                 return String("Error: ") + name + String(" reached 100 points but no redeem code left")
#         else:
#             # Hanya menambah poin, minimal payment
#             assert mbrPay.amount >= UInt64(1000), "Insufficient payment (need at least 1000 microAlgo)"
            
#             return String("Points added for ") + name + String(". Total points: ") + String.from_bytes(Arc4UInt64(total).bytes)
    
#     @abimethod()
#     def add_points_simple(self, name: String, points: UInt64) -> String:
#         """
#         Versi sederhana untuk Lora/UI wallet
#         User harus kirim ALGO ke contract SEBELUM memanggil method ini:
#         - Kirim 35,000 microAlgo jika akan mencapai 100 poin
#         - Kirim 1,000 microAlgo untuk update biasa
#         """
#         # Cek apakah user terdaftar
#         if name not in self.user_points:
#             return String("Error: User ") + name + String(" not registered. Please join first")
        
#         # Validasi kepemilikan nama
#         assert self.name_to_address[name] == Txn.sender, "Not authorized for this name"
        
#         # Get current points
#         current_points = self.user_points[name]
#         total = current_points + points
#         self.user_points[name] = total

#         # Cek apakah mencapai 100 poin dan belum dapat code
#         if total >= UInt64(100) and name not in self.user_code:            
#             code = self._get_available_code()
#             if code != String(""):
#                 self.user_code[name] = code
#                 self.redeemed[code] = UInt64(1)
#                 return (
#                     String("Congrats ") + name +
#                     String("! You reached ") + String.from_bytes(Arc4UInt64(total).bytes) +
#                     String(" points and earned redeem code: ") + code
#                 )
#             else:
#                 return String("Error: ") + name + String(" reached 100 points but no redeem code left")
#         else:            
#             return String("Points added for ") + name + String(". Total points: ") + String.from_bytes(Arc4UInt64(total).bytes)

#     @abimethod()
#     def get_points(self, name: String) -> UInt64:
#         """Melihat poin user (siapa saja bisa cek)"""
#         if name in self.user_points:
#             return self.user_points[name]
#         else:
#             return UInt64(0)

#     @abimethod()
#     def get_my_code(self, name: String) -> String:
#         """User melihat kode redeem mereka sendiri"""
#         if name not in self.name_to_address:
#             return String("Error: Name not registered")
        
#         assert self.name_to_address[name] == Txn.sender, "Not authorized for this name"
        
#         if name in self.user_code:
#             return self.user_code[name]
#         else:
#             return String("No code yet. Reach 100 points first")

#     @abimethod()
#     def redeem_code(
#         self, 
#         name: String, 
#         code: String, 
#         mbrPay: gtxn.PaymentTransaction,
#         ownerPay: gtxn.PaymentTransaction
#     ) -> String:
#         """
#         User redeem code untuk mendapat hadiah (untuk SDK/AlgoKit)
        
#         Atomic Group (3 transactions):
#         - Txn 0: mbrPay (user → contract, 15000 microAlgo untuk MBR pertama kali)
#         - Txn 1: ownerPay (user → owner, amount bebas sesuai hadiah)
#         - Txn 2: App call redeem_code
#         """
#         # Validasi MBR payment ke contract
#         assert mbrPay.sender == Txn.sender, "MBR sender mismatch"
#         assert mbrPay.receiver == Global.current_application_address, "MBR must go to contract"
        
#         # Validasi owner payment (ini adalah "hadiah" yang user bayar)
#         assert ownerPay.sender == Txn.sender, "Owner payment sender mismatch"
#         assert ownerPay.receiver == self.owner.value, "Payment must go to owner"
#         assert ownerPay.amount > UInt64(0), "Owner payment must be > 0"
        
#         # Cek MBR untuk pertama kali redeem
#         if name not in self.user_balances:
#             assert mbrPay.amount >= UInt64(15000), "Insufficient MBR (need 15000 microAlgo)"
#         else:
#             assert mbrPay.amount >= UInt64(1000), "Insufficient payment (need at least 1000 microAlgo)"
        
#         # Verify caller adalah registered user
#         if name not in self.name_to_address:
#             return String("Error: Name not registered")
        
#         assert self.name_to_address[name] == Txn.sender, "Not authorized for this name"
        
#         # Cek apakah user punya code
#         if name not in self.user_code:
#             return String("Error: No redeem code assigned to ") + name
        
#         user_assigned_code = self.user_code[name]
        
#         # Verify code cocok
#         if user_assigned_code != code:
#             return String("Error: Invalid redeem code")
        
#         # Cek status code
#         if code not in self.redeemed:
#             return String("Error: Code does not exist")
        
#         if self.redeemed[code] != UInt64(1):
#             return String("Error: Code already redeemed or invalid")
        
#         # Mark code sebagai sudah diredeeem (2 = used)
#         self.redeemed[code] = UInt64(2)
        
#         # Track payment amount
#         if name in self.user_balances:
#             self.user_balances[name] = self.user_balances[name] + ownerPay.amount
#         else:
#             self.user_balances[name] = ownerPay.amount
        
#         return String("Success! Code redeemed. Amount paid: ") + String.from_bytes(Arc4UInt64(ownerPay.amount).bytes) + String(" microAlgo")

#     @abimethod()
#     def redeem_code_simple(self, name: String, code: String, owner_payment: UInt64) -> String:
#         """
#         Versi sederhana untuk Lora/UI wallet
        
#         Cara pakai:
#         1. Kirim (15,000 + owner_payment) microAlgo ke contract address
#         2. Call method ini dengan nama, kode, dan jumlah yang mau bayar ke owner
        
#         Contoh: Mau bayar 100,000 microAlgo ke owner
#         - Kirim 115,000 microAlgo ke contract (15,000 MBR + 100,000 hadiah)
#         - Call redeem_code_simple(name="Alice", code="BOOK100A", owner_payment=100000)
#         """
#         # Verify caller adalah registered user
#         if name not in self.name_to_address:
#             return String("Error: Name not registered")
        
#         assert self.name_to_address[name] == Txn.sender, "Not authorized for this name"
        
#         # Cek apakah user punya code
#         if name not in self.user_code:
#             return String("Error: No redeem code assigned to ") + name
        
#         user_assigned_code = self.user_code[name]
        
#         # Verify code cocok
#         if user_assigned_code != code:
#             return String("Error: Invalid redeem code")
        
#         # Cek status code
#         if code not in self.redeemed:
#             return String("Error: Code does not exist")
        
#         if self.redeemed[code] != UInt64(1):
#             return String("Error: Code already redeemed or invalid")
        
#         # Mark code sebagai sudah diredeeem
#         self.redeemed[code] = UInt64(2)
        
#         # Track payment amount
#         if name in self.user_balances:
#             self.user_balances[name] = self.user_balances[name] + owner_payment
#         else:
#             self.user_balances[name] = owner_payment
        
#         return String("Success! Code redeemed. Amount recorded: ") + String.from_bytes(Arc4UInt64(owner_payment).bytes) + String(" microAlgo")

#     @abimethod()
#     def get_balance(self, name: String) -> UInt64:
#         """Melihat total yang sudah dibayarkan user (siapa saja bisa cek)"""
#         if name in self.user_balances:
#             return self.user_balances[name]
#         else:
#             return UInt64(0)

#     @abimethod()
#     def get_my_balance(self, name: String) -> UInt64:
#         """User melihat balance mereka sendiri"""
#         if name not in self.name_to_address:
#             return UInt64(0)
        
#         assert self.name_to_address[name] == Txn.sender, "Not authorized for this name"
        
#         if name in self.user_balances:
#             return self.user_balances[name]
#         else:
#             return UInt64(0)
    
#     @abimethod()
#     def get_owner(self) -> Account:
#         """Mendapatkan alamat owner contract"""
#         return self.owner.value
    
#     @abimethod()
#     def check_code_status(self, code: String) -> UInt64:
#         """
#         Cek status kode redeem
#         Return: 0 = available, 1 = assigned, 2 = redeemed, 999 = not found
#         """
#         if code in self.redeemed:
#             return self.redeemed[code]
#         else:
#             # Cek apakah kode ada di daftar redeem_codes
#             for i in urange(5):
#                 if self.redeem_codes[i] == code:
#                     return UInt64(0)  # Available
#             return UInt64(999)  # Not found


from algopy import ARC4Contract, String, BoxMap
from algopy.arc4 import abimethod

class Sesi(ARC4Contract):
    def __init__(self) -> None:
        self.names = BoxMap(String, String)

    @abimethod()
    def add_name(self, name: String) -> String:
        self.names[name] = String("1")
        return "Added name"

    @abimethod
    def get_name(self, name: String) -> String:
        value = self.names.get(name, default=String(""))
        if value != String(""):
            return  "Found"
        else:
            return "Name not found"

    @abimethod
    def hello(self, name: String) -> String:
        return String("Hello, ") + name
