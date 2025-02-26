import xlwt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from templated_email import send_templated_mail
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Submission, Status, Review, Reviewer, Decision, Resubmission, Amandement, News
from .forms import NewsForm, AmandementForm, AmandementUpdateForm, ResubmissionUpdateForm, ResubmissionForm, DecisionForm,ReviewerForm, UserRegistrationForm, UserForm, SubmissionForm, ProfileForm, StatusForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from bootstrap_datepicker_plus.widgets import DatePickerInput


@login_required
def dashboard(request):
    user = request.user
    news = News.objects.all()
    context = {
        'user': user,
        'news': news
    }
    return render(request, 'dashboard/dashboard.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
           # send_templated_mail(
           #     template_name='welcome',
           #     from_email='no-reply@ui.ac.id',
           #     recipient_list=[new_user.email],
           #     context={
           #         'username': new_user.username,
           #         'full_name': new_user.get_full_name(),
           #         'password': new_user.password
           #     },
                # Optional:
                # cc=['cc@example.com'],
                # bcc=['bcc@example.com'],
                # headers={'My-Custom-Header':'Custom Value'},
                # template_prefix="my_emails/",
                # template_suffix="email",
            #)

            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            profile.save()
            messages.success(request,
                             'Your registration has been succesfully.')

            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile/profile.html', context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        formuser = UserForm(instance=request.user,
                            data=request.POST)
        formprofile = ProfileForm(instance=request.user.profile,
                                  data=request.POST,
                                  files=request.FILES)

        # Check if the form is valid:
        if formuser.is_valid() and formprofile.is_valid():
            formuser.save()
            formprofile.save()

            messages.success(request, 'Your profile has been updated.')
        else:
            messages.error(request, 'Error ! Profile has not been updated.')
    else:
        formuser = UserForm(instance=request.user)
        formprofile = ProfileForm(instance=request.user.profile)

    context = {
        'formuser': formuser,
        'formprofile': formprofile,
    }
    return render(request, 'profile/profile_update.html', context)


@login_required
def submission_detail(request, slug):
    submission = get_object_or_404(Submission, slug=slug)
    status = get_object_or_404(Status, submission=submission)
    reviewers = Reviewer.objects.filter(submission=submission)
    reviews = Review.objects.filter(submission=submission)
    decisions = Decision.objects.filter(submission=submission)
    revisions = Resubmission.objects.filter(submission=submission)
    amandements = Amandement.objects.filter(submission=submission)

    context = {
        'object': submission,
        'status': status,
        'reviews': reviews,
        'reviewers': reviewers,
        'decisions': decisions,
        'revisions': revisions,

        'amandements': amandements
    }

    return render(request, 'dashboard/submission/submission_detail.html', context)


@login_required
def submission_create(request):
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission_form = form.save(commit=False)
            submission_form.user = request.user
            submission_form.save()
        #send_templated_mail(
        #    template_name='submission',
        #    from_email='info_kppikg@ui.ac.id',
        #    recipient_list=['scientific_kppikg@ui.ac.id'],
       #     context={
        #        'full_name': request.user.get_full_name(),
        #    },
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_prefix="my_emails/",
            # template_suffix="email",
        #)

        status = Status.objects.create(submission=submission_form)
        status.save()

        messages.success(request, 'Submission is succesfully created.')
        slug = form.instance.slug
        submission = get_object_or_404(Submission, slug=slug)

        return redirect(submission.get_absolute_url())
    context = {
        'form': form
    }
    return render(request, 'dashboard/submission/submission_create.html', context)


@login_required
def submission_update(request, slug):
    instance = get_object_or_404(Submission, slug=slug)
    form = SubmissionForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Submission is succesfully updated.')
        slug = form.instance.slug
        submission = get_object_or_404(Submission, slug=slug)
        return redirect(submission.get_absolute_url())
    context = {
        'form': form,
        'instance': 'object'
    }
    return render(request, 'dashboard/submission/submission_update.html', context)


@login_required
def submission_delete(request, slug):
    submission = get_object_or_404(Submission, slug=slug)

    if request.method == "POST":
        submission.delete()
        messages.success(request, 'Submission is successfully deleted')
        return redirect(submission.get_my_submission())

    context = {
        'object': submission
    }
    return render(request, 'dashboard/submission/submission_delete.html', context)


@login_required
def success(request):
    return render(request, "dashboard/submission/success.html")



@login_required
def submission_list(request):
    all_submission = Submission.objects.all().order_by('created_at')
    query = request.GET.get("q")
    if query:
        all_submission = all_submission.filter(Q(title__icontains=query) |
                                               Q(user__first_name__icontains=query) |
                                               Q(user__last_name__icontains=query)
                                                 ).distinct()
    paginator = Paginator(all_submission, 10)
    page = request.GET.get('page')
    try:
        submission = paginator.page(page)
    except PageNotAnInteger:
        submission = paginator.page(1)
    except EmptyPage:
        submission = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'object_list': submission
    }
    return render(request, 'dashboard/submission/submission_list.html', context)


@login_required
def my_submission_list(request):
    all_submission = Submission.objects.filter(user=request.user)
    query = request.GET.get("q")
    if query:
        all_submission = all_submission.filter(Q(title__icontains=query) |
                                               Q(user__first_name__icontains=query) |
                                               Q(user__last_name__icontains=query)
                                               ).distinct()
    paginator = Paginator(all_submission, 10)
    page = request.GET.get('page')
    try:
        submission = paginator.page(page)
    except PageNotAnInteger:
        submission = paginator.page(1)
    except EmptyPage:
        submission = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'object_list': submission
    }
    return render(request, 'dashboard/submission/my_submission_list.html', context)

@login_required
def status_update(request, id):
    instance = get_object_or_404(Status, id=id)
    form = StatusForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Status sudah diupdate.')

    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'dashboard/submission/status_update.html', context)


@login_required
def review(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = ReviewForm(request.POST, request.FILES)
    if form.is_valid():
        review_form = form.save(commit=False)
        review_form.reviewer = request.user
        review_form.submission = submission
        review_form.save()
        messages.success(request, 'Review sudah disimpan.')
        return redirect(submission.get_absolute_url())

    form = ReviewForm()
    context = {
        "form":form,
        'submission': submission
    }
    return render(request, 'dashboard/submission/review.html',context)


@login_required
def reviewer(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = ReviewerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        reviewer = get_object_or_404(User, pk=request.POST.get('reviewer'))
        reviewer_form = form.save(commit=False)
        reviewer_form.submission = submission
        reviewer_form.reviewer = reviewer
        reviewer_form.save()
        messages.success(request, 'Reviewer sudah dipilih')

    form = ReviewerForm()
    context = {
        "form":form,
        "submission": submission

    }
    return render(request, 'dashboard/submission/reviewer.html',context)


@login_required
def reviewer_detail(request, id):
    reviewer = get_object_or_404(Reviewer, id=id)

    context = {
        'object': reviewer,
    }

    return render(request, 'dashboard/submission/reviewer_detail.html', context)



@login_required
def reviewer_delete(request, id):
    reviewer = get_object_or_404(Reviewer, id=id)

    if request.method == "POST":
        reviewer.delete()
        messages.success(request, 'Reviewer sudah dihapus')
        return redirect(reviewer.get_submission_url())

    context = {
        'object': reviewer
    }
    return render(request, 'dashboard/submission/reviewer_delete.html', context)


@login_required
def reviewer_update(request, id):
    instance = get_object_or_404(Reviewer, id=id)
    form = ReviewerForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Reviewer sudah diupdate.')
        return redirect(instance.get_absolute_url())
    context = {
        'form': form,
        'object': instance
    }
    return render(request, 'dashboard/submission/reviewer_update.html', context)


@login_required
def reviewer_submission_list(request):
    all_submission = Reviewer.objects.filter(reviewer=request.user)
    context = {
        'object_list': all_submission
    }
    return render(request, 'dashboard/submission/reviewer_submission_list.html', context)


@login_required
def decision(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = DecisionForm(request.POST, request.FILES)
    if form.is_valid():
        decision_form = form.save(commit=False)
        decision_form.submission = submission
        decision_form.save()
        messages.success(request, 'Decision is successfully submited')

        return redirect(submission.get_absolute_url())

    form = DecisionForm()
    context = {
        "form": form,
        "submission": submission
    }
    return render(request, 'dashboard/submission/decision.html', context)


@login_required
def resubmission(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = ResubmissionForm(request.POST, request.FILES)
    if form.is_valid():
        resubmission_form = form.save(commit=False)
        resubmission_form.submission = submission
        resubmission_form.save()
        messages.success(request, 'Resubmission berhasil disimpan')

        return redirect(submission.get_absolute_url())

    form = ResubmissionForm()
    context = {
        "form": form,
        "submission": submission
    }
    return render(request, 'dashboard/submission/resubmission.html', context)


@login_required
def resubmission_update(request, id):
    instance = get_object_or_404(Resubmission, id=id)
    form = ResubmissionUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Telaah sudah disimpan.')
        return redirect(instance.get_submission_url())
    context = {
        'form': form,
        'object': instance
    }
    return render(request, 'dashboard/submission/resubmission_update.html', context)



@login_required
def resubmission_list(request):
    all_resubmission = Resubmission.objects.all().order_by('created_at')
    query = request.GET.get("q")
    if query:
        all_resubmission = all_resubmission.filter(Q(submission__title__icontains=query) |
                                               Q(submission__user__first_name__icontains=query) |
                                               Q(submission__user__last_name__icontains=query)
                                                 ).distinct()
    paginator = Paginator(all_resubmission, 10)
    page = request.GET.get('page')
    try:
        resubmission = paginator.page(page)
    except PageNotAnInteger:
        resubmission = paginator.page(1)
    except EmptyPage:
        resubmission = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'object_list': resubmission
    }
    return render(request, 'dashboard/submission/resubmission_list.html', context)


@login_required
def my_resubmission_list(request):
    all_resubmission = Resubmission.objects.filter(submission__user = request.user)
    query = request.GET.get("q")
    if query:
        all_resubmission = all_resubmission.filter(Q(submission__title__icontains=query) |
                                               Q(submission__user__first_name__icontains=query) |
                                               Q(submission__user__last_name__icontains=query)
                                               ).distinct()
    paginator = Paginator(all_resubmission, 10)
    page = request.GET.get('page')
    try:
        resubmission = paginator.page(page)
    except PageNotAnInteger:
        resubmission = paginator.page(1)
    except EmptyPage:
        resubmission = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'object_list': resubmission
    }
    return render(request, 'dashboard/submission/my_resubmission_list.html', context)


login_required
def resubmission_detail(request, id):
    resubmission = get_object_or_404(Resubmission, id=id)

    context = {
        'object': resubmission,
    }

    return render(request, 'dashboard/submission/resubmission_detail.html', context)



@login_required
def amandement(request, slug):
    submission = Submission.objects.get(slug=slug)
    form = AmandementForm(request.POST, request.FILES)
    if form.is_valid():
        amandement_form = form.save(commit=False)
        amandement_form.submission = submission
        amandement_form.save()
        messages.success(request, 'Amandemen berhasil disimpan')

        return redirect(submission.get_absolute_url())

    form = AmandementForm()
    context = {
        "form": form,
        "submission": submission
    }
    return render(request, 'dashboard/submission/amandement.html', context)


@login_required
def amandement_update(request, id):
    instance = get_object_or_404(Amandement, id=id)
    form = AmandementUpdateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Telaah sudah disimpan.')
        return redirect(instance.get_submission_url())
    context = {
        'form': form,
        'object': instance
    }
    return render(request, 'dashboard/submission/amandement_update.html', context)



@login_required
def amandement_list(request):
    all_amandement = Amandement.objects.all().order_by('created_at')
    query = request.GET.get("q")
    if query:
        all_amandement = all_amandement.filter(Q(submission__title__icontains=query) |
                                               Q(submission__user__first_name__icontains=query) |
                                               Q(submission__user__last_name__icontains=query)
                                                 ).distinct()
    paginator = Paginator(all_amandement, 10)
    page = request.GET.get('page')
    try:
        amandement = paginator.page(page)
    except PageNotAnInteger:
        amandement = paginator.page(1)
    except EmptyPage:
        amandement = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'object_list': amandement
    }
    return render(request, 'dashboard/submission/amandement_list.html', context)


@login_required
def my_amandement_list(request):
    all_amandement = Amandement.objects.filter(submission__user = request.user)
    query = request.GET.get("q")
    if query:
        all_amandement = all_amandement.filter(Q(submission__title__icontains=query) |
                                               Q(submission__user__first_name__icontains=query) |
                                               Q(submission__user__last_name__icontains=query)
                                               ).distinct()
    paginator = Paginator(all_amandement, 10)
    page = request.GET.get('page')
    try:
        amandement = paginator.page(page)
    except PageNotAnInteger:
        amandement = paginator.page(1)
    except EmptyPage:
        amandement = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'object_list': amandement
    }
    return render(request, 'dashboard/submission/my_amandement_list.html', context)


login_required
def amandement_detail(request, id):
    amandement = get_object_or_404(Amandement, id=id)

    context = {
        'object': amandement,
    }

    return render(request, 'dashboard/submission/amandement_detail.html', context)


@login_required
@staff_member_required
def news_create(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_form = form.save(commit=False)
            news_form.user = request.user
            news_form.save()
        #send_templated_mail(
        #    template_name='submission',
        #    from_email='info_kppikg@ui.ac.id',
        #    recipient_list=['scientific_kppikg@ui.ac.id'],
       #     context={
        #        'full_name': request.user.get_full_name(),
        #    },
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_prefix="my_emails/",
            # template_suffix="email",
        #)

        messages.success(request, 'News is succesfully created.')
        slug = form.instance.slug
        news = get_object_or_404(News, slug=slug)

        return redirect(news.get_absolute_url())
    context = {
        'form': form
    }
    return render(request, 'dashboard/news/news_create.html', context)

@login_required
@staff_member_required
def news_update(request, slug):
    instance = get_object_or_404(News, slug=slug)
    form = NewsForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'News is succesfully updated.')
        slug = form.instance.slug
        news = get_object_or_404(News, slug=slug)
        return redirect(news.get_absolute_url())
    context = {
        'form': form,
        'instance': 'object'
    }
    return render(request, 'dashboard/news/news_update.html', context)


@login_required
@staff_member_required
def news_delete(request, slug):
    news = get_object_or_404(News, slug=slug)

    if request.method == "POST":
        news.delete()
        messages.success(request, 'News is successfully deleted')
        return redirect(news.get_news_list())

    context = {
        'object': news
    }
    return render(request, 'dashboard/news/news_delete.html', context)

@login_required
@staff_member_required
def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)

    context = {
        'object': news,
    }

    return render(request, 'dashboard/news/news_detail.html', context)


@login_required
@staff_member_required
def news_list(request):
    all_news = News.objects.all().order_by('-created_at')
    query = request.GET.get("q")
    if query:
        all_news = all_news.filter(Q(news__title__icontains=query) |
                                               Q(news__contain__icontains=query)
                                                 ).distinct()
    paginator = Paginator(all_news, 10)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'object_list': news
    }
    return render(request, 'dashboard/news/news_list.html', context)