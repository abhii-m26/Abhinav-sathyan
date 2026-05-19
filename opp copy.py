class outer:
    def __init__(self):
        self.name = "outer class"

    class inner:
         def __initl__(self):
             self.name="inner class"

         def display(self):
           print("this is the inner class")

outer = outer()
print(outer.name)

inner = outer.inner()
print(inner.name)