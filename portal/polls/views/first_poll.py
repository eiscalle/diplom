# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import defaultdict
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.utils.functional import curry
from django.views.generic import View, TemplateView, ListView
from portal.polls.forms import FirstPollForm
from portal.polls.models import Question, Department, UserAnswer, Answer


class FirstPollStart(TemplateView):
    template_name = 'first_poll_start.html'
    form = FirstPollForm
    http_method_names = ['get', 'post']
    formset = None

    def get(self, request, *args, **kwargs):
        self.question = Question.objects.get(number=0)
        self.departments = Department.objects.all()

        departments_count = self.departments.count()
        first_user_answers = UserAnswer.objects.filter(user=request.user, department__in=self.departments, answer__question__number=0)
        first_answers_count = first_user_answers.count()
        if first_answers_count == departments_count:
            return HttpResponseRedirect(reverse('first_poll'))

        if self.formset is None:
            department_count = self.departments.count()
            self.formset = formset_factory(FirstPollForm, extra=department_count)

            self.formset = self.formset()
            for i, form in enumerate(self.formset.forms):
                form.initial = {'department': self.departments[i]}
                form.fields['answer'].queryset = Answer.objects.filter(question=self.question)

        return super(FirstPollStart, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.formset = formset_factory(FirstPollForm)
        self.formset = self.formset(request.POST)
        if self.formset.is_valid():
            for form in self.formset:
                user_answer = UserAnswer.objects.filter(user=request.user, department=form.instance.department, answer__question__number=0)
                if not user_answer.exists():
                    form.instance.user = request.user
                    form.save()
                else:
                    user_answer = user_answer[0]
                    user_answer.answer = form.instance.answer
                    user_answer.save()
            return HttpResponseRedirect(reverse('first_poll'))
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FirstPollStart, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['departments'] = {x.pk: x for x in self.departments}
        context['formset'] = self.formset
        return context


class FirstPollView(ListView):
    model = Question
    template_name = 'first_poll.html'
    formset = None
    current_department = None
    current_questions = None
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return super(FirstPollView, self).get_queryset().filter(number__gt=0)

    def post(self, request, *args, **kwargs):
        self.formset = formset_factory(FirstPollForm)
        self.formset = self.formset(request.POST)

        if self.formset.is_valid():
            for form in self.formset:
                question = Answer.objects.get(pk=form.instance.answer.pk).question
                user_answer = UserAnswer.objects.filter(user=request.user, department=form.instance.department, answer__question=question)
                if not user_answer.exists():
                    form.instance.user = request.user
                    form.save()
                else:
                    user_answer = user_answer[0]
                    user_answer.answer = form.instance.answer
                    user_answer.save()
            return HttpResponseRedirect(reverse('first_poll'))
        else:
            return self.get(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        user = request.user
        departments = Department.objects.all()
        departments_count = departments.count()
        first_user_answers = UserAnswer.objects.filter(user=user, department__in=departments, answer__question__number=0)
        first_answers_count = first_user_answers.count()
        if first_answers_count != departments_count:
            return HttpResponseRedirect(reverse('first_poll_start'))

        departments = [x.department for x in first_user_answers if x.answer.weight == 1]
        self.object_list = self.get_queryset()
        done_questions = defaultdict(list)
        for user_answer in UserAnswer.objects.filter(user=user, answer__question__number__gt=0).order_by('department'):
            done_questions[user_answer.department.pk].append(user_answer.answer.question)

        questions_by_departments = defaultdict(list)
        min_q_count = self.object_list.count()
        for department in departments:
            for question in self.object_list:
                if question not in done_questions[department.pk]:
                    questions_by_departments[department.pk].append(question)
            q_count = len(questions_by_departments[department.pk])
            if 0 < q_count <= min_q_count:
                min_q_count = q_count
                self.current_department = department
                self.current_questions = questions_by_departments[department.pk]
        if self.current_department is not None:
            if self.formset is None:
                self.formset = formset_factory(FirstPollForm, extra=min_q_count)

                self.formset = self.formset()
            for i, form in enumerate(self.formset.forms):
                form.initial = {'department': self.current_department}
                form.fields['answer'].queryset = Answer.objects.filter(question=self.current_questions[i])

        return super(FirstPollView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FirstPollView, self).get_context_data(**kwargs)

        context['department'] = self.current_department
        context['questions'] = self.current_questions
        context['formset'] = self.formset

        return context