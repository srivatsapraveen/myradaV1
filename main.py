from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import starlette.status as status
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse

from app.mob import mob_app
from app.web import web_app
from app.api import api_app

app = FastAPI()
app.mount("/mob", mob_app)
app.mount("/web", web_app)
app.mount("/api", api_app)
app.mount('/static', StaticFiles(directory="static"), name="site")
     
@app.get('/manifest.json')
def manifest():
    return FileResponse('static/manifest.json')

@app.get('/sw.js')
def service_worker():
    return FileResponse('static/sw.js')
     
def isMobileDevice(request): 
  result = False 
  #devices = ["Android", "webOS", "iPhone", "iPad", "iPod", "BlackBerry", "IEMobile", "Opera Mini"]
  devices = ["Android", "iPhone", "iPad"] 
  if any (device in request.headers['user-agent'] for device in devices): result = True 
  return result
    
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print (request.headers['user-agent'])
    #response.headers['Service-Worker-Allowed'] = '/'
    if (isMobileDevice(request)):
        return RedirectResponse('/mob',status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse('/web',status_code=status.HTTP_302_FOUND)
 
