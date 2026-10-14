## works yay

class BankAccount:
  def __init__(self,first_name,last_name,account_id,account_type,pin,balance):
    self.first_name = first_name
    self.last_name = last_name
    self.account_id = account_id
    self.account_type = account_type
    self.pin = pin
    self.balance = balance
  def deposit(self,amount):
    self.balance = self.balance + amount
    return self.balance
  def withdraw(self,amount):
    self.balance = self.balance - amount
    return self.balance
  def display_balance(self):
    return self.balance

david = BankAccount("David","Hartwig",1,"Premium",1234,100.0)

david.deposit(10)
print(david.balance)

david.withdraw(5)
print(david.balance)

print(david.display_balance())

paul = BankAccount("Paul","D",2,"Premium",1221,0)
paul.deposit(96)
paul.withdraw(25)
print(paul.display_balance())


