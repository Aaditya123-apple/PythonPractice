#Typecasting = the process of converting a variable from one data type to another
#str(), int(), float(), bool()

name = "Aaditya Bajaj"
check = ""
age = 18
cgpa = 9.5
is_student = True

# Using the type() function, we can check the data type of a variable
print(type(name))
print(type(age))
print(type(cgpa))
print(type(is_student))

age = float(age)
print(age)

cgpa = str(cgpa)
cgpa+='1' #->cgpa=cgpa+'1'
print(cgpa)

#If string is empty, it is considered as False. If it has any value, it is considered as True
name = bool(name)
print(name)
check = bool(check)
print(check)