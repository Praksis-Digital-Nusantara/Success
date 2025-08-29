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
from ..models import skPembimbing
import textwrap


def print_skpbb(request, id):
    context = web_name(request)  
    sk = skPembimbing.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 10)
    text_x = A4[0] / 2
    pos_y -= 5

    fakultas = context.get("faculty_name", "")
    universitas = context.get("university_name", "")
    prodi = sk.mhs.prodi.nama_prodi 

    pos_y -= dl(p, A4[0] / 2, pos_y, 1, "KEPUTUSAN DEKAN", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, fakultas.upper() + " " + universitas.upper(), 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "NOMOR : " + sk.nosurat, 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "TENTANG:", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "PENGANGKATAN PEMBIMBING", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "BAGI MAHASISWA PROGRAM STUDI " + prodi.upper(), 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, fakultas.upper(), 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, universitas.upper(), 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "TAHUN " + str(sk.date_in.year), 'B', 'C')


    def draw_aligned_text(canvas, label1, label2, label3, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset  # Update pos_y for the labels
        canvas.drawString(posd_x, pos_y, label1)
        canvas.drawString(posd_x + 70, pos_y, label2)
        canvas.drawString(posd_x + 80, pos_y, label3)
        
        # Membuat style untuk teks yang diratakan (justified)
        style = ParagraphStyle(
            'JustifyStyle',
            fontName="Times-Roman",
            fontSize=10,
            leading=12,
            alignment=TA_JUSTIFY,
            textColor=colors.black
        )
        # Membuat paragraph untuk teks yang akan diratakan
        paragraph = Paragraph(value, style)
        # Tentukan posisi teks dan lebar area teks
        text_width = 400  # Sesuaikan lebar teks agar hasil justification terlihat rapi
        text_height = paragraph.wrap(text_width, 0)[1]
        # Gambar teks pada canvas, pastikan Y disesuaikan dengan benar
        paragraph.drawOn(canvas, posd_x + 90, pos_y - text_height + 12)
        # Perbarui posisi Y setelah teks value
        pos_y -= text_height + 2  # Beri jarak antar baris setelah teks        
        return pos_y

    
    # print (judul)
    pos_y = draw_aligned_text(p, "Menimbang", ":", "", "Usulan Ketua Program Studi Manajemen dan Dekan Fakultas Ekonomi Universitas Negeri Makassar dengan nomor surat " + sk.nosurat + " pada tanggal " + tanggal_indo(sk.date_in) + " tentang Usulan Penerbitan SK Pembimbingan.", 20)
    pos_y -= 10   
    pos_y = draw_aligned_text(p, "", "", "1.", "Bahwa dalam rangka kelancaran penyelesaian studi untuk penulisan Skripsi bagi mahasiswa Program Studi Manajemen, maka dipandang perlu menetapkan Pembimbing.",  0)   
    pos_y = draw_aligned_text(p, "", "", "2.", "Bahwa untuk maksud tersebut di atas, maka dipandang perlu menerbitkan surat keputusannya",  0)

    pos_y = draw_aligned_text(p, "Mengingat", ":", "1.", "Surat Keputusan Fakultas Ekonomi Nomor 2875/D/T/2007;", 15)   
    pos_y = draw_aligned_text(p, "", "", "2.", "Peraturan Rektor Universitas Negeri Makassar Nomor 1 Tahun 2022 tentang Peraturan Akademik di Universitas Negeri Makassar;",  0)   
    pos_y = draw_aligned_text(p, "", "", "3.", "Keputusan Rapat Pimpinan Fakultas dan Ketua Prodi tanggal 7 November 2023;",  0)


    pos_y -= dl(p, A4[0] / 2, pos_y, 10, "MEMUTUSKAN:", 'B', 'C')

    def draw_aligned_text(canvas, label1, label2, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset  # Update pos_y for the labels
        canvas.drawString(posd_x, pos_y, label1)
        canvas.drawString(posd_x + 70, pos_y, label2)
        
        # Membuat style untuk teks yang diratakan (justified)
        style = ParagraphStyle(
            'JustifyStyle',
            fontName="Times-Roman",
            fontSize=10,
            leading=12,
            alignment=TA_JUSTIFY,
            textColor=colors.black
        )
        # Membuat paragraph untuk teks yang akan diratakan
        paragraph = Paragraph(value, style)
        # Tentukan posisi teks dan lebar area teks
        text_width = 410  # Sesuaikan lebar teks agar hasil justification terlihat rapi
        text_height = paragraph.wrap(text_width, 0)[1]
        # Gambar teks pada canvas, pastikan Y disesuaikan dengan benar
        paragraph.drawOn(canvas, posd_x + 80, pos_y - text_height + 12)
        # Perbarui posisi Y setelah teks value
        pos_y -= text_height + 2  # Beri jarak antar baris setelah teks        
        return pos_y

    

    pos_y = draw_aligned_text(p, "Menetapkan", ":", "Keputusan Dekan " + context.get("faculty_name", "") + " " + context.get("university_name", "") ,  20)

    pos_y = draw_aligned_text(
    p,
    "Pertama",
    ":",
    "Menunjuk sebagai pembimbing Skripsi Saudara(i): " '<b>'+
    sk.mhs.nim.first_name +'</b>' ", NIM: " + sk.mhs.nim.username +
    ", Program Studi " + prodi + ", " + fakultas + ", " + universitas +
    ", dengan Judul \"" '<b>'+ sk.judul + '</b>'"\".",
    10)
    pos_y = draw_aligned_text(p, "", "", "Oleh:",  0)
    pos_y = draw_aligned_text(p, "", "", '1. <b>' + sk.pembimbing1.nip.first_name + '</b>',  0)
    pos_y = draw_aligned_text(p, "", "", '2. <b>' + sk.pembimbing2.nip.first_name + '</b>',  0)


    pos_y = draw_aligned_text(p, "Kedua", ":", "Jika selama maksimal enam bulan tidak ada komunikasi/interaksi akademik antara mahasiswa dengan Tim Pembimbingnya, maka Surat Keputusan ini batal dengan sendirinya.",  5)
    pos_y = draw_aligned_text(p, "Ketiga", ":", "Segala biaya yang dikeluarkan sehubungan dengan keputusan ini dibebankan pada anggaran yang tersedia pada Fakultas Ekonomi Universitas Negeri Makassar.",  5)
    pos_y = draw_aligned_text(p, "Keempat", ":", "Surat Keputusan ini berlaku pada tanggal ditetapkan, sampai dengan selesainya ujian tutup yang bersangkutan, dengan ketentuan apabila dikemudian hari ternyata terdapat kekeliruan dalam Surat Keputusan ini, akan diperbaiki sebagaimana mestinya.",  5)
    
    if sk.ttd and sk.ttd.pejabat:
        panjang_nama_dekan = A4[0] - ( p.stringWidth(sk.ttd.pejabat.nip.first_name, "Times-Bold", 10) + 60)
        panjang_tanggal = A4[0] - ( p.stringWidth("pada tanggal : " + tanggal_indo(sk.date_in), "Times-Bold", 10) + 60)
        if panjang_nama_dekan < panjang_tanggal :
            pos_x_ttd = panjang_nama_dekan
        else :
            pos_x_ttd = panjang_tanggal

        pos_y -= dl(p, pos_x_ttd, pos_y, 10, "Ditetapkan di : " + context.get("address_ttd", ""), 'N', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 10, "pada tanggal : " +  tanggal_indo(sk.date_in), 'NU', 'L')
        p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/skpbb/' + str(sk.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
        pos_y -= dl(p, pos_x_ttd, pos_y, 70, sk.ttd.pejabat.nip.first_name, 'BU', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 10, "NIP. " + sk.ttd.pejabat.nip.username, 'B', 'L')
    else:
        pos_x_ttd = A4[0] - 200 
        pos_y -= dl(p, pos_x_ttd, pos_y, 10, "Ditetapkan di : " + context.get("address_ttd", ""), 'N', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 10, "pada tanggal : " +  tanggal_indo(sk.date_in), 'NU', 'L')
        p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/skpbb/' + str(sk.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
        pos_y -= 70 
        pos_y -= dl(p, pos_x_ttd, pos_y, 10, "[Tanda Tangan Dibatalkan]", 'B', 'L')


    pos_y -= -20  # Beri jarak dari bagian sebelumnya
    p.setFont("Times-Roman", 8)
    p.drawString(posd_x, pos_y, "Tembusan:")
    pos_y -= 10
    p.drawString(posd_x + 15, pos_y, "1. Rektor UNM")
    pos_y -= 10
    p.drawString(posd_x + 15, pos_y, "2. Ketua Prodi FE UNM")
    pos_y -= 10
    p.drawString(posd_x + 15, pos_y, "3. Mahasiswa/i ybs.")



    # Menutup halaman dan menyimpan PDF
    p.setTitle("SK Pembimbing " + str(sk.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="SK Pembimbing { str(sk.mhs) }.pdf"'
    return response