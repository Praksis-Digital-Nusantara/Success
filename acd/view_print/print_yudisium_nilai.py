from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph

from aam.context_processors import web_name
from ..print_utils import tanggal_indo, draw_kop_surat_fakultas, dl
from ..models import Ujian, Pejabat
import textwrap



def print_yudisium_nilai(request, id):
    context = web_name(request)

    data = Ujian.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 65 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "BERITA ACARA YUDIDIUM", 'BU', 'C')

    pos_y -= 30

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x + 30, pos_y, label)
        canvas.drawString(posd_x + 150, pos_y, ':')
        wrapped_text = textwrap.wrap(value, width=60)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 160, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 160, pos_y, line)
        return pos_y  
    
    pos_y = draw_aligned_text(p, "Nama", data.mhs_judul.mhs.nim.first_name,  15) 
    pos_y = draw_aligned_text(p, "NIM", data.mhs_judul.mhs.nim.username,  15) 
    pos_y = draw_aligned_text(p, "Program Studi", str(data.mhs_judul.mhs.prodi),  15) 
    pos_y = draw_aligned_text(p, "Judul Penelitian ", str(data.mhs_judul),  15)
    
    pos_y -= 15

    # Data tabel 4 kolom x 3 baris (isi contoh, silakan ganti sesuai kebutuhan)
    # Style untuk wrap text di tabel
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 11

    # Data tabel 4 kolom x 3 baris, kolom 2 dan 4 pakai Paragraph agar bisa wrap
    # Header tabel
    table_data = [
                    ["No", "Aspek", "KS", "SS", "B1", "B2", "U1", "U2", "Total"],
                    ["1", "Kajian Teori ", "KS", "SS", "B1", "B2", "U1", "U2"],
                    ["2", "Metode Penelitian ", "KS", "SS", "B1", "B2", "U1", "U2"],
                    ["3", "Pembahasan Hasil Penelitian ", "KS", "SS", "B1", "B2", "U1", "U2"],
                    ["4", "Kaidah Penulisan ", "KS", "SS", "B1", "B2", "U1", "U2"],
                    ["5", "Kemampuan Presentasi ", "KS", "SS", "B1", "B2", "U1", "U2"],
                    ["6", "Penguasaan Materi ", "KS", "SS", "B1", "B2", "U1", "U2"],
                ]

    # Buat Table object
    table = Table(table_data, colWidths=[30, 180, 30, 30, 30, 30, 30, 30, 50])

    # Style tabel
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),  # Kolom No rata tengah
        ('ALIGN', (2,0), (2,-1), 'CENTER'),  # Kolom No Induk rata tengah
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
    ]))

    # Hitung tinggi tabel sebelum menggambar
    table_width, table_height = table.wrapOn(p, 0, 0)

    # Misal ingin menulis tabel tepat di bawah pos_y:
    table_x = posd_x + 10
    table_y = pos_y - table_height  # geser ke bawah sesuai tinggi tabel

    # Gambar tabel
    table.drawOn(p, table_x, table_y)

    # Update pos_y jika ingin menulis di bawah tabel
    pos_y = table_y - 15 


    # Menutup halaman dan menyimpan PDF
    p.setTitle("Nilai Ujian Yudisium")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Nilai Ujian Yudisium") ".pdf"'
    return response
