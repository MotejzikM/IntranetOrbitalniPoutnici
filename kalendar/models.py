from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    showToTimeline = models.BooleanField(default=False)
    # seznam uživatelů, kteří jsou součástí události
    participants = models.ManyToManyField('auth.User', blank=True)

    
    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('kalendar:event_detail', args=[self.id])
    
    def is_upcoming(self):
        from django.utils import timezone
        return self.date > timezone.now()
    
    def is_past(self):
        from django.utils import timezone
        return self.date < timezone.now()
    
    def is_today(self):
        from django.utils import timezone
        return self.date.date() == timezone.now().date()
    
    def is_tomorrow(self):
        from django.utils import timezone
        return self.date.date() == (timezone.now() + timezone.timedelta(days=1)).date()

    class Meta:
        ordering = ['-date']  # Order events by date, newest first