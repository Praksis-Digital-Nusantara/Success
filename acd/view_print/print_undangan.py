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
from ..models import Proposal, Hasil, Ujian
import textwrap





def print_undangan(request, jn, id):
    context = web_name(request)
    if jn == 'Proposal':  
        undangan = Proposal.objects.get(id=id)
    else:
        undangan = Hasil.objects.get(id=id)

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
    

    pos_y = draw_aligned_text(p, "Nomor", undangan.no_surat, "Makassar, " + tanggal_indo(undangan.date_in), 15) 
    pos_y = draw_aligned_text(p, "Lampiran", "1 (satu) Naskah", "",  15)   
    pos_y = draw_aligned_text(p, "Perihal", "Undangan Seminar " + jn, "",  15)   

    pos_y -= dl(p, posd_x, pos_y, 30, "Kepada Yth,", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Bapak/Ibu Dosen", 'N', 'L')

    def draw_aligned_text(canvas, label1, label2, label3, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 20, pos_y, label1)
        canvas.drawString(posd_x + 40, pos_y, label2)
        canvas.drawString(posd_x + 120, pos_y, ":")
        canvas.drawString(posd_x + 130, pos_y, label3)
        return pos_y 

    pos_y = draw_aligned_text(p, "", "Ketua Prodi", undangan.ttd.pejabat.nip.first_name, 30)
    pos_y = draw_aligned_text(p, "", "Pembimbing I", undangan.pembimbing1.nip.first_name,  15)   
    pos_y = draw_aligned_text(p, "", "Pembimbing II", undangan.pembimbing2.nip.first_name,  15)   
    pos_y = draw_aligned_text(p, "", "Penanggap", undangan.penguji1.nip.first_name,  15)   
    pos_y = draw_aligned_text(p, "", "Moderator", undangan.pembimbing1.nip.first_name,  15)   

    pos_y -= dl(p, posd_x, pos_y, 30, "Dengan Hormat", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Kami mengundang Bapak/Ibu untuk menghadiri Seminar " + jn + " Penelitian Mahasiswa dalam rangka penyelesaian Skripsi atas nama:", 'N', 'L')

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 20, pos_y, label)
        canvas.drawString(posd_x + 100, pos_y, ':')
        wrapped_text = textwrap.wrap(value, width=80)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 110, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 110, pos_y, line)
        return pos_y  
    
    pos_y = draw_aligned_text(p, "Nama", undangan.mhs_judul.mhs.nim.first_name,  30) 
    pos_y = draw_aligned_text(p, "NIM", undangan.mhs_judul.mhs.nim.username,  15) 
    pos_y = draw_aligned_text(p, "Jurusan", undangan.mhs_judul.prodi.jurusan.nama_jurusan, 15)
    pos_y = draw_aligned_text(p, "Program Studi", undangan.mhs_judul.prodi.nama_prodi,  15) 
    pos_y = draw_aligned_text(p, "judul", undangan.mhs_judul.judul,  15) 

    pos_y -= dl(p, posd_x, pos_y, 15, "Seminar tersebut akan diselenggarakan pada:", 'N', 'L')
    pos_y = draw_aligned_text(p, "Hari/Tanggal", tanggal_indo(undangan.seminar_tgl, undangan.seminar_tgl),  15) 
    pos_y = draw_aligned_text(p, "Pukul", str(undangan.seminar_jam) + " WITA - Selesai",  15) 
    pos_y = draw_aligned_text(p, "Tempat", undangan.seminar_tempat,  15) 


    pos_y -= dl(p, posd_x, pos_y, 30, "Atas kehadiran dan kerja sama Bapak/Ibu kami ucapkan terima kasih.", 'N', 'L')


    panjang_nama_pejabat = A4[0] - ( p.stringWidth(undangan.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 300 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 350

    pos_y -= dl(p, pos_x_ttd, pos_y, 50, undangan.ttd.jabatan, 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, str(undangan.ttd.label or ""), 'N', 'L')
    if undangan.ttd_status == 'QRcode' :
        p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/upr/' + str(undangan.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, undangan.ttd.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + undangan.ttd.pejabat.nip.username, 'B', 'L')


    # Menutup halaman dan menyimpan PDF
    p.setTitle("Undangan " + jn + " " + str(undangan.mhs_judul.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Undangan {jn} {str(undangan.mhs_judul.mhs)}.pdf"'
    return response


###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################


def print_undangan_ujian(request, id):
    context = web_name(request)

    undangan = Ujian.objects.get(id=id)

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

    pos_y = draw_aligned_text(p, "Nomor", undangan.no_surat, tanggal_indo(undangan.date_in),  15)   
    pos_y = draw_aligned_text(p, "Lampiran", "1 (satu) Naskah", "",  15)   
    pos_y = draw_aligned_text(p, "Perihal", "Undangan Ujian Skripsi", "",  15)   

    pos_y -= dl(p, posd_x, pos_y, 30, "Kepada Yth,", 'N', 'L')

    def draw_aligned_text(canvas, label1, label2, label3, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 20, pos_y, label1)
        canvas.drawString(posd_x + 40, pos_y, label2)
        canvas.drawString(posd_x + 150, pos_y, ":")
        canvas.drawString(posd_x + 170, pos_y, label3)
        return pos_y 

    pos_y = draw_aligned_text(p, "1.", "Ketua Sidang", undangan.wd.pejabat.nip.first_name,  30)   
    pos_y = draw_aligned_text(p, "2.", "Sekretaris Sidang ", undangan.kaprodi.pejabat.nip.first_name,  15)   
    pos_y = draw_aligned_text(p, "1.", "Pembimbing I", undangan.pembimbing1.nip.first_name,  15)   
    pos_y = draw_aligned_text(p, "2.", "Pembimbing II", undangan.pembimbing2.nip.first_name,  15)   
    pos_y = draw_aligned_text(p, "3.", "Penguji I", undangan.penguji1.nip.first_name,  15)   
    pos_y = draw_aligned_text(p, "4.", "Penguji II", undangan.penguji2.nip.first_name,  15)   

    pos_y -= dl(p, posd_x, pos_y, 15, "di-", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Tempat", 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "", 'N', 'L') # enter kosong

    wrapped_text = textwrap.wrap(
        "Dengan hormat, kami mengundang Bapak/Ibu untuk untuk hadir dan menguji pada ujian skripsi bagi mahasiswa", 
        width=100 
    )
    for line in wrapped_text:
        pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L')

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 20, pos_y, label)
        canvas.drawString(posd_x + 100, pos_y, ':')
        wrapped_text = textwrap.wrap(value, width=80)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 110, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 110, pos_y, line)
        return pos_y  
    
    pos_y = draw_aligned_text(p, "Nama", undangan.mhs_judul.mhs.nim.first_name,  15) 
    pos_y = draw_aligned_text(p, "NIM", undangan.mhs_judul.mhs.nim.username,  15) 
    pos_y = draw_aligned_text(p, "Program Studi", undangan.mhs_judul.prodi.nama_prodi,  15) 
    pos_y = draw_aligned_text(p, "judul", undangan.mhs_judul.judul,  15) 

    pos_y = draw_aligned_text(p, "Hari/Tanggal", tanggal_indo(undangan.ujian_tgl, undangan.ujian_tgl),  30) 
    pos_y = draw_aligned_text(p, "Tempat", undangan.ujian_tempat,  15) 
    pos_y = draw_aligned_text(p, "Pukul", str(undangan.ujian_jam) + " WITA - Selesai",  15) 


    pos_y -= dl(p, posd_x, pos_y, 30, "Demikian disampaikan, atas perhatian dan kerjasamanya diucapkan terimakasih", 'N', 'L')


    panjang_nama_pejabat = A4[0] - ( p.stringWidth(undangan.dekan.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 300 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 300

    pos_y -= dl(p, pos_x_ttd, pos_y, 50, undangan.dekan.jabatan + ",", 'N', 'L')
    if undangan.ttd_status == 'QRcode' :
        p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/uuj/' + str(undangan.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, undangan.dekan.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + undangan.dekan.pejabat.nip.username, 'B', 'L')


    # Menutup halaman dan menyimpan PDF
    p.setTitle("SK Pembimbing ")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="SK Pembimbing.pdf"'
    return response