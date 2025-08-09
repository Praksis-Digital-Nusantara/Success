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
from ..models import SuketAktifKuliah, Pejabat
import textwrap



def print_suket_aktifkuliah(request, id):
    context = web_name(request)

    data = SuketAktifKuliah.objects.get(id=id)

    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 65 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat_fakultas(p, context)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5

    pos_y -= dl(p, A4[0] / 2, pos_y, 15, "SURAT KETERANGAN AKTIF KULIAH", 'BU', 'C')
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
    pos_y = draw_aligned_text(p, "Jabatan ", "Kepala Bagian Umum",  15)

    pos_y -= dl(p, posd_x, pos_y, 30, "Dengan ini menerangkan dengan sesungguhnya, bahwa :", 'N', 'L')


    pos_y = draw_aligned_text(p, "Nama", data.mhs.nim.first_name,  15) 
    pos_y = draw_aligned_text(p, "Tempat/Tanggal Lahir", data.mhs.tempat_lahir + ', ' + tanggal_indo(data.mhs.tgl_lahir),  15) 
    pos_y = draw_aligned_text(p, "NIM", data.mhs.nim.username,  15) 
    pos_y = draw_aligned_text(p, "Pada Perguruan Tinggi", context.get("university_name", ""),  15) 
    pos_y = draw_aligned_text(p, "Fakultas", context.get("faculty_name", ""),  15) 
    pos_y = draw_aligned_text(p, "Program Studi", str(data.mhs.prodi),  15) 
    pos_y = draw_aligned_text(p, "Alamat", data.mhs.alamat,  15)

    pos_y -= dl(p, posd_x, pos_y, 30, "Nama Orang Tua/Wali mahasiswa tersebut adalah :", 'N', 'L')

    pos_y = draw_aligned_text(p, "Nama", data.ortu_nama,  15)
    pos_y = draw_aligned_text(p, "NIP/NRP", data.ortu_nip,  15)
    pos_y = draw_aligned_text(p, "Golongan", data.ortu_gol,  15)
    pos_y = draw_aligned_text(p, "Pekerjaan", data.ortu_pekerjaan,  15)
    pos_y = draw_aligned_text(p, "Instansi", data.ortu_instansi,  15)
    pos_y = draw_aligned_text(p, "Alamat", data.ortu_alamat,  15)



    strata_prodi = data.mhs.prodi.strata
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
        "Nama tersebut di atas, masih aktif mengikuti perkuliahan Program " + strata_prodi + " Tahun Akademik " + data.tahun_akademik, 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)

    wrapped_text = textwrap.wrap(
        "Surat keterangan ini dibuat  untuk dipergunakan sebagaimana mestinya. ", 
        width=470 
    )
    for line in wrapped_text: pos_y -= dl(p, posd_x, pos_y, 15, line, 'N', 'J', width=470)
    

    panjang_nama_pejabat = A4[0] - ( p.stringWidth(data.ttd.pejabat.nip.first_name, "Times-Bold", 12) + 60)
    if panjang_nama_pejabat < 300 :
        pos_x_ttd = panjang_nama_pejabat
    else :
        pos_x_ttd = 300

        

    pos_y -= dl(p, pos_x_ttd, pos_y, 50, context.get("address_ttd", "") + ", " + tanggal_indo(data.date_in), 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "a.n Dekan", 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "Wakil Dekan Bidang Akademik", 'N', 'L')
    pos_y -= dl(p, pos_x_ttd, pos_y, 15, "u.b Kepala bagian Umum", 'N', 'L')
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
