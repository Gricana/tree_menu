from django.db import models
from django.shortcuts import reverse, NoReverseMatch


class Menu(models.Model):
    """
    A model representing a menu.
    """

    name = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    A model representing a menu item.
    """

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200, blank=True, null=True)
    named_url = models.SlugField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def get_absolute_url(self):
        """
        Returns the absolute URL of the menu item.
        """
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                pass
        return self.url or "#"

    def __str__(self):
        return f"{self.menu} - {self.title}"

    class Meta:
        ordering = ('menu',)
