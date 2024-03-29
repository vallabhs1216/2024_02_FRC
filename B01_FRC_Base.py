# ===== Libraries go here =====
import pandas
import math


# ===== Functions =====


# Shows instructions
def show_instructions():
    print('''\n
***** Instructions *****

The Program will ask you for:
 %- The name of the product you are selling
 %- The quantity of items you are planning on selling
 %- The cost of each product component
 %- How must money you want to make
 
The program will output a list of the cost and subtotals
for both variable and fixed cost. Finally the program will 
give a recommended price for each item for you to reach your profit
goal.

The data from this will also be written into a text file which has the same name as your product.

 ******************************''')


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

        if var_fixed == "variable":
            quantity = num_check("Quantity: ", "The amount must be a whole number. (More than zero)", int)
        else:
            quantity = 1

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
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


# Prints expense frames
def expense_print(heading, frame, subtotal):
    print()
    print(f"**** {heading} Costs ****")
    print(frame)
    print()
    print(f"{heading} Costs: ${subtotal:.2f}")
    return ""


# Work out profit goal and total sales required
def profit_goal(total_costs):
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:
        # Asks for a profit goal...
        response = input("What is your profit goal (eg $500 or 50%) ")

        # Check if first character is $...
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # Check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (everything before the %)
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no(f"Do you mean ${amount:.2f}. ie {amount:.2f} dollars? (y / n) ")

            # Set profit type based on user answer
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no(f"Do you mean {amount:.2f}%? (y / n) ")

            # Set profit type based on user answer
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # Return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


# Rounding function
def round_up(amount, round_to):
    return int(math.ceil(amount / round_to)) * round_to


# ===== Main routine =====


want_instructions = yes_no("Would you like instructions on how to use the program? ")

if want_instructions == "yes":
    show_instructions()

# Get product name
product_name = not_blank("Product name: ", "The product name can't be blank")

how_many = num_check("\nHow many items will you be producing? ",
                     "The number of items must be a whole number more than zero", int)

print()
print("Please enter your variable costs below...")
# Get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

print()

have_fixed = yes_no("Do you have fixed costs (y/n)? ")

if have_fixed == "yes":
    print("Please enter your fixed costs below... ")

    # Get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]

else:
    fixed_sub = 0
    fixed_frame = ""

# Work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculates total sales needed to each goal
sales_needed = all_costs + profit_target

# Asks user for rounding
round_to = num_check("Round to nearest...? $",
                     "Can't be 0", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print(f"Selling price (un-rounded) ${selling_price:.2f}")

recommended_price = round_up(selling_price, round_to)

# Write data to file


# ===== Printing area =====

print()
print(f"**** Fund Raising - {product_name} ****")
print()
expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame[['Cost']], fixed_sub)

print()
print(f"**** Total Costs: ${all_costs:.2f} ****")
print()

print()
print("**** Profit & Sales Targets ****\n")
print(f"Total Sales: ${all_costs + profit_target}")
print(f"Profit Target: ${profit_target:.2f}")

print()
print("**** Pricing ****")
print(f"Minimum Price: ${selling_price:.2f}")
print(f"Recommended Price: ${recommended_price:.2f}")

product_heading = f"**** Fund Raising - {product_name} ****\n\n"
total_costs_heading = f"\n\n**** Total Costs: ${all_costs:.2f} ****\n"
variable_heading = "\n**** Variable Costs ****\n"
fixed_heading = "\n\n**** Fixed Costs ****\n"

profit_sales_heading = "\n**** Profit & Sales Targets ****\n"
total_sales = f"Total Sales: ${all_costs + profit_target}\n"
profit_target = f"Profit Target: {profit_target:.2f} | "

pricing_heading = "\n*** Pricing ***\n"
selling_price = f"Minimum Price: ${selling_price:.2f} | "
recommended_price = f"Recommended price: {recommended_price:.2f}"

variable_txt = pandas.DataFrame.to_string(variable_frame)

if have_fixed == "yes":
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)
    to_write = [product_heading, variable_heading, variable_txt, fixed_heading, fixed_txt, total_costs_heading,
                profit_sales_heading, profit_target, total_sales, pricing_heading, selling_price,
                recommended_price]

else:
    to_write = [product_heading, variable_txt, total_costs_heading, profit_target, selling_price,
                recommended_price]

# Write to file...
# Create file to hold data (add .txt extension)
file_name = f"{product_name}.txt"
text_file = open(file_name, "w+")

# Heading
for item in to_write:
    text_file.write(item)

# Close file
text_file.close()
