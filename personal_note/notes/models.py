from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    shared_with = models.ManyToManyField(User, related_name='shared_topics', blank=True)
    #invite_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class NoteItem(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='note_items')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='note_images/', blank=True, null=True)
    deleted = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_notes')
    def __str__(self):
        return self.title or "（無標題）"
    '''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='note_items')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='note_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0)  # 用來排序
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    title = models.TextField(blank=True)
    
    def __str__(self):
        return self.content[:20] or "圖片"
    


    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='note_items')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='note_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField(blank=True)
    deleted = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='note_photos/', blank=True, null=True)

    def __str__(self):
        return f"NoteItem for {self.topic.name}"
    '''
