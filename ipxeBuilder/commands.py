class Command:
	def __init__(self, *args):
		self.args=args


	def code(self):
		return "echo Base command"


class Chain(Command):

	def code(self):
		return f"chain {self.args[0]}"

class Echo(Command):
	def code(self):
		return f"echo {self.args[0]}"


class Item(Command):
	def function(self, fn):
		self.func=fn

	def func(self):
		return [Echo("No function!")]

	def func_data(self):
		return f":{self.func.__name__}"+"\n"+'\n'.join([i.code() for i in self.func()])

	def code(self):
		return f'item {self.func.__name__} {self.args[0]}'



class Menu(Command):
	items=[]
	def item(self, item:Item):
		self.items.append(item)

	def code(self):
		x="menu "+self.args[0]+"\n"
		x+='\n'.join([item.code() for item in self.items])+"\nchoose item\ngoto ${item}\n" 
		x+='\n'.join([item.func_data() for item in self.items])+"\n"
		return x


class Loader(Command):
	def __init__(self, *args):
		self.args=[]
		self.initrds=[]
		self.kernel_path=""

	def initrd(self, path):
		self.initrds.append(path)

	def kernel(self, path):
		self.kernel_path=path

	def code(self):
		ret=f"kernel {self.kernel_path} "
		for i in self.initrds:
			d=i.split("/")[-1]
			ret += f" initrd={d}"
		for i in self.initrds:
			ret+=f"\ninitrd {i}"
		ret+="\nboot\n"
		return ret

class Wimboot(Command):
    def __init__(self, bcd, bootsdi, wimfile, wimfilename="boot.wim"):
        super().__init__()
        self.bcd, self.bootsdi, self.wimfile, self.wimfilename = bcd, bootsdi, wimfile, wimfilename
    
    def code(self):
        return """kernel /windows/wimboot
initrd {} BCD
initrd {} boot.sdi
initrd /windows/bootmgr bootmgr
initrd -n {} {} {}
boot""".format(self.bcd, self.bootsdi, self.wimfilename, self.wimfile, self.wimfilename)