from django.db import models

from modelcluster.fields import ParentalKey

from django.contrib import messages

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.models import Image
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from blog.models import BlogPage

from .email import send_form_email
from .forms import ContactForm


class HomePage(Page):
    body = RichTextField(blank=True)
    footer_copyright = models.CharField(blank="true", max_length=255)

    # splash_image = models.ForeignKey(
    #     'wagtailimages.Image',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+'
    # )
    # splash_image_caption = models.CharField(blank=True, max_length=250)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        # MultiFieldPanel([
        #     ImageChooserPanel('splash_image'),
        #     FieldPanel('splash_image_caption'),
        # ], 
        #     heading="Splash image"        
        MultiFieldPanel([
            FieldPanel('footer_copyright')  
        ], 
            heading="Footer"        
        ),
        InlinePanel('slider_items', label="Slider"),
        InlinePanel('partner_items', label="Partners"),
        
    ]

    def get_context(self, request, **kwargs):
        context = super(HomePage, self).get_context(request)

        contact = Contact.objects.live()[:1].get()
        context['contact'] = contact

        offers = OfferCategoryPage.objects.live()
        context['offers'] = offers

        career = CareerPage.objects.live()[:6]
        # career = career
        context['career'] = career

        projects = BlogPage.objects.live()
        projects = projects.order_by('-date')[:3]
        context['projects'] = projects
        return context

class Partners(Orderable):
    page = ParentalKey('HomePage', related_name='partner_items', null=True)
    title = models.CharField(max_length=255, verbose_name="Tytuł")
    image = models.ForeignKey(
        'wagtailimages.Image',
        related_name='+',
        verbose_name="Obrazek",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    link = models.TextField(null=True, blank=True, verbose_name="Link zewnętrzny")
    panels = [
        FieldPanel('title', classname="full"),
        ImageChooserPanel('image'),
        FieldPanel('link', classname="full"),
    ]

class SliderItem(Orderable):
    page = ParentalKey('HomePage', related_name='slider_items', null=True)
    title = models.CharField(max_length=255, verbose_name="Tytuł")
    description = RichTextField(verbose_name="Opis")
    link = models.TextField(null=True, blank=True, verbose_name="Link zewnętrzny")
    related_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        related_name='+',
        verbose_name="Obrazek",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel('title', classname="full"),
        FieldPanel('description', classname="full"),
        FieldPanel('link', classname="full"),
        PageChooserPanel('related_page'),
        ImageChooserPanel('image'),
        DocumentChooserPanel('file'),
    ]

class Policy(Page):
    body = RichTextField(verbose_name="Polityka prywatności")

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

class Contact(Page):
    email = models.EmailField(default="rim.kozlowski@gmail.com", verbose_name="Email hosta")
    # subtitle = models.TextField(verbose_name="Podtytuł")
    # title_main = models.TextField(verbose_name="Tytuł")
    # description = RichTextField(verbose_name="Opis")
    # subtitle_contact = models.TextField(verbose_name="Podtytuł")
    # title_contact = models.TextField(verbose_name="Tytuł")
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    content_panels = Page.content_panels + [
    #     # FieldPanel('email'),

        MultiFieldPanel([
            FieldPanel('lat'),
            FieldPanel('lng'),
            # FieldPanel('subtitle'),
            # FieldPanel('title_main'),
    #     #     FieldPanel('description'),

        ],
    #     #     heading="Informacje główne",
    #     #     classname="collapsible collapsed"
        ),

    #     # MultiFieldPanel([
    #     #     FieldPanel('subtitle_contact'),
    #     #     FieldPanel('title_contact'),
    #     #     InlinePanel('management_persons', label='Członek zarządu'),
    #     #     InlinePanel('project_management_persons', label='Członek project management'),
    #     #     InlinePanel('sales_department_persons', label='Członek działu handlowego'),
    #     #     InlinePanel('purchasing_department_persons', label='Członek działu zakupów'),

    #     # ],
    #     #     heading="Kadra",
    #     #     classname="collapsible collapsed"
    #     # ),

    ]

    def get_context(self, request, **kwargs):
        context = super(Contact, self).get_context(request)
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                send_form_email('Formularz kontaktowy ze strony', 'x', form, self.email)
                messages.info(request, 'Formularz został wysłany.')
            else:
                messages.error(request, 'Formularz zawiera błędy.')
        else:
            form = ContactForm()
        context['form'] = form
        return context

# CAREER

class CareerIndexPage(Page):
    intro = RichTextField(verbose_name="intro dla indeksu karier", blank=True)
    intro_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('intro_image')
    ]

    def get_context(self, request):
        # Update context to include only published careers
        context = super().get_context(request)
        careerPages = self.get_children().live()
        context['careerpages'] = careerPages
        return context
    
    # Parent page / subpage type rules

    subpage_types = [
        'home.CareerPage'
    ]

class CareerPage(Page):
    # title = models.CharField(max_length=255, verbose_name="Stanowisko")
    description = RichTextField(verbose_name="Opis stanowiska", blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            # FieldPanel('title'),
            FieldPanel('description')  
        ], heading="Kariera"
        )
    ]

# class CareerItem(Orderable):
#     page = ParentalKey('CareerPage', related_name="career_items", null=True)
#     title = models.CharField(max_length=255, verbose_name="Stanowisko")
#     description = RichTextField(verbose_name="Opis stanowiska")

#     panels = [
#         FieldPanel('title'),
#         FieldPanel('description')
#     ]


class OfferIndexPage(Page):
    # intro = RichTextField(blank=True)

    # content_panels = Page.content_panels + [
    #     FieldPanel('intro', classname="full")
    # ]

    def get_context(self, request):
        # Update context to include only published offers
        context = super().get_context(request)
        offersubindexes = self.get_children().live()
        context['offersubindexes'] = offersubindexes
        return context

class OfferCategoryPage(Page):
    intro = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    def get_context(self, request):
        # Update context to include only published offers
        context = super().get_context(request)
        offerPages = self.get_children().live()
        context['offerpages'] = offerPages
        return context

class OfferSubCategoryPage(Page):
    def get_context(self, request):
        # Update context to include only published offers
        context = super().get_context(request)
        offerPages = self.get_children().live()
        context['offerpages'] = offerPages
        return context

class OfferPage(Page):
#     # date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True)
#     intro_image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
    body = RichTextField(blank=True)

#     search_fields = Page.search_fields + [
#         index.SearchField('intro'),
#         index.SearchField('body'),
#     ]

    content_panels = Page.content_panels + [
        # FieldPanel('date'),
        FieldPanel('intro'),
        # ImageChooserPanel('intro_image'),
        FieldPanel('body', classname="full"),
        # InlinePanel('gallery_images', label="Gallery images"),
    ]

#     def main_image(self):
#         print(self.introImage)
#         return self.introImage
#         # print(self.gallery_images)
#         # gallery_item = self.gallery_images.first()
#         # if gallery_item:
#         #     return gallery_item.image
#         # else:
#         #     return None
    