from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "It works!"}

@app.get("/datasets")
def datasets():
    return {"message": "datasets_list"}

@app.get("/datasets/{dataset_id}")
def dataset(dataset_id: int):
    return {"message": f"dataset_{dataset_id}"}