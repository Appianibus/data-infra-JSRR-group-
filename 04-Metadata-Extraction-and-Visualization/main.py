from semmeta.metadata_extractor_module import SEMMetaData
from semmeta.json_cleaner_module import JSONReader
from semmeta.visualizer_module import Visualizer
def main():
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
        json_path = semmetadata.GetInsMetadata()

    cleaner = JSONReader(json_path, json_path)

    cleaner.clean()
    cleaner.save()

    visualizer = Visualizer(json_path, image_path)

    visualizer.show_image()
    visualizer.display_table()



