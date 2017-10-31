from write_elan_eaf_files import ElanDoc

ed = ElanDoc()
ed.add_annotation((0,1000), "Happy", tier_name="visual")
ed.add_annotation((200,1100), "Talking", tier_name="audio")
ed.dump()
ed.write("test.eaf")