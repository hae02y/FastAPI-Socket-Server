from fastapi import APIRouter
import csv, ast

from starlette.responses import FileResponse

router = APIRouter(prefix="/api")

from fastapi import APIRouter, Query
import csv, ast

@router.get("/polygons")
def get_polygons(ccm: int = Query(...)):
    polygons = []
    with open("static/parsed_info.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["ccm"]) != ccm:
                continue
            coords = ast.literal_eval(row["coords"])
            if coords == [(0, 0), (0, 0), (0, 0), (0, 0)]:
                continue
            polygons.append({
                "ccm": f"{row['ccm']}",
                "label": f"{row['ccm']},{row['scm']},{row['usm']}",
                "points": coords
            })
    return polygons

@router.get("/")
def serve_index():
    return FileResponse("static/index.html")
