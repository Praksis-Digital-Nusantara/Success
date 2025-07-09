from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from ..decorators_mhs import check_usermhs
from ..decorators_mhs import mahasiswa_required

from aam.context_processors import web_name

from ..print_utils import tanggal_indo, draw_kop_surat, dl

from ..models import SkripsiJudul, Pejabat

import textwrap


@mahasiswa_required
@check_usermhs
def print_pengajuanjudul(request):
    context = web_name(request)  
    usermhs = request.usermhs  
    response = HttpResponse(content_type="application/pdf")    
    p = canvas.Canvas(response, pagesize=A4)
    posd_x = 50 #posisi default x untuk bagian kiri
  
    # AMBIL KOP DI UTILS
    pos_y = draw_kop_surat(p, context, usermhs)

    # JUDUL SURAT 
    p.setFont("Times-Bold", 12)
    text_x = A4[0] / 2
    pos_y -= 5
    p.drawCentredString(text_x, pos_y, "LEMBAR PENGAJUAN JUDUL PENELITIAN")


    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset
        canvas.drawString(posd_x, pos_y, label)  
        canvas.drawString(180, pos_y, ":")  
        canvas.drawString(200, pos_y, value)        
        return pos_y

    pos_y -= dl(p, posd_x, pos_y, 30, "Identitas Mahasiswa : ", 'B', 'L')
    pos_y = draw_aligned_text(p, "Nama Mahasiswa", request.user.first_name, 12)
    pos_y = draw_aligned_text(p, "NIM", request.user.username, 12)
    pos_y = draw_aligned_text(p, "Program Studi", usermhs.prodi.nama_prodi, 12)
    pos_y = draw_aligned_text(p, "Tempat/ Tgl. Lahir", usermhs.tempat_lahir + ", "+tanggal_indo(usermhs.tgl_lahir), 12)


    pos_y -= dl(p, posd_x, pos_y, 30, "Judul yang diajukan :", 'B', 'L')

    def draw_aligned_text(canvas, label, value, y_offset):
        canvas.setFont("Times-Roman", 12)
        nonlocal pos_y
        pos_y -= y_offset 
        canvas.drawString(posd_x, pos_y, label)
        wrapped_text = textwrap.wrap(value, width=100)
        for i, line in enumerate(wrapped_text):
            if i == 0:
                canvas.drawString(posd_x + 20, pos_y, line) 
            else:
                pos_y -= 15 
                canvas.drawString(posd_x + 20, pos_y, line)
        return pos_y  
    
    judul = SkripsiJudul.objects.get(mhs=usermhs)
    # print (judul)
    pos_y = draw_aligned_text(p, "1.", judul.judul1,  15)   
    pos_y = draw_aligned_text(p, "2.", judul.judul2,  15)   
    pos_y = draw_aligned_text(p, "3.", judul.judul3,  15)


    pos_y -= dl(p, posd_x, pos_y, 30, "Dosen Pembimbing yang Diusulkan :", 'B', 'L')
    pos_y = draw_aligned_text(p, "1.", "...............",  15)   
    pos_y = draw_aligned_text(p, "2.", "...............",  15)

    # TEMPAT TANDA TANGAN
    pos_y -= dl(p, A4[0] - 250, pos_y, 20, context.get("address_ttd", "") + ", ....................", 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "Disetujui Oleh", 'N', 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, "Diajukan Oleh", 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "Penasehat Akademik,", 'N', 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, "Mahasiswa Ybs,", 'N', 'L')

    if judul.status != 'Waiting':
        p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/pgj_pa/' + str(judul.id)), 60, pos_y-50, width=40, height=40)
    

    p.drawImage(ImageReader(context.get("api_qrcode", "") + context.get("baseurl", "") + 't/pgj_mhs/' + str(judul.id)), A4[0] - 240, pos_y-50, width=40, height=40)

    pos_y -= dl(p, posd_x, pos_y, 60, usermhs.penasehat_akademik.nip.first_name, 'N', 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, request.user.first_name, 'N', 'L')

    pos_y -= dl(p, posd_x, pos_y, 15, "NIP." + usermhs.penasehat_akademik.nip.username, 'N', 'L')
    pos_y -= dl(p, A4[0] - 250, pos_y, 0, "NIM." + request.user.username, 'N', 'L')

    
    # ################################### BATAS #########################
    # pos_y -= dl(p, A4[0] / 2, pos_y, 30, "PERSETUJUAN PIMPINAN PROGRAM STUDI DAN JURUSAN", 'B', 'C')
    # pos_y -= dl(p, posd_x, pos_y, 20, "Judul yang disetujui:", 'B', 'L')
    
    # pos_y -= 15
    # p.setFont("Times-Roman", 12)
    # for _ in range(4):
    #     p.drawString(posd_x, pos_y, "......................................................................................................................................................")
    #     pos_y -= 15

    # pos_y -= dl(p, posd_x, pos_y, 20, "Pembimbing yang ditunjuk:", 'B', 'L')
    # pos_y -= dl(p, posd_x, pos_y, 20, "1. .............................", 'N', 'L')
    # pos_y -= dl(p, posd_x, pos_y, 20, "2. .............................", 'N', 'L')

    # pos_y -= dl(p, posd_x, pos_y, 20, "Mengetahui,", 'N', 'L')
    # pos_y -= dl(p, A4[0] - 250, pos_y, 0, "Ketua Program Studi", 'N', 'L')

    # pos_y -= dl(p, posd_x, pos_y, 15, "Ketua Jurusan " + usermhs.prodi.jurusan.nama_jurusan, 'N', 'L')
    # pos_y -= dl(p, A4[0] - 250, pos_y, 0, usermhs.prodi.nama_prodi, 'N', 'L')

    # jurusanP = JurusanPejabat.objects.get(jurusan=usermhs.prodi.jurusan)
    # prodiP = ProdiPejabat.objects.get(prodi=usermhs.prodi)

    # pos_y -= dl(p, posd_x, pos_y, 60, jurusanP.pejabat.first_name, 'B', 'L')
    # pos_y -= dl(p, A4[0] - 250, pos_y, 0, prodiP.pejabat.first_name, 'B', 'L')

    # pos_y -= dl(p, posd_x, pos_y, 15, "NIP."+jurusanP.pejabat.username, 'B', 'L')
    # pos_y -= dl(p, A4[0] - 250, pos_y, 0, "NIP."+prodiP.pejabat.username, 'B', 'L')




    # Menutup halaman dan menyimpan PDF
    p.setTitle("Cetak Usulan Judul "+request.user.username)
    p.showPage()
    p.save()
    response["Content-Disposition"] = f'inline; filename="Cetak Usulan Judul {request.user.username}.pdf"'
    return response