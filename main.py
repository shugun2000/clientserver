# This is to save user INPUT file
file_name = 'Test.txt'

with open(file_name, 'w', encoding='utf-8') as my_file:
    my_file.write(input('Your message: ') + '\n')

f = open('C:\Users\nhat\Documents\GitHub\clientserver') #This will open a file
lines = f.readlines() # This will make it reads all lines
print(lines) 