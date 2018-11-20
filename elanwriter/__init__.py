import xml.etree.cElementTree as ET
import warnings
import collections
import sys
import os
import datetime

__version__ = "0.0.0.dev2"

class ElanDoc(object):

    def __init__(self, rel_video_url=""):

        self.LINGUISTIC_TYPE_REF = "default-lt"

        # Implement a time annotation here
        self.ann_doc = ET.Element("ANNOTATION_DOCUMENT", AUTHOR="",
                                  DATE=datetime.datetime.now().strftime("%y-%m-%dT%H:%M:%S"),
                                  FORMAT="3.0",
                                  VERSION="3.0")
        self.header = ET.SubElement(self.ann_doc, "HEADER",
                                    MEDIA_FILE="",
                                    TIME_UNITS="milliseconds")

        # Implement a correct video type implementation here
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

        # Implement that you only write an empty tier if the file is indeed empty
        self.tiers = {"default": ET.SubElement(self.ann_doc,
                                   "TIER",
                                   LINGUISTIC_TYPE_REF=self.LINGUISTIC_TYPE_REF,
                                   TIER_ID="default")}

        self.time_slot_i = 1
        self.annotation_i = 1

    def add_annotation(self, time_tuple, annotation_text, tier_name="default"):
        # Parameter checking
        if not isinstance(annotation_text, str):
            try:
                warnings.warn("Cast annotation_text variabel of add_annotation from "+str(type(annotation_text))+" to string")
                annotation_text = str(annotation_text)
            except Exception as e:
                raise e

        if not isinstance(tier_name, str):
            try:
                warnings.warn("Cast tier_name variabel of add_annotation from "+str(type(tier_name))+" to string")
                tier_name = str(tier_name)
            except Exception as e:
                raise e
        
        if not isinstance(time_tuple, collections.Iterable):
            raise Exception("The time_tuple given to add_annotation is not an iterable (annotation_text="+annotation_text+")")
        elif len(time_tuple) != 2:
            raise Exception("The time_tuple given to add_annotation is not of length 2 (annotation_text="+annotation_text+", length="+str(len(time_tuple))+")")


        # Make a new tier in the XML file if it does not exist
        if tier_name not in self.tiers:
            self.tiers.update({tier_name:
                                ET.SubElement(self.ann_doc,
                                              "TIER",
                                              LINGUISTIC_TYPE_REF=self.LINGUISTIC_TYPE_REF,
                                              TIER_ID=tier_name)
                              })

        # Add the times to the time slot
        ET.SubElement(self.time_order, "TIME_SLOT",
                      TIME_SLOT_ID="ts"+str(self.time_slot_i),
                      TIME_VALUE=str(int(time_tuple[0])))
        ts1 = self.time_slot_i
        self.time_slot_i += 1
        ET.SubElement(self.time_order, "TIME_SLOT",
                      TIME_SLOT_ID="ts"+str(self.time_slot_i),
                      TIME_VALUE=str(int(time_tuple[1])))
        ts2 = self.time_slot_i
        self.time_slot_i += 1

        # Add the annotations to the tier
        ann = ET.SubElement(self.tiers[tier_name], "ANNOTATION")
        ann_align = ET.SubElement(ann, "ALIGNABLE_ANNOTATION",
                                  ANNOTATION_ID="a"+str(self.annotation_i),
                                  TIME_SLOT_REF1="ts"+str(ts1),
                                  TIME_SLOT_REF2="ts"+str(ts2))
        ET.SubElement(ann_align, "ANNOTATION_VALUE").text = annotation_text

    def dump(self):
        tree = ET.ElementTree(self.ann_doc)
        ET.dump(tree)

    def _get_doc(self):
        return self.ann_doc

    def write(self, filename="output.eaf"):
        tree = ET.ElementTree(self.ann_doc)
        tree.write(filename)

    # END CLASS ELANDOC

def write_elan_file(detections, video_path, output_path, feature_col_name):
      ##
    # Make the Elan file
    ##
    video_dir = os.path.dirname(video_path)
    video_filename = os.path.basename(video_path)

    output_dir = os.path.dirname(output_path)
    output_filename = os.path.basename(output_path)

    if video_dir == "":
        video_dir = "."

    if os.path.isfile(video_path):
        rel_video_path = os.path.join( os.path.relpath(video_dir, output_dir), video_filename )
    else:
        #warnings.warn("No video file found for the elan file. Video file: {}".format(video_path))
        rel_video_path = "video_not_found"

    #if not column_selection:
    column_selection = set(detections[feature_col_name])

    ed = ElanDoc(rel_video_path)
  
    ##
    # Start looping over the FEATURES
    for feat in column_selection:
      
        times = detections[detections[feature_col_name] == feat]
        for i in range(len(times)):
            annotation_name = times.iloc[i][feature_col_name]
            #if "modifier" in times.columns:
            #    if times.iloc[i]["modifier"] and not np.isnan(times.iloc[i]["modifier"]):
            annotation_name = feat#"I="+str(times.iloc[i]["modifier"])

            ed.add_annotation((1000*times.iloc[i]["start"], 1000*times.iloc[i]["end"]), 
                            annotation_name, tier_name=times.iloc[i][feature_col_name])
        if len(times) == 0:
            ed.add_annotation((0,0.1), 
                                "", feat)

    ed.write(output_path)