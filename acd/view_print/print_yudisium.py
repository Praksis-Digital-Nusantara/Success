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
from ..models import Yudisium
import textwrap

def print_yudisium(request, id):
    context = web_name(request)
    data = Yudisium.objects.filter(ujian__id=id).first()
  
    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 65 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)
    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 0

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "BERITA ACARA YUDISIUM", 'BU', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Nomor: " + str(data.no_surat), '', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "(Jalur Skripsi)", '', 'C')

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Pada hari ini " + tanggal_indo(data.date_in, data.date_in) + " telah diadakan Yudisium bagi mahasiswa:", 
        width=300 
    )
    for line in wrapped_text: 
        pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L', width=470)

    pos_y -= 20
    p.setFont("Times-Roman", 12)
    p.drawString(posd_x, pos_y, "Nama")
    p.drawString(posd_x + 120, pos_y, ":")
    p.drawString(posd_x + 140, pos_y, data.ujian.mhs_judul.mhs.nim.first_name)

    pos_y -= 15
    p.drawString(posd_x, pos_y, "Nomor Stambuk")
    p.drawString(posd_x + 120, pos_y, ":")
    p.drawString(posd_x + 140, pos_y, data.ujian.mhs_judul.mhs.nim.username)

    pos_y -= 15
    p.drawString(posd_x, pos_y, "Program Studi")
    p.drawString(posd_x + 120, pos_y, ":")
    p.drawString(posd_x + 140, pos_y, data.ujian.mhs_judul.prodi.nama_prodi)
    
    pos_y -= 15
    p.drawString(posd_x, pos_y, "Program")
    p.drawString(posd_x + 120, pos_y, ":")
    p.drawString(posd_x + 140, pos_y, "Skripsi")
    
    pos_y -= 15
    p.drawString(posd_x, pos_y, "Tempat Tgl Lahir")
    p.drawString(posd_x + 120, pos_y, ":")
    p.drawString(
        posd_x + 140,
        pos_y,
        f"{data.ujian.mhs_judul.mhs.tempat_lahir}, {tanggal_indo(data.ujian.mhs_judul.mhs.tgl_lahir)}"
    )

    pos_y -= 15
    p.drawString(posd_x, pos_y, "No. Telepon")
    p.drawString(posd_x + 120, pos_y, ":")
    p.drawString(posd_x + 140, pos_y, data.ujian.mhs_judul.mhs.telp)

    pos_y -= 10

    # Judul skripsi section
    wrapped_text = textwrap.wrap(
        "Dengan judul Skripsi sebagai berikut:", 
        width=70 
    )
    for line in wrapped_text: 
        pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L', width=470)

    # Judul dalam tanda kutip dan center
    pos_y -= 15
    judul_wrapped = textwrap.wrap(f'"{data.ujian.mhs_judul.judul}"', width=80)
    for line in judul_wrapped:
        pos_y -= dl(p, A4[0] / 2, pos_y, 15, line, 'N', 'C', width=400)

    pos_y -= 15

    # Panitia ujian section
    wrapped_text = textwrap.wrap(
        "Panitia Ujian terdiri dari:", 
        width=70 
    )
    for line in wrapped_text: 
        pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'L', width=470)

    panitia = [
        ("Ketua", data.ujian.dekan.pejabat.nip.first_name),
        ("Wakil Ketua", data.ujian.wd.pejabat.nip.first_name),
        ("Sekretaris", data.ujian.kaprodi.pejabat.nip.first_name),
        ("Pembimbing I", data.ujian.pembimbing1.nip.first_name),
        ("Pembimbing II", data.ujian.pembimbing2.nip.first_name),
        ("Penguji I", data.ujian.penguji1.nip.first_name),
        ("Penguji II", data.ujian.penguji2.nip.first_name)
    ]

    p.setFont("Times-Roman", 12)
    for idx, (jabatan, nama) in enumerate(panitia, 1):
        pos_y -= 25
        p.drawString(posd_x, pos_y, f"{idx}.")
        p.drawString(posd_x + 20, pos_y, jabatan)
        p.drawString(posd_x + 120, pos_y, ":")
        p.drawString(posd_x + 140, pos_y, nama)
        p.drawString(A4[0] - 150, pos_y, "(……………………)")

    pos_y -= 10

    # Hasil ujian section
    wrapped_text = textwrap.wrap(
        "Hasil ujian Skripsi diputuskan sebagai berikut :", 
        width=70 
    )
    for line in wrapped_text: 
        pos_y -= dl(p, posd_x, pos_y, 20, line, 'N', 'L', width=470)

    hasil_ujian = [
        ("Nilai", str(data.ipk)),
        ("Lulus dengan nilai yudisium", data.kualifikasi),
    ]

    for idx, (label, nilai) in enumerate(hasil_ujian, 1):
        pos_y -= 15
        p.drawString(posd_x, pos_y, f"{idx}.")
        p.drawString(posd_x + 20, pos_y, label)
        p.drawString(posd_x + 200, pos_y, ":")
        p.drawString(posd_x + 220, pos_y, nilai)

    pos_y -= 20

    # Signature section
    panjang_nama_pejabat = A4[0] - ( p.stringWidth(data.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 400:
        pos_x_ttd = panjang_nama_pejabat
    else:
        pos_x_ttd = 400        
    
    # Tanggal dan tempat
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, f"Makassar, {tanggal_indo(data.date_in)}", 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, data.ttd.jabatan + ",", 'N', 'L')    
    pos_y -= dl(p, pos_x_ttd, pos_y, 60, data.ttd.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + data.ttd.pejabat.nip.username, 'N', 'L')

    # Catatan di bagian bawah
    pos_y -= 2
    p.setFont("Times-Roman", 10)
    catatan = [
        "Catatan:",
        "1. Coret yang tidak perlu",
        "2. Dibuat 7 rangkap dan setelah ujian satu rangkap yang asli dikirim kembali ke BAAK",
        "3. Terlampir satu eksemplar skripsi untuk kelengkapan penerbitan ijazah"
    ]
    
    for line in catatan:
        pos_y -= 12
        p.drawString(posd_x, pos_y, line)

    # Menutup halaman dan menyimpan PDF
    p.setTitle("Berita Acara Yudisium")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Berita Acara Yudisium.pdf"'
    return response