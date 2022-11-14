def log(text):
    with open("log.txt", "w") as file:
        file.write(str(text))