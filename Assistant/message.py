class Message:

    def __init__(self, content, date, type):
        self.type = type
        self.content = content
        self.date = date

    def toDict(self):
        return {
            "content": self.content,
            "type": self.type,
            "date": self.date
        }

    def toStr(self):
        return f"content={self.content} date={self.date} type={self.type}"