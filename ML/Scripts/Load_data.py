import os 

def load_data(DATA_PATH) :
    """
      téléchargement du dataset
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset introuvable : {DATA_PATH}")

    print(f" Dataset prêt : {DATA_PATH}")





if __name__=='__main__':
 data_path = "data/dataset.parquet"  

 path = load_data(data_path)
