import xml.etree.cElementTree as ET
# import main


class ElanDoc(object):

    def __init__(self, rel_video_url=""):# , tier_name="default"):

        self.LINGUISTIC_TYPE_REF = "default-lt"

        self.ann_doc = ET.Element("ANNOTATION_DOCUMENT", AUTHOR="",
                                  DATE="2017-10-26T14:58:41+01:00",
                                  FORMAT="3.0",
                                  VERSION="3.0")
        self.header = ET.SubElement(self.ann_doc, "HEADER",
                                    MEDIA_FILE="",
                                    TIME_UNITS="milliseconds")

        ET.SubElement(self.header, "MEDIA_DESCRIPTOR",
                        MEDIA_URL="file:///./"+rel_video_url,
                        MIME_TYPE="video/mp4",
                        RELATIVE_MEDIA_URL="./"+rel_video_url)

        ET.SubElement(self.ann_doc, "LINGUISTIC_TYPE",
                      GRAPHIC_REFERENCES="false",
                      LINGUISTIC_TYPE_ID="default-lt",
                      TIME_ALIGNABLE="true")
        ET.SubElement(self.ann_doc, "LOCALE",
                      COUNTRY_CODE="US",
                      LANGUAGE_CODE="en")

#         <CONSTRAINT DESCRIPTION="Time subdivision of parent annotation's time interval, no time gaps allowed within this interval" STEREOTYPE="Time_Subdivision"/>
#         <CONSTRAINT DESCRIPTION="Symbolic subdivision of a parent annotation. Annotations refering to the same parent are ordered" STEREOTYPE="Symbolic_Subdivision"/>
#         <CONSTRAINT DESCRIPTION="1-1 association with a parent annotation" STEREOTYPE="Symbolic_Association"/>
#         <CONSTRAINT DESCRIPTION="Time alignable annotations within the parent annotation's time interval, gaps are allowed" STEREOTYPE="Included_In"/>

        self.time_order = ET.SubElement(self.ann_doc,
                                        "TIME_ORDER")

        self.tiers = {"default": ET.SubElement(self.ann_doc,
                                   "TIER",
                                   LINGUISTIC_TYPE_REF=self.LINGUISTIC_TYPE_REF,
                                   TIER_ID="default")}

        self.time_slot_i = 1
        self.annotation_i = 1

    def add_annotation(self, time_tuple, annotation_text, tier_name="default"):
        if tier_name not in self.tiers:
            self.tiers.update({tier_name:
                                ET.SubElement(self.ann_doc,
                                              "TIER",
                                              LINGUISTIC_TYPE_REF=self.LINGUISTIC_TYPE_REF,
                                              TIER_ID=tier_name)
                              })

        ET.SubElement(self.time_order, "TIME_SLOT",
                      TIME_SLOT_ID="ts"+str(self.time_slot_i),
                      TIME_VALUE=str(time_tuple[0]))
        ts1 = self.time_slot_i
        self.time_slot_i += 1
        ET.SubElement(self.time_order, "TIME_SLOT",
                      TIME_SLOT_ID="ts"+str(self.time_slot_i),
                      TIME_VALUE=str(time_tuple[1]))
        ts2 = self.time_slot_i
        self.time_slot_i += 1

        ann = ET.SubElement(self.tiers[tier_name], "ANNOTATION")
        ann_align = ET.SubElement(ann, "ALIGNABLE_ANNOTATION",
                                  ANNOTATION_ID="a"+str(self.annotation_i),
                                  TIME_SLOT_REF1="ts"+str(ts1),
                                  TIME_SLOT_REF2="ts"+str(ts2))
        ET.SubElement(ann_align, "ANNOTATION_VALUE").text = annotation_text

    def dump(self):
        tree = ET.ElementTree(self.ann_doc)
        ET.dump(tree)

    def write(self, filename="output.eaf"):
        tree = ET.ElementTree(self.ann_doc)
        tree.write(filename)
# ET.SubElement(doc, "field1", name="blah").text = "some value1"
# ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
