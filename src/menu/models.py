from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='items', verbose_name='Parent Item')
    ordering = models.PositiveIntegerField(default=0)
    url = models.CharField(max_length=255, default='', verbose_name='URL')
    use_named_url = models.BooleanField(default=False)

    class Meta:
        ordering = ['ordering', 'name']

    def __str__(self):
        return f'{self.name} ({self.menu.name})'

