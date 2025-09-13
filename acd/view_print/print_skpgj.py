from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Paragraph
from reportlab.lib import colors

from aam.context_processors import web_name
from ..print_utils import tanggal_indo, draw_kop_surat_fakultas, dl
from ..models import skPenguji
import textwrap


def print_skpgj(request, id):
    context = web_name(request)  
    sk = skPenguji.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 6, "SURAT KEPUTUSAN", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 12, "Nomor : " + sk.nosurat, 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "DEKAN FAKULTAS EKONOMI DAN BISNIS", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 12, "UNIVERSITAS NEGERI MAKASSAR", 'B', 'C')

    def draw_aligned_text(canvas, label1, label2, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset  # Update pos_y for the labels
        canvas.drawString(posd_x, pos_y, label1)
        canvas.drawString(posd_x + 100, pos_y, label2)
        
        # Membuat style untuk teks yang diratakan (justified)
        style = ParagraphStyle(
            'JustifyStyle',
            fontName="Times-Roman",
            fontSize=12,
            leading=14,
            alignment=TA_JUSTIFY,
            textColor=colors.black
        )
        # Membuat paragraph untuk teks yang akan diratakan
        paragraph = Paragraph(value, style)
        # Tentukan posisi teks dan lebar area teks
        text_width = 380  # Sesuaikan lebar teks agar hasil justification terlihat rapi
        text_height = paragraph.wrap(text_width, 0)[1]
        # Gambar teks pada canvas, pastikan Y disesuaikan dengan benar
        paragraph.drawOn(canvas, posd_x + 110, pos_y - text_height + 12)
        # Perbarui posisi Y setelah teks value
        pos_y -= text_height + 2  # Beri jarak antar baris setelah teks        
        return pos_y

    # Bagian Membacakan (diringkas)
    pos_y = draw_aligned_text(p, "Membacakan", ":", "Surat Keputusan Program Studi " + sk.usulan.mhs_judul.prodi.nama_prodi, 18)   
    pos_y = draw_aligned_text(p, "", "", "Nomor : " + sk.nosurat,  0)
    # Bagian Mengingat (diringkas)
     # Bagian Mengingat 
    p.setFont("Times-Roman", 12)
    pos_y -= 15
    p.drawString(posd_x, pos_y, "Mengingat")
    p.drawString(posd_x + 100, pos_y, ":")
    p.drawString(posd_x + 110, pos_y, "1. Undang-undang Nomor 20 Tahun 2003")
    pos_y -= 12
    p.drawString(posd_x + 110, pos_y, "2. Peraturan Pemerintah Nomor 60 Tahun 1999")
    pos_y -= 12
    p.drawString(posd_x + 110, pos_y, "3. Keputusan Presiden Nomor 93 Tahun 1999")
    pos_y -= 12
    p.drawString(posd_x + 110, pos_y, "4. Keputusan Mendikbud Nomor 277/0/Tahun 1999")
    pos_y -= 12
    p.drawString(posd_x + 110, pos_y, "5. Keputusan Mendiknas Nomor 025/0/Tahun 2002")
    pos_y -= 12
    p.drawString(posd_x + 110, pos_y, "6. Keputusan Rektor UNM Nomor 1073/PP/2010")
    pos_y -= 12
    p.drawString(posd_x + 110, pos_y, "7. Keputusan Kemendikbud Nomor 48 Tahun 2011")
    
    pos_y -= 12
    p.drawString(posd_x + 110, pos_y, "8. Keputusan Rektor UNM Nomor 05/ UN 36/ KP/ 2012")   

    pos_y -= dl(p, A4[0] / 2, pos_y, 17, "MEMUTUSKAN", 'B', 'C')

    pos_y = draw_aligned_text(p, "Menetapkan", ":", "Dosen yang tersebut namanya di bawah ini sebagai Panitia Ujian Skripsi Mahasiswa:",  15)

    # Data Mahasiswa - Posisi titik dua diperbaiki
    p.setFont("Times-Roman", 12)
    pos_y -= 7
    p.drawString(posd_x + 110, pos_y, "Nama")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.mhs_judul.mhs.nim.first_name)
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "NIM")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.mhs_judul.mhs.nim.username)
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Program Studi")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.mhs_judul.prodi.nama_prodi)  # sesuaikan dengan field yang ada
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Fakultas")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, "Fakultas Ekonomi dan Bisnis")
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Judul Skripsi")
    p.drawString(posd_x + 190, pos_y, ":")
    # Gunakan textwrap untuk judul yang panjang
    judul_wrapped = textwrap.fill(sk.usulan.mhs_judul.judul if hasattr(sk.usulan.mhs_judul, 'judul') else "Judul Skripsi", width=50)
    judul_lines = judul_wrapped.split('\n')
    for i, line in enumerate(judul_lines):
        if i == 0:
            p.drawString(posd_x + 210, pos_y, line)
        else:
            pos_y -= 12
            p.drawString(posd_x + 210, pos_y, line)

    pos_y -= 20
    p.drawString(posd_x, pos_y, "Dengan susunan Panitia Ujian Skripsi sebagai berikut:")

    # Susunan Panitia - Posisi titik dua diperbaiki
    pos_y -= 20
    p.setFont("Times-Roman", 12)
    p.drawString(posd_x + 97, pos_y, "1. Ketua")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.ketua.pejabat.nip.first_name)  # sesuaikan dengan field yang ada

    pos_y -= 15
    p.drawString(posd_x + 97, pos_y, "2. Anggota")
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Wakil Ketua")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.wakil.pejabat.nip.first_name)
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Sekretaris")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.sekretaris.nip.first_name)
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Pembimbing I")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.mhs_judul.pembimbing1.nip.first_name)
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Pembimbing II")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.mhs_judul.pembimbing2.nip.first_name)
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Penguji I")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.penguji1.nip.first_name)
    
    pos_y -= 15
    p.drawString(posd_x + 110, pos_y, "Penguji II")
    p.drawString(posd_x + 190, pos_y, ":")
    p.drawString(posd_x + 210, pos_y, sk.usulan.penguji2.nip.first_name)

    pos_y -= 20
    # Gunakan textwrap untuk memecah teks panjang
    teks_tugas = "Panitia Ujian Skripsi bertugas memeriksa dan menilai mahasiswa tersebut sesuai dengan peraturan dan pedoman penilaian."
    teks_wrapped = textwrap.fill(teks_tugas, width=100)  # 80 karakter per baris
    teks_lines = teks_wrapped.split('\n')
    for line in teks_lines:
        p.drawString(posd_x, pos_y, line)
        pos_y -= 12

    # Tempat dan tanggal
    panjang_nama_dekan = A4[0] - ( p.stringWidth(sk.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    panjang_tanggal = A4[0] - ( p.stringWidth("Pada Tanggal : " + tanggal_indo(sk.date_in), "Times-Bold", 12) + 60)
    if panjang_nama_dekan < panjang_tanggal :
        pos_x_ttd = panjang_nama_dekan
    else :
        pos_x_ttd = panjang_tanggal

    pos_y -= 10
    p.drawString(pos_x_ttd, pos_y, "Ditetapkan di : " + context.get("address_ttd", ""))
    pos_y -= 12
    p.drawString(pos_x_ttd, pos_y, "Pada Tanggal : " + tanggal_indo(sk.date_in))
    
    pos_y -= 15
    p.drawString(pos_x_ttd, pos_y, "Dekan,")
    
    # QR Code
    p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/skpgj/' + str(sk.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    
    pos_y -= 60
    p.setFont("Times-Bold", 12)
    p.drawString(pos_x_ttd, pos_y, sk.ttd.pejabat.nip.first_name)
    pos_y -= 15
    p.drawString(pos_x_ttd, pos_y, "NIP. " + sk.ttd.pejabat.nip.username)

    # Menutup halaman dan menyimpan PDF
    p.setTitle("SK Penguji " + str(sk.usulan.mhs_judul.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="SK Penguji { str(sk.usulan.mhs_judul.mhs) }.pdf"'
    return response