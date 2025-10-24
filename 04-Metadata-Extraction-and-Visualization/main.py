from semmeta.metadata_extractor_module import SEMMetaData
from semmeta.json_cleaner_module import JSONReader
from semmeta.visualizer_module import Visualizer

import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as pltimg

def main():
    output_file = None
    image_path = input("Provide image path:")

    sem = SEMMetaData(image_path)

        # 3. Open the image
    img = sem.OpenCheckImage(image_path)
    
    # Proceed only if image opened successfully
    if img is not None:
    
        # 4. Extract raw metadata
        raw_metadata, image_tags = sem.ImageMetadata(img)
        #print("✅ Raw metadata keys:", raw_metadata)
    
        # 5. Extract standard EXIF metadata
        exif_keys, exif_numbers = sem.SEMEXIF()
        found_exif, missing_exif = sem.GetExifMetadata(img, exif_keys, exif_numbers)
        exif_dict = sem.ExifMetaDict(found_exif, missing_exif)
    
        # Optional: print EXIF metadata
        #print("✅ EXIF metadata sample:", exif_dict)
    
        # 6. Extract SEM instrument metadata (tag 34118)
        sem_meta_list = sem.GetInsMetadata()
        sem_dict = sem.InsMetaDict(sem_meta_list)
        #print("✅ SEM instrument metadata:", sem_dict)
    
        # 7. Combine EXIF + SEM metadata
        #combined_metadata = {"EXIF": exif_dict, "SEM_Instrument": sem_dict}
    
        output_file = sem.final_out_json()
        print(f"✅ Metadata saved to {output_file}")
        

    cleaner = JSONReader(output_file, output_file)

    cleaner.clean()
    cleaner.save()

    visualizer = Visualizer(output_file, image_path)

    visualizer.show_image()
    visualizer.display_table()

main()



