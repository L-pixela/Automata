import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$",txt)

if x:
    print("There is a match!")

else:
    print("No match!")