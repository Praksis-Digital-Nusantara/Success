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
from ..models import SuketBebasKuliah, SuketBebasPlagiasi
import textwrap


def print_suket_bebasplagiasi(request, id):
    context = web_name(request)

    data = SuketBebasPlagiasi.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "SURAT KETERANGAN BEBAS PLAGIASI", 'B', 'C')


    wrapped_text = textwrap.wrap(
        "Surat Keterangan ini dibuat untuk menerangkan, mahasiswa dibawah ini:", 
        width=100 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 50, line, 'N', 'L')

    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "", 'B', 'C')

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 30, pos_y, label)
        canvas.drawString(posd_x + 150, pos_y, ':')
        wrapped_text = textwrap.wrap(value, width=100)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 160, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 160, pos_y, line)
        return pos_y  
    
    pos_y = draw_aligned_text(p, "Nama", data.mhs.nim.first_name,  15) 
    pos_y = draw_aligned_text(p, "NIM", data.mhs.nim.username,  15) 
    pos_y = draw_aligned_text(p, "Tempat/Tanggal Lahir", data.mhs.tempat_lahir + ', ' + tanggal_indo(data.mhs.tgl_lahir),  15) 
    pos_y = draw_aligned_text(p, "Alamat", data.mhs.alamat,  15)
    
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "", 'B', 'C')

    wrapped_text = textwrap.wrap(
        "Adalah benar mahasiswa program studi " + data.mhs.prodi.nama_prodi + " " +  context.get("faculty_name", "") + " " + context.get("university_name", "") + ", dan telah melakukan pengecekan penulisan dengan nilai kesamaan " + str(data.nilai_plagiasi) + " %.",
        width=100 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L')

    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "", 'B', 'C')

    wrapped_text = textwrap.wrap(
        "Sehingga mahasiswa tersebut dinyatakan bebas terhadap plagiasme, Demikian surat keterangan ini saya buat dengan sebenar-benarnya. Atas perhatiaanya kami ucapkan terima kasih.",
        width=100 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L')


    if data.ttd and data.ttd.pejabat:
        panjang_nama_pejabat = A4[0] - ( p.stringWidth(data.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
        if panjang_nama_pejabat < 300 :
            pos_x_ttd = panjang_nama_pejabat
        else :
            pos_x_ttd = 300

            

        pos_y -= dl(p, pos_x_ttd, pos_y, 50, context.get("address_ttd", "") + ", " + tanggal_indo(data.date_in), 'N', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 15, data.ttd.jabatan + ",", 'N', 'L')
        if data.ttd_status == 'QRcode' :
            p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/sbp/' + str(data.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
        pos_y -= dl(p, pos_x_ttd, pos_y, 70, data.ttd.pejabat.nip.first_name, 'BU', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + data.ttd.pejabat.nip.username, 'B', 'L')
    else:
        # fallback kalau TTD kosong
        pos_x_ttd = 300
        pos_y -= dl(p, pos_x_ttd, pos_y, 70, "PEJABAT MEMBATALKAN TTD E-DOCUMENTS", 'B', 'L')

    # Menutup halaman dan menyimpan PDF
    p.setTitle("Bebas Plagiasi ")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Bebas Plagiasi.pdf"'
    return response