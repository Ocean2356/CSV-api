from fastapi import FastAPI, File, UploadFile
from fastapi import Response
from fastapi.responses import JSONResponse
import pandas as pd
from pandas import DataFrame
import uuid

app = FastAPI()

datasets = {}

@app.get("/")
def home():
    return {"message": "It works!"}
    # return Response(content = "It works!", media_type = "text/plain")

@app.get("/datasets")
def list_dataset():
    if len(datasets) == 0: return {"message": "no_datasets"}
    filename_id = {datasets[i]["filename"][0]: str(i) for i in datasets}
    return {"message": "datasets_list", "datasets": filename_id}
    # return Response(content =  datasets, media_type = "application/json")

@app.delete("/datasets")
def clear_all_datasets():
    datasets.clear()
    return {"message": "datasets_cleared"}
    # return Response(headers = "datasets_cleared", media_type = "application/json")

@app.post("/datasets")
def create_dataset(dataset: UploadFile = File(...)):
    contents = dataset.file
    df = pd.read_csv(contents)
    df["filename"] = dataset.filename
    dataset_id = uuid.uuid4()
    datasets[dataset_id] = df
    return {"message": "dataset_created", "dataset_id": dataset_id}
    # return Response(headers = "dataset_created", content = {"dataset_id": dataset_id}, media_type = "application/json")

@app.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: uuid.UUID):
    if dataset_id not in datasets: return {"message": "dataset_not_found"}
    del datasets[dataset_id]
    return {"message": "dataset_deleted"}
    # return Response(content = "dataset_deleted", media_type = "text/plain")

    
# return the file name, and size of the dataset object
@app.get("/datasets/{dataset_id}")
def info_dataset(dataset_id: uuid.UUID):
    if dataset_id not in datasets: return {"message": "dataset_not_found"}
    return {"message": "dataset_info", "filename": datasets[dataset_id]["filename"][0], "size": datasets[dataset_id].shape[0]}
    # return Response(header = "dataset_info",
    #                 content = {"filename": datasets[dataset_id]["filename"][0], "size": datasets[dataset_id].shape[0]},
    #                 media_type = "application/json")