from algopy import ARC4Contract, BoxMap, UInt64, gtxn, Txn, Global, subroutine
from algopy.arc4 import abimethod, String


class ReadingIt(ARC4Contract):
    def __init__(self) -> None:
        # BoxMap penyimpanan berbasis nama user
        self.users = BoxMap(String, UInt64)
        self.points = BoxMap(String, UInt64)
        self.user_balances = BoxMap(String, UInt64)
        self.codes = BoxMap(String, String)         # user -> code
        self.code_status = BoxMap(String, UInt64)   # code -> 1 jika digunakan

        # Statistik global
        self.total_users = UInt64(0)
        self.total_deposited = UInt64(0)

    # ---------------------------------------------------------------------
    @abimethod()
    def hello(self, name: String) -> String:
        return String("Hello, ") + name

    # ---------------------------------------------------------------------
    @abimethod()
    def addUser(self, name: String) -> String:
        if name in self.users:
            return String("User already exists")

        self.users[name] = UInt64(1)
        self.points[name] = UInt64(0)
        self.user_balances[name] = UInt64(0)
        self.total_users += UInt64(1)
        return String("User added successfully")

    # ---------------------------------------------------------------------
    @abimethod()
    def checkUserExist(self, name: String) -> String:
        if name in self.users:
            return String("User exists")
        return String("User not found")

    # ---------------------------------------------------------------------
    @abimethod()
    def addUserPoint(self, name: String, point: UInt64) -> String:
        if name not in self.users:
            return String("User not found")

        current_points = self.points[name]
        new_total = current_points + point
        self.points[name] = new_total

        # Reward jika mencapai >= 100
        if new_total >= UInt64(100) and name not in self.codes:
            available_code = self._get_available_code()
            if available_code == String("NONE"):
                return String("No more reward codes available")

            self.codes[name] = available_code
            self.code_status[available_code] = UInt64(1)
            return String("Congratulations! You got reward code: ") + available_code

        return String("Points added successfully")

    # ---------------------------------------------------------------------
    @abimethod()
    def getUserPoint(self, name: String) -> UInt64:
        if name not in self.points:
            return UInt64(0)
        return self.points[name]

    # ---------------------------------------------------------------------
    @abimethod()
    def getMyBalance(self, name: String) -> UInt64:
        amt, hasDeposited = self.user_balances.maybe(name)
        if not hasDeposited:
            return UInt64(0)
        return amt

    # ---------------------------------------------------------------------
    @abimethod()
    def deposit(self, name: String, mbrPay: gtxn.PaymentTransaction) -> UInt64:
        # Validasi transaksi
        assert mbrPay.sender == Txn.sender, "Sender mismatch"
        assert mbrPay.receiver == Global.current_application_address, "Invalid receiver"
        assert mbrPay.amount > 0, "Zero amount"

        amt, hasDeposited = self.user_balances.maybe(name)

        if hasDeposited:
            self.user_balances[name] = amt + mbrPay.amount
        else:
            self.user_balances[name] = mbrPay.amount

        self.total_deposited += mbrPay.amount
        return self.user_balances[name]

    # ---------------------------------------------------------------------
    @abimethod()
    def redeemCode(self, name: String, code: String) -> String:
        if name not in self.codes:
            return String("No reward code available")

        stored_code = self.codes[name]
        if stored_code != code:
            return String("Invalid code")

        reward_amount = UInt64(100_000)
        current_balance = self.user_balances[name]
        self.user_balances[name] = current_balance + reward_amount

        del self.codes[name]
        del self.code_status[code]

        self.total_deposited += reward_amount
        return String("Code redeemed successfully! Deposit added.")

    # ---------------------------------------------------------------------
    @subroutine
    def _get_available_code(self) -> String:
        # Hardcode 10 kode statis (tidak pakai list)
        if String("CODE1") not in self.code_status:
            return String("CODE1")
        if String("CODE2") not in self.code_status:
            return String("CODE2")
        if String("CODE3") not in self.code_status:
            return String("CODE3")
        if String("CODE4") not in self.code_status:
            return String("CODE4")
        if String("CODE5") not in self.code_status:
            return String("CODE5")
        if String("CODE6") not in self.code_status:
            return String("CODE6")
        if String("CODE7") not in self.code_status:
            return String("CODE7")
        if String("CODE8") not in self.code_status:
            return String("CODE8")
        if String("CODE9") not in self.code_status:
            return String("CODE9")
        if String("CODE10") not in self.code_status:
            return String("CODE10")
        return String("NONE")
