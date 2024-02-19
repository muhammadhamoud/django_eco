from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django_google_maps import fields as map_fields


"""
House Module
Rent Module
Login Module
Booking Module
Renter Module
Broker Module
https://www.toptal.com/django/youtube-api-integration-uploading-videos
"""

class Image(models.Model):
    pass

class Date(models.Model):
    start_date = models.DateField(
        _('Start Date'),
        help_text=_('Enter a start date.'),
    )
    start_year = models.PositiveSmallIntegerField(default=2023)

class PropertyControl(models.Model):
    property_code = models.CharField(_('Property Code'), max_length=10, unique=True, help_text=_('Enter a unique code for the property.'))
    begin_date = models.DateField(_('Begin Date'), help_text=_('Enter the date the property is scheduled to become active and start accepting reservations.'))
    end_date = models.DateField(_('End Date'), null=True, blank=True, help_text=_('Enter the date the property is no longer considered active/operational.'))
    chain_mode = models.CharField(_('Chain Mode'), max_length=50, null=True, blank=True, help_text=_('Select a chain mode from the list; if applicable. This activates chain-specific business logic and features.'))
    country_mode = models.CharField(_('Country Mode'), max_length=50, null=True, blank=True, help_text=_('Select a country mode from the list; if applicable. This activates country-specific business logic and features.'))
    currency = models.CharField(_('Currency'), max_length=3, help_text=_('Select the local (property) currency from the list.'))
    currency_format = models.CharField(_('Currency Format'), max_length=20, help_text=_('Select the currency format mask from the list.'))
    short_date_format = models.CharField(_('Short Date Format'), max_length=10, help_text=_('Select the short date format from the list.'))
    time_format = models.CharField(_('Time Format'), max_length=10, help_text=_('Select the time format mask from the list.'))
    time_zone = models.CharField(_('Time Zone'), max_length=50, help_text=_('Select the property time zone from the list; this ensures the correct time is reflected in OPERA Cloud.'))
    long_date_format = models.CharField(_('Long Date Format'), max_length=20, help_text=_('Select the long date format from the list.'))

    class Meta:
        verbose_name = _('Property Control')
        verbose_name_plural = _('Property Controls')

    def __str__(self):
        return self.hotel_code

    def get_absolute_url(self):
        return reverse_lazy('property_control_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super(PropertyControl, self).save(*args, **kwargs)

class Contact(models.Model):
    user_profile = models.ForeignKey('User', on_delete=models.CASCADE, related_name='contacts', verbose_name='User profile')
    primary = models.BooleanField(default=False, verbose_name='Primary contact')

    class Meta:
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.user_profile.username

    def save(self, *args, **kwargs):
        # Only one primary contact per user profile
        if self.primary:
            self.user_profile.contacts.exclude(pk=self.pk).update(primary=False)
        super().save(*args, **kwargs)

class ServiceRequestCode(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text=_('The Service Request code'))
    description = models.CharField(max_length=255, help_text=_('The description of the Service Request code'))
    department = models.ForeignKey('Department', on_delete=models.PROTECT, help_text=_('The department associated with this Service Request'))
    restrict_changes = models.BooleanField(default=False, help_text=_('Check to restrict changes'))

    class Meta:
        verbose_name_plural = 'Service Request Codes'

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse_lazy('service-request-code-detail', args=[str(self.id)])

class ServiceRequestPriority(models.Model):
    code = models.CharField(
        verbose_name=_('Service Request code'),
        max_length=50,
        help_text=_('Enter the Service Request code.')
    )
    description = models.CharField(
        verbose_name=_('Description'),
        max_length=100,
        help_text=_('Enter the description of the Service Request Priority.')
    )
    translation = models.TextField(
        verbose_name=_('Manage Translation'),
        null=True,
        blank=True,
        help_text=_('Open the multi-language descriptions screen and configure a translated menu name for each language.')
    )
    sequence = models.IntegerField(
        verbose_name=_('Sequence'),
        default=0,
        help_text=_('Enter a display sequence.')
    )

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('service-request-priority-detail', args=[str(self.id)])

class GuestType(models.Model):
    pass

class ReservationType(models.Model):
    pass

class ReservationOrginCodes(models.Model):
    pass

class DateRange(models.Model):
    start_date = models.DateField(
        _('Start Date'),
        help_text=_('Enter a start date.'),
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        _('End Date'),
        help_text=_('Enter an end date.'),
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse_lazy('date_range_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"

    class Meta:
        verbose_name = _('Date Range')
        verbose_name_plural = _('Date Ranges')


class PropertyAddress(models.Model):
    country = models.CharField(_("Country"), max_length=100, blank=True, null=True, help_text=_("Select a country from the list."))
    # address = models.CharField(_("Address"), max_length=255, blank=True, null=True, help_text=_("Enter the street address."))
    city = models.CharField(_("City"), max_length=100, blank=True, null=True, help_text=_("Enter the city (suburb)."))
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True, null=True, help_text=_("Enter the post code."))
    region = models.CharField(_("Region"), max_length=100, blank=True, null=True, help_text=_("Select a region from the list."))
    state = models.CharField(_("State"), max_length=100, blank=True, null=True, help_text=_("Select a state from the list."))
    
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True, help_text=_("Enter primary phone number for the property."))
    toll_free = models.CharField(_("Toll Free"), max_length=20, blank=True, null=True, help_text=_("Enter toll-free phone number for the property."))
    fax = models.CharField(_("Fax"), max_length=20, blank=True, null=True, help_text=_("Enter fax number for the property."))
    email = models.EmailField(_("Email"), max_length=255, blank=True, null=True, help_text=_("Enter the email address of the property (eg GM email address)."))
    web = models.URLField(_("Web"), max_length=255, blank=True, null=True, help_text=_("Enter the website URL for the property."))
    
    address = map_fields.AddressField(_("Address"), max_length=255, blank=True, null=True, help_text=_("Enter the street address."))
    geolocation = map_fields.GeoLocationField(_("Geo Location"), max_length=255, blank=True, null=True, help_text=_("Enter the Geo Location."))

    # is_international = 

    class Meta:
        verbose_name = _("Property Address")
        verbose_name_plural = _("Property Addresses")
    
    def __str__(self):
        return self.address
    
    def get_absolute_url(self):
        return reverse_lazy('property_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        # custom save logic here
        super().save(*args, **kwargs)

class PropertyCategory(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text=_("Enter a code for the Hotel Category."))
    description = models.CharField(max_length=50, help_text=_("Enter a description for the Hotel Category."))
    translations = models.JSONField(blank=True, null=True, help_text=_("Enter translated descriptions for each language."))
    sequence = models.PositiveIntegerField(help_text=_("Enter a display sequence."))

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('hotelcategory_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Hotel Categories")
        ordering = ['sequence']

class PropertyType(models.Model):
    """
    A model representing a property type.
    Fields:
    - code: a code for the property type
    - description: a description for the property type
    - sequence: a display sequence
    """
    code = models.CharField(
        max_length=30,
        help_text=_('Enter a code for the property type.'),
        verbose_name=_('Code'),
        primary_key=True
    )
    description = models.CharField(
        max_length=100,
        help_text=_('Enter a description for the property type.'),
        verbose_name=_('Description')
    )
    sequence = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_('Enter a display sequence.'),
        verbose_name=_('Sequence')
    )

    class Meta:
        verbose_name = _('property type')
        verbose_name_plural = _('property types')

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('property_type_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        # Force the name, city values to title case
        self.description = str(self.description).title()
        self.code = str(self.code).title()
   
        # Call the original save method
        super(PropertyType, self).save(*args, **kwargs)

class RoomType(models.Model):
    pass

class RoomClass(models.Model):
    pass

class RoomPool(models.Model):
    pass

class Bathrooms(models.Model):
    pass

class PropertyFeatures(models.Model):
    pass

class Furnishing(models.Model):
    pass

class Parking(models.Model):
    pass

class CommunicationMethod(models.Model):
    """Call, SMS, Email or Whatsapp"""
    code = models.CharField(
        _('code'),
        max_length=10,
        help_text=_('The code of the communication method.')
    )
    description = models.CharField(
        _('description'),
        max_length=100,
        help_text=_('The description of the communication method.')
    )
    sequence = models.IntegerField(
        _('sequence'),
        default=0,
        blank=True,
        null=True,
        help_text=_('The display sequence of the communication method.')
    )

    class Meta:
        verbose_name = _('communication method')
        verbose_name_plural = _('communication methods')

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('communication_method_detail', args=[str(self.id)])

    def get_edit_url(self):
        return reverse_lazy('communication_method_edit', args=[str(self.id)])

class NoteType(models.Model):
    """
    Represents a type of note that can be added to a group of related notes.

    """
    notes_group = models.ForeignKey(
        'NotesGroup',
        on_delete=models.CASCADE,
        help_text=_('Select the note group to which this note type belongs.'),
    )
    code = models.CharField(
        max_length=255,
        help_text=_("Enter a code for this note type. Note: note type codes cannot contain ampersands (&)."),
    )
    description = models.CharField(
        max_length=255,
        help_text=_('Enter a description for this note type.'),
    )
    display_seq = models.IntegerField(
        blank=True,
        null=True,
        help_text=_('Enter a number to control the position of the note type in the list. If left blank, notes will appear in alphabetical order.'),
    )
    is_internal = models.BooleanField(
        default=False,
        help_text=_('Designate notes of this type as internal by default when they are created. Notes marked as "internal" will not be included in the OXI or OXI-HUB message to integrated systems.'),
    )
    can_override_internal = models.BooleanField(
        default=False,
        help_text=_('Allow the user creating a note of this type to choose whether to make the note internal or not.'),
    )
    is_default = models.BooleanField(
        default=False,
        help_text=_('Specify this note type as the default for its group.'),
    )
    default_note_text = models.TextField(
        blank=True,
        null=True,
        help_text=_('Create a default note that will display when the current Note Type and the Notes option is selected in OPERA Cloud. Users can modify this note when Notes are called from within the application.'),
    )

    class Meta:
        verbose_name = _('note type')
        verbose_name_plural = _('note types')

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('note_type_detail', args=[str(self.id)])

    def get_edit_url(self):
        return reverse_lazy('note_type_edit', args=[str(self.id)])

    # def save(self, *args, **kwargs):
    #     # If this note type is set as default, un-set all other default note types for its group

class PropertyDetailCategory(models.Model):
    """
    Model representing a property detail category.
    """
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text=_("Enter a code for the Property Detail Category.")
    )
    description = models.CharField(
        max_length=255,
        help_text=_("Enter a description for the Property Detail Category.")
    )
    sequence = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        help_text=_("Enter a display sequence.")
    )

    # Translation fields

    class Meta:
        verbose_name = _("property detail category")
        verbose_name_plural = _("property detail categories")

    def __str__(self):
        """
        String representation of the Property Detail Category object.
        """
        return self.description

    def get_absolute_url(self):
        """
        Returns the URL to access a detail record for this Property Detail
        """
        return reverse_lazy('property_detail_category_detail', args=[str(self.id)])

class PropertyDetail(models.Model):
    """
    Model representing a property detail.
    """
    code = models.CharField(
        max_length=10,
        help_text=_('Enter a code for the Property Detail.'),
    )
    category = models.ForeignKey(
        PropertyDetailCategory,
        on_delete=models.CASCADE,
        help_text=_('Select the Property Detail Category from the list.'),
    )
    sequence = models.IntegerField(
        blank=True, null=True,
        help_text=_('Enter a display sequence.'),
    )

    class Meta:
        verbose_name_plural = _('Property Details')

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse_lazy('property_detail_detail', args=[str(self.id)])

class PropertyDetailValue(models.Model):
    """
    Model representing a value of a property detail.
    """
    code = models.CharField(
        max_length=10,
        help_text=_('Enter a code for the Property Detail Value.'),
    )
    description = models.CharField(
        max_length=100,
        help_text=_('Enter a description for the Property Detail Value.'),
    )
    sequence = models.IntegerField(
        blank=True, null=True,
        help_text=_('Enter a display sequence.'),
    )
    property_detail = models.ForeignKey(
        PropertyDetail,
        on_delete=models.CASCADE,
        help_text=_('Select the Property Detail from the list.'),
    )

    class Meta:
        verbose_name_plural = _('Property Detail Values')

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse_lazy('property_detail_value_detail', args=[str(self.id)])

class BusinessUnit(models.Model):
    """
    Model representing a business unit.
    """
    code = models.CharField(
        max_length=10,
        verbose_name=_("Code"),
        help_text=_("Enter a code for the Business Unit.")
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
        help_text=_("Enter a description for the Business Unit.")
    )
    translations = models.TextField(
        verbose_name=_("Translations"),
        help_text=_("Add translated descriptions for each language.")
    )
    sequence = models.PositiveIntegerField(
        verbose_name=_("Sequence"),
        help_text=_("Enter a display sequence.")
    )
    
    def __str__(self):
        return self.description
    
    def get_absolute_url(self):
        return reverse_lazy('business_unit_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name_plural = _("Business Units")
        ordering = ['sequence']

class OperatingUnit(models.Model):
    """
    Model representing an operating unit.
    """

    code = models.CharField(
        max_length=10,
        unique=True,
        help_text=_("Enter a code for the operating unit.")
    )
    description = models.CharField(
        max_length=50,
        help_text=_("Enter a description for the operating unit.")
    )
    sequence = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Enter a display sequence for the operating unit.")
    )

    class Meta:
        verbose_name = _("Operating Unit")
        verbose_name_plural = _("Operating Units")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('operatingunit-detail', args=[str(self.id)])

class Property(models.Model):
    """
    A model representing a property.
    """
    code = models.CharField(
        _("Property Name"),
        max_length=100,
        help_text=_("Enter the property code / should be unique."),
        unique=True,
        primary_key=True,
    )
    name = models.CharField(
        _("Property Name"),
        max_length=100,
        help_text=_("Enter the property name."),
        null=True,
        blank=True,
    )
    legal_owner = models.CharField(
        _("Legal Owner"),
        max_length=100,
        help_text=_("Enter the legal owner / company name."),
        null=True,
        blank=True,
    )
    # PROPERTY_TYPES = (
    #     ("hotel", _("Hotel")),
    #     ("resort", _("Resort")),
    #     ("motel", _("Motel")),
    #     ("guest_house", _("Guest House")),
    # )
    # property_type = models.OneToOneField(PropertyType,
    #     _("Property Type"),
    #     max_length=20,
    #     # choices=PROPERTY_TYPES,
    #     help_text=_("Select a property type from the list."),
    #     # null=True,
    #     # blank=True,
    #     on_delete=models.CASCADE
    # )
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='property')

    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    sqmeter = models.PositiveIntegerField()
    sqft = models.PositiveIntegerField()
    garage_spaces = models.PositiveIntegerField(default=0)
    built_year = models.PositiveIntegerField()

    swimming_pool = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)

    # Renting-specific fields
    is_for_rent = models.BooleanField(default=False)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available_for_rent = models.DateField(blank=True, null=True)

    # Selling-specific fields
    is_for_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available_for_sale = models.DateField(blank=True, null=True)


    number_of_floors = models.PositiveIntegerField(
        _("Number of Floors"),
        help_text=_("Enter the number of floors."),
        null=True,
        blank=True,
    )
    total_rooms = models.PositiveIntegerField(
        _("Total Rooms"),
        help_text=_("Enter the total number of accommodation rooms."),
        null=True,
        blank=True,
    )
    number_of_beds = models.PositiveIntegerField(
        _("Number of Beds"),
        help_text=_("Enter the number of beds."),
        null=True,
        blank=True,
    )
    property_information_url = models.URLField(
        _("Property Information URL"),
        help_text=_("Enter a URL of website with further property details."),
        null=True,
        blank=True,
    )
    check_out_time = models.TimeField(
        _("Check out Time"),
        help_text=_("Enter the default check out time."),
        null=True,
        blank=True,
    )
    check_in_time = models.TimeField(
        _("Check in Time"),
        help_text=_("Enter the default check in time."),
        null=True,
        blank=True,
    )
    latitude = models.FloatField(
        _("Latitude"),
        help_text=_("Enter the location of the property (available via Google Maps)."),
        null=True,
        blank=True,
    )
    longitude = models.FloatField(
        _("Longitude"),
        help_text=_("Enter the location of the property (available via Google Maps)."),
        null=True,
        blank=True,
    )
    base_language = models.CharField(
        _("Base Language"),
        max_length=20,
        help_text=_("Enter the primary configuration language of the property."),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def __str__(self):
        return F"{str(self.code)}-{str(self.name)}"

    def get_absolute_url(self):
        return reverse_lazy("property_detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Force the name, city values to title case
        self.name = str(self.name).title()
        self.code = str(self.code).upper()
        
        # from django.core.exceptions import ValidationError
        
        # # Check if the value of my_field is unique
        # if Property.objects.filter(code=self.code).exists():
        #     raise ValidationError(f'The value of {self.code} must be unique')

        # Call the original save method
        super(Property, self).save(*args, **kwargs)

class MarketCodes(models.Model):
    pass

class SubMarketCodes(models.Model):
    pass

class BusinessSegment(models.Model):
    pass

class SourceCodes(models.Model):
    pass

class SourceGroups(models.Model):
    pass

class AttractionCategory(models.Model):
    code = models.CharField(
        max_length=10,
        help_text=_("Enter an attraction category code."),
    )
    description = models.CharField(
        max_length=255,
        help_text=_("Enter the description for the attraction category."),
    )
    sequence = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Enter a display sequence."),
    )

    class Meta:
        verbose_name = _("attraction category")
        verbose_name_plural = _("attraction categories")

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy("attraction_category_detail", args=[str(self.id)])

class Attraction(models.Model):
    code = models.CharField(max_length=10, verbose_name=_('code'))
    description = models.CharField(max_length=255, verbose_name=_('description'))
    category = models.ForeignKey(AttractionCategory, on_delete=models.CASCADE, verbose_name=_('category'))
    city = models.CharField(max_length=50, verbose_name=_('city'))
    state = models.CharField(max_length=50, verbose_name=_('state'))
    website = models.URLField(max_length=255, verbose_name=_('website'))
    distance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('distance'))
    distance_type = models.CharField(max_length=10, verbose_name=_('distance type'))
    driving_time = models.CharField(max_length=50, verbose_name=_('driving time'))
    price_range = models.CharField(max_length=50, verbose_name=_('price range'))
    hours = models.CharField(max_length=100, verbose_name=_('hours'))
    sequence = models.IntegerField(verbose_name=_('sequence'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_('latitude'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_('longitude'))
    general_directions = models.TextField(blank=True, verbose_name=_('general directions'))

    def __str__(self):
        return self.code + ' - ' + self.description

    def get_absolute_url(self):
        return reverse_lazy('attraction_detail', args=[str(self.id)])

    class Meta:
        verbose_name = _('attraction')
        verbose_name_plural = _('attractions')
        ordering = ('sequence',)

class PropertyViews(models.Model):
    pass

class LastUpdate(models.Model):
    pass

class RentPricing(models.Model):
    property = models.OneToOneField('Property', on_delete=models.CASCADE, related_name='rent_pricing')
    is_for_rent = models.BooleanField(default=False)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available_for_rent = models.DateField(blank=True, null=True)

class SalePricing(models.Model):
    property = models.OneToOneField('Property', on_delete=models.CASCADE, related_name='sale_pricing')
    is_for_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available_for_sale = models.DateField(blank=True, null=True)

class OwnerTeam(models.Model):
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text=_("Enter a code for the team."),
    )
    description = models.CharField(
        max_length=255,
        help_text=_("Enter a description for the owner team."),
    )
    translations = models.JSONField(
        blank=True,
        null=True,
        help_text=_("Select to open the multi-language descriptions screen and configure a translated menu name for each language."),
    )
    sequence = models.PositiveIntegerField(
        default=0,
        help_text=_("Enter a display sequence."),
    )

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('owner-team-detail', args=[str(self.id)])

    class Meta:
        verbose_name = _("Owner Team")
        verbose_name_plural = _("Owner Teams")
        ordering = ['sequence', 'description']

class Favorate():
    pass

class PaymentType():
    # banks list خدمات التمويل
    # خدمات عقارية
    pass

class PropertyConditions():
    pass

class Listing(models.Model):
    # realtor = models.ForeignKey(Realtor,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    address = models.CharField(max_length=255)

    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    
    price = models.IntegerField()


    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5,decimal_places=1)

    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)

    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.title
    





    