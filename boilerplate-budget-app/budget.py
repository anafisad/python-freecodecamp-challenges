class Category:
    def __str__(self):
        output = ""
        output += self.name.center(30, "*")
        for entry in self.ledger:
            amount = round(entry["amount"], 2)
            whole, decimal = str(float(amount)).split(".")
            amount_string = whole + "." + decimal.ljust(2, "0")
            description = entry["description"]
            output = output + "\n" + \
                description[:23].ljust(23, " ") + \
                amount_string[:7].rjust(7, " ")
        output += "\nTotal: " + str(self.get_balance())
        return output

    def __init__(self, name):
        self.ledger = []
        self.name = name

    def deposit(self, amount, description=""):
        entry = {
            "amount": amount,
            "description": description
        }
        self.ledger.append(entry)

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False

        entry = {
            "amount": amount * -1,
            "description": description
        }
        self.ledger.append(entry)
        return True

    def get_balance(self):
        balance = 0
        for entry in self.ledger:
            balance += entry["amount"]
        return round(balance, 2)

    def transfer(self, amount, destination):
        if not self.check_funds(amount):
            return False

        description_source = "Transfer to " + destination.name
        self.withdraw(amount, description_source)

        description_destination = "Transfer from " + self.name
        destination.deposit(amount, description_destination)

        return True

    def check_funds(self, amount):
        balance = self.get_balance()
        return balance >= amount


def create_spend_chart(categories):
    output = ""
    output += "Percentage spent by category\n"
    percentages = list(reversed([i * 10 for i in range(11)]))
    percentages_len_max = len(str(max(percentages)))

    # compute percentages
    spenditures = []
    spenditures_total = 0
    for category in categories:
        spenditure = 0
        for entry in category.ledger:
            if entry["amount"] < 0:
                spenditure += abs(entry["amount"])
        spenditures.append(spenditure)
        spenditures_total += spenditure

    spenditures_percentages = [
        round(spenditure / spenditures_total * 100) for spenditure in spenditures]

    for percentage in percentages:
        output += str(percentage).rjust(percentages_len_max, " ")
        output += "|"
        for spenditures_percentage in spenditures_percentages:
            output += " "
            if spenditures_percentage >= percentage:
                output += "o"
            else:
                output += " "
            output += " "

        output += " \n"

    output += " " * (percentages_len_max + 1)
    output += "---" * len(categories)
    output += "-\n"

    names = [category.name for category in categories]
    names_len = [len(name) for name in names]
    for index_column in range(max(names_len)):
        output += " " * (percentages_len_max + 1)
        for index_row in range(len(names)):
            output += " "
            try:
                letter = names[index_row][index_column]
            except IndexError:
                output += " "
            else:
                output += letter
            output += " "
        output += " \n"

    return output[:-1]