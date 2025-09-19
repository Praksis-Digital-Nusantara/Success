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


def print_persetujuan_waktu_ujian(request, id):
    context = web_name(request)
    pwu = Ujian.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50  # posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5
    pos_y -= dl(p, text_x, pos_y, 5, "PERSETUJUAN WAKTU UJIAN SKRIPSI", 'B', 'C')
    pos_y -= dl(p, posd_x, pos_y, 30, "Kepada Yth,", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Bapak/Ibu/Ketua/Wakil Ketua/Dosen Pembimbing/Penanggap", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "di-", 'N', 'L')
    pos_y -= dl(p, posd_x, pos_y, 15, "Tempat", 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "", 'N', 'L')  # enter kosong

    wrapped_text = textwrap.wrap(
        "Dalam rangka pelaksanaan ujian skripsi mahasiswa berikut:", 
        width=100 
    )
    for line in wrapped_text:
        pos_y -= dl(p, posd_x, pos_y, 30, line, 'N', 'L')

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
    
    # Data mahasiswa
    pos_y = draw_aligned_text(p, "Nama", pwu.mhs_judul.mhs.nim.first_name, 30) 
    pos_y = draw_aligned_text(p, "NIM", pwu.mhs_judul.mhs.nim.username, 15) 
    pos_y = draw_aligned_text(p, "Jurusan", pwu.mhs_judul.mhs.prodi.jurusan.nama_jurusan, 15) 
    pos_y = draw_aligned_text(p, "Program Studi", pwu.mhs_judul.prodi.nama_prodi, 15) 
    pos_y = draw_aligned_text(p, "Judul", pwu.mhs_judul.judul, 15) 
    pos_y -= dl(p, posd_x, pos_y, 30, "Dimohon kesediaan Bapak/Ibu untuk memberikan persetujuan waktu:", 'N', 'L')

    # ======================================================
    # FUNGSI TABEL WAKTU UJIAN (DIPERBAIKI)
    # ======================================================
    def draw_exam_schedule_table(p, pos_x, pos_y, row_height=30):
        # Lebar kolom sesuai dengan gambar
        p.setLineWidth(0.8)
        col_widths = [25, 180, 80, 120, 100]  # NO, Nama, Jabatan, Waktu, Tanda Tangan
        num_rows = 8  # total baris (header + 7 data)
        
        # Hitung total lebar tabel
        table_width = sum(col_widths)
        
        # ====== GAMBAR GARIS HORIZONTAL ======
        for i in range(num_rows + 1):
            y = pos_y - (i * row_height)
            if 2 <= i <= 7:  # Baris dalam area merge (kecuali baris pertama setelah header)
                # Gambar garis horizontal hanya sampai kolom ke-3
                merge_start_x = pos_x + sum(col_widths[:3])
                p.line(pos_x, y, merge_start_x, y)
                # Gambar garis horizontal setelah area merge
                merge_end_x = pos_x + sum(col_widths[:4])
                p.line(merge_end_x, y, pos_x + table_width, y)
            else:
                # Gambar garis horizontal normal (header, baris pertama setelah header, dan baris terakhir)
                p.line(pos_x, y, pos_x + table_width, y)
        
        # ====== GAMBAR GARIS VERTIKAL ======
        x = pos_x
        for i, w in enumerate(col_widths):
            # Gambar semua garis vertikal normal (tidak ada yang dihilangkan)
            p.line(x, pos_y, x, pos_y - (num_rows * row_height))
            x += w
        
        # Garis vertikal terakhir (kanan tabel)
        p.line(x, pos_y, x, pos_y - (num_rows * row_height))
        
        # ====== HEADER TABEL ======
        p.setFont("Times-Bold", 11)
        headers = ["NO", "Nama", "Jabatan", "Waktu yang Disediakan", "Tanda Tangan"]
        
        # Gambar header normal kecuali kolom "Waktu yang Disediakan"
        x = pos_x
        for i, header in enumerate(headers):
            if header == "Waktu yang Disediakan":
                x += col_widths[i]
                continue
            
            # Posisi tengah kolom
            center_x = x + col_widths[i] / 2
            center_y = pos_y - row_height + 15
            p.drawCentredString(center_x, center_y, header)
            x += col_widths[i]
        
        # ====== HEADER KHUSUS "Waktu yang Disediakan" ======
        waktu_x = pos_x + sum(col_widths[:3])  # Posisi kolom waktu
        waktu_w = col_widths[3]                # Lebar kolom waktu
        
        # Posisi tengah kolom waktu
        center_x = waktu_x + waktu_w / 2
        center_y = pos_y - (row_height / 2)
        
        # Tulis teks header dalam 2 baris
        p.drawCentredString(center_x, center_y + 6, "Waktu yang")
        p.drawCentredString(center_x, center_y - 6, "Disediakan")
        
        # ====== ISI TABEL ======
        p.setFont("Times-Roman", 11)
        
        # Data pembimbing dan penguji
        table_data = [
            {"nama": pwu.dekan.pejabat.nip.first_name if pwu.pembimbing1 else "", 
             "jabatan": "Ketua"},
            {"nama": pwu.wd.pejabat.nip.first_name if pwu.pembimbing2 else "", 
             "jabatan": "Wakil Ketua"},
            {"nama": pwu.sekretaris.nip.first_name if pwu.sekretaris else "", 
             "jabatan": "Sekretaris"},
            {"nama": pwu.pembimbing1.nip.first_name if pwu.pembimbing1 else "", 
             "jabatan": "Pembimbing I"},
            {"nama": pwu.pembimbing2.nip.first_name if pwu.pembimbing2 else "", 
             "jabatan": "Pembimbing II"},
            {"nama": pwu.penguji1.nip.first_name if pwu.penguji1 else "", 
             "jabatan": "Penanggap I"},
            {"nama": pwu.penguji2.nip.first_name if pwu.penguji2 else "", 
             "jabatan": "Penanggap II"},
        ]
        
        # Fungsi untuk memecah nama yang terlalu panjang
        def wrap_text_by_width(text, font_name, font_size, max_width):
            """
            Memecah text berdasarkan lebar pixel maksimum
            """
            if not text:
                return [""]
            
            # Cek apakah text muat dalam satu baris
            text_width = p.stringWidth(text, font_name, font_size)
            if text_width <= max_width:
                return [text]
            
            # Jika tidak muat, pecah berdasarkan kata
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                # Test apakah menambah kata ini masih muat
                test_line = current_line + (" " if current_line else "") + word
                test_width = p.stringWidth(test_line, font_name, font_size)
                
                if test_width <= max_width:
                    current_line = test_line
                else:
                    # Jika current_line kosong tapi kata tunggal terlalu panjang
                    if not current_line:
                        # Paksa masukkan kata walaupun panjang
                        current_line = word
                    else:
                        # Simpan baris saat ini dan mulai baris baru
                        lines.append(current_line)
                        current_line = word
            
            # Tambahkan sisa baris terakhir
            if current_line:
                lines.append(current_line)
            
            return lines
        
        # Isi semua baris 1-7 dengan nomor urut, nama, dan jabatan
        for row in range(1, 8):
            # Nomor urut
            center_x = pos_x + col_widths[0] / 2
            center_y = pos_y - ((row + 1) * row_height) + 14
            p.drawCentredString(center_x, center_y, str(row))
            
            # Nama dan Jabatan
            if row <= len(table_data):
                # Nama (kolom ke-2) - dengan text wrapping khusus untuk nama
                nama = table_data[row - 1]["nama"]
                nama_x = pos_x + col_widths[0] + 10  # Posisi kiri kolom nama + padding
                
                # Pecah nama jika terlalu panjang
                # Kurangi padding dari lebar kolom (10 pixel kiri + 10 pixel kanan)
                max_nama_width = col_widths[1] - 20
                nama_lines = wrap_text_by_width(nama, "Times-Roman", 11, max_nama_width)
                
                # Gambar setiap baris nama
                for i, line in enumerate(nama_lines):
                    nama_y = pos_y - ((row + 1) * row_height) + 14 - (i * 10)  # 12 pixel jarak antar baris
                    p.drawString(nama_x, nama_y, line)
                
                # Jabatan (kolom ke-3) - tetap dalam satu baris
                jabatan = table_data[row - 1]["jabatan"]
                jabatan_x = pos_x + col_widths[0] + col_widths[1] + 10  # Posisi kiri kolom jabatan + padding
                jabatan_y = pos_y - ((row + 1) * row_height) + 15
                p.drawString(jabatan_x, jabatan_y, jabatan)

                ttd_center_x = pos_x + sum(col_widths[:4]) + 5  # Posisi tengah kolom tanda tangan
                ttd_center_y = pos_y - ((row + 1) * row_height) + 15
                p.drawCentredString(ttd_center_x, ttd_center_y, str(row))
        
        merge_start_row = 1
        merge_end_row = 7
        total_merge_height = (merge_end_row - merge_start_row + 1) * row_height
        
        # Posisi tengah vertikal dari area merge
        merge_center_y = pos_y - ((merge_start_row + 1) * row_height) - (total_merge_height / 2) + row_height
        merge_center_x = waktu_x + waktu_w / 2
        
        p.setFont("Times-Bold", 10)
        p.drawCentredString(merge_center_x, merge_center_y + 8, tanggal_indo(pwu.ujian_tgl, pwu.ujian_tgl))
        p.drawCentredString(merge_center_x, merge_center_y - 8, str(pwu.ujian_jam) + " WITA - Selesai",)
        return pos_y - (num_rows * row_height)
    
    pos_y -= 20  # Beri jarak sebelum tabel
    pos_y = draw_exam_schedule_table(p, posd_x, pos_y)

    panjang_nama_pejabat = A4[0] - ( p.stringWidth(pwu.kaprodi.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 300 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 360
    pos_y -= dl(p, pos_x_ttd, pos_y, 30, "Makassar, " + tanggal_indo(pwu.date_in), 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Ketua Program Studi " + pwu.kaprodi.prodi.nama_prodi,  'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, pwu.kaprodi.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + pwu.kaprodi.pejabat.nip.username, 'B', 'L')

    # Tutup PDF
    p.setTitle("Persetujuan Waktu Ujian Skripsi")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Persetujuan_Waktu_Ujian.pdf"'
    return response