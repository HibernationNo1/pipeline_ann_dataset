from hibernation_no1.database.mysql import create_table
        
def whether_run_commit(cfg, database, image_list):
    print(f" >> confirm before commit to database: {cfg.db.db_name}")
    print(f" >>     number of images: {len(image_list)}")
    print(f" >>     category of dataset: {cfg.dvc.dataset_cate}")
    print(f" >>     version of annotations dataset: {cfg.dvc.ann.version}")
    print(f" >>\n           enter 'y' to commit ")
    commit = input()
    
    if commit in ["y", "Y", "yes"]: 
        print(" >>          run commit!")
        database.commit()
    else:
        print(f" >>     user enter `{commit}`, not commit to database...  ")