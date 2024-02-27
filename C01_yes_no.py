# Functions go here

# Checks thet user has entered yes / no to a questions
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

# Main routine


# Ask the user if they have played before
while True:
    want_instructions = yes_no("Do you want  instructions? ").lower()

    # If they say yes, output 'display instructions'
    # If they say no, output 'program continues'
    # If they say anything else, outputs error

    if want_instructions == "yes":
        print("Instructions")


    print("program continues")
    print()
        