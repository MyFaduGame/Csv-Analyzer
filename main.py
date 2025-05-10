import os
import uuid
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import openai, uvicorn, requests

# === Configuration ===
openai.api_key = 'OPENAI_API_KEY'

UPLOAD_DIR = "uploads"
GRAPH_DIR = "graphs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

data_store = {}

# === FastAPI Setup ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Serve Graph Images ===
app.mount("/graphs", StaticFiles(directory=GRAPH_DIR), name="graphs")

# === Upload CSV and Analyze ===
@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)
    data_store[file_id] = df

    csv_summary = generate_csv_summary(df)
    explanation = await ask_chatgpt(f"Analyze this CSV summary and explain it:\n{csv_summary}")
    graphs = generate_graphs(df, file_id)

    return {
        "file_id": file_id,
        "chatgpt_explanation": explanation,
        "graph_paths": [f"/graphs/{os.path.basename(p)}" for p in graphs],
        "columns": df.columns.tolist()
    }

# === Ask Question About CSV ===
@app.post("/ask/{file_id}")
async def ask_about_csv(file_id: str, payload: dict):
    if file_id not in data_store:
        return JSONResponse(status_code=404, content={"error": "File ID not found"})

    df = data_store[file_id]
    question = payload.get("question", "")
    if not question:
        return JSONResponse(status_code=400, content={"error": "Question required"})

    csv_summary = generate_csv_summary(df)
    prompt = f"Dataset summary:\n{csv_summary}\n\nUser's question:\n{question}"
    answer = await ask_chatgpt(prompt)

    return {"answer": answer}

# === CSV Summary Helper ===
def generate_csv_summary(df: pd.DataFrame) -> str:
    summary = {
        "columns": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "stats": df.describe(include="all").fillna("").to_dict()
    }
    return json.dumps(summary)

# === Graph Generator ===
def generate_graphs(df: pd.DataFrame, file_id: str):
    graph_paths = []

    for column in df.columns:
        try:
            if pd.api.types.is_numeric_dtype(df[column]):
                plt.figure()
                sns.histplot(df[column].dropna(), kde=True)
                file_name = f"{file_id}_{column}_hist.png"
            elif df[column].nunique() <= 10:
                plt.figure()
                df[column].value_counts().plot.pie(autopct="%1.1f%%")
                plt.ylabel("")
                file_name = f"{file_id}_{column}_pie.png"
            else:
                continue

            path = os.path.join(GRAPH_DIR, file_name)
            plt.title(f"{column} Visualization")
            plt.savefig(path)
            plt.close()
            graph_paths.append(path)
        except Exception as e:
            print(f"Error generating graph for {column}: {e}")

    return graph_paths

# === ChatGPT Integration ===
async def ask_chatgpt(prompt: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a data analyst. Explain and answer questions about user datasets."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    return result["choices"][0]["message"]["content"]

# === Run Server ===
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
