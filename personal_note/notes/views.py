from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Topic, NoteItem, User
from .forms import TopicForm,NoteItemForm, ShareTopicForm
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site



# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            form = CustomUserCreationForm()
            return redirect('topic_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('topic_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def topic_list(request):
    # 目前先傳空列表，之後可加上 notes 主題
    return render(request, 'notes/topic_list.html', {'topics': []})

@login_required
def topic_list(request):
    query = request.GET.get('q', '')  # 取得搜尋關鍵字
    topics = Topic.objects.filter(owner=request.user, deleted=False)

    if query:
        topics = topics.filter(Q(name__icontains=query) | Q(content__icontains=query))

    topic_forms = {}
    for topic in topics:
        topic_forms[topic.id] = NoteItemForm()

    context = {
        'topics': topics,
        'topic_form': TopicForm(),
        'note_forms': topic_forms,
        'query': query,
        'not_found': query and not topics.exists(),  # 若查詢有值且找不到資料
    }
    return render(request, 'notes/topic_list.html', context)
    '''
    query = request.GET.get('q')
    if query:
        topics = Topic.objects.filter(Q(name__icontains=query), deleted=False, owner=request.user)
    else:
        topics = Topic.objects.filter(deleted=False, owner=request.user)

    return render(request, 'notes/topic_list.html', {'topics': topics})    
'''
'''
    topics = Topic.objects.filter(deleted=False).prefetch_related('note_items')
    topic_forms = []

    for topic in topics:
        form = NoteItemForm()
        topic_forms.append((topic, form))

    context = {
        'topic_forms': topic_forms,
    }
    return render(request, 'notes/topic_list.html', context)
'''
'''
    query = request.GET.get('q')
    if query:
        topics = Topic.objects.filter(
            Q(name__icontains=query),
            deleted=False,
            owner=request.user
        )
    else:
        topics = Topic.objects.filter(deleted=False, owner=request.user)

    topic_forms = {topic.id: NoteItemForm() for topic in topics}
    topic_form = TopicForm()

    return render(request,  'notes/topic_list.html', context, 'topic_list.html', {
        'topics': topics,
        'topic_forms': topic_forms,
        'topic_form': topic_form,
        'query': query,
    })
    '''

@login_required
def topic_create(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.owner = request.user
            topic.save()
            return redirect('topic_list')
    else:
        form = TopicForm()
    return render(request, 'notes/topic_form.html', {'form': form})

@login_required
def topic_delete(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    if request.method == 'POST':
        topic.deleted = True
        topic.save()
        return redirect('topic_list')
    return render(request, 'notes/topic_confirm_delete.html', {'topic': topic})

@login_required
def topic_trash(request):
    trashed_topics = Topic.objects.filter(owner=request.user, deleted=True)
    return render(request, 'notes/topic_trash.html', {'topics': trashed_topics})

@login_required
def topic_restore(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user, deleted=True)
    topic.deleted = False
    topic.save()
    return redirect('topic_trash')

@login_required
def topic_edit(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user, deleted=False)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('topic_list')
    else:
        form = TopicForm(instance=topic)
    return render(request, 'notes/topic_form.html', {'form': form})

def trash_list(request):
    topics = Topic.objects.filter(owner=request.user, deleted=True).order_by('-deleted_at')
    return render(request, 'notes/trash_list.html', {'topics': topics})

def restore_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk, owner=request.user, deleted=True)
    topic.deleted = False
    topic.deleted_at = None
    topic.save()
    return redirect('notes:trash_list')

def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk, owner=request.user)
    topic.deleted = True
    topic.deleted_at = timezone.now() 
    topic.save()
    return redirect('notes:trash_list')  

def edit_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk, owner=request.user, deleted=False)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('notes:topic_list')
    else:
        form = TopicForm(instance=topic)

    return render(request, 'notes/topic_form.html', {'form': form, 'edit_mode': True})
'''
@login_required
def edit_note(request, pk):
    note = get_object_or_404(NoteItem, pk=pk, topic__owner=request.user)
    if request.method == 'POST':
        form = NoteItemForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('topic_detail', topic_id=note.topic.id)
    else:
        form = NoteItemForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(NoteItem, pk=pk, topic__owner=request.user)
    topic_id = note.topic.id
    note.delete()
    return redirect('topic_detail', topic_id=topic_id)
'''
@login_required
def create_note_item(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    if request.method == 'POST':
        form = NoteItemForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.topic = topic
            note.save()
    return redirect('topic_list')

@login_required
def edit_note_item(request, note_id):
    note = get_object_or_404(NoteItem, id=note_id)

    # 檢查是否為擁有者或共編者
    if request.user != note.topic.owner and request.user not in note.topic.shared_with.all():
        return redirect('topic_list')

    if request.method == 'POST':
        form = NoteItemForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.last_edited_by = request.user
            note.save()
            return redirect('topic_detail', topic_id=note.topic.id)
    else:
        form = NoteItemForm(instance=note)

    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})
    '''
    note = get_object_or_404(NoteItem, id=note_id, topic__owner=request.user)
    if request.user != note.topic.owner and request.user not in note.topic.shared_with.all():
        return HttpResponseForbidden("您沒有權限編輯此筆記。")


    if request.user != note.topic.owner and request.user not in note.topic.shared_with.all():
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = NoteItemForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.updated_by = request.user
            note.last_edited_by = request.user 
            note.save()            
            return redirect('topic_detail', topic_id=note.topic.id)
    else:
        form = NoteItemForm(instance=note)

    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})
'''
    '''
    note = get_object_or_404(NoteItem, id=note_id, topic__owner=request.user)
    if request.method == 'POST':
        form = NoteItemForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('topic_list')
    else:
        form = NoteItemForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})
    
    note = get_object_or_404(NoteItem, id=note_id, topic__owner=request.user)
    if request.method == 'POST':
        form = NoteItemForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('topic_list')
    else:
        form = NoteItemForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})
    '''
'''
@login_required
def delete_note_item(request, item_id):
    note = get_object_or_404(NoteItem, id=item_id, topic__owner=request.user)
    note.deleted = True
    note.deleted_at = timezone.now()
    note.save()
    return redirect('topic_list')
'''
def delete_note_item(request, topic_id, note_item_id):
    note_item = get_object_or_404(NoteItem, id=note_item_id, topic__id=topic_id)
    note_item.delete()
    return redirect('topic_detail', topic_id=topic_id)

@login_required(login_url='login')
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    #note_items = topic.note_items.all().order_by('created_at')  # 取得該主題下的所有筆記
    note_items = topic.note_items.all() 
    form = NoteItemForm()

    if topic.owner != request.user and request.user not in topic.shared_with.all():
        return HttpResponseForbidden("您沒有權限檢視這個主題。")

    if request.method == 'POST':
        form = NoteItemForm(request.POST, request.FILES)
        if form.is_valid():
            note_item = form.save(commit=False)
            note_item.topic = topic
            #note.last_edited_by = request.user
            note_item.save()
            return redirect('topic_detail', topic_id=topic.id)

    return render(request, 'notes/topic_detail.html', {
        'topic': topic,
        'note_items': note_items,
        'form': form
    })
'''
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user, deleted=False)
    note_items = topic.noteitem_set.all().order_by('-id')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        photo = request.FILES.get('photo')

        NoteItem.objects.create(topic=topic, title=title, content=content, photo=photo)
        return redirect('topic_detail', topic_id=topic.id)

    return render(request, 'notes/topic_detail.html', {
        'topic': topic,
        'note_items': note_items,
    })'''
@login_required
@login_required
def share_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    
    if request.method == 'POST':
        form = ShareTopicForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user_to_share = User.objects.get(email=email)
                topic.shared_with.add(user_to_share)

                # 組成連結
                current_site = get_current_site(request)
                topic_url = reverse('topic_detail', args=[topic.id])
                full_url = f"http://{current_site.domain}{topic_url}"

                # 寄送 email
                subject = f"{request.user.username} 分享了一個主題給你"
                message = f"你可以點擊以下連結查看並編輯主題：\n\n{full_url}"
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

                messages.success(request, f'已成功分享給 {email}')
            except User.DoesNotExist:
                messages.error(request, f"無法分享，找不到 {email} 的使用者帳號")
            
            return redirect('topic_detail', topic_id=topic.id)
    else:
        form = ShareTopicForm()

    return render(request, 'notes/share_topic.html', {'form': form, 'topic': topic})
'''
@login_required
def share_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    if request.method == 'POST':
        form = ShareTopicForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user_to_share = User.objects.get(email=email)
                topic.shared_with.add(user_to_share)

                # 寄送 email 通知
                send_mail(
                    subject=f"{request.user.username} 分享了主題：{topic.name}",
                    message=f"你已被加入為可以共同編輯主題『{topic.name}』的使用者。",
                    from_email='noreply@example.com',
                    recipient_list=[email],
                )
                return redirect('topic_detail', topic_id=topic.id)
            except User.DoesNotExist:
                form.add_error('email', '此使用者尚未註冊')
    else:
        form = ShareTopicForm()
    return render(request, 'notes/share_topic.html', {'form': form, 'topic': topic})
'''
'''
@login_required
def accept_invite(request, token):
    email = request.GET.get('email')
    topic = get_object_or_404(Topic, invite_token=token)
    if request.user.email == email:
        topic.shared_with.add(request.user)
        messages.success(request, f'你已加入主題：{topic.name}')
    else:
        messages.error(request, '此邀請連結無效或與你的帳號不符。')
    return redirect('topic_list')'''