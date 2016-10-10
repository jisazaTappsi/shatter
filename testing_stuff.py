
def g():
	def f():
		pass
	f()
	print(str(f.func_closure))
	pass


g()
print (str(g.func_closure))

print("{f} {g}".format(g='2', f='{f}'))


class A:

	def __init__(self):
		pass

	@staticmethod
	def f():
		pass


import weakref


class Foo(object):

    def __init__(self):
        self.text = "Hello World"
        self.bar = Bar(self)


class Bar(object):
    def __init__(self, parent):
        self.parent = weakref.ref(parent)    # <= garbage-collector safe!
        self.newText = parent.text

foo = Foo()