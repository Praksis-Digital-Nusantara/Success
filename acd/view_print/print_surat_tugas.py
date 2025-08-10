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
from ..models import SuratTugas, Pejabat, SuratTugas_NamaDosen, SuratTugas_NamaMhs
import textwrap



def print_surat_tugas(request, id):
    context = web_name(request)

    data = SuratTugas.objects.get(id=id)
    data_dosen = SuratTugas_NamaDosen.objects.filter(surat=data).order_by('urut')
    data_mhs= SuratTugas_NamaMhs.objects.filter(surat=data).order_by('urut')

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 65 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "SURAT TUGAS", 'BU', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Nomor: " + data.no_surat, 'N', 'C')

    pos_y -= dl(p, posd_x, pos_y, 30, "Yang bertanda tangan di bawah ini  :", 'N', 'L')

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
    
    pos_y = draw_aligned_text(p, "Nama", data.ttd.pejabat.nip.first_name,  15) 
    pos_y = draw_aligned_text(p, "NIP", data.ttd.pejabat.nip.username,  15) 
    pos_y = draw_aligned_text(p, "Pangkat/Golongan", str(data.ttd.pejabat.pangkat) + " / " + str(data.ttd.pejabat.golongan),  15) 
    if data.ttd.jabatan == 'Dekan':
        pos_y = draw_aligned_text(p, "Jabatan", "Dekan " + context.get("faculty_name", ""),  15)
    else:
        pos_y = draw_aligned_text(p, "Jabatan ", "Wakil Dekan Bidang Umum dan Keuangan",  15)

    
    pos_y -= dl(p, posd_x, pos_y, 30, "Memberikan tugas kepada : ", 'N', 'L')
    pos_y -= 15


    # Data tabel 4 kolom x 3 baris (isi contoh, silakan ganti sesuai kebutuhan)
    # Style untuk wrap text di tabel
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = 'Times-Roman'
    styleN.fontSize = 11

    # Data tabel 4 kolom x 3 baris, kolom 2 dan 4 pakai Paragraph agar bisa wrap
    # Header tabel
    table_data = [["No", "Nama", "No Induk", "Jabatan"]]

    # Tambahkan baris dari data_dosen
    for idx, datatb in enumerate(data_dosen, start=1):
        nama = getattr(datatb.dosen.nip, 'first_name', '') if datatb.dosen and datatb.dosen.nip else ''
        no_induk = getattr(datatb.dosen.nip, 'username', '') if datatb.dosen and datatb.dosen.nip else ''
        jabatan = datatb.jabatan if datatb.jabatan else ''
        table_data.append([
            str(idx),
            Paragraph(nama or '-', styleN),
            Paragraph(no_induk or '-', styleN),
            Paragraph(jabatan or '-', styleN)
        ])
    start_idx = len(data_dosen) + 1

    for idx, datatb in enumerate(data_mhs, start=start_idx):
        nama = getattr(datatb.mhs.nim, 'first_name', '') if datatb.mhs and datatb.mhs.nim else ''
        no_induk = getattr(datatb.mhs.nim, 'username', '') if datatb.mhs and datatb.mhs.nim else ''
        jabatan = datatb.jabatan if datatb.jabatan else ''
        table_data.append([
            str(idx),
            Paragraph(nama or '-', styleN),
            Paragraph(no_induk or '-', styleN),
            Paragraph(jabatan or '-', styleN)
        ])

    # Buat Table object
    table = Table(table_data, colWidths=[30, 180, 120, 120])

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




    wrapped_text = textwrap.wrap(
        "Untuk mengikuti Kegiatan " + data.nama_kegiatan +  ", yang akan dilaksanakan pada: ", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    if data.tgl_mulai == data.tgl_selesai:
        tgl_hari_kegiatan = tanggal_indo(data.tgl_mulai, hari_obj="hari_tgl")
    else:
        tgl_hari_kegiatan = tanggal_indo(data.tgl_mulai, hari_obj="hari_only") + " - " + tanggal_indo(data.tgl_selesai, hari_obj="hari_only") + ", " + tanggal_indo(data.tgl_mulai, hari_obj="tgl_only") + " - " + tanggal_indo(data.tgl_selesai, hari_obj="tgl_only")

    pos_y = draw_aligned_text(p, "Hari/Tanggal", tgl_hari_kegiatan,  15) 
    pos_y = draw_aligned_text(p, "Waktu", str(data.jam) + " WITA - Selesai",  15) 
    pos_y = draw_aligned_text(p, "Tempat", data.tempat,  15) 

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Segala biaya pada kegiatan tersebut dibebankan pada yang bersangkutan.", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Demikian surat tugas ini dibuat untuk dilaksanakan dengan penuh tanggung jawab dan segera menyampaikan laporannya secara tertulis kepada dekan dan atau pimpinan fakultas setelah melaksanakan tugas yang diamanahkan.", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    

    panjang_nama_pejabat = A4[0] - ( p.stringWidth(data.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 300 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 300        

    pos_y -= dl(p, pos_x_ttd, pos_y, 30, context.get("address_ttd", "") + ", " + tanggal_indo(data.date_in), 'N', 'L')

    if data.ttd.jabatan == 'Dekan':
        pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Dekan,", 'N', 'L')
    else:
        pos_y -= dl(p, pos_x_ttd, pos_y, 15, "a.n Dekan", 'N', 'L')
        pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Wakil Dekan Bidang Umum dan Keuangan,", 'N', 'L')
    


    if data.ttd_status == 'QRcode' :
        p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/sak/' + str(data.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, data.ttd.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + data.ttd.pejabat.nip.username, 'B', 'L')


    # Menutup halaman dan menyimpan PDF
    p.setTitle("Surat Keterangan Aktif Kuliah")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Surat Keterangan Aktif Kuliah ".pdf"'
    return response
