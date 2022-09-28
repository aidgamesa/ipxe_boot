from ipxeBuilder import Builder, Menu, Item, Wimboot, Loader
import os

class Start:
	def code():
		return ":start"

builder=Builder()
builder.add(Start)

menu=Menu("menu")

item=Item("debian stable")
@item.function
def simple():
	loader=Loader()
	type="stable"
	base=f"http://ftp.debian.org/debian/dists/{type}/main/installer-amd64/current/images/netboot/debian-installer/amd64"
	loader.kernel(f"{base}/linux")
	loader.initrd(f"{base}/initrd.gz")
	loader.initrd(f"{base}/initrd.gz")
	return loader,

menu.item(item)

item=Item("windows 7 pe (BETA)")
@item.function
def w7pe():
    baseurl="/windows/w7pe"
    loader=Wimboot(
        baseurl+"/BCD",
        baseurl+"/boot.sdi",
        baseurl+"/XM86.wim",
        "XM86.wim"
    )
    return loader,

menu.item(item)

builder.add(menu)

def app(environ, start_response):

  #data = f"Hello, {environ['RAW_URI']}!\n{builder.build()}".encode()
  data=builder.build().encode()
  url=environ['RAW_URI'][1:]
  if url.split("/")[0]=="windows":
    file=url
    if os.path.isfile(file):
      with open(file, "rb") as f:
        data=f.read()
    else:
      data="404 NOT FOUND".encode()
  #data=url.encode()
  start_response("200 OK", [
    ("Content-Type", "text/plain"),
    ("Content-Length", str(len(data)))
  ])
  
  return iter([data])
