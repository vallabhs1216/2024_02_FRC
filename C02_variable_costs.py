# ===== Libraries go here =====
import pandas


# ===== Functions =====
# Checks that input is either a float or an integer that is more than zero. Takes in custom error message.
def num_check(question, error, num_type):
    valid = False
    while not valid:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
            else:
                return response
        except ValueError:
            print(error)


# Checks that response is not blank.
def not_blank(question, error):
    while True:
        response = input(question)

        if response == "":
            print(f"{error}. \nPlease try again.\n")
            continue

        return response


# Checks that user has entered yes / no to a questions
def yes_no(question):
    to_check = ["yes", "no"]

    valid = False
    while not valid:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("Please enter either yes or no...\n")


# Currency formatting function
def currency(x):
    return f"${x:.2f}"


# Gets expenses, return list which has
# the data frame and sub-total
def get_expenses(var_fixed):
    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component, quantity and price
    item_name = ""
    while item_name.lower() != "xxx":
        print()
        # Get name, quantity and item
        item_name = not_blank("Item name: ", "The component name can't be blank.")

        if item_name.lower() == "xxx":
            break

        quantity = num_check("Quantity: ", "The amount must be a whole number. (More than zero)", int)

        price = num_check("How much for a single item? $", "The price must be a number (More than 0)", float)

        # Add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # Find sub-total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apple(currency)

    return [expense_frame, sub_total]


# ===== Main routine =====


# Get product name
product_name = not_blank("Product name: ", "The product name can't be blank")

variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

# ===== Printing area =====

print()
print(variable_frame)
print()
