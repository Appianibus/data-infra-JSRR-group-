#write python class that read a .tif file
#write python class that read a .tif file
import os, sys, glob
#import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ExifTags #Image processing and metadata
import json
import re

# Class Initialization

class SEMMetaData:
    def __init__(self, image_metadata={}, semext=('tif','TIF'), semInsTag=[34118]):
        #semext is a tuple corresponding to the valid extension, 34118 is a TIFF tag ofte used by SEM instruments to store extra data
        #define  the following attributes: semext, image_megadata, semInsTag, images_tags (array to store image tag values)
        self.image_metadata = image_metadata
        self.semext = semext
        self.semInsTag = semInsTag
        self.images_tags = [] #it stores as an array 

    def OpenCheckImage(self, image):

        try:
            img = Image.open(image)
            print(f"✅ Image opened successfully: {image}")
            return img
        
        except Exception as e:
            print(f"⚠️ Error opening image '{image}': {e}")
            return None

    def ImageMetadata(self, img):
        """
        Extracts raw metadata from image,
        including tag identifiers 34118
        tip: use img.tag
        """

        self.image_metadata = img.tag
        self.image_tags = np.array(self.image_metadata)
        return self.image_metadata, self.image_tags


    def SEMEXIF(self):

        """
        Provides access to standard EXIF tag mappings from PIL.

        Returns:
            - exif_keys (list): Human-readable EXIF tag names
            - exif_number (list): Corresponding numeric tag identifiers used in image metadata.
        """

        # Get the PIL EXIF tag dictionary to map names to numeric keys
        exif_dict = {k: v for v, k in ExifTags.TAGS.items()}
        # or
        #exif_dict = dict([ (k, v) for v, k in ExifTags.TAGS.items() ])

        # Extract all tag names (keys) from the reversed dictionary
        exif_keys = [key for key in exif_dict]

        # Extract corresponding numeric identifiers for each tag name
        exif_number = [exif_dict[k] for k in exif_keys]
        return exif_keys, exif_number

    # Extract Standard EXIF Metadata from SEM Image


    def GetExifMetadata(self, img, exif_keys, exif_number):

        """
        Extracts standard EXIF metadata from a SEM image.
        """

        # based on std EXIF TAGS (from PIL), we store exif metadata in found_exif_metadata variable
        found_exif_metadata=[(img.tag[idx][:], word) for idx, word in zip(exif_number, exif_keys) if idx in self.image_tags]

        # if the key is not available in the image save its value as none
        none_exif_metadata = [(word, None) for num, word in zip(exif_number, exif_keys)  if num not in self.image_tags]
        return found_exif_metadata, none_exif_metadata

    # Construct Unified EXIF Metadata Dictionary
    def ExifMetaDict(self, found_exif_metadata, none_exif_metadata):

        """
        Creates a unified dictionary from found and missing EXIF metadata entries.
        Returns:
            - dict: Combined dictionary of EXIF metadata, excluding 'ColorMap' entries.
        """

        found_metadict = dict((subl[1], subl[0][0]) for subl in found_exif_metadata if subl[1]!="ColorMap")
        none_metadict = dict((subl[0], subl[1]) for subl in none_exif_metadata if subl[0]!="ColorMap")
        allexif_metadict = {**found_metadict, **none_metadict}
        return allexif_metadict

    

    

    
    def clean_instrument_metadata(self, raw_text):
        """
        Cleans and converts the SEM metadata string into key-value pairs.
        """
        pattern = re.compile(r"([A-Za-z0-9_\-\. %\(\)]+?)\s*=\s*([^\=]+?)(?=\s+[A-Z]{2,3}[_A-Z0-9]+|$)")
        metadata = {}
        for key, value in pattern.findall(raw_text):
            key = re.sub(r'\s+', ' ', key).strip()
            value = value.strip()
            metadata[key] = value
        return metadata

    
    def GetInsMetadata(self):
        tag = self.semInsTag[0]  # usually 34118
        if tag not in self.image_metadata:
            return []

        raw_data = self.image_metadata[tag]

        # If tuple, take first element
        if isinstance(raw_data, tuple) and len(raw_data) > 0:
            raw_data = raw_data[0]

        # Decode bytes if necessary
        if isinstance(raw_data, (bytes, bytearray)):
            raw_data = raw_data.decode(errors="ignore")

        # Replace line breaks, remove null chars
        text = str(raw_data).replace("\r", " ").replace("\n", ";,|").replace("\x00", "")

        # Split on common delimiters ; or , or | 
        parts = re.split(r"[;,|]", text)
        cleaned_list = [p.strip() for p in parts if p.strip()]

        return cleaned_list


    def InsMetaDict(self, ins_list):
        """
        Convert cleaned list into dictionary, normalize keys and values.
        """
        if not ins_list:
            return {}

        ins_dict = {}
        for item in ins_list:
            # Split by = or : (first occurrence only)
            if "=" in item:
                key, value = item.split("=", 1)
            elif ":" in item:
                key, value = item.split(":", 1)
            else:
                key, value = item, None

            key = key.strip().title()  # normalize capitalization
            value = value.strip() if value else None

            # Remove trailing units and spaces
            if value:
                value = re.sub(r"\s+", " ", value)
                value = value.replace("mm", "").replace("kV", "").replace("x", "").strip()

            # Avoid duplicates by checking existing key
            if key in ins_dict:
                key = key + "_2"

            ins_dict[key] = value

        return ins_dict




    # Open file in write mode and Export SEM Metadata to JSON Format with json.dump
    #def WriteSEMJson(self,file, semdict):
       # with open(file, "w") as semoutfile:
        #    json.dump(semdict, semoutfile)
        #return

    def clean_instrument_metadata(raw_text):
    # Remove weird prefixes like "DP_", "AP_", etc., but keep meaningful words
    # Split on known separators like " = " or ":", ensuring we get key-value pairs
        pattern = re.compile(r"([A-Za-z0-9_\-\. %\(\)]+?)\s*=\s*([^\n]+)")
        metadata = {}
        for match in pattern.findall(raw_text):
            key = re.sub(r'\s+', ' ', match[0]).strip()
            value = match[1].strip()
            metadata[key] = value
        return metadata

    # Example usage
        raw_data = """DP_EHT_VAC_READY EHT Vac ready = Yes DP_FIB_MODE FIB Mode = Imaging AP_MAG Mag = 14.63 K X AP_WORKING_DISTANCE WD = 3.198"""
        cleaned_dict = clean_instrument_metadata(raw_data)

    # Save to JSON (optional)
        with open("cleaned_metadata.json", "w") as f:
            json.dump(cleaned_dict, f, indent=4)

        print(len(cleaned_dict), "entries cleaned")



  # 8. Save combined metadata to JSON
    def final_out_json(self):
        out = self.InsMetaDict(self.GetInsMetadata())
        output_file = "output/sample_image_metadata.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:

            json.dump(out, f, indent=4, ensure_ascii=False)

        return (output_file)

        # Open file in write mode and Export SEM Metadata to JSON Format with json.dump
    def WriteSEMJson(self,file, semdict):
        with open(file, "w") as semoutfile:
            json.dump(semdict, semoutfile)
        return
