class Father:
    def __init__(self):
        self.a = 1


class Foo(Father):
    def __init__(self):
        self.x = 1
        super().__init__()

        self.init_foo()

    def foo(self):
        self.y = 2

    def init_foo(self):
        self.z = 3

    def bar(self, x, y, **kwargs):
        print(x)
        print(y)
        for entry in kwargs:
            print(kwargs[entry])

    def listen(self, data):
        print(data, self.x)


class Son:
    def __init__(self):
        self.func = None
    def call(self, func=None):
        data = 2
        if self.func is None:
            self.func = func
        self.func(data)


if __name__ == "__main__":
    import cv2
    img = cv2.imread("test.png")

    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

    print(img.shape[0])

    cv2.imshow("test", img)
    cv2.waitKey(2000)

