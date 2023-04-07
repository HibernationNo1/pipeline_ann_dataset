db = dict(
    host=None, 
    port=None, 
    user='hibernation', 
    db_name='pipeline_database',      
    charset='utf8',   
    
    table = dict(
        # name of `annotations data`` table     
        # annotations data: dataset made with labelme.exe
        anns = "ann_data",      
        anns_schema = f"""
                              CREATE TABLE ann_data (
                              id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                              json_name VARCHAR(200) NOT NULL,
                              image_name VARCHAR(200) NOT NULL,
                              category VARCHAR(20) NOT NULL,
                              ann_version VARCHAR(10) NOT NULL,
                              PRIMARY KEY(id)
                              );
                              """,
            # json_name: path of json file
            # image_name: path of image file
            # category: category of dataset
            # ann_version: version of annotation dataset
    
        # name of `image dataset`` table.     
        # image dataset: images for training or validation
        image_data = "image_data",    
        image_data_schema = f"""
                                      CREATE TABLE image_data (
                                      id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                                      dataset_purpose VARCHAR(10) NOT NULL,     # rename to purpose
                                      image_name VARCHAR(200) NOT NULL,
                                      record_file VARCHAR(200) NOT NULL, 
                                      category VARCHAR(20) NOT NULL,
                                      train_version VARCHAR(10) NOT NULL,
                                      PRIMARY KEY(id)
                                      );
                                      """,
            # dataset_purpose: one of `train` and `val`
            # image_name: path of image data file for train or validation
            # category: category of dataset
            # train_version: version of recorded dataset 
        
        # name of `recorded dataset` table
        # recorded dataset: dataset that combines annotations data into a single file 
        train_data = "train_data",      
        train_data_schema = f"""     
                                      CREATE TABLE train_data (
                                      id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                                      dataset_purpose VARCHAR(10) NOT NULL,
                                      category VARCHAR(20) NOT NULL,
                                      record_file VARCHAR(200) NOT NULL,
                                      train_version VARCHAR(10) NOT NULL,
                                      PRIMARY KEY(id)
                                      );
                                      """
            # dataset_purpose: one of `train` and `val`
            # record_file: path of record dataset file(.json format). 
            #              are for train or validation(e.g. train_dataset.json or val_data.json)
            # category: category of dataset
            # train_version: version of recorded dataset 
    )

)