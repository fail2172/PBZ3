from django.db import models

class Attribute(models.Model):
	attribute_name = models.CharField(max_length = 30)
	attribute_value = models.CharField(max_length = 30, default = '0')

class Individual(models.Model):
	individual_name = models.CharField(max_length = 30)
	attributes = models.ManyToManyField(Attribute)

class SubConcept1(models.Model):
	sub_concept_name = models.CharField(max_length = 30)
	individuals = models.ManyToManyField(Individual)

class SubConcept(models.Model):
	sub_concept_name = models.CharField(max_length = 30)
	individuals = models.ManyToManyField(Individual)
	sub_concepts1 = models.ManyToManyField(SubConcept1)

class Concept(models.Model):
	concept_name = models.CharField(max_length = 30)
	individuals = models.ManyToManyField(Individual)
	sub_concepts = models.ManyToManyField(SubConcept)


class Ontology(models.Model):
	ontology_name = models.CharField(max_length = 30, default = 'test_ontology')
	comment = models.CharField(max_length = 1200, default = '')
	concepts = models.ManyToManyField(Concept)	

#	def save(self, *args, **kwargs):
#		ontology_exist = True
#		for i in Ontology.objects.all():
#			if i.ontology_name == self.ontology_name:
#				ontology_exist = False
#		if ontology_exist:
#			super().save(*args, **kwargs)



