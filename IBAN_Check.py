
def Input_Iban():
    country_code = "1314"
    country_code_addition = "00"
    bank_number = input(print("Gib die Bankleitzahl ein:\n"))
    account_number = input(print("Gib die Kontonummer:\n"))
    account_calc_number = bank_number + account_number + country_code + country_code_addition
    check_number = 98 - (int(account_calc_number) % 97)
    iban = "DE" + str(check_number) + bank_number + account_number
    print(iban)

def Fast_Iban(bank_number,account_number):
    country_code = "1314"
    country_code_addition = "00"
    account_calc_number = bank_number + account_number + country_code + country_code_addition
    check_number = 98 - (int(account_calc_number) % 97)
    iban = "DE" + str(check_number) + bank_number + account_number
    print(iban)


Fast_Iban("12345678","1234567890")
Input_Iban()


