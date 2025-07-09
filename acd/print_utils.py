from datetime import datetime, date

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

def draw_kop_surat_fakultas(p, context):

    width, height = A4
    logo_path = context.get("baseurl", "") + "static/img/logo.png"

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
    # draw_centered_text(p, f"Jurusan {usermhs.prodi.jurusan.nama_jurusan}", 15, 12, True, True)
    draw_centered_text(p, "Alamat: " + context.get("address", ""), 15, 10)
    draw_centered_text(p, "Telepon: " +  context.get("telp","") + " Fax: " + context.get("fax",""), 10, 10)
    draw_centered_text(p, "Laman: " +  context.get("website","") + " Email: " +  context.get("email",""), 10, 10)

    # Garis bawah
    p.setLineWidth(2)
    p.line(50, pos_y - 10, width - 50, pos_y - 10)

    return pos_y - 30  # Kembalikan posisi Y terakhir untuk digunakan di konten lain



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
    # draw_centered_text(p, f"Jurusan {usermhs.prodi.jurusan.nama_jurusan}", 15, 12, True, True)
    draw_centered_text(p, "Alamat: " + context.get("address", ""), 15, 10)
    draw_centered_text(p, "Telepon: " +  context.get("telp","") + " Fax: " + context.get("fax",""), 10, 10)
    draw_centered_text(p, "Laman: " +  context.get("website","") + " Email: " +  context.get("email",""), 10, 10)

    # Garis bawah
    p.setLineWidth(2)
    p.line(50, pos_y - 10, width - 50, pos_y - 10)

    return pos_y - 30  # Kembalikan posisi Y terakhir untuk digunakan di konten lain



def tanggal_indo(tanggal_obj, hari_obj=None):
    bulan_dict = {
        "January": "Januari", "February": "Februari", "March": "Maret",
        "April": "April", "May": "Mei", "June": "Juni",
        "July": "Juli", "August": "Agustus", "September": "September",
        "October": "Oktober", "November": "November", "December": "Desember"
    }

    hari_dict = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }

    if isinstance(tanggal_obj, str):
        tanggal_obj = datetime.strptime(tanggal_obj, "%Y-%m-%d").date()

    bulan_inggris = tanggal_obj.strftime("%B")
    bulan_indonesia = bulan_dict.get(bulan_inggris, bulan_inggris)

    # Format tanggal tanpa leading zero (hilangkan '0' di depan)
    tanggal_hari = tanggal_obj.strftime("%d").lstrip("0")
    tahun = tanggal_obj.strftime("%Y")
    tanggal_format = f"{tanggal_hari} {bulan_indonesia} {tahun}"

    if hari_obj:
        if isinstance(hari_obj, str):
            hari_obj = datetime.strptime(hari_obj, "%Y-%m-%d").date()
        nama_hari = hari_dict.get(hari_obj.strftime("%A"), hari_obj.strftime("%A"))
        return f"{nama_hari}, {tanggal_format}"
    else:
        return tanggal_format


def dl(canvas, dl_pos_x, pos_y, dl_pos_y, dl_text, dl_style="N", dl_align='L'):
    pos_y -= dl_pos_y  # Pindah ke baris berikutnya
    dl_style = dl_style.upper()

    # Tentukan style berdasarkan input
    is_bold = 'B' in dl_style
    is_italic = 'I' in dl_style
    is_underline = 'U' in dl_style

    # Pilih font yang sesuai
    if is_bold and is_italic:
        font = "Times-BoldItalic"
    elif is_bold:
        font = "Times-Bold"
    elif is_italic:
        font = "Times-Italic"
    else:
        font = "Times-Roman"  # Default (jika "N")

    canvas.setFont(font, 12)

    # Gambar teks dengan alignment yang dipilih
    if dl_align == 'C':
        canvas.drawCentredString(dl_pos_x, pos_y, dl_text)
        text_width = canvas.stringWidth(dl_text, font, 12) / 2
    else:
        canvas.drawString(dl_pos_x, pos_y, dl_text)
        text_width = canvas.stringWidth(dl_text, font, 12)

    # Jika underline aktif, tambahkan garis di bawah teks
    if is_underline:
        line_y = pos_y - 2  # Garis sedikit di bawah teks
        canvas.line(dl_pos_x, line_y, dl_pos_x + text_width, line_y)

    return dl_pos_y  # Kembalikan posisi yang diperbarui