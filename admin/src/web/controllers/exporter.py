import pdfkit
import pandas as pd
from bs4 import BeautifulSoup
from flask import render_template, make_response, Response, url_for
import platform
import os
from src.core import image
from src.web.helpers.adaptators import generate_qr


# Socios downlad options
def pdf_report(socios):
    # Render
    options = {
        "enable-local-file-access": None,
        'encoding':'utf-8'
    }
    rendered = render_template('socios/export.html', socios=socios)

    # Windows
    if platform.system() == 'Windows':
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdf = pdfkit.from_string(rendered, False, options=options, configuration = config)
    # Linux or MacOs
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        pdf = pdfkit.from_string(rendered, False, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = "attachment; filename=listado-socios.pdf"

    return response

def csv_report(socios):
    def divide_chunks(l, n):
        new_rows = []
        for i in range(0, len(l), n):
            x= l[i:i + n]
            new_rows.append(x)
        return new_rows

    rendered = render_template('socios/export.html', socios=socios)
    soup = BeautifulSoup(rendered, 'html.parser')

    # Header
    headers = [th.text.replace('\n', '') for th in soup.select("th")]

    # Data
    rows = [td.text.replace('\n', '').replace(" ", "") for td in soup.select("td")]
    divided_rows = divide_chunks(rows, len(headers))
    
    df = pd.DataFrame(divided_rows, columns=headers)
    
    return Response(
        df.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=listado-socios.csv"}
    )

# Cuota recibo download options
def cuota_pdf_report(informacion):

    # Render
    options = {
        'enable-local-file-access': None,
        'encoding':'utf-8',
        'dpi': '300',
    }    
    rendered = render_template('cuotas/export_comprobante.html', comprobante=informacion, get_image_file_as_base64_data=get_image_file_as_base64_data)
    comp = os.path.abspath(os.path.join(os.getcwd(), "public", "css", "style_export_comprobante.css"))
    bootstrap = os.path.abspath(os.path.join(os.getcwd(), "public", "css", "comprobante_bootstrap.min.css"))
    css = [comp, bootstrap]
    
    # Windows
    if platform.system() == 'Windows':
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdf = pdfkit.from_string(rendered, False, options=options, configuration=config, css=css)
    # Linux or MacOs
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        pdf = pdfkit.from_string(rendered, False, options=options, css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    nro_cuota = informacion['id']
    fecha_cuota = informacion['fecha_pago']
    response.headers['Content-Disposition'] = "attachment; filename=cuota_{}_{}.pdf".format(fecha_cuota, nro_cuota)

    return response

# Base 64 Decoding for logo.png
import base64

def get_image_file_as_base64_data():
    with open('public/images/logo_comprobante.png', 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()


def carnet_pdf_export(carnet):
    # Render
    options = {
        'enable-local-file-access': None,
        'encoding':'utf-8',
        'dpi': '300',
        'page-height': '100', 
        'page-width': '150',
    }

    upload = image.get_image(carnet['image_id'])
    qr = generate_qr('https://admin-grupo19.proyecto2022.linti.unlp.edu.ar/socio/{}/carnet'.format(carnet['id']))
    rendered = render_template('socios/export_carnet.html', carnet=carnet, image=upload, qr=qr)

    comp = os.path.abspath(os.path.join(os.getcwd(), "public", "css", "style_export_carnet.css"))
    bootstrap = os.path.abspath(os.path.join(os.getcwd(), "public", "css", "comprobante_bootstrap.min.css"))
    css = [comp, bootstrap]
    
    # Windows
    if platform.system() == 'Windows':
        path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdf = pdfkit.from_string(rendered, False, options=options, configuration=config, css=css)
    # Linux or MacOs
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        pdf = pdfkit.from_string(rendered, False, options=options, css=css)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = "attachment; filename=carnet_socio_{}.pdf".format(carnet['id'])

    return response