from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Prodi, ProdiPejabat

from .forms_fakultas import formProfile, formProdiEdit, formProdiPejabatEdit

from .decorators_fakultas import check_userfakultas
from .decorators_fakultas import fakultas_required



@fakultas_required
@check_userfakultas
def profile_fakultas(request):
    userfakultas = request.userfakultas    
    if request.method == 'POST':
        form = formProfile(request.POST, request.FILES, instance=userfakultas)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/acd/profile_fakultas')
    else:
        form = formProfile(instance=userfakultas)

    context = {
        'title' : 'Edit Profile',
        'heading' : 'Edit Profile',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'form': form,
    }
    return render(request, 'fakultas/set/profile.html', context)


########### SET PRODI #####################################################

@fakultas_required
@check_userfakultas
def prodi_list(request):           
    userfakultas = request.userfakultas
    prodi_list = Prodi.objects.all()
    context = {
        'title': 'Set Prodi',
        'heading': 'Program Studi',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'prodi_list' : prodi_list,
    }
    return render(request, 'fakultas/set/prodi_list.html', context)


@fakultas_required
@check_userfakultas
def prodi_edit(request, id):           
    userfakultas = request.userfakultas
    if id == 0:
        prodi = None
    else:
        prodi = get_object_or_404(Prodi, id=id)

    if request.method == 'POST':
        if 'delete' in request.POST:  # Jika tombol delete ditekan
            if prodi:
                prodi.delete()
                messages.success(request, 'Prodi berhasil dihapus.')
                return redirect('/acd/prodi_list') 
            else:
                messages.error(request, 'Prodi tidak ditemukan.')
        else:
            form = formProdiEdit(request.POST, instance=prodi)
            if form.is_valid():
                prodi = form.save(commit=False) 
                prodi.save()
                messages.success(request, 'Prodi berhasil disimpan.')
                return redirect(f'/acd/prodi_edit/{prodi.id}')
            else:
                messages.error(request, 'Periksa kembali isian form.') 
    else:
        form = formProdiEdit(instance=prodi)

    context = {
        'title': 'Set Program Studi',
        'heading': 'Set Program Studi',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'form': form,
        'prodi': prodi 
    }
    return render(request, 'fakultas/set/prodi_edit.html', context)




@fakultas_required
@check_userfakultas
def prodi_pejabat_list(request):           
    userfakultas = request.userfakultas
    prodi_list = ProdiPejabat.objects.all()
    context = {
        'title': 'Set Pejabat Prodi',
        'heading': 'Pejabat Program Studi',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'prodi_list' : prodi_list,
    }
    return render(request, 'fakultas/set/prodi_pejabat_list.html', context)


@fakultas_required
@check_userfakultas
def prodi_pejabat_edit(request, id):           
    userfakultas = request.userfakultas
    if id == 0:
        pejabat = None
    else:
        pejabat = get_object_or_404(ProdiPejabat, id=id)

    if request.method == 'POST':
        if 'delete' in request.POST:  # Jika tombol delete ditekan
            if pejabat:
                pejabat.delete()
                messages.success(request, 'Pejabat berhasil dihapus.')
                return redirect('/acd/prodi_pejabat_list') 
            else:
                messages.error(request, 'Pejabat tidak ditemukan.')
        else:
            form = formProdiPejabatEdit(request.POST, instance=pejabat)
            if form.is_valid():
                pejabat = form.save(commit=False) 
                pejabat.save()
                messages.success(request, 'Pejabat berhasil disimpan.')
                return redirect(f'/acd/prodi_pejabat_edit/{pejabat.id}')
            else:
                messages.error(request, 'Periksa kembali isian form.') 
    else:
        form = formProdiPejabatEdit(instance=pejabat)

    context = {
        'title': 'Set Pejabat Prodi',
        'heading': 'Kelolah Pejabat',
        'userfakultas' : userfakultas,
        'photo' : userfakultas.photo,
        'form': form,
    }
    return render(request, 'fakultas/set/prodi_pejabat_edit.html', context)