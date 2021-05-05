from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView
from smart_open import smart_open

from .models import Document
from .forms import DocumentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
def home(request):
    if request.method == 'POST':
        print("POST")
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'], user=request.user)

            if newdoc.in_format():
                newdoc.save()

                # Redirect to the document list after POST
                return redirect(reverse("pts", kwargs={"newdoc_uuid": newdoc.uuid}))

            else:
                messages.error(request, 'ERROR: Insert a CSV with the columns: "POINT", "LONG", "LAT"')
                return HttpResponseRedirect(reverse('homepage'))

    else:
        print("GET")
        form = DocumentForm()
        context = {
            'form': form
        }
        return render(request, "main_app/homepage.html", context)


@login_required
def pts(request, newdoc_uuid):
    doc = Document.objects.filter(uuid=newdoc_uuid).first()

    if request.method == 'GET':
        with doc.docfile.open('r') as file_content:
            doclines = file_content.readlines()
            doclines = [n.decode().split(",") for n in doclines]

        return render(request, "main_app/pts.html", {'doclines': doclines[1:], 'headers': doclines[0]})

    if request.method == 'POST':
        return redirect(reverse("links", kwargs={"newdoc_uuid": newdoc_uuid}))


@login_required
def links(request, newdoc_uuid):
    doc = Document.objects.filter(uuid=newdoc_uuid).first()

    json_links = doc.calc_links()
    print(list(json_links.keys())[0])

    return render(request, "main_app/links.html", {'links': json_links})


class UserPointsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Document
    template_name = "main_app/user_points.html"
    context_object_name = "point_docs"
    paginate_by = 1

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return super().get_queryset().filter(user=user).order_by('-date_created')

    def get_context_data(self, **kwargs):
        all_docs = self.get_queryset()
        all_files = []

        for doc in all_docs:
            uuid = doc.uuid

            with smart_open(doc.docfile.path, 'rb') as file_content:
                doclines = file_content.readlines()
                doclines = [n.decode().split(",") for n in doclines]

                all_files.append({
                    "headers": doclines[0],
                    "points": doclines[1:],
                    "uuid": uuid
                })


            # with doc.docfile.open('r') as file_content:
            #     doclines = file_content.readlines()
            #     doclines = [n.decode().split(",") for n in doclines]
            #
            #     all_files.append({
            #         "headers": doclines[0],
            #         "points": doclines[1:],
            #         "uuid": uuid
            #     })

        page_size = self.get_paginate_by(all_files)
        if page_size:
            paginator, page, all_files, is_paginated = self.paginate_queryset(all_files, page_size)
            new_context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'all_files': all_files
            }

        else:
            new_context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'all_files': all_files
            }

        context = super(UserPointsListView, self).get_context_data(**kwargs)

        context.update(new_context)

        return context

    def test_func(self):
        if self.request.user.username == 'admin':
            return True
        elif self.request.user.username == self.kwargs.get('username'):
            return True
        else:
            return False


class CustomDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_success_url(self):
        return reverse_lazy("user-points", kwargs={"username": self.kwargs.get('username')})

    def test_func(self):
        if self.request.user.username == 'admin':
            return True
        elif self.request.user.username == self.kwargs.get('username'):
            return True
        else:
            return False
