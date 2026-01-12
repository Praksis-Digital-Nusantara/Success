from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.utils import timezone
import textwrap

# Import Decorator & Utils
from ..decorators_dosen import check_userdosen, dosen_required
from aam.context_processors import web_name
from ..print_utils import tanggal_indo, draw_kop_surat, dl
from ..models import SkripsiJudul, Pejabat


def print_persetujuan_judul(request, id):
    # 1. Ambil Data
    judul = get_object_or_404(SkripsiJudul, id=id)
    usermhs = judul.mhs
    now = timezone.now().date()
    
    # Context
    context = web_name(request)  
    
    # Cari Kajur & Kaprodi
    jurusan_mhs = usermhs.prodi.jurusan if usermhs.prodi else None
    
    kajur = None
    if jurusan_mhs:
        kajur = Pejabat.objects.filter(
            jabatan='Ketua Jurusan',
            jurusan=jurusan_mhs,
            tgl_mulai__lte=now,
            tgl_selesai__gte=now
        ).first()

    kaprodi = Pejabat.objects.filter(
        jabatan='Ketua Prodi',
        prodi=usermhs.prodi,
        tgl_mulai__lte=now,
        tgl_selesai__gte=now
    ).first()

    # Data Kajur untuk Halaman 2 (Sender)
    kajur_nama = kajur.pejabat.nip.first_name if kajur else "(....................................)"
    kajur_nip = kajur.pejabat.nip.username if kajur else "...................................."

    # Setup PDF
    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 
    width, height = A4

    # =========================================================================
    # HALAMAN 1: USULAN JUDUL TUGAS AKHIR
    # =========================================================================
    
    # Kop Surat Halaman 1
    pos_y = draw_kop_surat(p, context, usermhs)

    # Judul
    p.setFont("Times-Bold", 12)
    p.drawCentredString(width / 2, pos_y - 5, "USULAN JUDUL TUGAS AKHIR")
    pos_y -= 25

    # Helper function text align
    def draw_aligned_text(canvas, label, value, y_offset, val_x=200):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset
        canvas.drawString(posd_x, pos_y, label)  
        canvas.drawString(180, pos_y, ":")  
        canvas.drawString(val_x, pos_y, value if value else "-")        
        return pos_y

    # Identitas Mahasiswa
    fname = usermhs.nim.first_name.title() if usermhs.nim.first_name else ""
    # mhs_name = f"{usermhs.nim.first_name}" 
    mhs_name = f"{fname}".strip()
    pos_y = draw_aligned_text(p, "Nama Mahasiswa", mhs_name, 12)
    pos_y = draw_aligned_text(p, "NIM", usermhs.nim.username, 15)
    
    nama_jurusan = usermhs.prodi.jurusan.nama_jurusan if usermhs.prodi and usermhs.prodi.jurusan else "-"
    pos_y = draw_aligned_text(p, "Jurusan", nama_jurusan, 15)
    pos_y = draw_aligned_text(p, "Program Studi", usermhs.prodi.nama_prodi, 15)
    
    ttl = f"{usermhs.tempat_lahir}, {tanggal_indo(usermhs.tgl_lahir)}"
    pos_y = draw_aligned_text(p, "Tempat/ Tgl. Lahir", ttl, 15)

    # Judul yang diajukan
    pos_y -= dl(p, posd_x, pos_y, 30, "Judul Yang Diajukan :", 'B', 'L')

    def draw_multiline_item(canvas, number, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x, pos_y, number)
        clean_value = value if value else "................................................"
        wrapped_text = textwrap.wrap(clean_value, width=100)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 20, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 20, pos_y, line)
        return pos_y  
    
    pos_y = draw_multiline_item(p, "1.", judul.judul1,  15)   
    pos_y = draw_multiline_item(p, "2.", judul.judul2,  15)   
    pos_y = draw_multiline_item(p, "3.", judul.judul3,  15)

    # Tanda Tangan Tengah (Pengajuan)
    pos_y -= 25
    ttd_top_y = pos_y
    left_x = posd_x
    right_x = width - 250
    
    p.drawString(right_x, ttd_top_y, f"{context.get('address_ttd', 'Makassar')}, {tanggal_indo(judul.date_in)}")
    ttd_top_y -= 15
    p.drawString(left_x, ttd_top_y, "Disetujui Oleh")
    p.drawString(right_x, ttd_top_y, "Diajukan Oleh")
    ttd_top_y -= 15
    p.drawString(left_x, ttd_top_y, "Penasehat Akademik,")
    p.drawString(right_x, ttd_top_y, "Mahasiswa Ybs,")

    # QR Code Placeholder
    if judul.status != 'Waiting' and usermhs.penasehat_akademik:
        try:
            qr_path = context.get("api_qrcode", "") + context.get("baseurl", "") + 't/puj/' + str(judul.id)
            p.drawImage(ImageReader(qr_path), left_x + 10, ttd_top_y - 55, width=40, height=40)
        except: pass

    try:
        qr_mhs_path = context.get("api_qrcode", "") + context.get("baseurl", "") + 't/puj/' + str(judul.id)
        p.drawImage(ImageReader(qr_mhs_path), right_x + 10, ttd_top_y - 55, width=40, height=40)
    except: pass

    ttd_top_y -= 70
    pa_name = usermhs.penasehat_akademik.nip.first_name if usermhs.penasehat_akademik else ".........................."
    pa_nip = usermhs.penasehat_akademik.nip.username if usermhs.penasehat_akademik else ".........................."
    
    p.setFont("Times-Bold", 12)
    p.drawString(left_x, ttd_top_y, pa_name)
    p.setFont("Times-Roman", 12)
    p.drawString(left_x, ttd_top_y - 15, "NIP. " + pa_nip)

    p.setFont("Times-Bold", 12)
    p.drawString(right_x, ttd_top_y, mhs_name)
    p.setFont("Times-Roman", 12)
    p.drawString(right_x, ttd_top_y - 15, "NIM. " + usermhs.nim.username)

    pos_y = ttd_top_y - 40

    # Bagian Bawah: Persetujuan Pimpinan
    p.line(posd_x, pos_y, width-50, pos_y)
    pos_y -= 20
    p.setFont("Times-Bold", 12)
    p.drawCentredString(width / 2, pos_y, "PERSETUJUAN PIMPINAN PROGRAM STUDI DAN JURUSAN")
    
    pos_y -= 25
    p.drawString(posd_x, pos_y, "Judul yang disetujui:")
    final_judul = judul.judul if judul.kajur_persetujuan == 'Approved' else "............................................................................................................"
    
    pos_y -= 15
    p.setFont("Times-Roman", 12)
    wrapped_final = textwrap.wrap(final_judul, width=90)
    for line in wrapped_final:
        p.drawString(posd_x, pos_y, line)
        pos_y -= 15
    if len(wrapped_final) < 2: pos_y -= 15

    pos_y -= 10
    p.setFont("Times-Bold", 12)
    p.drawString(posd_x, pos_y, "Pembimbing yang ditunjuk:")
    p.setFont("Times-Roman", 12)
    pbb1 = judul.pembimbing1.nip.first_name if judul.pembimbing1 else "..........................................................."
    pos_y -= 15
    p.drawString(posd_x, pos_y, f"1. {pbb1}")
    pbb2 = judul.pembimbing2.nip.first_name if judul.pembimbing2 else "..........................................................."
    pos_y -= 15
    p.drawString(posd_x, pos_y, f"2. {pbb2}")

    pos_y -= 30
    ttd_bot_y = pos_y
    p.drawString(left_x, ttd_bot_y, "Mengetahui,")
    ttd_bot_y -= 15
    p.drawString(left_x, ttd_bot_y, "Ketua Program Studi")
    p.drawString(left_x, ttd_bot_y - 15, usermhs.prodi.nama_prodi)

    ttd_bot_y_right = pos_y - 15
    p.drawString(right_x, ttd_bot_y_right, f"Ketua {nama_jurusan}")

    ttd_bot_y -= 70

    if judul.kajur_persetujuan == 'Approved':
        try:
            # Sesuaikan 't/pgj_kajur/' dengan URL pattern QR code Anda
            qr_kajur_path = context.get("api_qrcode", "") + context.get("baseurl", "") + 't/puj/' + str(judul.id)
            # Posisi: X = right_x (posisi kajur), Y = ttd_bot_y + 10 (sedikit di atas nama)
            p.drawImage(ImageReader(qr_kajur_path), right_x + 10, ttd_bot_y + 10, width=40, height=40)
        except Exception as e:
            print(f"Error loading QR Kajur: {e}")
            pass

    if judul.kajur_persetujuan == 'Approved':
            try:
                # Sesuaikan 't/pgj_kajur/' dengan URL pattern QR code Anda
                qr_kaprodi_path = context.get("api_qrcode", "") + context.get("baseurl", "") + 't/puj/' + str(judul.id)
                p.drawImage(ImageReader(qr_kaprodi_path), left_x + 10, ttd_bot_y + 10, width=40, height=40)
            except Exception as e:
                print(f"Error loading QR Kajur: {e}")
                pass

    kaprodi_nama = kaprodi.pejabat.nip.first_name if kaprodi else "(....................................)"
    kaprodi_nip = kaprodi.pejabat.nip.username if kaprodi else "...................................."
    
    p.setFont("Times-Bold", 12)
    p.drawString(left_x, ttd_bot_y, kaprodi_nama)
    p.setFont("Times-Roman", 12)
    p.drawString(left_x, ttd_bot_y - 15, "NIP. " + kaprodi_nip)

    p.setFont("Times-Bold", 12)
    p.drawString(right_x, ttd_bot_y, kajur_nama)
    p.setFont("Times-Roman", 12)
    p.drawString(right_x, ttd_bot_y - 15, "NIP. " + kajur_nip)

    # =========================================================================
    # HALAMAN 2: PERMOHONAN PENERBITAN SK 
    # =========================================================================
    
    p.showPage()  # <--- PINDAH HALAMAN
    
    # Reset Posisi Y untuk halaman baru
    # Gambar Kop Surat Halaman 2
    pos_y = draw_kop_surat(p, context, usermhs)
    
    # Judul Halaman 2 [cite: 47]
    pos_y -= 5
    p.setFont("Times-Bold", 12)
    p.drawCentredString(width / 2, pos_y, "PERMOHONAN PENERBITAN SK PEMBIMBING TUGAS AKHIR")
    
    # Tujuan Surat [cite: 48-50]
    pos_y -= 35
    p.setFont("Times-Roman", 12)
    p.drawString(posd_x, pos_y, "Kepada Yth.")
    pos_y -= 15
    p.drawString(posd_x, pos_y, "Dekan Fakultas Ekonomi dan Bisnis UNM") # Sesuaikan Fakultas jika dinamis
    pos_y -= 15
    p.drawString(posd_x, pos_y, "Di Makassar")
    
    # Pembuka [cite: 51]
    pos_y -= 25
    p.drawString(posd_x, pos_y, "Dengan hormat,")
    pos_y -= 15
    p.drawString(posd_x, pos_y, "Yang bertanda tangan dibawah ini,")
    
    # Identitas Kajur (Yang bertanda tangan) [cite: 53-55]
    pos_y -= 15
    draw_aligned_text(p, "Nama", kajur_nama, 0, 200)
    pos_y -= 15
    draw_aligned_text(p, "NIP", kajur_nip, 0, 200)
    pos_y -= 15
    draw_aligned_text(p, "Jabatan", f"Ketua {nama_jurusan}", 0, 200)
    
    # Keterangan Mahasiswa [cite: 56]
    pos_y -= 25
    p.drawString(posd_x, pos_y, "Menerangkan bahwa mahasiswa atas nama:")
    
    # Identitas Mahasiswa di Hal 2 [cite: 57-60]
    pos_y -= 15
    draw_aligned_text(p, "Nama", mhs_name, 0, 200)
    pos_y -= 15
    draw_aligned_text(p, "NIM", usermhs.nim.username, 0, 200)
    pos_y -= 15
    draw_aligned_text(p, "Jurusan", nama_jurusan, 0, 200)
    pos_y -= 15
    draw_aligned_text(p, "Program Studi", usermhs.prodi.nama_prodi, 0, 200)
    
    # Isi Surat (Body Text) [cite: 62-63]
    pos_y -= 25
    body_text = (
        "Telah mengusulkan judul Tugas Akhir dan telah disetujui oleh dosen Penasihat Akademik. "
        "Untuk itu kami memohon kepada Bapak/Ibu untuk memberikan/menerbitkan SK Pembimbing Tugas Akhir "
        "sesuai dengan Judul Tugas Akhir (Terlampir) kepada mahasiswa yang bersangkutan."
    )
    
    text_object = p.beginText(posd_x, pos_y)
    text_object.setFont("Times-Roman", 12)
    # textwrap body agar rapi kanan-kiri (approx)
    wrapped_body = textwrap.wrap(body_text, width=85)
    for line in wrapped_body:
        text_object.textLine(line)
    p.drawText(text_object)
    
    # Update pos_y setelah paragraf
    pos_y -= (len(wrapped_body) * 14) + 10
    
    # Penutup [cite: 64]
    closing_text = "Demikian penyampaian kami, atas perhatian dan kerjasama Bapak/Ibu kami ucapkan terima kasih."
    p.drawString(posd_x, pos_y, closing_text)
    
    # Tanda Tangan Kajur (Kanan Bawah) [cite: 65-69]
    pos_y -= 40
    right_x_ttd = width - 250
    p.drawString(right_x_ttd, pos_y, f"Makassar, {tanggal_indo(now)}")
    pos_y -= 15
    p.drawString(right_x_ttd, pos_y, f"Ketua {nama_jurusan},")
    
    pos_y -= 60
    
    # --- LOGIC QR CODE KAJUR HALAMAN 2 ---
    if judul.kajur_persetujuan == 'Approved':
        try:
            qr_kajur_path = context.get("api_qrcode", "") + context.get("baseurl", "") + 't/puj/' + str(judul.id)
            p.drawImage(ImageReader(qr_kajur_path), right_x_ttd + 10, pos_y + 10, width=40, height=40)
        except Exception: pass


    p.setFont("Times-Bold", 12)
    p.drawString(right_x_ttd, pos_y, kajur_nama)
    p.setFont("Times-Roman", 12)
    p.drawString(right_x_ttd, pos_y - 15, f"NIP. {kajur_nip}")
    
    # Catatan Kaki (Footer Info) [cite: 70-72]
    # Posisi di paling bawah halaman
    footer_y = 100
    p.setFont("Times-Italic", 10)
    p.drawString(posd_x, footer_y, "Catatan:")
    footer_y -= 12
    p.drawString(posd_x, footer_y, "Setelah diisi lengkap dengan tandatangan Ketua Program studi, silahkan dibawah ke ketua jurusan untuk ditandatangani.")
    # footer_y -= 12
    # p.drawString(posd_x, footer_y, "Info lebih lanjut (WA): ...")

    # Finalisasi
    p.setTitle(f"Usulan & Permohonan SK - {usermhs.nim.username}")
    p.showPage()
    p.save()
    
    filename = f"Usulan_SK_{usermhs.nim.username}.pdf"
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
