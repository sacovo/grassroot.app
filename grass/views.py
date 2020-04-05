from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail

import phonenumbers

from formtools.wizard.views import SessionWizardView

from allauth.account.adapter import DefaultAccountAdapter
from feincms3.regions import Regions
from grass.models import Grassroot, Location, User, Category, Membership, LandingPage
from django.contrib.auth.forms import PasswordResetForm

from django.utils.text import slugify

from grass.renderer import renderer
from grass.forms import SignupForm, DescriptionStep, MissionStep, ContactForm

# Create your views here.


def landing_page(request, pk):
    grassroot = get_object_or_404(Grassroot, pk=pk)

    page = grassroot.landing_page

    return render(request, page.template.template_name, {
        "page": page,
        "grassroot": grassroot,
        "title": grassroot.name,
        "regions": Regions.from_item(
            page, renderer=renderer,
        )
    })


class SignupWizzard(SessionWizardView):
    form_list = [SignupForm, DescriptionStep, MissionStep]
    template_name = 'grass/form_step.html'

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()

        location = Location.objects.create(
            city=data['city'],
            zip_code=data['zip_code'],
            lat=data['lat'],
            lng=data['lng'],
        )

        grassroot = Grassroot.objects.create(
            name=data['group_name'],
            description=data['description'],
            mission=data['mission'],
            location=location,
        )

        grassroot.categories.set(data['categories'])
        grassroot.save()

        LandingPage.objects.create(
            grassroot=grassroot
        )

        self.request.session['group_pk'] = grassroot.pk

        if self.request.user.is_authenticated:
            return redirect('link-account')

        return redirect('login_or_signup')


def login_or_signup(request):
    return render(request, 'grass/login_or_signup.html', {
        'title': "Complete registration",
    })


@login_required
def link_account(request):
    pk = request.session['group_pk']
    grassroot = Grassroot.objects.get(pk=pk)
    user = request.user

    Membership.objects.create(
        user=user,
        grassroot=grassroot,
        role=1,
    )

    return render(request, 'grass/link_successful.html', {
        'user': user,
        'grassroot': grassroot,
    })


def home(request):
    return render(request, 'grass/home.html', {

    })


@login_required
def dashboard(request, pk):
    grassroot = get_object_or_404(Grassroot, pk=pk)

    request.session['group_pk'] = grassroot.pk

    return render(request, 'grass/dashboard.html', {
        'grassroot': grassroot,
        'title': "Dashboard: " + grassroot.name,
    })


def map_view(request):

    return render(request, 'grass/map.html', {
        'grassroot_list': Grassroot.objects.all(),
        'title': "Grassroots"
    })


@login_required
def edit_landing_page(request):
    pass


def about_view(request):
    form = ContactForm()
    message = ''

    if request.POST:
        form = ContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            email = data['your_email']
            name = data['your_name']
            send_mail(
                f"Message from {name} - {email}",
                data['your_message'],
                'contact@grassroot.app',
                ['sandro@covo.ch'],
                fail_silently=True,
            )
            message = 'Your message was sent.'
            form = ContactForm()

    return render(request, 'grass/about.html', {
        'form': form,
        'message': message,
    })
