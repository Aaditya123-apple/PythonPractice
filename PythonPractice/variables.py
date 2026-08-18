# Variable = A container for a value (string, integer, float, boolean)
# A variable behaves as if it was the value it contains

#Strings
first_name = "Aadi"
food = "Burger"

#Integers
age = 18

#Floats
price = 299.99
cgpa = 9.5

print (first_name)

# Using f before the quotation marks allows us to use variables inside the string
# Along with {}
print (f"Hello {first_name}!")

#{} is called a placeholder. It is replaced with the value of the variable inside it
print(f"{first_name} likes {food}")
print(f"{first_name} is {age} years old")
print(f"{first_name} is buying a {food} for ${price}")
print(f"{first_name} has a CGPA of {cgpa}")

#Boolean -> True or False
is_student = True
is_online = False
print(f"Are you a student?: {is_student}")


#if else conditions
if is_student: print("You are a student")
else: print("You are not a student")

if is_online: print(f"{first_name} is online")
else: print(f"{first_name} is offline")