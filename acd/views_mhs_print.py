from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from .decorators_mhs import check_usermhs
from .decorators_mhs import mahasiswa_required

from aam.context_processors import web_name

from .utils import tanggal_indo, draw_kop_surat

from .models import SkripsiJudul

import textwrap




@mahasiswa_required
@check_usermhs
def print_pengajuanjudul(request):
    context = web_name(request)  
    usermhs = request.usermhs  
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="kop_surat.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat(p, context, usermhs)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5
    p.drawCentredString(text_x, pos_y, "USULAN JUDUL TUGAS AKHIR")


    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset
        canvas.drawString(posd_x, pos_y, label)  
        canvas.drawString(180, pos_y, ":")  
        canvas.drawString(200, pos_y, value)        
        return pos_y

    pos_y = draw_aligned_text(p, "Nama Mahasiswa", request.user.first_name, 25)
    pos_y = draw_aligned_text(p, "NIM", request.user.username, 15)
    pos_y = draw_aligned_text(p, "Jurusan", usermhs.prodi.jurusan.nama_jurusan, 15)
    pos_y = draw_aligned_text(p, "Program Studi", usermhs.prodi.nama_prodi, 15)
    pos_y = draw_aligned_text(p, "Tempat/ Tgl. Lahir", usermhs.tempat_lahir + ", "+tanggal_indo(usermhs.tgl_lahir), 15)


    p.setFont("Times-Bold", 12)
    pos_y -= 25
    p.drawString(posd_x, pos_y, "Judul yang diajukan")

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x, pos_y, label)
        wrapped_text = textwrap.wrap(value, width=100)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 20, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 20, pos_y, line)
        return pos_y  
    
    judul = SkripsiJudul.objects.get(user=request.user)
    print (judul)

    pos_y = draw_aligned_text(p, "1.", judul.judul_1,  20)   
    pos_y = draw_aligned_text(p, "2.", judul.judul_2,  20)   
    pos_y = draw_aligned_text(p, "3.", judul.judul_3,  20)   


    # Menutup halaman dan menyimpan PDF
    p.setTitle("Cetak Usulan Judul "+request.user.username)
    p.showPage()
    p.save()

    return response