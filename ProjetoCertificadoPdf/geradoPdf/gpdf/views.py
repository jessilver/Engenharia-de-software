import os
from django.shortcuts import render
from django.views.generic import View
from PIL import Image, ImageDraw, ImageFont
from geradoPdf import settings
from fpdf import FPDF


class Index(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        imagePath = os.path.join(settings.BASE_DIR, 'gpdf', 'static', 'image', 'certificado_base.jpg')
        certificado = Image.open(imagePath)

        try:
            fonteNome = ImageFont.truetype("arial.ttf", 175)
            fontePadrao = ImageFont.truetype("arial.ttf", 120)
        except IOError:
            return render(request, 'index.html', {'error': 'Fonte não encontrada!'})

        nomeAluno = request.POST.get('nomeAluno', "")
        cpfAluno = request.POST.get('cpfAluno', "")
        rgAluno = request.POST.get('rgAluno', "")
        nomeCurso = request.POST.get('nomeCurso', "")
        inicioCurso = request.POST.get('inicioCurso', "")
        fimCurso = request.POST.get('fimCurso', "")
        cargaHoraria = request.POST.get('cargaHoraria', "")
        instituicao = request.POST.get('instituicao', "")
        diretor = request.POST.get('diretor', "")

        inicioCurso = str(inicioCurso).split('-')
        inicioCurso = inicioCurso[-1]+'/'+inicioCurso[-2]+'/'+inicioCurso[-3]
        fimCurso = str(fimCurso).split('-')
        fimCurso = fimCurso[-1]+'/'+fimCurso[-2]+'/'+fimCurso[-3]

        desenho = ImageDraw.Draw(certificado)
        desenho.text((2030, 2070), nomeAluno, font=fonteNome, fill="black")
        desenho.text((2540, 2380), cpfAluno, font=fontePadrao, fill="black")
        desenho.text((3850, 2380), rgAluno, font=fontePadrao, fill="black")
        desenho.text((680, 2575), nomeCurso, font=fontePadrao, fill="black")
        desenho.text((2970, 2575), inicioCurso, font=fontePadrao, fill="black")
        desenho.text((3850, 2575), fimCurso, font=fontePadrao, fill="black")
        desenho.text((1650, 2770), cargaHoraria, font=fontePadrao, fill="black")
        desenho.text((3220, 2770), instituicao, font=fontePadrao, fill="black")
        desenho.text((510, 3320), diretor, font=fontePadrao, fill="black")

        finalPath = os.path.join(settings.BASE_DIR, 'gpdf', 'static', 'image', 'certificadoFinal.jpg')
        certificado.save(finalPath)

        larguraPx, alturaPx = certificado.size

        larguraMm = larguraPx * 25.4 / 72
        alturaMm = alturaPx * 25.4 / 72

        outputDir = os.path.join(settings.BASE_DIR, 'gpdf', 'static', 'pdf')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        pdfFilename = f'certificado_{nomeAluno}.pdf'
        pdfPath = os.path.join(outputDir, pdfFilename.replace(" ","-"))

        pdf = FPDF(unit="mm", format=[larguraMm, alturaMm])
        pdf.add_page()
        pdf.image(finalPath, x=0, y=0, w=larguraMm, h=alturaMm)
        pdf.output(pdfPath)

        return render(request, "index.html", {'success': 'Certificado gerado com sucesso!', 'pdfUrl': f'/static/pdf/{pdfFilename.replace(" ","-")}'})