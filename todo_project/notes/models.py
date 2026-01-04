from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Folder(models.Model):
    COLOR_CHOICES = [
        ('#C7D2FE', 'Blue'),      # Light blue
        ('#FECACA', 'Red'),       # Light red/pink
        ('#FDE68A', 'Yellow'),    # Light yellow
        ('#BBF7D0', 'Green'),     # Light green
        ('#DDD6FE', 'Purple'),    # Light purple
        ('#FED7AA', 'Orange'),    # Light orange
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#C7D2FE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return self.name
    
    def note_count(self):
        return self.notes.count()


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-updated_at']
    
    def __str__(self):
        return self.title
    
    def get_preview(self):
        """Return first 100 characters of content"""
        return self.content[:100] + '...' if len(self.content) > 100 else self.content
