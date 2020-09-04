import json
import os
from os import path

DIRECTORY = "./images"

def create_info():
    return {
        "year": 2020,
        "version": "0.1.0",
        "description": "PlantVillage dataset in COCO format",
        "contributor": "Jonah Henriksson"
    }

def add_image(file_path):
    return {
        "id": int(path.basename(file_path).rsplit("-", 1)[1].split(".")[0]),
        "width": 256,
        "height": 256,
        "file_name": path.basename(file_path),
        "license": 1
    }

def create_license():
    return {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)",
        "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/"
    }

def create_annotation(file_path, categories):
    category = path.basename(file_path).rsplit("-",1)[0]
    if category in categories:
        category_id = categories[category]["id"]
        id_ = int(path.basename(file_path).rsplit("-", 1)[1].split(".")[0])
        return {            
            "id": id_,
            "image_id": id_,
            "category_id": category_id,
            "segmentation": [],
            "area": 65536,
            "bbox": [0, 0, 256, 256],
            "iscrowd": 0,
            "ignore": 0,
        }
    else:
        num = len(categories) + 1
        id_ = int(path.basename(file_path).rsplit("-", 1)[1].split(".")[0])
        categories[category] = {
            "id": num,
            "name": category,
            "supercategory": "none"
        }
        category_id = categories[category]["id"]
        return {            
            "id": id_,
            "image_id": id_,
            "category_id": category_id,
            "segmentation": [],
            "area": 65536,
            "bbox": [0, 0, 256, 256],
            "iscrowd": 0,
            "ignore": 0,
        }

if __name__ == "__main__":
    file = {
        "info": create_info(),
        "type": "instances",
        "licenses": [create_license()],
        "images": [],
        "annotations": [],
        "categories": []
    }
    categories = {}
    for entry in os.scandir(DIRECTORY):
        if entry.path.endswith(".jpg") and entry.is_file():
            file["images"].append(add_image(entry.path))
            file["annotations"].append(create_annotation(entry.path, categories))
    file["categories"] = list(categories.values())
    with open(path.join(DIRECTORY, "_dataset.json"), "w") as f:
        json.dump(file, f)
    