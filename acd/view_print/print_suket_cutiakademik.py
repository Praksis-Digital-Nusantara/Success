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
from ..models import SuketCutiAkademik, Pejabat
import textwrap



def print_suket_cutiakademik(request, id):
    context = web_name(request)

    data = SuketCutiAkademik.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 65 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "SURAT KETERANGAN CUTI AKADEMIK", 'BU', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Nomor: " + data.no_surat, 'N', 'C')

    pos_y -= dl(p, posd_x, pos_y, 30, "Kepada Yth,", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Wakil Rektor Bidang Akademik", 'B', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Cq. Kepala BAAK UNM", 'B', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "di", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Tempat", 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 30, "Diberikan kepada:", 'N', 'L')

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
    pos_y = draw_aligned_text(p, "Tempat/Tanggal Lahir", data.mhs.tempat_lahir + ', ' + tanggal_indo(data.mhs.tgl_lahir),  15) 
    pos_y = draw_aligned_text(p, "NIM", data.mhs.nim.username,  15) 
    pos_y = draw_aligned_text(p, "Fakultas", context.get("faculty_name", ""),  15) 
    pos_y = draw_aligned_text(p, "Program Studi", str(data.mhs.prodi),  15) 
    pos_y = draw_aligned_text(p, "Terakhir Terdaftat", data.terakhir_terdaftar,  15)

    pos_y -= dl(p, posd_x, pos_y, 30, "Berdasarkan ketentuan akademik yang berlaku, maka kepadanya diberikan cuti akademik pada semester " + data.cuti_semester + " Tahun Akademik " + data.tahun_akademik + " terhitung mulai bulan " + data.terhitung_cuti + ".", 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 30, "Pada akhir masa melaksanakan cuti akademik wajib melapor pada loket Fakultas masing-masing di BAAK untuk membayar SPP/UKT dalam rangka mengikuti kembali perkuliahan " + data.kembali_aktif, 'N', 'L')


    wrapped_text = textwrap.wrap(
        "Demikian surat keterangan ini diberikan untuk dipergunakan sebagaimana mestinya. ", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 30, line, 'N', 'J', width=470)

    if data.ttd and data.ttd.pejabat:
        panjang_nama_pejabat = A4[0] - ( p.stringWidth(data.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
        if panjang_nama_pejabat < 300 :
            pos_x_ttd = panjang_nama_pejabat
        else :
            pos_x_ttd = 300

            

        pos_y -= dl(p, pos_x_ttd, pos_y, 50, context.get("address_ttd", "") + ", " + tanggal_indo(data.date_in), 'N', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Dekan Fakultas Ekonomi dan Bisnis", 'N', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Universitas Negeri Makassar", 'N', 'L')
        if data.ttd_status == 'QRcode' :
            p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/scak/' + str(data.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
        pos_y -= dl(p, pos_x_ttd, pos_y, 70, data.ttd.pejabat.nip.first_name, 'BU', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + data.ttd.pejabat.nip.username, 'B', 'L')
    else: 
        pos_y = draw_aligned_text(p,"STATUS", "PEJABAT MEMBATALKAN TTD DOKUMEN",  15)


    tembusan_list = [
        "Tembusan:",
        "1. Wakil Rektor Bid. Akademik (sebagai laporan)",
        "2. Kepala BAAK UNM",
        "3. Ketua Program Studi"
    ]
    pos_y -= 50  # Reduced line spacing for smaller font

    # Set font size to 8 for tembusan items
    p.setFont("Times-Roman", 8)
    for item in tembusan_list:
        pos_y -= 12  # Reduced line spacing for smaller font
        p.drawString(posd_x, pos_y, item)

    # Menutup halaman dan menyimpan PDF
    p.setTitle("Surat Keterangan Cuti Akademik")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Surat Keterangan Cuti Akademik ".pdf"'
    return response