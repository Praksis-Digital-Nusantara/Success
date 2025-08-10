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
from ..models import SuketIzinLab, Pejabat
import textwrap



def print_suket_izinlab(request, id):
    context = web_name(request)

    data = SuketIzinLab.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 65 #posisi default x untuk bagian kiri
  
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
    pos_y = draw_aligned_text(p, "Lampiran", "1 (satu) Berkas", "",  15)   
    pos_y = draw_aligned_text(p, "Perihal", " Permohonan Izin Pemakaian Labratorium dan Peminjaman Alat Laboratorium ", "",  15)   

    pos_y -= dl(p, posd_x, pos_y, 30, "Kepada Yth,", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Kepala UPA Laboratorium Terpadu", 'B', 'L')

    lab = data.lab    
    lab_list = [l.strip() for l in lab.split(',') if l.strip()]
    for lab_item in lab_list:
        pos_y -= dl(p, posd_x, pos_y, 15, "(" + lab_item + ")", 'B', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "di -,", 'N', 'L')
    pos_y -= dl(p, posd_x+10, pos_y, 15, "Tempat", 'N', 'L')
    pos_y -= dl(p, posd_x+10, pos_y, 30, "Dengan Hormat", 'N', 'L')

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Melalui surat ini kami sampaikan bahwa mahasiswa atas nama : ", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)


    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 30, pos_y, label)
        canvas.drawString(posd_x + 150, pos_y, ':')
        wrapped_text = textwrap.wrap(value, width=80)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 160, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 160, pos_y, line)
        return pos_y  
    
    pos_y = draw_aligned_text(p, "Nama", data.mhs.nim.first_name,  30) 
    pos_y = draw_aligned_text(p, "NIM", data.mhs.nim.username,  15) 
    pos_y = draw_aligned_text(p, "Program Studi", str(data.mhs.prodi),  15) 

    pos_y -= dl(p, posd_x, pos_y, 30, "Akan melaksanakan penelitian skripsi yang berjudul:", 'N', 'L')

    wrapped_text = textwrap.wrap(
        "``" + str(data.judul) + "``", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'IB', 'J', width=470)

    wrapped_text = textwrap.wrap(
        "Oleh karena itu kami mohon dapat dipinjamkan ruangan Laboratorium beserta alat dan bahan yang diperlukan (terlampir) pada Tanggal " + tanggal_indo(data.waktu_mulai) + " sampai dengan " + tanggal_indo(data.waktu_selesai) + ".", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Demikian surat ini kami buat atas perhatian dan kerjasamanya kami sampaikan terima kasih.", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)
    

    panjang_nama_pejabat = A4[0] - ( p.stringWidth(data.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 300 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 300

        

    pos_y -= dl(p, pos_x_ttd, pos_y, 45, "a.n Dekan", 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Wakil Dekan Bidang Akademik", 'N', 'L')
    if data.ttd_status == 'QRcode' :
        p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/sil/' + str(data.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, data.ttd.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + data.ttd.pejabat.nip.username, 'B', 'L')


    # Menutup halaman dan menyimpan PDF
    p.setTitle("Surat Izin Lab")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Surat Izin Lab") ".pdf"'
    return response
