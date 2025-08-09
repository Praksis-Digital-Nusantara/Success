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
from ..models import Yudisium
import textwrap





def print_yudisium(request, id):
    context = web_name(request)
    data = Yudisium.objects.filter(ujian__id=id).first()
  
    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 65 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    # pos_y = draw_kop_surat_fakultas(p, context)
    pos_y = 800  # Set a default position for the top of the page

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "BERITA ACARA YUDISIUM", 'BU', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "Nomor: " + str(data.no_surat), '', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 30, "BISMILLAHIRRAHMANIRRAHIM", '', 'C')
    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "ASSALAMUALIKUM WARAHMATULLAHI WABARAKATUH", '', 'C') 

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Dengan Rahmat Tuhan Yang Maha Esa, Dekan " + context.get("faculty_name", "") + " " + context.get("university_name", "") + "  Menyatakan bahwa Pada hari ini " + tanggal_indo(data.date_in, data.date_in) + " mahasiswa berhak mengikutkan gelar akademik di belakang nama, dengan catatan: ", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    wrapped_text = textwrap.wrap(
        data.catatan, 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    pos_y -= dl(p, posd_x, pos_y, 15, "Nama Mahasiswa : " + data.ujian.mhs_judul.mhs.nim.first_name, 'N', 'L') 
    pos_y -= dl(p, posd_x, pos_y, 15, "NIM : " + data.ujian.mhs_judul.mhs.nim.username, 'N', 'L') 


    strata_prodi = data.ujian.mhs_judul.mhs.prodi.strata
    if strata_prodi == 'S1':
        label_strata = "Strata Satu (S1)"
    elif strata_prodi == 'S2':
        label_strata = "Strata Dua (S2)"
    elif strata_prodi == 'D4':
        label_strata = "Diploma Empat (D4)"
    elif strata_prodi == 'D3':
        label_strata = "Diploma Tiga (D3)"
    elif strata_prodi == 'D2':
        label_strata = "Diploma Dua (D2)"
    elif strata_prodi == 'D1':
        label_strata = "Diploma Satu (D1)"


    wrapped_text = textwrap.wrap(
        "Program Studi " + str(data.ujian.mhs_judul.mhs.prodi) + ", telah lulus pada " + label_strata + " dengan Indeks Prestasi Kumulatif (IPK) : " + str(data.ipk) + "  atau  dengan kualifikasi : " + data.kualifikasi, 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Dengan demikian andapabila dalam jangka waktu 1 minggu terhitung mulai dari tanggal berita acara yudisium ini anda tidak memenuhi semua kewajiban yang terkait di prodi, fakultas, maupun universitas., maka kelulusan anda ditunda / sampai 1 bulan kemudian .", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Selamat dan sukses atas keberhasilan yang saudara raih pada hari ini. Selamat berbahagia buat anda dan seluruh keluarga anda seraya menyampaikan terima kasih atas kepercayaannya kepada kami kepada Lembaga ini " + context.get("faculty_name", "") + " " + context.get("university_name", "") + " semoga kepercayaan dan Kerjasama ini dapat kita jalin sepanjang masa.", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    wrapped_text = textwrap.wrap(
        "Pesan kami, janganlah berhenti belajar..Karena sukses yang anda raih pada hari ini adalah modal awal menuju masyarakat yang lebih luas, disanalah dimasyarakat dengan tingkat strata anda akan menjalani ujian yang hakiki, dan kami yakin denga modal yang anda miliki dan dengan belajar terus menerus kami yakin anda akan lulus dan mendapatkan apresiasi tertinggi dari masyarakat. Kami selalu menanti kabar kesuksesan anda selanjutnya.", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Terimakasih juga saya sampaikan kepada dosen penasehat akademik, pimpinan Prodi beserta jajarannya, dosen pembimbing, teristimewa kepada dewan penguji dan segenap bapak/ibu dosen dan staf yang telah mengemban tugas dan Amanah ini dengan sangat baik sehimgga mengantarkan anak kita meraih sukses pada hari ini.", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    pos_y -= 15

    wrapped_text = textwrap.wrap(
        "Akhirnya semoga segala aktivitas kita semua senantiasa bernilai ibadah disisi Allahu Rabbul Alamin. Sekian, dan jika ada yg kurang mohon dimaafkan", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)
    wrapped_text = textwrap.wrap(
        "Wassalamualaikum Warahmatullahi wabarakatuh", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    pos_y -= 15

   
    panjang_nama_pejabat = A4[0] - ( p.stringWidth(data.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 300 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 300        
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, data.ttd.jabatan + ",", 'N', 'L')    
    pos_y -= dl(p, pos_x_ttd, pos_y, 70, data.ttd.pejabat.nip.first_name, 'BU', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "NIP. " + data.ttd.pejabat.nip.username, 'B', 'L')


    # Menutup halaman dan menyimpan PDF
    p.setTitle("Berita Acara Yudisium")
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Berita Acara Yudisium.pdf"'
    return response