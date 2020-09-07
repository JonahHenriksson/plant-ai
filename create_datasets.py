import os
import re
from shutil import copyfile

IMAGES_DIR = "./images"
TRAIN_DIR = "./train-images"
TEST_DIR = "./test-images"

if __name__ == "__main__":
    print("Creating Training and Testing Sets")
    files = os.listdir(IMAGES_DIR)

    classes = {}

    for f in files:
        m = re.search("[^-]+-[^-]+", f)
        if m:
            class_prefix = m.group(0)
            if class_prefix in classes:
                classes[class_prefix] += 1 
            else:
                classes[class_prefix] = 0
    
    template = "{}-{:06d}.jpg"
    total_num = 0
    train_num = 0
    test_num = 0
    for class_prefix in classes:
        print("{}: {:06d} images".format(class_prefix, classes[class_prefix]))
        num = int(classes[class_prefix] * 0.7)
        for train_index in range(num):
            old_name = template.format(class_prefix, total_num)
            train_name = template.format(class_prefix, train_num)
            old_file = os.path.join(IMAGES_DIR, old_name)
            train_file = os.path.join(TRAIN_DIR, train_name)
            copyfile(old_file, train_file)
            train_num += 1
            total_num += 1
        
        for test_index in range(num, classes[class_prefix]+1):
            old_name = template.format(class_prefix, total_num)
            test_name = template.format(class_prefix, test_num)
            old_file = os.path.join(IMAGES_DIR, old_name)
            test_file = os.path.join(TEST_DIR, test_name)
            copyfile(old_file, test_file)
            test_num += 1
            total_num += 1
    
    print("Finished")
    
