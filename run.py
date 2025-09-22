from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import customers, accounts, transactions, products, insurance, reminders, agent_actions, dashboard

app = FastAPI(title="Banking Chatbot Agent API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Routers
app.include_router(customers.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(products.router)
app.include_router(insurance.router)
app.include_router(reminders.router)
app.include_router(agent_actions.router)
app.include_router(dashboard.router)
