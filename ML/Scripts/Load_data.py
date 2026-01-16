import os 

def load_data(DATASET_PATH) :
    """
      téléchargement du dataset
    """
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset introuvable : {DATASET_PATH}")

    print(f" Dataset prêt : {DATASET_PATH}")





if __name__=='__main__':
 data_path = "data/dataset.parquet"  

 path = load_data(data_path)
