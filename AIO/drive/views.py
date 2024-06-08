import os
import shutil
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Folder

@login_required
def index(request):
    base_path = os.path.join(settings.MEDIA_ROOT, 'files', request.user.username)
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
    return render(request, 'drive/index.html', {'folders': folders, 'files': files})

@login_required
def view_folder(request, folder_name):
    base_path = os.path.join(settings.MEDIA_ROOT, 'files', request.user.username, folder_name)
    if not os.path.exists(base_path):
        raise Http404("Folder does not exist")
    subfolders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
    return render(request, 'drive/folder.html', {'folder_name': folder_name, 'subfolders': subfolders, 'files': files})
    
@login_required
def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        upload_path = os.path.join(settings.MEDIA_ROOT, 'files', request.user.username, request.POST.get('path', ''))
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        file_path = os.path.join(upload_path, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    return redirect('index')  # Redirect to index if accessed via GET

@login_required
def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('name')
        parent_folder = request.POST.get('path', '')
        base_path = os.path.join(settings.MEDIA_ROOT, 'files', request.user.username, parent_folder)
        new_folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    return redirect('index')  # Redirect to index if accessed via GET

@csrf_exempt
def delete_folder(request, folder_name):
    if request.method == 'POST':
        # folder_name should include the username part, like 'files/rocke/12123'
        folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)
        try:
            # Debugging statements
            print(f"Received request to delete folder: {folder_name}")
            print(f"Resolved folder path: {folder_path}")
            
            if os.path.exists(folder_path):
                print(f"Folder exists: {folder_path}")
                shutil.rmtree(folder_path)
                print(f"Folder deleted: {folder_path}")
                return JsonResponse({'success': True})
            else:
                print(f"Folder does not exist: {folder_path}")
                return JsonResponse({'success': False, 'error': 'Folder does not exist'}, status=400)
        except Exception as e:
            print(f"Error deleting folder: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        print(f"Invalid request method: {request.method}")
    return JsonResponse({'success': False}, status=400)


@login_required
def download_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'files', request.user.username, file_name)
    if not os.path.exists(file_path):
        raise Http404("File does not exist")
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

@login_required
def delete_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'files', request.user.username, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    return JsonResponse({'success': True})
