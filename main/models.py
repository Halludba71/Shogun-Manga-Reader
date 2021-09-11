from django.db import models

# Create your models here.

"""
manga cover needs to be downloaded,
should be downloaded to a manga directory and given a unique identifier

i have chosen the identifier to be a md5 hash so that there are no two identical identifiers

the identifier is then assigned like so manga [ cover: identieer]
"""

class manga(models.Model):
	title = models.TextField(default='', blank=True)
	cover = models.TextField(default='', blank=True)

	def __str__(self):
		return self.title