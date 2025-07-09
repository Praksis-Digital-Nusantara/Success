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
from ..models import IzinPenelitian
import textwrap





def print_izinpenelitian(request, id):
    context = web_name(request)
    data = IzinPenelitian.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    def draw_aligned_text(canvas, label1, label2, label3, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x, pos_y, label1)
        canvas.drawString(posd_x + 50, pos_y, ':')
        canvas.drawString(posd_x + 60, pos_y, label2)
        canvas.drawString(posd_x + 400, pos_y, label3)
        return pos_y 
    

    pos_y = draw_aligned_text(p, "Nomor", data.no_surat, tanggal_indo(data.date_in),  15)   
    pos_y = draw_aligned_text(p, "Lampiran", "1 (satu) Naskah", "",  15)   
    pos_y = draw_aligned_text(p, "Perihal", "Permohonan Izin Penelitian ", "",  15)   

    pos_y -= dl(p, posd_x, pos_y, 30, "Kepada Yth: " + data.pimpinan, 'N', 'L')
    if data.pimpinancq is not None:
        pos_y -= dl(p, posd_x, pos_y, 15, "cq. " + data.pimpinancq, 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "di-", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "   Tempat", 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 30, "Dengan hormat disampaikan kepada saudara bahwa mahasiswa tersebut di bawah ini:", 'N', 'L')

    def draw_aligned_text(canvas, label1, label2, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 20, pos_y, label1)
        canvas.drawString(posd_x + 120, pos_y, ":")
        canvas.drawString(posd_x + 135, pos_y, label2)
        return pos_y 

    pos_y = draw_aligned_text(p, "Nama", data.mhs_judul.mhs.nim.first_name,  30)   
    pos_y = draw_aligned_text(p, "NIM", data.mhs_judul.mhs.nim.username,  15)   
    pos_y = draw_aligned_text(p, "Program Studi", data.mhs_judul.mhs.prodi.nama_prodi,  15)   
    pos_y = draw_aligned_text(p, "Fakultas", context.get("faculty_name", ""),  15)   

    pos_y -= dl(p, posd_x, pos_y, 15, "", 'N', 'L') # enter kosong

    wrapped_text = textwrap.wrap(
        "Akan mengadakan penelitian dalam rangka penyelesaian studi pada program sarjana " + 
        context.get("faculty_short_name", "") + " " + context.get("university_name", "") + " dengan  penelitian:", 
        width=100  # Sesuaikan lebar teks
    )
    for line in wrapped_text:
        pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L')
    

    def draw_aligned_text(canvas, label1,label2, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 20, pos_y, label1)
        canvas.drawString(posd_x + 120, pos_y, label2)
        wrapped_text = textwrap.wrap(value, width=70)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 135, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 135, pos_y, line)
        return pos_y  
    
    pos_y = draw_aligned_text(p, "Judul", ":", data.mhs_judul.judul,  30) 
    pos_y = draw_aligned_text(p, "Dosen Pembimbing", ":", "1. " + data.mhs_judul.pembimbing1.nip.first_name,  15) 
    pos_y = draw_aligned_text(p, "", "", "2. " + data.mhs_judul.pembimbing2.nip.first_name,  15) 
    pos_y = draw_aligned_text(p, "Lokasi Penelitian", ":", data.lokasi,  15) 
    
    pos_y -= dl(p, posd_x, pos_y, 15, "", 'N', 'L') # enter kosong

    wrapped_text = textwrap.wrap(
        "Kemudian pengurusan segala sesuatunya yang berkaitan dengan penelitian tersebut akan diselesaikan oleh mahasiswa yang bersangkutan.", 
        width=100 
    )
    for line in wrapped_text:
        pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L')

    wrapped_text = textwrap.wrap(
        "Demikian permohonan ini kami sampaikan, atas perhatian dan kerjasamanya diucapkan terimakasih..", 
        width=100 
    )
    for line in wrapped_text:
        pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L')



    panjang_nama_pejabat = A4[0] - ( p.stringWidth(data.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 300 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 300

    pos_y -= dl(p, pos_x_ttd, pos_y, 50, data.ttd.jabatan, 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Bidang Akademik dan Kemahasiswaan", 'N', 'L')
    if data.ttd_status == 'QRcode' :
        p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/izp/' + str(data.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, data.ttd.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + data.ttd.pejabat.nip.username, 'B', 'L')


    # Menutup halaman dan menyimpan PDF
    p.setTitle("SK Pembimbing ")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="SK Pembimbing.pdf"'
    return response