class Student(object):
    def __init__(self, name, chinese,math,english):
        self.name = name
        self.chinese=chinese
        self.math=math
        self.english=english

    def __str__(self):
        return f"姓名{self.name}|语文成绩：{self.chinese}|数学成绩：{self.math}|英语成绩：{self.english}|总分：{self.chinese + self.english + self.math}"
    def update_score(self,chinese=None,math=None,english=None):
        if chinese is not None:
            self.chinese=chinese
        if math is not None:
            self.math=math
        if english is not None:
            self.english=english


if __name__ == '__main__':
    s1 = Student("<UNK>",None,None,None)
    print(s1)