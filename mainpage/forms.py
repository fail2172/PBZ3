from django import forms
from .models import *

class AddConceptForm(forms.Form):
	new_concept_name = forms.CharField(max_length = 30, label='Concept')

class SaveForm(forms.Form):
	file_name = forms.CharField(max_length = 30, label='File name')

class OpenForm(forms.Form):
	file = forms.FileField( label='File name')

class CommentForm(forms.Form):
	text = forms.CharField(max_length = 1200, label='', widget=forms.Textarea())

class addConceptIndividualAttrForm(forms.Form):
	new_attribute_name = forms.CharField(max_length = 30, label='Attribute name')
	new_attribute_value = forms.CharField(max_length = 30, label='Attribute value')
	concept_for_attribute_name = forms.CharField(max_length = 30, label='класс атрибута', widget = forms.HiddenInput())
	individual_for_attribute_name = forms.CharField(max_length = 30, label='экземпляр атрибута', widget = forms.HiddenInput())

class addSubConceptIndividualAttrForm(forms.Form):
	new_attr_name = forms.CharField(max_length = 30, label='Attribute name')
	new_attr_value = forms.CharField(max_length = 30, label='Attribute value')
	subconc_for_attribute_name = forms.CharField(max_length = 30, label='подкласс атрибута', widget = forms.HiddenInput())
	conc_for_attribute_name = forms.CharField(max_length = 30, label='класс атрибута', widget = forms.HiddenInput())
	individ_for_attribute_name = forms.CharField(max_length = 30, label='экземпляр атрибута', widget = forms.HiddenInput())


class addSubSubConceptIndividualAttrForm(forms.Form):
	new_attrn = forms.CharField(max_length = 30, label='Attribute name')
	new_attrv = forms.CharField(max_length = 30, label='Attribute value')
	subcon_for_attribute_name = forms.CharField(max_length = 30, label='подкласс атрибута', widget = forms.HiddenInput())
	subsubcon_for_attribute_name = forms.CharField(max_length = 30, label='подподкласс атрибута', widget = forms.HiddenInput())
	con_for_attribute_name = forms.CharField(max_length = 30, label='класс атрибута', widget = forms.HiddenInput())
	ind_for_attribute_name = forms.CharField(max_length = 30, label='экземпляр атрибута', widget = forms.HiddenInput())

class DeleteConceptForm(forms.Form):
	del_concept_name = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())

class DeleteOntologyForm(forms.Form):
	del_ontology_name = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())

class DeleteConceptIndividualForm(forms.Form):
	del_concept_ind_name = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	del_indc_name = forms.CharField(max_length = 30, label='экземпляр', widget = forms.HiddenInput())

class DeleteSubConceptIndividualForm(forms.Form):
	del_subconcept_ind_name = forms.CharField(max_length = 30, label='подкласс', widget = forms.HiddenInput())
	del_conc_ind_name = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	del_indsc_name = forms.CharField(max_length = 30, label='экземпляр', widget = forms.HiddenInput())

class DeleteSubSubConceptIndividualForm(forms.Form):
	del_subsubcon_ind_name = forms.CharField(max_length = 30, label='подподкласс', widget = forms.HiddenInput())
	del_subcon_ind_name = forms.CharField(max_length = 30, label='подкласс', widget = forms.HiddenInput())
	del_con_ind_name = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	del_indssc_name = forms.CharField(max_length = 30, label='экземпляр', widget = forms.HiddenInput())

class DeleteSubConceptForm(forms.Form):
	concept_name_for_del_sub = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	del_subconcept_name = forms.CharField(max_length = 30, label='подкласс', widget = forms.HiddenInput())

class DeleteSubSubConceptForm(forms.Form):
	concept_name_for_del_sub_sub = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	sub_concept_name_for_del_sub_sub = forms.CharField(max_length = 30, label='подкласс', widget = forms.HiddenInput())
	del_sub_sub_concept_name = forms.CharField(max_length = 30, label='подподкласс', widget = forms.HiddenInput())


class AddIndividualOrSubForm(forms.Form):
	concept_individual_name = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	new_individual_name = forms.CharField(max_length = 30, label='Individual')
	new_sub_concept_name = forms.CharField(max_length = 30, label='SubConcept')

class AddIndividualOrSubSubForm(forms.Form):
	concept_name_for_sub = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	sub_concept_individual_name = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	new_sub_individual_name = forms.CharField(max_length = 30, label='Individual')
	new_sub_sub_concept_name = forms.CharField(max_length = 30, label='SubConcept')

class AddIndividualForSubSubForm(forms.Form):
	concept_name_for_sub_add = forms.CharField(max_length = 30, label='класс', widget = forms.HiddenInput())
	sub_concept_individual_name_add = forms.CharField(max_length = 30, label='подкласс', widget = forms.HiddenInput())
	sub_sub_concept_individual_name_add = forms.CharField(max_length = 30, label='подподкласс', widget = forms.HiddenInput())
	individual_name_for_sub_sub = forms.CharField(max_length = 30, label='Individual')


class CreateOntologyForm(forms.Form):
	new_ontology_name = forms.CharField(max_length = 30, label='')

class OntologyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.type

class ChoiseOntologyForm(forms.Form):
	def __init__(self, *args,**kwargs):
		super().__init__(*args,**kwargs)
		ontology_choices = []
		for i in Ontology.objects.all():
			ontology_choices.append((i.ontology_name, i.ontology_name))
		print(ontology_choices)
		self.fields['ontologys'] =forms.ChoiceField(choices=ontology_choices, label='')
	
	ontologys = forms.ChoiceField()

class QueryForm(forms.Form):

	def __init__(self, *args,**kwargs):
		ontology = kwargs.pop('ontology', None)
		super().__init__(*args,**kwargs)
		concept_choices = []
		attribute_choices = []
		attr_names = []
		check = False
		for i in ontology.concepts.all():
			concept_choices.append((i.concept_name, i.concept_name))
			for ind in i.individuals.all():
				for attrn in ind.attributes.all():
					for ch_atr in attribute_choices:
						n = str(ch_atr)
						n = n.replace('\'', '')
						n = n.replace('(', '')
						n = n.replace(')', '')
						n = n.split(',')[0]
						attr_names.append(n)
					if attrn.attribute_name not in attr_names:
						attribute_choices.append((attrn.attribute_name, attrn.attribute_name))

			for j in i.sub_concepts.all():
				concept_choices.append((j.sub_concept_name, j.sub_concept_name))
				for indiv in j.individuals.all():
					for attr_n in indiv.attributes.all():
						for ch_atr in attribute_choices:
							n = str(ch_atr)
							n = n.replace('\'', '')
							n = n.replace('(', '')
							n = n.replace(')', '')
							n = n.split(',')[0]
							attr_names.append(n)
						if attr_n.attribute_name not in attr_names:
							attribute_choices.append((attr_n.attribute_name, attr_n.attribute_name))
				for g in j.sub_concepts1.all():
					concept_choices.append((g.sub_concept_name, g.sub_concept_name))
					for individ in g.individuals.all():
						for attr_name in individ.attributes.all():
							for ch_atr in attribute_choices:
								n = str(ch_atr)
								n = n.replace('\'', '')
								n = n.replace('(', '')
								n = n.replace(')', '')
								n = n.split(',')[0]
								attr_names.append(n)
							if attr_name.attribute_name not in attr_names:
								attribute_choices.append((attr_name.attribute_name, attr_name.attribute_name))

		print(concept_choices) 
		self.fields['concepts'] =forms.ChoiceField(choices=concept_choices, label='Individual of concept')  
		self.fields['attributes1'] =forms.ChoiceField(choices=attribute_choices, label='Attribute 1') 
		self.fields['attributes2'] =forms.ChoiceField(choices=attribute_choices, label='Attribute 2', required=False) 
		self.fields['attributes3'] =forms.ChoiceField(choices=attribute_choices, label='Attribute 3', required=False)  
                                                      
	concepts = forms.ChoiceField()
	attributes1 = forms.ChoiceField()
	attrv1 = forms.CharField(max_length = 20, label='Attribute value 1')
	attributes2 = forms.ChoiceField()
	attrv2 = forms.CharField(max_length = 20, label='Attribute value 2', required=False)
	attributes3 = forms.ChoiceField()
	attrv3 = forms.CharField(max_length = 20, label='Attribute value 3', required=False)