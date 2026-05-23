'''f = open('bot.txt', 'r')
f.close()'''
'''with open('example.txt', 'w', encoding="utf-8") as file:
    file.write("hello\n")
    file.write("how are you?\n")
    file.write("Привіт")'''
'''with open('example.txt', 'r') as file:
    content = file.read()
    print("Весь вміст: ")
    print(content)'''
'''with open('example.txt', 'r') as file:
    print("Читання по рядках: ")
    for line in file:
        print(line.strip())'''
'''with open('example.txt', 'r') as file:
    first_line = file.readline()
    print(first_line)'''
'''with open('example.txt', 'r') as file:
    lines = file.readlines()
    print(lines[1].strip())'''
'''with open('example.txt', 'a') as file:
    file.write("\nhi")'''
'''with open('example.txt', 'r+', encoding="utf-8") as file:
    old_content = file.read()
    print("Було у файлі: ", old_content)
    file.write("Bye")
    file.seek(0)
    new_content = file.read()
    print("Стало у файлі: ", new_content)'''