#write a python class for extraction and visualization
class Visualizer:
    
    keys = ["AP_WD", "AP_BEAM_TIME", "AP_IMAGE_PIXEL_SIZE", "AP_HOLDER_HEIGHT", "AP_BEAM_CURRENT", "AP_HOLDER_DIAMETER"]

    def __init__(self, json_path, image_path):
        self.json_path = json_path
        self.image_path = image_path
        


    def extract_features(self):
        with open(self.json_path, "r") as f:
            data = json.load(f)
        

        extracted_features = {}

        for k in self.keys:
            extracted_features[k] = data[k]

        return extracted_features 
    
    def show_image(self):
        image = pltimg.imread(self.image_path)
        plt.imshow(image)
        plt.show()

    def display_table(self):
        data_values = []
        features = self.extract_features()
        for k in self.keys:
            x = features[k]
            data_values.append(x)

        variables = []
        measures = []
        values = []

        for d in data_values:
            temp = d.split("=")
            variables.append(temp[0].strip())
            
            temp2 = temp[1].strip().split(" ")
            values.append(temp2[0])
            measures.append(temp2[1])

        dataframe = pd.DataFrame({
            "Variables" : variables,
            "Values": values,
            "Measures": measures
        })
            
        return dataframe 
