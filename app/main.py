from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routers import reports


app = FastAPI()
app.include_router(reports.router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(req: Request):
    return templates.TemplateResponse("root.html", {"request": req})


# users = [
#     {"name": "John", "email": "john@gmail.com"},
#     {"name": "Maria", "email": "maria@gmail.com"},
#     {"name": "Hector", "email": "hector@gmail.com"},
#     {"name": "Lisa", "email": "list@gmail.com"},
# ]


# @app.get("/users", response_class=HTMLResponse)
# async def get_users(req: Request):
#     return templates.TemplateResponse(
#         "users/index.html", {"request": req, "users": users}
#     )


# @app.post("/users", response_class=HTMLResponse)
# async def post_users(req: Request):
#     data = await req.form()
#     formdata = jsonable_encoder(data)
#     users.append(formdata)
#     print(users)
#     return templates.TemplateResponse(
#         "users/index.html", {"request": req, "users": users}
#     )
