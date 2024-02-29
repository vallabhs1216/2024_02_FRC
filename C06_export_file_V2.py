import pandas

# Frames and context for export

variable_dict = {
    "Item": ["Mugs", "Printing", "Packaging"],
    "Quantity": [300, 300, 50],
    "Price": [1, .5, .75]
}

fixed_dict = {
    "Item": ["Rent", "Artwork", "Advertising"],
    "Price": [25, 35, 10]
}

variable_frame = pandas.DataFrame(variable_dict)
fixed_frame = pandas.DataFrame(fixed_dict)

# Changes frames to strings
variable_txt = pandas.DataFrame.to_string(variable_frame)
fixed_txt = pandas.DataFrame.to_string(fixed_frame)

product_name = "Cheese Wheels"
profit_target = "$100.00"
required_sales = "$200.00"
recommended_price = "The recommended price is $5.00"

print(variable_frame)


to_write = [product_name, variable_txt, fixed_txt, profit_target, required_sales, recommended_price]


# Write to file...
# Create file to hold data (add .txt extension
file_name = f"{product_name}.txt"
text_file = open(file_name, "w+")


# Heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")


# Close file
text_file.close()

for item in to_write:
    print(item)
    print()
