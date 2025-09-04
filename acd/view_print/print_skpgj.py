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

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "KEPUTUSAN DEKAN FAKULTAS KEGURUAN DAN ILMU PENDIDIKAN:", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "UNIVERSITAS SULAWESI BARAT:", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "Nomor : " + sk.nosurat, 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "TENTANG:", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "PENETAPAN PENGUJI PROPOSAL, HASIL PENELITIAN:", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "DAN UJIAN SKRIPSI MAHASISWA FAKULTAS KEGURUAN DAN:", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "ILMU PENDIDIKAN UNIVERSITAS SULAWESI BARAT:", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 25, "DEKAN FAKULTAS KEGURUAN DAN ILMU PENDIDIKAN:", 'B', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "UNIVERSITAS SULAWESI BARAT:", 'B', 'C')


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
            fontSize=12,
            leading=14,
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
    pos_y = draw_aligned_text(p, "Menimbang", ":", "a.", "bahwa untuk membantu mahasiswa Fakultas Keguruan dan Ilmu Pendidikan Universitas Sulawesi Barat dalam menyelesaikan  Skripsinya, maka perlu mengangkat Pembimbing Proposal, Hasil Penelitian dan Ujian Skripsi Mahasiswa", 20)   
    pos_y = draw_aligned_text(p, "", "", "b.", "bahwa untuk keperluan dimaksud, maka mereka yang tersebut namanya dalam surat Keputusan ini dianggap memenuhi syarat akademik dan dipandang cakap sebagai Pembimbing Proposal, Hasil Penelitian dan Ujian Skripsi Mahasiswa",  0)   
    pos_y = draw_aligned_text(p, "", "", "c.", "bahwa sehubungan dengan point a dan b di atas, perlu diterbitkan Surat Keputusan sebagai Pembimbing Proposal, Hasil Penelitian dan Ujian Skripsi  mahasiswa.",  0)

    pos_y = draw_aligned_text(p, "Mengingat", ":", "1.", "Undang – Undang Nomor 20 Tahun 2003 tentang Sistem Pendidikan Nasional", 20)   
    pos_y = draw_aligned_text(p, "", "", "2.", "Undang – Undang Nomor 12 Tahun 2012 tentang Pendidikan Tinggi",  0)   
    pos_y = draw_aligned_text(p, "", "", "3.", "Peraturan Pemerintah Nomor 4 Tahun 2014 tentang Pengelolaan dan Penyelenggaraan Pendidikan.",  0)
    pos_y = draw_aligned_text(p, "", "", "4.", "Peraturan Presiden Republik Indonesia Nomor 8 Tahun 2012 tentang Kerangka Kualifikasi Nasional Indonesia",  0)
    pos_y = draw_aligned_text(p, "", "", "5.", "Peraturan Pemerintah Nomor 36 Tahun 2013, tentang Pendirian Universitas Sulawesi Barat Tanggal 13 Mei 2013",  0)
    pos_y = draw_aligned_text(p, "", "", "6.", "Surat Keputusan Rektor Unsulbar 12451/M/KP/2019, tentang pengangkatan Dekan Fakultas Keguruan dan Ilmu Pendidikan Universitas Sulawesi Barat",  0)


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
            fontSize=12,
            leading=14,
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

    pos_y = draw_aligned_text(p, "Menetapkan", ":", "KEPUTUSAN DEKAN FAKULTAS KEGURUAN DAN ILMU PENDIDIKAN",  20)

    p.showPage()
    pos_y = 750

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "MEMUTUSKAN:", 'B', 'C')

    pos_y = draw_aligned_text(p, "Memperhatikan", ":", "Usulan dari Program Studi tentang nama mahasiswa yang menyusun proposal dan  nama  penguji I dan penguji II",  20)



    pos_y = draw_aligned_text(p, "KESATU", ":", "Mengangkat saudara (i) :",  20)
    pos_y = draw_aligned_text(p, "", "", "1." + sk.proposal.penguji1.nip.first_name,  0)
    pos_y = draw_aligned_text(p, "", "", "2." + sk.proposal.penguji2.nip.first_name,  0)
    pos_y = draw_aligned_text(p, "", "", "Sebagai Penguji Proposal, Hasil,Penelitian dan Ujian Skripsi mahasiswa atas nama  : " + sk.proposal.mhs_judul.mhs.nim.first_name + "  Nim : " + sk.proposal.mhs_judul.mhs.nim.username,  0)

    pos_y = draw_aligned_text(p, "KEDUA", ":", "Saudara (i) yang tercantum dalam Surat Keputusan ini diberikan wewenang dan tanggung jawab untuk membimbing mahasiswa dalam Seminar Proposal, Seminar Hasil Penelitian dan Ujian Skripsi.",  20)
    pos_y = draw_aligned_text(p, "KETIGA", ":", "Surat Keputusan ini disampaikan kepada masing-masing yang bersangkutan untuk diketahui dan dilaksanakan dengan penuh rasa tanggung jawab.",  20)
    pos_y = draw_aligned_text(p, "KEEMPAT", ":", "Surat Keputusan ini berlaku sejak tanggal ditetapkan dengan ketentuan, apabila dikemudian hari ternyata terdapat kekeliruan dalam penetapan Surat Keputusan ini, maka akan diperbaiki sebagaiman mestinya.",  20)

    panjang_nama_dekan = A4[0] - ( p.stringWidth(sk.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    panjang_tanggal = A4[0] - ( p.stringWidth("pada tanggal : " + tanggal_indo(sk.date_in), "Times-Bold", 12) + 60)
    if panjang_nama_dekan < panjang_tanggal :
        pos_x_ttd = panjang_nama_dekan
    else :
        pos_x_ttd = panjang_tanggal

    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Ditetapkan di : " + context.get("address_ttd", ""), 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "pada tanggal : " +  tanggal_indo(sk.date_in), 'NU', 'L')
    p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/skpgj/' + str(sk.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, sk.ttd.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + sk.ttd.pejabat.nip.username, 'B', 'L')


    # Menutup halaman dan menyimpan PDF
    p.setTitle("SK Penguji " + str(sk.proposal.mhs_judul.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="SK Penguji { str(sk.proposal.mhs_judul.mhs) }.pdf"'
    return response