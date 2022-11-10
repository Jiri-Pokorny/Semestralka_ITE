class logger():
    def __init__(self) -> None:
        pass
        
    def log(self, text):
        with open("log.txt", "w") as file:
            file.write(text)
