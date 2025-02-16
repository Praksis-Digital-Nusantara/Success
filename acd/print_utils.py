from datetime import datetime, date

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

def draw_kop_surat(p, context, usermhs):

    width, height = A4
    logo_path = "static/img/logo.png"

    # Tambahkan logo
    p.drawImage(ImageReader(logo_path), 50, height - 120, width=80, height=80)

    # Posisi awal teks
    text_x = width / 2 + 30
    pos_y = height - 50  

    # Fungsi untuk menulis teks tengah
    def draw_centered_text(canvas, text, y_offset, font_size=12, bold=False, uppercase=False):
        nonlocal pos_y
        if uppercase:
            text = text.upper()  # Ubah teks ke huruf besar jika opsi diaktifkan
        
        if bold:
            canvas.setFont("Times-Bold", font_size)  
        else:
            canvas.setFont("Times-Roman", font_size)
        
        text_width = canvas.stringWidth(text, "Times-Roman", font_size)
        pos_y -= y_offset  
        canvas.drawString(text_x - text_width / 2, pos_y, text)

    # Tambahkan informasi kop surat
    draw_centered_text(p, context.get("ministry_name", ""), 0, 12, True, True)
    draw_centered_text(p, context.get("university_name", ""), 15, 14, True, True)
    draw_centered_text(p, context.get("faculty_name", ""), 15, 12, True, True)
    draw_centered_text(p, f"Jurusan {usermhs.prodi.jurusan.nama_jurusan}", 15, 12, True, True)
    draw_centered_text(p, "Alamat: Jl. Raya Pendidikan Makassar", 15, 10)
    draw_centered_text(p, "Telepon: (0411) 889464 - 881244 Fax. (0411) 889464", 10, 10)
    draw_centered_text(p, "Laman: www.fe.unm.ac.id ; Email: bisnis_kewirausahaanfe@unm.ac.id", 10, 10)

    # Garis bawah
    p.setLineWidth(2)
    p.line(50, pos_y - 10, width - 50, pos_y - 10)

    return pos_y - 30  # Kembalikan posisi Y terakhir untuk digunakan di konten lain



def tanggal_indo(tanggal_obj):
    bulan_dict = {
        "January": "Januari", "February": "Februari", "March": "Maret",
        "April": "April", "May": "Mei", "June": "Juni",
        "July": "Juli", "August": "Agustus", "September": "September",
        "October": "Oktober", "November": "November", "December": "Desember"
    }

    if isinstance(tanggal_obj, str):
        tanggal_obj = datetime.strptime(tanggal_obj, "%Y-%m-%d").date()
    
    bulan_inggris = tanggal_obj.strftime("%B")  # Ambil nama bulan dalam bahasa Inggris
    bulan_indonesia = bulan_dict.get(bulan_inggris, bulan_inggris)  # Ambil nama bulan dari dict
    return tanggal_obj.strftime("%d") + f" {bulan_indonesia} " + tanggal_obj.strftime("%Y")


def dl(canvas, dl_pos_x, pos_y, dl_pos_y, dl_text, dl_bold=False, dl_align='L'):
    pos_y -= dl_pos_y
    if dl_bold==False:
        canvas.setFont("Times-Roman", 12)
    else:
        canvas.setFont("Times-Bold", 12)
    if dl_align=='C':
        canvas.drawCentredString(dl_pos_x, pos_y, dl_text)
    else:    
        canvas.drawString(dl_pos_x, pos_y, dl_text)
    return dl_pos_y