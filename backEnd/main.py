from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
import polars as pl

app = FastAPI()

# Carga y transforma el archivo CSV a Parquet
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    df = pl.read_csv(content)
    df.write_parquet("data.parquet")
    return {"message": "File uploaded and converted to parquet successfully!"}

# Consulta la información y devuelve las métricas solicitadas
@app.get("/metrics/")
async def get_metrics():
    lazy_frame = pl.scan_parquet("data.parquet")
    metrics = {}

    # Lista de campos a analizar
    fields = [
        "compactness", "circularity", "distance_circularity", "radius_ratio",
        "pr.axis_aspect_ratio", "max.length_aspect_ratio", "scatter_ratio",
        "elongatedness", "pr.axis_rectangularity", "max.length_rectangularity",
        "scaled_variance", "scaled_variance.1", "scaled_radius_of_gyration",
        "scaled_radius_of_gyration.1", "skewness_about", "skewness_about.1",
        "skewness_about.2", "hollows_ratio"
    ]

    # Calcula la desviación estándar
    for field in fields:
        grouped_std = lazy_frame.groupby("class").agg(pl.col(field).std().alias(field))
        metrics[field] = grouped_std.collect().to_pandas().to_dict(orient="records")

    return metrics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
