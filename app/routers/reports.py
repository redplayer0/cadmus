from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from libs.personal_report import generate_personal_report

print(generate_personal_report)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/personal_report", response_class=HTMLResponse)
async def get_personal_report(req: Request):
    return templates.TemplateResponse("personal_report_form.html", {"request": req})


@router.post("/personal_report")
async def post_personal_report(req: Request):
    data = await req.form()
    formdata = jsonable_encoder(data)
    doc = generate_personal_report(formdata)
    response = Response(content=doc.read(), media_type="application/pdf")
    response.headers["Content-Disposition"] = 'attachment; filename="report.pdf"'

    return response
