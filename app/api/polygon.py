from fastapi import APIRouter
import csv, ast

from starlette.responses import FileResponse

router = APIRouter(prefix="/canvas")

from fastapi import APIRouter, Query
import csv, ast

@router.get("/polygons")
def get_polygons(ccm: int = Query(...)):
    polygons = []
    with open("static/parsed_info.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row["ccm"])+1 != ccm:
                continue
            coords = ast.literal_eval(row["coords"])
            if coords == [(0, 0), (0, 0), (0, 0), (0, 0)]:
                continue

            ccm = int(row['ccm']) + 1
            scm = int(row['scm']) + 1
            usm = int(row['usm']) + 1

            print(f"{ccm},{scm},{usm}")

            polygons.append({
                "label": f"{ccm},{scm},{usm}",
                "points": coords
            })
    return polygons

@router.get("")
def serve_index():
    return FileResponse("static/index.html")
