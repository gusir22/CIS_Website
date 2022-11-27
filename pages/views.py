# pages/views.py
from datetime import datetime

from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q

from .models import (
    QandA,
    QandACategory,
    HomePageAnnouncements,
    ServiceAreas,
    AboutUsText,
    TermandConditions,
    OperationBlocks,
)

from products.models import (
    ProductCategory,
    ProductStyle,
    Product,
)
from projects.models import (
    ProjectExhibition,
)
from accounts.models import CustomUser

from .forms import (
    ContactForm,
    RequestEstimateForm,
)

class SandboxView(TemplateView):
    """Used to try concepts in a clean slate. This view should be deleted when pushed to live production"""
    template_name = 'pages/sandbox.html'

    def get_context_data(self, **kwargs):
        context = super(SandboxView, self).get_context_data(**kwargs)
        return context


# HOMEPAGE #############################################################################################################
########################################################################################################################

class HomePageView(TemplateView):
    """Home Page View"""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        # Extract all announcements
        context['announcements'] = HomePageAnnouncements.objects.all()

        # Extract service areas alphabetically
        context['service_areas'] = ServiceAreas.objects.all().order_by('area')

        # Pick 4 random project exhibitions
        random_exhibitions = ProjectExhibition.objects.all().order_by('?')[0:4]
        context['project_exhibitions'] = random_exhibitions

        # Extract about us text info
        about_us_text = AboutUsText.objects.first()
        context['about_us_text'] = about_us_text

        return context


# Q&A'S ################################################################################################################
########################################################################################################################

class QandAView(TemplateView):
    """Template view for the Q&A models"""
    template_name = 'pages/q&a.html'

    def get_context_data(self, **kwargs):
        context = super(QandAView, self).get_context_data(**kwargs)

        # Create a dictionary {category_name: [questions_in_category]} of each category
        # and a list of all the questions within the category and append the dictionary to the
        # topics list that is then iterated in the template to create dynamic dropdown q&a cards
        categories = QandACategory.objects.all()  # get all categories to iterate in the template
        context['topics'] = []  # Init empty list
        for category in categories:
            questions = QandA.objects.all().filter(category=category)   # filter the questions by current category
            category_dict = {category.name: questions}  # create dictionary entry
            context['topics'].append(category_dict)  # add to topics q&a list

        return context


# PRODUCTS #############################################################################################################
########################################################################################################################

class ProductsPublicListView(TemplateView):
    """Products list View"""
    template_name = 'pages/products_list_public.html'
    #template_name = 'pages/sandbox.html'

    def get_product_line_context(self):
        """Retrieves the necessary data for a dynamic display of the entire product catalog. The method returns a
        nested data structure of a list of dictionaries that store the category and product lines. Each product
        line is composed of listings stored in a dictionary by style name and list of products as shown below:

        product_catalog = [
            {
                'category':category,
                'product_lines':[
                    {
                        'style':style,
                        'products':[p1,p2,p3,pn]
                    }
                ]
            },
        ]

        This data is then extracted and iterated to be displayed in a template view
        """
        categories = ProductCategory.objects.all()  # Extract all product categories available to the public
        product_catalog = []  # init empty list for upcoming loop
        iteration_helper = 0  # init a helper flag to append data to the right list
        for category in categories:
            # save a new entry to a list in inside the products catalog
            product_catalog.append(
                {
                    'category': category,  # save category name
                    'product_lines': []  # init empty list of product lines for later use
                }
            )

            # extract a list of all styles in the current category
            product_styles = ProductStyle.objects.all().filter(category=category)

            for style in product_styles:
                # extract a list of all products in the current style
                products = Product.objects.all().filter(style=style)

                # append a dictionary to the product line list of the current product category being extracted
                product_catalog[iteration_helper]['product_lines'].append(
                    {
                        'style': style,  # save style name
                        'products': products  # save a list of the products available under this particular style
                    }
                )

            iteration_helper += 1  # index next category

        return product_catalog

    def get_context_data(self, **kwargs):
        context = super(ProductsPublicListView, self).get_context_data(**kwargs)
        context['product_catalog'] = self.get_product_line_context()
        return context


class ProductPublicDetailView(DetailView):
    """Product Public Detail View"""
    model = Product
    template_name = 'pages/product_detail_public.html'
    context_object_name = 'product'


class ProductPublicSearchResultsListView(ListView):
    """Displays the product search results for the user. Only displays products available to the public"""
    model  = Product
    template_name = 'pages/product_search_results_list_public.html'
    context_object_name = 'product_results'

    def get_context_data(self, **kwargs):
        context = super(ProductPublicSearchResultsListView, self).get_context_data(**kwargs)
        search_request = self.request.GET.get("q")
        context['q'] = search_request
        return context

    def get_queryset(self):
        search_request = self.request.GET.get("q")

        return Product.objects.filter(
            # search by product name
            Q(name__icontains=search_request)
            # search by product style
            | Q(style__name__icontains=search_request)
            # search by product category
            | Q(style__category__name_plural__icontains=search_request)
            | Q(style__category__name_singular__icontains=search_request)
            # search by product, style, and category tags
            | Q(tags__icontains=search_request)
            | Q(style__tags__icontains=search_request)
            | Q(style__category__tags__icontains=search_request)
        )


# TERMS AND CONDITIONS #################################################################################################
########################################################################################################################

class TermandConditionsView(ListView):
    model= TermandConditions
    template_name = 'pages/terms_and_conditions.html/'
    context_object_name = 'sections'


# PROJECT GALLERY ######################################################################################################
########################################################################################################################

class ProjectPublicGalleryView(TemplateView):
    template_name = 'pages/project_gallery_public.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectPublicGalleryView, self).get_context_data(**kwargs)
        context['project_exhibitions'] = ProjectExhibition.objects.all()
        return context


class ProjectPublicDetailView(DetailView):
    """Project Public Detail View"""
    model = ProjectExhibition
    template_name = 'pages/project_detail_public.html'
    context_object_name = 'project'


class ProjectPublicSearchResultsListView(ListView):
    """Displays the project search results for the user."""
    model  = ProjectExhibition
    template_name = 'pages/project_search_results_list_public.html'
    context_object_name = 'project_exhibitions'

    def get_context_data(self, **kwargs):
        context = super(ProjectPublicSearchResultsListView, self).get_context_data(**kwargs)
        search_request = self.request.GET.get("q")
        context['q'] = search_request
        return context

    def get_queryset(self):
        search_request = self.request.GET.get("q")

        return ProjectExhibition.objects.filter(
            # search by project tags
            Q(tags__icontains=search_request)
        )


# CONTACT ##############################################################################################################
########################################################################################################################

class ContactView(FormView):
    """Displays the contact page and its details"""
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = "/contact/success/"

    def form_valid(self, form):
        subject = f"{form.cleaned_data['subject']}"
        from_email = 'gustavo@cisfencing.com'
        date = datetime.now()  # Get contact request time
        message = f"""
                Contact Request

                Date: {date.strftime("%m/%d/%y %H:%M")}
                ---------------------------------------------------------
                Name: {form.cleaned_data['full_name']}
                Phone Number: {form.cleaned_data['phone_number']}
                Contact Email: {form.cleaned_data['contact_email']}
                Subject: {subject}
                ----------------------------------------------------------
                
                {form.cleaned_data['message']}

                """
        send_mail(subject, message, from_email, ['contact@cisfencing.com'], fail_silently=False)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)

        # Get all dynamic operation block objects
        context['operation_schedule'] = OperationBlocks.objects.all()

        # Determine if there are any team members
        team = CustomUser.objects.filter(~Q(type='CUSTOMER'))
        context['team_flag'] = team

        if team:
            admin_members = CustomUser.objects.filter(type='ADMINISTRATION')
            staff_members = CustomUser.objects.filter(type='STAFF')
            sales_members = CustomUser.objects.filter(type='SALES')
            construction_members = CustomUser.objects.filter(type='CONSTRUCTION')
            context['admin_members'] = admin_members
            context['staff_members'] = staff_members
            context['sales_members'] = sales_members
            context['construction_members'] = construction_members


        return context


class ContactSuccessView(TemplateView):
    """Displays the contact success page and its details"""
    template_name = 'pages/contact_success.html'

    def get_context_data(self, **kwargs):
        context = super(ContactSuccessView, self).get_context_data(**kwargs)
        return context


# REQUEST QUOTES #######################################################################################################
########################################################################################################################

class RequestEstimatesView(FormView):
    """Displays the contact page and its details"""
    template_name = 'pages/request_estimate_form.html'
    form_class = RequestEstimateForm
    success_url = "/request_estimate/success/"

    def form_valid(self, form):
        full_name = form.cleaned_data['full_name']
        from_email = 'gustavo@cisfencing.com'
        subject = f'Estimate Request - {full_name}'
        date = datetime.now()  # Get contact request time
        message = f"""
                Estimate Request

                Date: {date.strftime("%m/%d/%y %H:%M")}
                ---------------------------------------------------------
                CUSTOMER:
                    Name: {full_name}
                    Phone Number: {form.cleaned_data['phone_number']}
                    Contact Email: {form.cleaned_data['contact_email']}
                    Project Site:
                        {form.cleaned_data['street_address']},
                        {form.cleaned_data['city']}, Fl {form.cleaned_data['zip_code']}
                ----------------------------------------------------------
                DETAILS:
                    Pool Code: {form.cleaned_data['pool_code']}
                    Owner-Builder: {form.cleaned_data['owner_permit']}
                    HOA: {form.cleaned_data['hoa_flag']}
                ----------------------------------------------------------
                PROJECT DESCRIPTION:
                    {form.cleaned_data['project_description']}

                """
        send_mail(subject, message, from_email, ['contact@cisfencing.com'], fail_silently=False)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RequestEstimatesView, self).get_context_data(**kwargs)
        return context


class RequestEstimatesSuccessView(TemplateView):
    """Displays the contact success page and its details"""
    template_name = 'pages/request_estimate_form_success.html'

    def get_context_data(self, **kwargs):
        context = super(RequestEstimatesSuccessView, self).get_context_data(**kwargs)
        return context

