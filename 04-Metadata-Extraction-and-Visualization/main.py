from semmeta.metadata_extractor_module import SEMMetaData
from semmeta.json_cleaner_module import JSONReader
from semmeta.visualizer_module import Visualizer
def main():
    image_path = input("Provide image path:")

    semmetadata = SEMMetaData(image_path)
    json_path = semmetadata.GetInsMetadata()

    cleaner = JSONReader(json_path, json_path)

    cleaner.clean()
    cleaner.save()

    visualizer = Visualizer(json_path, image_path)

    visualizer.show_image()
    visualizer.display_table()
