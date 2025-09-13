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
from ..models import SkripsiJudul, Pejabat, Proposal
import textwrap



def print_pengesahan(request, jn, id):
    context = web_name(request)  
    skripsi = SkripsiJudul.objects.get(id=id)

    if jn == 'proposal':
        jn = 'Seminar Proposal'
    elif jn == 'hasil':
        jn = 'Seminar Hasil'
    elif jn == 'ujian':
        jn = 'Ujian Tutup Skripsi'

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50  # posisi default x kiri
  
    # AMBIL KOP
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL
    p.setFont("Times-Bold", 12)
    pos_y -= 10
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "LEMBAR PENGESAHAN", 'B', 'C')

    def draw_aligned_text(canvas, value, y_offset, bold=False):
        nonlocal pos_y
        pos_y -= y_offset
        styles = getSampleStyleSheet()
        style = ParagraphStyle(
            name='Centered',
            parent=styles['Normal'],
            fontName='Times-Bold' if bold else 'Times-Roman',
            fontSize=12,
            alignment=TA_CENTER,
            leading=14,
        )
        paragraph = Paragraph(value, style)
        text_width = 400
        _, text_height = paragraph.wrap(text_width, 100)
        paragraph.drawOn(canvas, (A4[0] - text_width) / 2, pos_y - text_height + 12)
        pos_y -= text_height + 2
        return pos_y

    # Judul skripsi
    pos_y = draw_aligned_text(p, skripsi.judul.upper(), 40, False)  

    # Identitas mahasiswa
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Diusulkan Oleh", 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, skripsi.mhs.nim.first_name.upper(), 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, skripsi.mhs.nim.username, 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Program Studi " + skripsi.prodi.nama_prodi, 'N', 'C')

    # Keterangan persetujuan
    pos_y = draw_aligned_text(
        p, "Telah diperiksa dan disetujui untuk dapat melanjutkan ke tahap " + jn, 40, False
    )  
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "Disetujui Oleh:", 'N', 'C')

    # Ambil pejabat
    kaprodi = Pejabat.objects.get(jabatan='Ketua Prodi', prodi=skripsi.prodi)
    try:
        kajur = Pejabat.objects.get(jabatan='Ketua Jurusan', jurusan=skripsi.prodi.jurusan)
    except Pejabat.DoesNotExist:
        kajur = None

    # Tentukan posisi X untuk kanan
    def posisi_kanan(nama):
        panjang = A4[0] - (p.stringWidth(nama, "Times-Bold", 12) + 60)
        return panjang if panjang < 410 else 350

    # ============================
    # POSISI PEMBIMBING
    # ============================
    pos_y_pemb = pos_y - 50
    

    # Pembimbing I (kiri)
    pos_x_pemb1 = 80
    pos_y_pemb1 = pos_y_pemb
    pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 15, "Pembimbing I", 'N', 'L')
    pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 70, skripsi.pembimbing1.nip.first_name, 'BU', 'L')
    pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 15, "NIP. " + skripsi.pembimbing1.nip.username, 'B', 'L')

    # Pembimbing II (kanan)
    pos_x_pemb2 = 360
    pos_y_pemb2 = pos_y_pemb
    pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 15, "Pembimbing II", 'N', 'L')
    pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 70, skripsi.pembimbing2.nip.first_name, 'BU', 'L')
    pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 15, "NIP. " + skripsi.pembimbing2.nip.username, 'B', 'L')

    # ============================
    # POSISI KAJUR & KAPRODI
    # ============================
    if jn != 'Seminar Proposal':
        pos_y_ttd = pos_y_pemb - 150
        pos_y_ttd -= dl(p, A4[0] / 2, pos_y_ttd, 20, "Mengetahui:", 'N', 'C')


        # Kajur (kiri)
        if kajur:
            pos_x_kajur = 360
            pos_y_kajur = pos_y_ttd
            # pos_y_kajur -= dl(p, pos_x_kajur, pos_y_kajur, 15, kajur.jabatan, 'N', 'L')
            pos_y_kajur -= dl(p, pos_x_kajur, pos_y_kajur, 15, kajur.label if getattr(kajur, 'label', None) else "", 'N', 'L')
            pos_y_kajur -= dl(p, pos_x_kajur, pos_y_kajur, 70, kajur.pejabat.nip.first_name, 'BU', 'L')
            pos_y_kajur -= dl(p, pos_x_kajur, pos_y_kajur, 15, "NIP. " + kajur.pejabat.nip.username, 'B', 'L')

        # Kaprodi (kanan)
        pos_x_kaprodi = 80
        pos_y_kaprodi = pos_y_ttd
        # pos_y_kaprodi -= dl(p, pos_x_kaprodi, pos_y_kaprodi, 15, kaprodi.jabatan, 'N', 'L')
        pos_y_kaprodi -= dl(p, pos_x_kaprodi, pos_y_kaprodi, 15, "Ketua Prodi " +  str(kaprodi.prodi), 'N', 'L')
        pos_y_kaprodi -= dl(p, pos_x_kaprodi, pos_y_kaprodi, 70, kaprodi.pejabat.nip.first_name, 'BU', 'L')
        pos_y_kaprodi -= dl(p, pos_x_kaprodi, pos_y_kaprodi, 15, "NIP. " + kaprodi.pejabat.nip.username, 'B', 'L')

    # ============================
    # SELESAI
    # ============================
    p.setTitle("Pengesahan " + jn + " " + str(skripsi.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Pengesahan {jn} {str(skripsi.mhs)}.pdf"'
    return response


################### PRINT PERSETUJUAN PENELITIAN #########################

def print_persetujuan_penelitian(request, id):
    context = web_name(request)  
    skripsi = Proposal.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 5, "PERSETUJUAN MELAKSANAKAN PENELITIAN", 'B', 'C')
   

    def draw_aligned_text(canvas, value, y_offset, bold=False):
        nonlocal pos_y
        pos_y -= y_offset
        styles = getSampleStyleSheet()
        style = ParagraphStyle(
            name='Centered',
            parent=styles['Normal'],
            fontName='Times-Bold' if bold else 'Times-Roman',
            fontSize=12,
            alignment=TA_CENTER,
            leading=14,
        )

        paragraph = Paragraph(value, style)
        text_width = 400
        _, text_height = paragraph.wrap(text_width, 100)

        paragraph.drawOn(canvas, (A4[0] - text_width) / 2, pos_y - text_height + 12)

        pos_y -= text_height + 2
        return pos_y


    pos_y = draw_aligned_text(p, skripsi.mhs_judul.judul.upper(), 30, False)  


    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Diusulkan Oleh", 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, skripsi.mhs_judul.mhs.nim.first_name.upper(), 'N', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 20, skripsi.mhs_judul.mhs.nim.username, 'N', 'C')
    pos_y = draw_aligned_text(p, "telah melewati tahapan proposal dan disetujui untuk dapat melaksanakan penelitian ", 20, False)  

    pos_y -= dl(p, A4[0] / 2, pos_y, 20, "Disetujui Oleh:", 'N', 'C')



    # ============================
    # POSISI PEMBIMBING
    # ============================
    pos_y_pemb = pos_y - 50
    

    # Pembimbing I (kiri)
    pos_x_pemb1 = 80
    pos_y_pemb1 = pos_y_pemb
    pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 15, "Pembimbing I", 'N', 'L')
    pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 70, skripsi.pembimbing1.nip.first_name, 'BU', 'L')
    pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 15, "NIP. " + skripsi.pembimbing1.nip.username, 'B', 'L')

    # Pembimbing II (kanan)
    pos_x_pemb2 = 360
    pos_y_pemb2 = pos_y_pemb
    pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 15, "Pembimbing II", 'N', 'L')
    pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 70, skripsi.pembimbing2.nip.first_name, 'BU', 'L')
    pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 15, "NIP. " + skripsi.pembimbing2.nip.username, 'B', 'L')


    # # ============================
    # # POSISI PENGUJI
    # # ============================
    # pos_y_pemb = pos_y - 170
    

    # # Penguji I (kiri)
    # pos_x_pemb1 = 80
    # pos_y_pemb1 = pos_y_pemb
    # pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 15, "Penguji I", 'N', 'L')
    # pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 70, skripsi.penguji1.nip.first_name, 'BU', 'L')
    # pos_y_pemb1 -= dl(p, pos_x_pemb1, pos_y_pemb1, 15, "NIP. " + skripsi.penguji1.nip.username, 'B', 'L')

    # # Penguji II (kanan)
    # if skripsi.penguji2:
    #     pos_x_pemb2 = 360
    #     pos_y_pemb2 = pos_y_pemb
    #     pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 15, "Penguji II", 'N', 'L')
    #     pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 70, skripsi.penguji2.nip.first_name, 'BU', 'L')
    #     pos_y_pemb2 -= dl(p, pos_x_pemb2, pos_y_pemb2, 15, "NIP. " + skripsi.penguji2.nip.username, 'B', 'L')
    # else:
    #     pass


    # kaprodi = Pejabat.objects.get(jabatan='Ketua Prodi', prodi=skripsi.mhs_judul.prodi)
    # panjang_nama_pejabat = A4[0] - ( p.stringWidth(kaprodi.pejabat.nip.first_name, "Times-Bold", 12) + 55)
    # if panjang_nama_pejabat < 250 :
    #     pos_x_ttd = panjang_nama_pejabat
    # else :
    #     pos_x_ttd = 80

    # pos_y -= dl(p, pos_x_ttd, pos_y, 320, context.get("address_ttd", "") + ", ......................", 'N', 'L')
    # # pos_y -= dl(p, pos_x_ttd, pos_y, 15, kaprodi.jabatan, 'N', 'L')
    # pos_y -= dl(p, pos_x_ttd, pos_y, 15, kaprodi.label, 'N', 'L')
    # # p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/skpbb/' + str(sk.id)), pos_x_ttd+10, pos_y-50, width=40, height=40)
    # pos_y -= dl(p, pos_x_ttd, pos_y, 95, kaprodi.pejabat.nip.first_name, 'BU', 'L')
    # pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + kaprodi.pejabat.nip.username, 'B', 'L')

    # Menutup halaman dan menyimpan PDF
    p.setTitle("Persetujuan Penelitian " + str(skripsi.mhs_judul.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Persetujuan Penelitian {str(skripsi.mhs_judul.mhs)}.pdf"'
    return response


def print_permohonan_penerbitan_sip(request, id):
    context = web_name(request)  
    skripsi = Proposal.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    
    # MARGIN SETTINGS UNTUK CENTER ALIGNMENT
    margin_left = 70    # Margin kiri
    margin_right = 70   # Margin kanan  
    content_width = A4[0] - margin_left - margin_right  # Lebar konten
    center_x = A4[0] / 2  # Titik tengah halaman
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # CARI KETUA JURUSAN - dengan pengecekan error
    kajur = Pejabat.objects.get(jabatan='Ketua Jurusan', jurusan=skripsi.mhs_judul.prodi.jurusan)
    kajur_nama = kajur.pejabat.nip.first_name
    kajur_nip = kajur.pejabat.nip.username
    kajur_jabatan = kajur.jabatan
    kajur_label = kajur.label or ""
    
    # JUDUL SURAT - CENTER ALIGNED
    p.setFont("Times-Bold", 12)
    pos_y -= 20
    judul = "PERMOHONAN PENERBITAN SURAT IZIN PENELITIAN"
    judul_width = p.stringWidth(judul, "Times-Bold", 12)
    judul_x = (A4[0] - judul_width) / 2  # Center alignment
    p.drawString(judul_x, pos_y, judul)
    pos_y -= 30
   
    # KEPADA YTH - LEFT ALIGNED DENGAN MARGIN
    p.setFont("Times-Roman", 12)
    pos_y -= 10
    p.drawString(margin_left, pos_y, "Kepada Yth.")
    pos_y -= 15
    
    p.setFont("Times-Bold", 12)
    p.drawString(margin_left + 20, pos_y, "Wakil Dekan Bidang Akademik")
    pos_y -= 15
    
    p.setFont("Times-Roman", 12)
    p.drawString(margin_left + 20, pos_y, "Fakultas Ekonomi dan Bisnis UNM")
    pos_y -= 15
    p.drawString(margin_left, pos_y, "Di")
    pos_y -= 15
    p.drawString(margin_left + 20, pos_y, "Tempat")
    pos_y -= 25

    # PEMBUKA SURAT
    p.drawString(margin_left, pos_y, "Dengan hormat,")
    pos_y -= 17
    p.drawString(margin_left, pos_y, "Yang bertanda tangan dibawah ini:")
    pos_y -= 20

    # Function untuk draw table dengan margin yang konsisten
    def draw_table_row_centered(canvas, label, value, y_pos, indent=70):
        canvas.setFont("Times-Roman", 12)
        canvas.drawString(margin_left + indent, y_pos, label)
        canvas.drawString(margin_left + indent + 80, y_pos, ": " + str(value))
        return y_pos - 16
    
    # DATA KETUA JURUSAN
    pos_y = draw_table_row_centered(p, "Nama", kajur_nama, pos_y)
    if kajur_nip:  # Hanya tampilkan NIP jika ada
        pos_y = draw_table_row_centered(p, "NIP", kajur_nip, pos_y)
    pos_y = draw_table_row_centered(p, "Jabatan", kajur_jabatan + " " + kajur_label, pos_y)
    pos_y -= 5

    # MENERANGKAN BAHWA
    p.drawString(margin_left, pos_y, "Menerangkan bahwa mahasiswa dengan identitas berikut:")
    pos_y -= 20
    
    # DATA MAHASISWA
    pos_y = draw_table_row_centered(p, "Nama", skripsi.mhs_judul.mhs.nim.first_name, pos_y)
    pos_y = draw_table_row_centered(p, "NIM", skripsi.mhs_judul.mhs.nim.username, pos_y)
    pos_y = draw_table_row_centered(p, "Jurusan", skripsi.mhs_judul.prodi.jurusan.nama_jurusan, pos_y)
    pos_y = draw_table_row_centered(p, "Program Studi", skripsi.mhs_judul.prodi.nama_prodi, pos_y)
    
    # JUDUL dengan text wrapping jika terlalu panjang
    judul_text = str(skripsi.mhs_judul.judul)
    available_width = content_width - 150  # Sisakan ruang untuk "Judul : "
    
    # Cek apakah judul perlu di-wrap
    judul_width = p.stringWidth(judul_text, "Times-Roman", 12)
    if judul_width > available_width:
        # Wrap judul berdasarkan lebar pixel yang tersedia
        def wrap_judul_by_width(canvas, text, max_width, font="Times-Roman", font_size=12):
            canvas.setFont(font, font_size)
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = current_line + [word]
                test_text = " ".join(test_line)
                
                if canvas.stringWidth(test_text, font, font_size) <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            
            if current_line:
                lines.append(" ".join(current_line))
            return lines
        
        wrapped_judul = wrap_judul_by_width(p, judul_text, available_width)
        
        # Tulis baris pertama dengan label "Judul"
        p.drawString(margin_left + 70, pos_y, "Judul")
        p.drawString(margin_left + 70 + 80, pos_y, ": " + wrapped_judul[0])
        pos_y -= 16
        
        # Tulis baris selanjutnya sejajar dengan awal teks baris pertama
        start_x_continuation = margin_left + 70 + 80 + p.stringWidth(": ", "Times-Roman", 12)
        for line in wrapped_judul[1:]:
            p.drawString(start_x_continuation, pos_y, line)
            pos_y -= 16
    else:
        pos_y = draw_table_row_centered(p, "Judul", judul_text, pos_y)
    
    pos_y -= 10
    
    # ISI SURAT DENGAN TEXT WRAPPING YANG LEBIH AKURAT
    #     pos_y = draw_aligned_text(p, "Hari/Tanggal", tanggal_indo(undangan.seminar_tgl, undangan.seminar_tgl),  15) 
    isi_text = ("Telah melaksanakan seminar proposal pada hari " + tanggal_indo(skripsi.seminar_tgl, skripsi.seminar_tgl)  + ", Serta telah "
                "menyelesaikan perbaikan-perbaikan dari dosen pembimbing dan penanggap. Untuk itu, "
                "kami harap kepada Wakil Dekan Bidang Akademik FE UNM untuk menerbitkan Surat "
                "Izin Penelitian kepada mahasiswa yang bersangkutan. Atas perhatiannya kami ucapkan "
                "terima kasih.")
    
    # Fungsi untuk text wrapping yang lebih akurat berdasarkan lebar pixel
    def wrap_text_by_width(canvas, text, max_width, font="Times-Roman", font_size=12):
        canvas.setFont(font, font_size)
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Test jika menambahkan kata ini
            test_line = current_line + [word]
            test_text = " ".join(test_line)
            
            if canvas.stringWidth(test_text, font, font_size) <= max_width:
                current_line.append(word)
            else:
                if current_line:  # Jika ada kata di line saat ini
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:  # Jika kata terlalu panjang untuk satu baris
                    lines.append(word)
                    current_line = []
        
        if current_line:  # Tambahkan line terakhir
            lines.append(" ".join(current_line))
        
        return lines
    
    # Wrap text dengan lebar yang tepat
    wrapped_lines = wrap_text_by_width(p, isi_text, content_width)
    
    for line in wrapped_lines:
        p.drawString(margin_left, pos_y, line)
        pos_y -= 15
    
    # TANGGAL DAN TEMPAT - RIGHT ALIGNED
    pos_y -= 20
    tanggal_tempat = context.get("address_ttd", "") + ", ......................"
    ttd_x = A4[0] - margin_right - p.stringWidth(tanggal_tempat, "Times-Roman", 12)
    p.drawString(ttd_x, pos_y, tanggal_tempat)
    pos_y -= 15
    
    # JABATAN PENANDATANGAN - RIGHT ALIGNED  
    jabatan_text = kajur_jabatan + " " + kajur_label
    jabatan_x = A4[0] - margin_right - p.stringWidth(jabatan_text, "Times-Roman", 12)
    p.drawString(jabatan_x, pos_y, jabatan_text)
    pos_y -= 90
    
    # NAMA DAN NIP PENANDATANGAN - RIGHT ALIGNED
    if kajur:  # Jika ketua jurusan ada
        p.setFont("Times-Bold", 12)
        nama_x = A4[0] - margin_right - p.stringWidth(kajur_nama, "Times-Bold", 12)
        p.drawString(nama_x, pos_y, kajur_nama)
        pos_y -= 15
        
        if kajur_nip:  # Hanya tampilkan NIP jika ada
            nip_text = "NIP. " + kajur_nip
            nip_x = A4[0] - margin_right - p.stringWidth(nip_text, "Times-Bold", 12)
            p.drawString(nip_x, pos_y, nip_text)
    else:
        # Jika ketua jurusan belum ditentukan
        p.setFont("Times-Bold", 12)
        placeholder_text = "[Belum Ditandatangani]"
        placeholder_x = A4[0] - margin_right - p.stringWidth(placeholder_text, "Times-Bold", 12)
        p.drawString(placeholder_x, pos_y, placeholder_text)
    
    pos_y -= 30
    
    # TEMBUSAN - LEFT ALIGNED
    p.setFont("Times-Bold", 12)
    p.drawString(margin_left, pos_y, "Tembusan:")
    pos_y -= 15
    
    p.setFont("Times-Roman", 12)
    p.drawString(margin_left, pos_y, "1. Dekan")
    pos_y -= 15
    p.drawString(margin_left, pos_y, "2. Arsip")

    # Menutup halaman dan menyimpan PDF
    p.setTitle("Permohonan Penerbitan SIP " + str(skripsi.mhs_judul.mhs))
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Permohonan Penerbitan SIP {str(skripsi.mhs_judul.mhs)}.pdf"'
    return response