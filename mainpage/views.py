from django.shortcuts import render
from .models import *
from .forms import *

history_of_work_ontology = []

def create_and_change(request, context):
	if request.method == 'POST':
		choice_ontology_form = ChoiseOntologyForm(request.POST)
		context['choice_ontology_form'] = choice_ontology_form
		if choice_ontology_form.is_valid():
			work_ontology_name = choice_ontology_form.cleaned_data['ontologys']
			work_ontology = ''
			for i in Ontology.objects.all():
				if work_ontology_name == i.ontology_name:
					work_ontology = i
			if len(history_of_work_ontology) == 0:	
				if work_ontology != '':	
					history_of_work_ontology.append(work_ontology)
			elif len(history_of_work_ontology) > 0:
				if work_ontology != '' and work_ontology != history_of_work_ontology[-1]:
					history_of_work_ontology.append(work_ontology)
		if len(history_of_work_ontology) > 0:
			context['work_ontology'] = history_of_work_ontology[-1]
			print(history_of_work_ontology)
	else:
		choice_ontology_form = ChoiseOntologyForm(request.POST)
		context['choice_ontology_form'] = choice_ontology_form


	if request.method == 'POST':
		create_ontology_form = CreateOntologyForm(request.POST)
		context['create_ontology_form'] = create_ontology_form
		check = True
		if create_ontology_form.is_valid():
			new_ontology_name = create_ontology_form.cleaned_data.get('new_ontology_name')
			if new_ontology_name != '':
				for i in Ontology.objects.all():
					if new_ontology_name == i.ontology_name:
						check = False
				if check:
					new_ontolgy = Ontology(ontology_name = new_ontology_name)
					new_ontolgy.save()
					history_of_work_ontology.append(new_ontolgy)
					context['work_ontology'] = history_of_work_ontology[-1]
					choice_ontology_form = ChoiseOntologyForm(request.POST)
					context['choice_ontology_form'] = choice_ontology_form
					if choice_ontology_form.is_valid():
						pass
	else:
		create_ontology_form = CreateOntologyForm(request.POST)
		context['create_ontology_form'] = create_ontology_form

def index(request):

	context ={
	}
	context['checked'] = 1
	if len(history_of_work_ontology) > 0:
		context['work_ontology'] = history_of_work_ontology[-1]
	create_and_change(request, context)

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			comment_form = CommentForm(request.POST)
			context['comment_form'] = comment_form
			if comment_form.is_valid():
				text = comment_form.cleaned_data['text']
				if text != '':
					history_of_work_ontology[-1].comment = text
					history_of_work_ontology[-1].save()
	else:
		comment_form = CommentForm(request.POST)
		context['comment_form'] = comment_form


	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			add_concept_check = True
			add_concept_form = AddConceptForm(request.POST)
			context['add_concept_form'] = add_concept_form
			if add_concept_form.is_valid():
				new_concept_name = add_concept_form.cleaned_data.get('new_concept_name')
				#globals()['concept_%s' % new_concept_name] = Concept(concept_name = new_concept_name)
				for i in history_of_work_ontology[-1].concepts.all():
					if new_concept_name == i.concept_name:
						add_concept_check = False
				if new_concept_name != '' and add_concept_check:
					con = Concept(concept_name = new_concept_name)
					con.save()
					history_of_work_ontology[-1].concepts.add(con)
					history_of_work_ontology[-1].save()
	else:
		add_concept_form = AddConceptForm(request.POST)
		context['add_concept_form'] = add_concept_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			delete_concept_form = DeleteConceptForm(request.POST)
			context['delete_concept_form'] = delete_concept_form
			if delete_concept_form.is_valid():
				del_concept_name = delete_concept_form.cleaned_data.get('del_concept_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if del_concept_name == i.concept_name:
						i.delete()
	else:
		delete_concept_form = DeleteConceptForm(request.POST)
		context['delete_concept_form'] = delete_concept_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			delete_concept_individual_form = DeleteConceptIndividualForm(request.POST)
			context['delete_concept_individual_form'] = delete_concept_individual_form
			if delete_concept_individual_form.is_valid():
				del_concept_ind_name = delete_concept_individual_form.cleaned_data.get('del_concept_ind_name')
				del_indc_name = delete_concept_individual_form.cleaned_data.get('del_indc_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if del_concept_ind_name == i.concept_name:
						dci = i
						for j in dci.individuals.all():
							if del_indc_name == j.individual_name:
								j.delete()
	else:
		delete_concept_individual_form = DeleteConceptIndividualForm(request.POST)
		context['delete_concept_individual_form'] = delete_concept_individual_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			delete_sub_concept_individual_form = DeleteSubConceptIndividualForm(request.POST)
			context['delete_sub_concept_individual_form'] = delete_sub_concept_individual_form
			if delete_sub_concept_individual_form.is_valid():
				del_subconcept_ind_name = delete_sub_concept_individual_form.cleaned_data.get('del_subconcept_ind_name')
				del_conc_ind_name = delete_sub_concept_individual_form.cleaned_data.get('del_conc_ind_name')
				del_indsc_name = delete_sub_concept_individual_form.cleaned_data.get('del_indsc_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if del_conc_ind_name == i.concept_name:
						dci = i
						for j in dci.sub_concepts.all():
							if del_subconcept_ind_name == j.sub_concept_name:
								dsci = j
								for k in dsci.individuals.all():
									if del_indsc_name == k.individual_name:
										k.delete()
	else:
		delete_sub_concept_individual_form = DeleteSubConceptIndividualForm(request.POST)
		context['delete_sub_concept_individual_form'] = delete_sub_concept_individual_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			delete_sub_sub_concept_individual_form = DeleteSubSubConceptIndividualForm(request.POST)
			context['delete_sub_sub_concept_individual_form'] = delete_sub_sub_concept_individual_form
			if delete_sub_sub_concept_individual_form.is_valid():
				del_subsubcon_ind_name = delete_sub_sub_concept_individual_form.cleaned_data.get('del_subsubcon_ind_name')
				del_subcon_ind_name = delete_sub_sub_concept_individual_form.cleaned_data.get('del_subcon_ind_name')
				del_con_ind_name = delete_sub_sub_concept_individual_form.cleaned_data.get('del_con_ind_name')
				del_indssc_name = delete_sub_sub_concept_individual_form.cleaned_data.get('del_indssc_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if del_con_ind_name == i.concept_name:
						dci = i
						for j in dci.sub_concepts.all():
							if del_subcon_ind_name == j.sub_concept_name:
								dsci = j
								for k in dsci.sub_concepts1.all():
									if del_subsubcon_ind_name == k.sub_concept_name:
										dssci = k
										for l in dssci.individuals.all():
											if del_indssc_name == l.individual_name:
												l.delete()
	else:
		delete_sub_sub_concept_individual_form = DeleteSubSubConceptIndividualForm(request.POST)
		context['delete_sub_sub_concept_individual_form'] = delete_sub_sub_concept_individual_form		

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			delete_ontology_form = DeleteOntologyForm(request.POST)
			context['delete_ontology_form'] = delete_ontology_form
			if delete_ontology_form.is_valid():
				del_ontology_name = delete_ontology_form.cleaned_data.get('del_ontology_name')
				for i in Ontology.objects.all():
					if del_ontology_name == i.ontology_name:
						i.delete()
	else:
		delete_ontology_form = DeleteOntologyForm(request.POST)
		context['delete_ontology_form'] = delete_ontology_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			delete_subconcept_form = DeleteSubConceptForm(request.POST)
			context['delete_subconcept_form'] = delete_subconcept_form
			if delete_subconcept_form.is_valid():
				del_subconcept_name = delete_subconcept_form.cleaned_data.get('del_subconcept_name')
				concept_name_for_del_sub = delete_subconcept_form.cleaned_data.get('concept_name_for_del_sub')
				for i in history_of_work_ontology[-1].concepts.all():
					if concept_name_for_del_sub == i.concept_name:
						concept_for_del_sub = i
						for j in concept_for_del_sub.sub_concepts.all():
							if del_subconcept_name == j.sub_concept_name:
								j.delete()
	else:
		delete_subconcept_form = DeleteSubConceptForm(request.POST)
		context['delete_subconcept_form'] = delete_subconcept_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			delete_sub_subconcept_form = DeleteSubSubConceptForm(request.POST)
			context['delete_sub_subconcept_form'] = delete_sub_subconcept_form
			if delete_sub_subconcept_form.is_valid():
				concept_name_for_del_sub_sub = delete_sub_subconcept_form.cleaned_data.get('concept_name_for_del_sub_sub')
				sub_concept_name_for_del_sub_sub = delete_sub_subconcept_form.cleaned_data.get('sub_concept_name_for_del_sub_sub')
				del_sub_sub_concept_name = delete_sub_subconcept_form.cleaned_data.get('del_sub_sub_concept_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if concept_name_for_del_sub_sub == i.concept_name:
						concept_for_del_sub_sub = i
						for j in concept_for_del_sub_sub.sub_concepts.all():
							if sub_concept_name_for_del_sub_sub == j.sub_concept_name:
								sub_concept_for_del_sub_sub = j
								for k in sub_concept_for_del_sub_sub.sub_concepts1.all():
									if del_sub_sub_concept_name == k.sub_concept_name:
										k.delete()
	else:
		delete_sub_subconcept_form = DeleteSubSubConceptForm(request.POST)
		context['delete_sub_subconcept_form'] = delete_sub_subconcept_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			save_form = SaveForm(request.POST)
			context['save_form'] = save_form
			if save_form.is_valid():
				file_name = save_form.cleaned_data.get('file_name')
				if file_name != '':
					f1 = open(file_name + ".rdf", 'w')					
					f1.write('Онтология :' + history_of_work_ontology[-1].ontology_name + '\n')
					f1.write('Комментарий :' + history_of_work_ontology[-1].comment + '\n')
					for concept in history_of_work_ontology[-1].concepts.all():
						f1.write('--Класс :' + concept.concept_name + '\n')
						if len(concept.individuals.all()):
							for individual in concept.individuals.all():
								f1.write('----Экземпляр класса :' + concept.concept_name + ' : ' + individual.individual_name + '\n')
								if len(individual.attributes.all()) > 0:
									for atr in individual.attributes.all():
										f1.write('------Аттрибут экземпляра (класса) :' + concept.concept_name + ' : ' + individual.individual_name + ' : ' + atr.attribute_name + ' : ' + atr.attribute_value + '\n')
								#f1.write('\n')
						if len(concept.sub_concepts.all()) > 0:
							for sub_concept in concept.sub_concepts.all():
								f1.write('----Подкласс класса :' + concept.concept_name +   ' : ' + sub_concept.sub_concept_name + '\n')
								if len(sub_concept.individuals.all()) > 0:
									for individual in sub_concept.individuals.all():
										f1.write('------Экземпляр подкласса :' + concept.concept_name + ' : ' + sub_concept.sub_concept_name + ' : ' + individual.individual_name + '\n')
										if len(individual.attributes.all()) > 0:
											for atr in individual.attributes.all():
												f1.write('--------Аттрибут экземпляра (подкласса) :' + concept.concept_name + ' : ' +  sub_concept.sub_concept_name  + ' : ' + individual.individual_name  + ' : ' + atr.attribute_name + ' : ' + atr.attribute_value + '\n')
										#f1.write('\n')
								if len(sub_concept.sub_concepts1.all()) > 0:
									for sub_concept1 in sub_concept.sub_concepts1.all():
										f1.write('------Подподкласс подкласса :'+ concept.concept_name + ' : ' + sub_concept.sub_concept_name +  ' : ' + sub_concept1.sub_concept_name + '\n')
										if len(sub_concept1.individuals.all()) > 0:
											for individual in sub_concept1.individuals.all():
												f1.write('--------Экземпляр подподкласса :' + concept.concept_name + ' : ' + sub_concept.sub_concept_name + ' : ' + sub_concept1.sub_concept_name + ' : ' + individual.individual_name + '\n')
												if len(individual.attributes.all()) > 0:
													for atr in individual.attributes.all():
														f1.write('----------Аттрибут экземпляра (подподкласса) :' + concept.concept_name + ' : ' + sub_concept.sub_concept_name + ' : ' + sub_concept1.sub_concept_name + ' : ' + individual.individual_name +  ' : ' + atr.attribute_name + ' : ' + atr.attribute_value + '\n')
												#f1.write('\n')
	else:
		save_form = SaveForm(request.POST)
		context['save_form'] = save_form

	if request.method == 'POST':
		open_form = OpenForm(request.POST, request.FILES)
		context['open_form'] = open_form
		if open_form.is_valid():
			if request.FILES.get("file") != None:
				f = open(str(request.FILES.get("file")), 'r')
				fr = f.readlines()
				exist_ontology_check = True
				create_ontology_check = True
				comment_file = ''
				for fstr in fr:

					if fstr.startswith('Онтология'):
						ontology_name_file = fstr.replace('Онтология :', '')
						ontology_name_file = ontology_name_file.replace('\n', '')
						for i in Ontology.objects.all():
							if ontology_name_file == i.ontology_name:
								history_of_work_ontology.append(i)
								context['work_ontology'] = history_of_work_ontology[-1]
								exist_ontology_check = False

					if exist_ontology_check:
						if create_ontology_check:
							ont = Ontology(ontology_name = ontology_name_file)
							ont.save()
							create_ontology_check = False

						if fstr.startswith('Комментарий'):
							comment_file = fstr.replace('Комментарий :', '')
							comment_file = comment_file.replace('\n', '')
							ont.comment = comment_file
							ont.save()

					
						if fstr.startswith('--Класс'):
							concept_name_file = fstr.replace('--Класс :', '')
							concept_name_file = concept_name_file.replace('\n', '')
							con = Concept(concept_name = concept_name_file)
							con.save()
							ont.concepts.add(con)
							ont.save()

						if fstr.startswith('----Экземпляр класса :'):
							individual_name_file = fstr.replace('----Экземпляр класса :', '')
							individual_name_file = individual_name_file.replace('\n', '')
							con = individual_name_file.split(':')[0]
							con = con.replace(' ','')
							ind = individual_name_file.split(':')[1]
							ind = ind.replace(' ','')
							for i in ont.concepts.all():
								if con == i.concept_name:
									indiv = Individual(individual_name = ind)
									indiv.save()
									i.individuals.add(indiv)
									i.save()

						if fstr.startswith('------Аттрибут экземпляра (класса) :'):
							atr_name_file = fstr.replace('------Аттрибут экземпляра (класса) :', '')
							atr_name_file = atr_name_file.replace('\n', '')
							con = atr_name_file.split(':')[0]
							con = con.replace(' ','')
							ind = atr_name_file.split(':')[1]
							ind = ind.replace(' ','')
							atrn = atr_name_file.split(':')[2]
							atrn = atrn.replace(' ','')
							atrv = atr_name_file.split(':')[3]
							atrv = atrv.replace(' ','')
							for i in ont.concepts.all():
								if con == i.concept_name:
									cont = i
									for j in cont.individuals.all():
										if ind == j.individual_name:
											attr = Attribute(attribute_name = atrn, attribute_value = atrv)
											attr.save()
											j.attributes.add(attr)
											j.save()

						if fstr.startswith('----Подкласс класса :'):
							subcon_file = fstr.replace('----Подкласс класса :', '')
							subcon_file = subcon_file.replace('\n', '')
							con = subcon_file.split(':')[0]
							con = con.replace(' ','')
							subcon = subcon_file.split(':')[1]
							subcon = subcon.replace(' ','')
							for i in ont.concepts.all():
								if con == i.concept_name:
									subcont = SubConcept(sub_concept_name = subcon)
									subcont.save()
									i.sub_concepts.add(subcont)
									i.save()

						if fstr.startswith('------Экземпляр подкласса :'):
							ind_subcon_file = fstr.replace('------Экземпляр подкласса :', '')
							ind_subcon_file = ind_subcon_file.replace('\n', '')
							con = ind_subcon_file.split(':')[0]
							con = con.replace(' ','')
							subcon = ind_subcon_file.split(':')[1]
							subcon = subcon.replace(' ','')
							ind = ind_subcon_file.split(':')[2]
							ind = ind.replace(' ','')
							for i in ont.concepts.all():
								if con == i.concept_name:
									cont = i
									for j in cont.sub_concepts.all():
										if subcon == j.sub_concept_name:
											indiv = Individual(individual_name = ind)
											indiv.save()
											j.individuals.add(indiv)
											j.save()


						if fstr.startswith('--------Аттрибут экземпляра (подкласса) :'):
							atr_ind_subcon_file = fstr.replace('--------Аттрибут экземпляра (подкласса) :', '')
							atr_ind_subcon_file = atr_ind_subcon_file.replace('\n', '')
							con = atr_ind_subcon_file.split(':')[0]
							con = con.replace(' ','')
							subcon = atr_ind_subcon_file.split(':')[1]
							subcon = subcon.replace(' ','')
							ind = atr_ind_subcon_file.split(':')[2]
							ind = ind.replace(' ','')
							atrn = atr_ind_subcon_file.split(':')[3]
							atrn = atrn.replace(' ','')
							atrv = atr_ind_subcon_file.split(':')[4]
							atrv = atrv.replace(' ','')
							for i in ont.concepts.all():
								if con == i.concept_name:
									cont = i
									for j in cont.sub_concepts.all():
										if subcon == j.sub_concept_name:
											subcont = j
											for k in subcont.individuals.all():
												if ind == k.individual_name:
													attr = Attribute(attribute_name = atrn, attribute_value = atrv)
													attr.save()
													k.attributes.add(attr)
													k.save()


						if fstr.startswith('------Подподкласс подкласса :'):
							subsubcon_file = fstr.replace('------Подподкласс подкласса :', '')
							subsubcon_file = subsubcon_file.replace('\n', '')
							con = subsubcon_file.split(':')[0]
							con = con.replace(' ','')
							subcon = subsubcon_file.split(':')[1]
							subcon = subcon.replace(' ','')
							subsubcon = subsubcon_file.split(':')[2]
							subsubcon = subsubcon.replace(' ','')
							for i in ont.concepts.all():
								if con == i.concept_name:
									cont = i
									for j in cont.sub_concepts.all():
										if subcon == j.sub_concept_name:
											subcont1 = SubConcept1(sub_concept_name = subsubcon)
											subcont1.save()
											j.sub_concepts1.add(subcont1)
											j.save()


						if fstr.startswith('--------Экземпляр подподкласса :'):
							ind_subsubcon_file = fstr.replace('--------Экземпляр подподкласса :', '')
							ind_subsubcon_file = ind_subsubcon_file.replace('\n', '')
							con = ind_subsubcon_file.split(':')[0]
							con = con.replace(' ','')
							subcon = ind_subsubcon_file.split(':')[1]
							subcon = subcon.replace(' ','')
							subsubcon = ind_subsubcon_file.split(':')[2]
							subsubcon = subsubcon.replace(' ','')
							ind = ind_subsubcon_file.split(':')[3]
							ind = ind.replace(' ','')
							for i in ont.concepts.all():
								if con == i.concept_name:
									cont = i
									for j in cont.sub_concepts.all():
										if subcon == j.sub_concept_name:
											subcont = j
											for k in subcont.sub_concepts1.all():
												if subsubcon == k.sub_concept_name:
													indiv = Individual(individual_name = ind)
													indiv.save()
													k.individuals.add(indiv)
													k.save()

						if fstr.startswith('----------Аттрибут экземпляра (подподкласса) :'):
							atr_ind_subsubcon_file = fstr.replace('----------Аттрибут экземпляра (подподкласса) :', '')
							atr_ind_subsubcon_file = atr_ind_subsubcon_file.replace('\n', '')
							con = atr_ind_subsubcon_file.split(':')[0]
							con = con.replace(' ','')
							subcon = atr_ind_subsubcon_file.split(':')[1]
							subcon = subcon.replace(' ','')
							subsubcon = atr_ind_subsubcon_file.split(':')[2]
							subsubcon = subsubcon.replace(' ','')
							ind = atr_ind_subsubcon_file.split(':')[3]
							ind = ind.replace(' ','')
							atrn = atr_ind_subsubcon_file.split(':')[4]
							atrn = atrn.replace(' ','')
							atrv = atr_ind_subsubcon_file.split(':')[5]
							atrv = atrv.replace(' ','')
							for i in ont.concepts.all():
								if con == i.concept_name:
									cont = i
									for j in cont.sub_concepts.all():
										if subcon == j.sub_concept_name:
											subcont = j
											for k in subcont.sub_concepts1.all():
												if subsubcon == k.sub_concept_name:
													subsubcont = k
													for t in subsubcont.individuals.all():
														if ind == t.individual_name:
															attr = Attribute(attribute_name = atrn, attribute_value = atrv)
															attr.save()
															t.attributes.add(attr)
															attr.save()
						if create_ontology_check:
							history_of_work_ontology.append(ont)
							context['work_ontology'] = history_of_work_ontology[-1]
	else:
		open_form = OpenForm(request.POST, request.FILES)
		context['open_form'] = open_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			add_individual_or_sub_form = AddIndividualOrSubForm(request.POST)
			context['add_individual_or_sub_form'] = add_individual_or_sub_form
			if add_individual_or_sub_form.is_valid():
				concept_check = False
				not_exist_individual = True
				not_exist_sub_concept = True
				new_individual_name = add_individual_or_sub_form.cleaned_data.get('new_individual_name')
				concept_individual_name = add_individual_or_sub_form.cleaned_data.get('concept_individual_name')
				new_sub_concept_name = add_individual_or_sub_form.cleaned_data.get('new_sub_concept_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if concept_individual_name == i.concept_name:
						concept_for_new_individual = i
						concept_check = True
						for j in concept_for_new_individual.individuals.all():
							if new_individual_name == j.individual_name:
								not_exist_individual = False
						for j in concept_for_new_individual.sub_concepts.all():
							if new_sub_concept_name == j.sub_concept_name:
								not_exist_sub_concept = False
				if new_individual_name != '' and concept_check and not_exist_individual :
					ind = Individual(individual_name = new_individual_name)
					ind.save()
					concept_for_new_individual.individuals.add(ind)
				if new_sub_concept_name != '' and concept_check and not_exist_sub_concept:
					subcon = SubConcept(sub_concept_name = new_sub_concept_name)
					subcon.save()
					concept_for_new_individual.sub_concepts.add(subcon)
	else:
		add_individual_or_sub_form = AddIndividualOrSubForm(request.POST)
		context['add_individual_or_sub_form'] = add_individual_or_sub_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			add_individual_or_sub_sub_form = AddIndividualOrSubSubForm(request.POST)
			context['add_individual_or_sub_sub_form'] = add_individual_or_sub_sub_form
			if add_individual_or_sub_sub_form.is_valid():
				concept_check = False
				sub_concept_check = False
				not_exist_individual = True
				not_exist_sub_sub_concept = True
				concept_name_for_sub = add_individual_or_sub_sub_form.cleaned_data.get('concept_name_for_sub')
				sub_concept_individual_name = add_individual_or_sub_sub_form.cleaned_data.get('sub_concept_individual_name')
				new_sub_individual_name = add_individual_or_sub_sub_form.cleaned_data.get('new_sub_individual_name')			
				new_sub_sub_concept_name = add_individual_or_sub_sub_form.cleaned_data.get('new_sub_sub_concept_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if concept_name_for_sub == i.concept_name:
						concept_for_new_sub = i
						concept_check = True 
				if concept_check:
					if len(concept_for_new_sub.sub_concepts.all()) > 0:
						for i in concept_for_new_sub.sub_concepts.all():
							if sub_concept_individual_name == i.sub_concept_name:
								sub_concept_for_new_sub = i
								sub_concept_check = True
								for j in sub_concept_for_new_sub.sub_concepts1.all():
									if new_sub_sub_concept_name == j.sub_concept_name:
										not_exist_sub_sub_concept = False
								for j in sub_concept_for_new_sub.individuals.all():
									if new_sub_individual_name == j.individual_name:
										not_exist_individual = False
						if new_sub_individual_name != '' and sub_concept_check and not_exist_individual: 
							ind = Individual(individual_name = new_sub_individual_name)
							ind.save()
							sub_concept_for_new_sub.individuals.add(ind)
						if new_sub_sub_concept_name != '' and sub_concept_check and not_exist_sub_sub_concept:
							subcon = SubConcept1(sub_concept_name = new_sub_sub_concept_name)
							subcon.save()
							sub_concept_for_new_sub.sub_concepts1.add(subcon)
	else:
		add_individual_or_sub_sub_form = AddIndividualOrSubSubForm(request.POST)
		context['add_individual_or_sub_sub_form'] = add_individual_or_sub_sub_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			add_individual_for_sub_sub_form = AddIndividualForSubSubForm(request.POST)
			context['add_individual_for_sub_sub_form'] = add_individual_for_sub_sub_form
			if add_individual_for_sub_sub_form.is_valid():
				concept_check = False
				sub_concept_check = False
				sub_sub_concept_chek = False
				not_exist_individual = True
				concept_name_for_sub = add_individual_for_sub_sub_form.cleaned_data.get('concept_name_for_sub_add')
				sub_concept_individual_name = add_individual_for_sub_sub_form.cleaned_data.get('sub_concept_individual_name_add')
				individual_name_for_sub_sub = add_individual_for_sub_sub_form.cleaned_data.get('individual_name_for_sub_sub')			
				sub_sub_concept_individual_name = add_individual_for_sub_sub_form.cleaned_data.get('sub_sub_concept_individual_name_add')
				for i in history_of_work_ontology[-1].concepts.all():
					if concept_name_for_sub == i.concept_name:
						concept_for_new_sub = i
						concept_check = True 
				if concept_check:
					if len(concept_for_new_sub.sub_concepts.all()) > 0:
						for i in concept_for_new_sub.sub_concepts.all():
							if sub_concept_individual_name == i.sub_concept_name:
								sub_concept_for_new_sub = i
								sub_concept_check = True
				if sub_concept_check:
					if len(sub_concept_for_new_sub.sub_concepts1.all()) > 0:
						for j in sub_concept_for_new_sub.sub_concepts1.all():
							if sub_sub_concept_individual_name == j.sub_concept_name:
								sub_sub_concept_for_new_ind = j
								sub_sub_concept_chek = True
								if len(sub_sub_concept_for_new_ind.individuals.all()) > 0:
									for ind in sub_sub_concept_for_new_ind.individuals.all():
										if individual_name_for_sub_sub == ind.individual_name:
											not_exist_individual = False
				if individual_name_for_sub_sub != '' and concept_check and sub_concept_check and sub_sub_concept_chek and not_exist_individual:
					ind = Individual(individual_name = individual_name_for_sub_sub)
					ind.save()
					sub_sub_concept_for_new_ind.individuals.add(ind)
	else:
		add_individual_for_sub_sub_form = AddIndividualForSubSubForm(request.POST)
		context['add_individual_for_sub_sub_form'] = add_individual_for_sub_sub_form

	if len(Ontology.objects.all()) == 0:
		return render(request, 'mainpage/initpage.html', context)
	else:
		return render(request, 'mainpage/index.html', context)

def attributes(request):
	context ={
	}
	context['checked'] = 2
	if len(history_of_work_ontology) > 0:
		context['work_ontology'] = history_of_work_ontology[-1]
	create_and_change(request, context)
	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			add_attribute_con_form = addConceptIndividualAttrForm(request.POST)
			context['add_attribute_con_form'] = add_attribute_con_form
			if add_attribute_con_form.is_valid():
				concept_check = False
				individual_check = False
				attr_check = True
				new_attribute_name = add_attribute_con_form.cleaned_data.get('new_attribute_name')
				new_attribute_value = add_attribute_con_form.cleaned_data.get('new_attribute_value')
				concept_for_attribute_name = add_attribute_con_form.cleaned_data.get('concept_for_attribute_name')
				individual_for_attribute_name = add_attribute_con_form.cleaned_data.get('individual_for_attribute_name')
				print(history_of_work_ontology[-1])
				for i in history_of_work_ontology[-1].concepts.all():
					if concept_for_attribute_name == i.concept_name:
						concept_for_attribute = i
						concept_check = True
						for i in concept_for_attribute.individuals.all():
							if individual_for_attribute_name == i.individual_name:
								individual_for_attribute = i
								individual_check = True
								for g in individual_for_attribute.attributes.all():
									if new_attribute_name == g.attribute_name:
										attr_check = False

				if new_attribute_name != '' and new_attribute_value != '' and concept_check and individual_check and attr_check:
					atr = Attribute(attribute_name = new_attribute_name, attribute_value = new_attribute_value)
					atr.save()
					individual_for_attribute.attributes.add(atr)
					individual_for_attribute.save()
	else:
		add_attribute_con_form = addConceptIndividualAttrForm(request.POST)
		context['add_attribute_con_form'] = add_attribute_con_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			add_attribute_subcon_form = addSubConceptIndividualAttrForm(request.POST)
			context['add_attribute_subcon_form'] = add_attribute_subcon_form
			if add_attribute_subcon_form.is_valid():
				concept_check = False
				subconcept_chek = False
				individual_check = False
				attr_check = True
				new_attr_name = add_attribute_subcon_form.cleaned_data.get('new_attr_name')
				new_attr_value = add_attribute_subcon_form.cleaned_data.get('new_attr_value')
				subconc_for_attribute_name = add_attribute_subcon_form.cleaned_data.get('subconc_for_attribute_name')
				conc_for_attribute_name = add_attribute_subcon_form.cleaned_data.get('conc_for_attribute_name')
				individ_for_attribute_name = add_attribute_subcon_form.cleaned_data.get('individ_for_attribute_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if conc_for_attribute_name == i.concept_name:
						concept_for_attribute = i
						concept_check = True
						for j in concept_for_attribute.sub_concepts.all():
							if subconc_for_attribute_name == j.sub_concept_name:
								subconc_for_attribute = j
								subconcept_chek = True
								for k in subconc_for_attribute.individuals.all():
									if individ_for_attribute_name == k.individual_name:
										individ_for_attribute = k
										individual_check = True
										for g in individ_for_attribute.attributes.all():
											if new_attr_name == g.attribute_name:
												attr_check = False

				if new_attr_name != '' and new_attr_value != '' and concept_check and individual_check and subconcept_chek and attr_check:
					atr = Attribute(attribute_name = new_attr_name, attribute_value = new_attr_value)
					atr.save()
					individ_for_attribute.attributes.add(atr)
					individ_for_attribute.save()
	else:
		add_attribute_subcon_form = addSubConceptIndividualAttrForm(request.POST)
		context['add_attribute_subcon_form'] = add_attribute_subcon_form

	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			add_attribute_subsubcon_form = addSubSubConceptIndividualAttrForm(request.POST)
			context['add_attribute_subsubcon_form'] = add_attribute_subsubcon_form
			if add_attribute_subsubcon_form.is_valid():
				concept_check = False
				subconcept_chek = False
				subsubconcept_chek = False
				individual_check = False
				attr_check = True
				new_attrn = add_attribute_subsubcon_form.cleaned_data.get('new_attrn')
				new_attrv = add_attribute_subsubcon_form.cleaned_data.get('new_attrv')
				subsubcon_for_attribute_name = add_attribute_subsubcon_form.cleaned_data.get('subsubcon_for_attribute_name')
				subcon_for_attribute_name = add_attribute_subsubcon_form.cleaned_data.get('subcon_for_attribute_name')
				con_for_attribute_name = add_attribute_subsubcon_form.cleaned_data.get('con_for_attribute_name')
				ind_for_attribute_name = add_attribute_subsubcon_form.cleaned_data.get('ind_for_attribute_name')
				for i in history_of_work_ontology[-1].concepts.all():
					if con_for_attribute_name == i.concept_name:
						con_for_attribute = i
						concept_check = True
						for j in con_for_attribute.sub_concepts.all():
							if subcon_for_attribute_name == j.sub_concept_name:
								subcon_for_attribute = j
								subconcept_chek = True
								for k in subcon_for_attribute.sub_concepts1.all():
									if subsubcon_for_attribute_name == k.sub_concept_name:
										subsubcon_for_attribute = k
										subsubconcept_chek = True
										for l in subsubcon_for_attribute.individuals.all():
											if ind_for_attribute_name == l.individual_name:
												ind_for_attribute = l
												individual_check = True
												for g in ind_for_attribute.attributes.all():
													if new_attrn == g.attribute_name:
														attr_check = False

				if new_attrn != '' and new_attrv != '' and concept_check and individual_check and subconcept_chek and subsubconcept_chek and attr_check:
					atr = Attribute(attribute_name = new_attrn, attribute_value = new_attrv)
					atr.save()
					ind_for_attribute.attributes.add(atr)
					ind_for_attribute.save()
	else:
		add_attribute_subsubcon_form = addSubSubConceptIndividualAttrForm(request.POST)
		context['add_attribute_subsubcon_form'] = add_attribute_subsubcon_form

	if len(Ontology.objects.all()) == 0:
		return render(request, 'mainpage/initpage.html', context)
	else:
		return render(request, 'mainpage/index.html', context)

def requests(request):
	context ={
	}
	context['checked'] = 3
	if len(history_of_work_ontology) > 0:
		context['work_ontology'] = history_of_work_ontology[-1]
	create_and_change(request, context)
	if request.method == 'POST':
		if len(history_of_work_ontology) > 0:
			query_Form = QueryForm(request.POST, ontology = history_of_work_ontology[-1])
			context['query_Form'] = query_Form
			query_result = []
			query_result1 = []
			query_result2 = []
			query_result3 = []
			check2 = False
			check3 = False
			if query_Form.is_valid():
				con_query_name = query_Form.cleaned_data['concepts']
				attrn_query1 = query_Form.cleaned_data['attributes1']
				attrv_query1 = query_Form.cleaned_data['attrv1']
				attrn_query2 = query_Form.cleaned_data['attributes2']
				attrv_query2 = query_Form.cleaned_data['attrv2']
				attrn_query3 = query_Form.cleaned_data['attributes3']
				attrv_query3 = query_Form.cleaned_data['attrv3']

				for i in history_of_work_ontology[-1].concepts.all():
					if con_query_name == i.concept_name:
						con_query = i
						for j in con_query.individuals.all():
							for atr in j.attributes.all():
								if attrn_query1 == atr.attribute_name and attrv_query1 == atr.attribute_value:
									query_result1.append(j.individual_name)
								if attrn_query2 == atr.attribute_name and attrv_query2 == atr.attribute_value:
									query_result2.append(j.individual_name)
								if attrn_query3 == atr.attribute_name and attrv_query3 == atr.attribute_value:
									query_result3.append(j.individual_name)

					for sub_con in i.sub_concepts.all():
						if con_query_name == sub_con.sub_concept_name:
							con_query = sub_con
							for j in con_query.individuals.all():
								for atr in j.attributes.all():
									if attrn_query1 == atr.attribute_name and attrv_query1 == atr.attribute_value:
										query_result1.append(j.individual_name)
									if attrn_query2 == atr.attribute_name and attrv_query2 == atr.attribute_value:
										query_result2.append(j.individual_name)
									if attrn_query3 == atr.attribute_name and attrv_query3 == atr.attribute_value:
										query_result3.append(j.individual_name)

						for sub_con1 in sub_con.sub_concepts1.all():
							if con_query_name == sub_con1.sub_concept_name:
								con_query = sub_con1
								for j in con_query.individuals.all():
									for atr in j.attributes.all():
										if attrn_query1 == atr.attribute_name and attrv_query1 == atr.attribute_value:
											query_result1.append(j.individual_name)
										if attrn_query2 == atr.attribute_name and attrv_query2 == atr.attribute_value:
											query_result2.append(j.individual_name)
										if attrn_query3 == atr.attribute_name and attrv_query3 == atr.attribute_value:
											query_result3.append(j.individual_name)		

				if attrv_query2 != '' and attrv_query3 == '':
					for i in query_result1:
						for j in query_result2:
							if i == j:
								query_result.append(j)
					context['query_result'] = query_result

				if attrv_query3 != '' and attrv_query2 == '':
					for i in query_result1:
						for j in query_result3:
							if i == j:
								query_result.append(j)
					context['query_result'] = query_result

				if attrv_query3 != '' and attrv_query2 != '':
					for i in query_result1:
						for j in query_result3:
							for k in query_result2:
								if i == j and i == k and j == k:
									query_result.append(j)
					context['query_result'] = query_result

				if attrv_query3 == '' and attrv_query2 == '':
					for i in query_result1:
						query_result.append(i)
					context['query_result'] = query_result
	else:
		if len(history_of_work_ontology) > 0:
			query_Form = QueryForm(request.POST, ontology = history_of_work_ontology[-1])
			context['query_Form'] = query_Form

	if len(Ontology.objects.all()) == 0:
		return render(request, 'mainpage/initpage.html', context)
	else:
		return render(request, 'mainpage/index.html', context)

def relations(request):
	context ={
	}
	context['checked'] = 4
	if len(history_of_work_ontology) > 0:
		context['work_ontology'] = history_of_work_ontology[-1]
	create_and_change(request, context)
	if len(Ontology.objects.all()) == 0:
		return render(request, 'mainpage/initpage.html', context)
	else:
		return render(request, 'mainpage/index.html', context)

