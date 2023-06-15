from fastapi import FastAPI, File, UploadFile
from fastapi import Response
from fastapi.responses import JSONResponse, FileResponse
import pandas as pd
from pandas import DataFrame
import uuid
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

app = FastAPI()

datasets = {}

# It works 
@app.get("/")
def home():
    return {"message": "It works!"}
    # return Response(content = "It works!", media_type = "text/plain")

# return the list of datasets
@app.get("/datasets")
def list_dataset():
    if len(datasets) == 0: return {"message": "no_datasets"}
    filename_id = {datasets[i]["filename"][0]: str(i) for i in datasets}
    return {"message": "datasets_list", "datasets": filename_id}
    # return Response(content =  datasets, media_type = "application/json")

# clear all datasets
@app.delete("/datasets")
def clear_all_datasets():
    datasets.clear()
    return {"message": "datasets_cleared"}
    # return Response(headers = "datasets_cleared", media_type = "application/json")

# create a dataset
@app.post("/datasets")
def create_dataset(dataset: UploadFile = File(...)):
    contents = dataset.file
    df = pd.read_csv(contents)
    df["filename"] = dataset.filename
    dataset_id = uuid.uuid4()
    datasets[dataset_id] = df
    return {"message": "dataset_created", "dataset_id": dataset_id}
    # return Response(headers = "dataset_created", content = {"dataset_id": dataset_id}, media_type = "application/json")

# delete a dataset
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

# return the dataset in excel format
@app.get("/datasets/{dataset_id}/excel")
def excel_dataset(dataset_id: uuid.UUID):
    if dataset_id not in datasets: return {"message": "dataset_not_found"}
    return {"message": "dataset_excel", "dataset_excel": datasets[dataset_id].to_csv()}

# return the stats of the dataset
@app.get("/datasets/{dataset_id}/stats")
def stats_dataset(dataset_id: uuid.UUID):
    if dataset_id not in datasets: return {"message": "dataset_not_found"}
    return {"message": "dataset_stats", "stats": datasets[dataset_id].describe()}

# return the dataset in pdf format
@app.get("/datasets/{dataset_id}/plot")
def plot_dataset(dataset_id: uuid.UUID):
    if dataset_id not in datasets: return {"message": "dataset_not_found"}
    df = datasets[dataset_id]
    tmp = "_histograms.pdf"
    pp = PdfPages(tmp)
    for col in df.select_dtypes(include="number").columns:
        plt.hist(df[col], bins=10)
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        pp.savefig(plt.gcf())
        plt.clf()
    pp.close()
    return FileResponse(tmp, media_type="application/pdf")
