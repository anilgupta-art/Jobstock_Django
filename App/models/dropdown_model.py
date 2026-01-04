from django.db import models

class DropdownGroup(models.Model):
    text = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text
    class Meta:
        db_table = 'dropdown_group'
        verbose_name = 'Dropdown Group'
        verbose_name_plural = 'Dropdown Groups'

class DropdownMaster(models.Model):
    group = models.ForeignKey(DropdownGroup, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.group.text} - {self.text}"
    class Meta:
        db_table = 'dropdown_master'
        verbose_name = 'Dropdown Master'
        verbose_name_plural = 'Dropdown Masters'
        ordering = ['group', 'sort_order', 'text']
