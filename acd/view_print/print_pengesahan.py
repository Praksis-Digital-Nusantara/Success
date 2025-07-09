from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from reportlab.lib import colors

from aam.context_processors import web_name
from ..print_utils import tanggal_indo, draw_kop_surat_fakultas, dl
from ..models import SkripsiJudul, Pejabat, Proposal
import textwrap





def print_pengesahan(request, jn, id):
    context = web_name(request)  
    skripsi = SkripsiJudul.objects.get(id=id)

    if jn == 'proposal':
        jn = 'Seminar Proposal'
    elif jn == 'hasil':
        jn = 'Seminar Hasil'
    elif jn == 'ujian':
        jn = 'Ujian Tutup Skripsi'

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "LEMBAR PENGESAHAN", 'B', 'C')
   

    def draw_aligned_text(canvas, value, y_offset, bold=False):
        nonlocal pos_y
        pos_y -= y_offset
        styles = getSampleStyleSheet()
        style = ParagraphStyle(
            name='Centered',
            parent=styles['Normal'],
            fontName='Times-Bold' if bold else 'Times-Roman',
            fontSize=12,
            alignment=TA_CENTER,
            leading=14,
        )

        paragraph = Paragraph(value, style)
        text_width = 400
        _, text_height = paragraph.wrap(text_width, 100)

        paragraph.drawOn(canvas, (A4[0] - text_width) / 2, pos_y - text_height + 12)

        pos_y -= text_height + 2
        return pos_y


    pos_y = draw_aligned_text(p, skripsi.judul.upper(), 40, False)  


    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Diusulkan Oleh", 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, skripsi.mhs.nim.first_name.upper(), 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, skripsi.mhs.nim.username, 'N', 'C')
    pos_y = draw_aligned_text(p, "telah diperiksa dan disetujui untuk dapat melanjutkan ke tahap " + jn, 20, False)  

    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "Disetujui Oleh:", 'N', 'C')

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 70, pos_y, label)
        wrapped_text = textwrap.wrap(value, width=100)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 250, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 250, pos_y, line)
        return pos_y  
    
  
    pos_y = draw_aligned_text(p, "Pembimbing I : ", skripsi.pembimbing1.nip.first_name,  100)   
    pos_y = draw_aligned_text(p, "", "NIP. " + skripsi.pembimbing1.nip.username,  15)   
    pos_y = draw_aligned_text(p, "Pembimbing II : ", skripsi.pembimbing2.nip.first_name,  100)   
    pos_y = draw_aligned_text(p, "", "NIP. " + skripsi.pembimbing2.nip.username,  15)   

    kaprodi = Pejabat.objects.get(jabatan='Ketua Prodi', prodi=skripsi.prodi)

    panjang_nama_pejabat = A4[0] - ( p.stringWidth(kaprodi.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 250 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 300

    pos_y -= dl(p, pos_x_ttd, pos_y, 70, context.get("address_ttd", "") + ", ......................", 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, kaprodi.jabatan, 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, str(kaprodi.prodi), 'N', 'L')
    # p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/skpbb/' + str(sk.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, kaprodi.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + kaprodi.pejabat.nip.username, 'B', 'L')




    # Menutup halaman dan menyimpan PDF
    p.setTitle("Pengesahan " + jn + " " + str(skripsi.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Pengesahan {jn} {str(skripsi.mhs)}.pdf"'
    return response




################### PRINT PERSETUJUAN PENELITIAN #########################

def print_persetujuan_penelitian(request, id):
    context = web_name(request)  
    skripsi = Proposal.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 5, "PERSETUJUAN MELAKSANAKAN PENELITIAN", 'B', 'C')
   

    def draw_aligned_text(canvas, value, y_offset, bold=False):
        nonlocal pos_y
        pos_y -= y_offset
        styles = getSampleStyleSheet()
        style = ParagraphStyle(
            name='Centered',
            parent=styles['Normal'],
            fontName='Times-Bold' if bold else 'Times-Roman',
            fontSize=12,
            alignment=TA_CENTER,
            leading=14,
        )

        paragraph = Paragraph(value, style)
        text_width = 400
        _, text_height = paragraph.wrap(text_width, 100)

        paragraph.drawOn(canvas, (A4[0] - text_width) / 2, pos_y - text_height + 12)

        pos_y -= text_height + 2
        return pos_y


    pos_y = draw_aligned_text(p, skripsi.mhs_judul.judul.upper(), 30, False)  


    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Diusulkan Oleh", 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, skripsi.mhs_judul.mhs.nim.first_name.upper(), 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, skripsi.mhs_judul.mhs.nim.username, 'N', 'C')
    pos_y = draw_aligned_text(p, "telah melewati tahapan proposal dan disetujui untuk dapat melaksanakan penelitian ", 20, False)  

    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "Disetujui Oleh:", 'N', 'C')

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 70, pos_y, label)
        wrapped_text = textwrap.wrap(value, width=100)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 250, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 250, pos_y, line)
        return pos_y  
    
  
    pos_y = draw_aligned_text(p, "Pembimbing I : ", skripsi.pembimbing1.nip.first_name,  55)   
    pos_y = draw_aligned_text(p, "", "NIP. " + skripsi.pembimbing1.nip.username,  15)   
    pos_y = draw_aligned_text(p, "Pembimbing II : ", skripsi.pembimbing2.nip.first_name,  55)   
    pos_y = draw_aligned_text(p, "", "NIP. " + skripsi.pembimbing2.nip.username,  15)   
    pos_y = draw_aligned_text(p, "Penguji I : ", skripsi.penguji1.nip.first_name,  55)   
    pos_y = draw_aligned_text(p, "", "NIP. " + skripsi.penguji1.nip.username,  15)   
    pos_y = draw_aligned_text(p, "Penguji II : ", skripsi.penguji2.nip.first_name,  55)   
    pos_y = draw_aligned_text(p, "", "NIP. " + skripsi.penguji2.nip.username,  15)   

    kaprodi = Pejabat.objects.get(jabatan='Ketua Prodi', prodi=skripsi.mhs_judul.prodi)

    panjang_nama_pejabat = A4[0] - ( p.stringWidth(kaprodi.pejabat.nip.first_name, "Times-Bold", 12) + 55)
    if panjang_nama_pejabat < 250 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 300

    pos_y -= dl(p, pos_x_ttd, pos_y, 30, context.get("address_ttd", "") + ", ......................", 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, kaprodi.jabatan, 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, kaprodi.label, 'N', 'L')
    # p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/skpbb/' + str(sk.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    pos_y -= dl(p, pos_x_ttd, pos_y, 55, kaprodi.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + kaprodi.pejabat.nip.username, 'B', 'L')



 




    # Menutup halaman dan menyimpan PDF
    p.setTitle("Persetujuan Penelitian " + str(skripsi.mhs_judul.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Persetujuan Penelitian {str(skripsi.mhs_judul.mhs)}.pdf"'
    return response