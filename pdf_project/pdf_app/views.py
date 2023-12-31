from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from io import BytesIO
from xhtml2pdf import pisa


class PDFView(View):
    def get(self, request):
        return render(request, 'pdf_app/formulario.html')

    def post(self, request):
        nombre = request.POST.get('nombre', '')
        contenido = request.POST.get('contenido', '')

        template = get_template('pdf_app/pdf_template.html')
        context = {'nombre': nombre, 'contenido': contenido}
        html = template.render(context)

        pdf_file = self.create_pdf(html)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="ArchivoDescargadoYCreadoPorOwer.pdf"'
        response.write(pdf_file.getvalue())

        return response

    def create_pdf(self, html):
        pdf_file = BytesIO()

        pisa.CreatePDF(html, dest=pdf_file)

        return pdf_file


class PDFDownloadView(View):
    def get(self, request):
        return render(request, 'pdf_app/formulario.html')

    def post(self, request):
        nombre = request.POST.get('nombre', '')
        contenido = request.POST.get('contenido', '')

        template = get_template('pdf_app/pdf_template.html')
        context = {'nombre': nombre, 'contenido': contenido}
        html = template.render(context)

        pdf_file = PDFView().create_pdf(html)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ArchivoDescargadoYCreadoPorOwer.pdf"'
        response.write(pdf_file.getvalue())

        return response
