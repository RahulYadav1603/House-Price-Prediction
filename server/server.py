from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import util

app = FastAPI()

# Mount static files directory for CSS, JS, images, etc.
app.mount("/static", StaticFiles(directory="client/static"), name="static")

# Set up Jinja2Templates for HTML templates
templates = Jinja2Templates(directory="client")

@app.get("/main", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})

@app.get("/get_location_names")
async def get_location_names():
    try:
        locations = util.get_location_names()
        return JSONResponse(content={'locations': locations})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_home_price")
async def predict_home_price(request: Request):
    try:
        data = await request.json()
        total_sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))

        if not location or total_sqft <= 0 or bhk <= 0 or bath <= 0:
            raise HTTPException(status_code=400, detail="Invalid input values.")

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        return JSONResponse(content={'estimated_price': estimated_price})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Call load_saved_artifacts when the app starts
@app.on_event("startup")
async def startup_event():
    util.load_saved_artifacts()
