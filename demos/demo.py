from elanwriter import ElanDoc

class iets(object):
	def niks(self):
		print("niks")


ed = ElanDoc()
ed.add_annotation((int(31.0), int(2359.0)), "iets")
# ed.add_annotation((0,1000), "Happy", tier_name="visual")
# ed.add_annotation((200,1100), "Talking", tier_name="audio")
# ed.add_annotation((200,1100), iets(), tier_name="audio")
# try:
# 	ed.add_annotation([2000], "foutje", tier_name="audio")
# except Exception as e:
# 	print(".")


#ed.dump()
ed.write("test.eaf")