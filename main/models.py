from django.db import models
import json
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

	options = [
	('Manga', 'Manga'),
	('Novel', 'Novel')
	]
	type = models.CharField(max_length=6,choices=options, default='Manga')
	description = models.TextField(default=None, blank=True)
	categories = models.TextField(default="All,")
	source = models.IntegerField()
	author = models.TextField(default="", blank=True)
	orientation = models.TextField(default="left-to-right")
	NumChapters = models.IntegerField(default=0)
	url = models.TextField(default="")
	leftToRead = models.IntegerField()
	updating = models.BooleanField(default=False)
	def chapters_to_arr(self):
		return json.loads(self.chapters)
		
	def __str__(self):
		return self.title

class extension(models.Model):
	name = models.TextField(default="")
	path = models.TextField(default="")
	logo = models.TextField(default="")

	def __str__(self):
		return self.name
		
"""
The below items aren't needed for now
"""
class sources(models.Model):
	name = models.TextField(default='', blank=True)

	def __str__(self):
		return self.name

class chapter(models.Model):
	name = models.TextField(default="")
	url = models.TextField(default="")
	read = models.BooleanField(default=False)
	lastRead = models.IntegerField(default=0)
	comicId = models.IntegerField()
	index = models.IntegerField()
	downloaded = models.BooleanField(default=False)

	def __str__(self):
		return self.name
	
class category(models.Model):
	name = models.TextField(default='', blank=True)
	def __str__(self):
		return self.name

class mangaCategory(models.Model):
	categoryid = models.IntegerField()
	mangaid = models.IntegerField()

class download(models.Model):
	name = models.TextField(default="")
	chapterid = models.IntegerField()
	totalPages = models.IntegerField(default=0)
	downloaded = models.IntegerField(default=0)

class setting(models.Model):
	name = models.TextField()
	state = models.BooleanField()

	def __str__(self):
		return self.name
