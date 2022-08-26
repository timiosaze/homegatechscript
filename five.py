import re
# str = "Type:Roof flatNo. of rooms: 4 Floor: 2 Number of floors: 2 Surface living: 116 m2Last refurbishment: 2008 Year built: 1960"
# one = re.findall(":(:?(\s\w+)|(\w+))", str)
# for x in one:
#     print(x[0])
    
# two = re.findall("(\w+):", str)
# for x in two:
#     print(x)

# str = "6095 bbjbdsakd"
# print(str.split()[-1])
str = ""
one = re.search("tel:(\+\d+)", str.replace(" ","")).group(1)
print(one)


