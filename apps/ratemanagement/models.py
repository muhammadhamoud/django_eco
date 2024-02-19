from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Define choices for the days of the week
DAY_CHOICES = [
    ('Sun', _('Sunday')),
    ('Mon', _('Monday')),
    ('Tue', _('Tuesday')),
    ('Wed', _('Wednesday')),
    ('Thu', _('Thursday')),
    ('Fri', _('Friday')),
    ('Sat', _('Saturday')),
]

class DayOfTheWeek(models.Model):

    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES, verbose_name=_("Day of Week"), unique=True)
    
    def day_number(self):
        # Calculate the day number based on the index of the chosen day name in DAY_CHOICES
        return (self.DAY_CHOICES.index((self.day_of_week, self.get_day_of_week_display())) + 1)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.get_day_of_week_display()

    class Meta:
        verbose_name = _("Day of the Week")
        verbose_name_plural = _("Days of the Week")

class RatePool(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Rate Pool Code"))
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Rate Pool Name"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse_lazy('ratepool_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Rate Pool")
        verbose_name_plural = _("Rate Pools")
        ordering = ['name']

class RateType(models.Model):
    RATE_TYPE_CHOICES = [
        ('System Generated', _('System Generated')),
        ('Weekend', _('Weekend')),
        ('Weekday', _('Weekday')),
        ('Seven Day', _('Seven Day')),
    ]
    rate_type = models.CharField(max_length=20, choices=RATE_TYPE_CHOICES, verbose_name=_("Rate Type"), unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.rate_type

    class Meta:
        verbose_name = _("Rate Type")
        verbose_name_plural = _("Rate Types")

class RateSegment(models.Model):
    code = models.CharField(max_length=3, unique=True, help_text=_("Enter a code for the Hotel Category."))
    description = models.CharField(max_length=50, help_text=_("Enter a description for the Hotel Category."))
    sequence = models.PositiveIntegerField(help_text=_("Enter a display sequence."))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('rate_segment_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.description = str(self.description).title()
        self.code = str(self.code).upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Rate Segments")
        ordering = ['sequence']

class RateSegmentGroup(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text=_("Enter a code for the Hotel Category."))
    description = models.CharField(max_length=50, help_text=_("Enter a description for the Hotel Category."))
    sequence = models.PositiveIntegerField(help_text=_("Enter a display sequence."))
    segment = models.ManyToManyField(RateSegment, related_name='rate_segment')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('rate_segment_group_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.description = str(self.description).title()
        self.code = str(self.code).upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Rate Segment Groups")
        ordering = ['sequence']

class RateCategory(models.Model):
    code = models.CharField(max_length=3, unique=True, help_text=_("Enter a code for the Rate Category."))
    description = models.CharField(max_length=50, help_text=_("Enter a description for the Rate Category."))
    # Add other fields as needed
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse_lazy('rate_category_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.description = str(self.description).title()
        self.code = str(self.code).upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Rate Categories")
        ordering = ['code']

class RateCode(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Rate Code"))
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Rate Code Name"))
    
    # Add relationships to other models
    rate_pool = models.ForeignKey(RatePool, on_delete=models.CASCADE, verbose_name=_("Rate Pool"))
    rate_type = models.ForeignKey(RateType, on_delete=models.CASCADE, verbose_name=_("Rate Type"))
    rate_segment = models.ForeignKey(RateSegment, on_delete=models.CASCADE, verbose_name=_("Rate Segment"))
    rate_category = models.ForeignKey(RateCategory, on_delete=models.CASCADE, verbose_name=_("Rate Category"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('rate_code_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.name = str(self.name).title()
        self.code = str(self.code).upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Rate Code")
        verbose_name_plural = _("Rate Codes")
        ordering = ['name']

class RateCodeCluster(models.Model):
    code = models.CharField(max_length=3, unique=True, verbose_name=_("Cluster Code"))
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Cluster Name"))
    rate_codes = models.ManyToManyField(RateCode, related_name='clusters', verbose_name=_("Rate Codes"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('rate_code_cluster_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.description = str(self.description).title()
        self.code = str(self.code).upper()
        super().save(*args, **kwargs)



    class Meta:
        verbose_name = _("Rate Code Cluster")
        verbose_name_plural = _("Rate Code Clusters")
        ordering = ['name']

class RateOffer(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Offer Name"))
    rate_codes = models.ManyToManyField(RateCode, related_name='offers', verbose_name=_("Rate Codes"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('rate_offer_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.name = str(self.name).title()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Rate Offer")
        verbose_name_plural = _("Rate Offers")
        ordering = ['name']

class RateRestriction(models.Model):
    code = models.CharField(max_length=3, unique=True, help_text=_("Enter a code for the Rate Restriction."))
    description = models.CharField(max_length=50, help_text=_("Enter a description for the Rate Restriction."))
    minimum_stay = models.PositiveIntegerField(default=1, verbose_name=_("Minimum Stay"))
    maximum_stay = models.PositiveIntegerField(default=365, verbose_name=_("Maximum Stay"))
    book_in_advance = models.PositiveIntegerField(default=0, verbose_name=_("Book in Advance (Days)"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Rate Restriction for {self.code}"

    class Meta:
        verbose_name = _("Rate Restriction")
        verbose_name_plural = _("Rate Restrictions")

class RateSeason(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Season Name"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Rate Season")
        verbose_name_plural = _("Rate Seasons")

class RateMirror(models.Model):
    original_rate = models.ForeignKey(RateCode, on_delete=models.CASCADE, related_name='original_rate_mirror')
    mirrored_rate = models.ForeignKey(RateCode, on_delete=models.CASCADE, related_name='mirrored_rate_mirror')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.original_rate} Mirrors {self.mirrored_rate}"

    class Meta:
        verbose_name = _("Rate Mirror")
        verbose_name_plural = _("Rate Mirrors")

class RateOfferProduct(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Rate Offer Product Code"))
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Rate Offer Product Name"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Rate Offer Product")
        verbose_name_plural = _("Rate Offer Products")

class RateRuleType(models.Model):
    RATE_RULE_TYPE_CHOICES = [
        ('None Defined', _('None Defined')),
        ('Fixed', _('Fixed')),
        ('Percentage Above', _('Percentage Above')),
        ('Percentage Below', _('Percentage Below')),
        ('Amount Above', _('Amount Above')),
        ('Amount Below', _('Amount Below')),
        ('Equal', _('Equal')),
    ]
    rate_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Rate Amount"))
    rate_amount_calculated = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Rate Amount Calculcated"))
    rate_type = models.CharField(max_length=20, choices=RATE_RULE_TYPE_CHOICES, verbose_name=_("Rate Rule Choice"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.rate_type

    class Meta:
        verbose_name = _("Rate Rule Type")
        verbose_name_plural = _("Rate Rule Types")


# forms.py
# from django.forms.widgets import SelectMultiple

# class MultiSelectWidget(SelectMultiple):
#     def value_from_datadict(self, data, files, name):
#         return data.getlist(name)


# class RateAvailabilityRules(models.Model):
#     days_of_week = models.ManyToManyField(DayOfTheWeek, verbose_name=_("Day of the Week"), blank=True)
#     request_arrival_day = models.ManyToManyField(DayOfTheWeek, verbose_name=_("Request Arrival Day"), blank=True)
#     request_stayover_day = models.ManyToManyField(DayOfTheWeek, verbose_name=_("Request Stayover Day"), blank=True)
#     length_of_stay_required = models.PositiveIntegerField(default=0, verbose_name=_("Length of Stay Required"))
#     advance_booking_required = models.PositiveIntegerField(default=0, verbose_name=_("Advance Booking Required"))
#     blackout_dates = models.BooleanField(default=False, verbose_name=_("Blackout Dates"))
    # created = models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return ", ".join([day.get_day_name_display() for day in self.days_of_week.all()])

#     class Meta:
#         verbose_name = _("Rate Availability Rule")
#         verbose_name_plural = _("Rate Availability Rules")


class RateAvailabilityRule(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Rate Availability Rule Name"))
    days_of_week = models.ManyToManyField(DayOfTheWeek, verbose_name=_("Day of the Week"), blank=True, related_name='days_of_week')
    request_arrival_day = models.ManyToManyField(DayOfTheWeek, verbose_name=_("Request Arrival Day"), blank=True, related_name='request_arrival_day')
    request_stayover_day = models.ManyToManyField(DayOfTheWeek, verbose_name=_("Request Stayover Day"), blank=True, related_name='request_stayover_day')
    length_of_stay_required = models.PositiveIntegerField(default=0, verbose_name=_("Length of Stay Required"))
    advance_booking_required = models.PositiveIntegerField(default=0, verbose_name=_("Advance Booking Required"))
    blackout_dates = models.BooleanField(default=False, verbose_name=_("Blackout Dates"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Rate Availability Rule")
        verbose_name_plural = _("Rate Availability Rules")

    @property
    def available_days(self):
        return self.days_of_week.split(',') if self.days_of_week else []

    @available_days.setter
    def available_days(self, value):
        self.days_of_week = ','.join(value)
    
    @staticmethod
    def available_days_choices():
        return DAY_CHOICES

class RateAmounts(models.Model):
    rate_code = models.ForeignKey(RateCode, on_delete=models.CASCADE, verbose_name=_("Rate Code"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    rate_gross = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Rate Gross"))
    rate_net = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Rate Net"))
    rate_rule_type = models.ForeignKey(RateRuleType, on_delete=models.SET_NULL, verbose_name=_("Rate Rule Type"), blank=True, null=True)
    availability_rule = models.ForeignKey(RateAvailabilityRule, on_delete=models.CASCADE, verbose_name=_("Availability Rule"), blank=True, null=True)
    mirror_rate_code = models.ForeignKey(RateCode, on_delete=models.SET_NULL, related_name='mirrored_rates', verbose_name=_("Mirror Rate Code"), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rate_code} - {self.start_date} to {self.end_date}"

    def get_absolute_url(self):
        return reverse_lazy('rate_amount_detail', args=[str(self.id)])

    # def calculate_rate_net(self):
    #     if self.rate_rule_type:
    #         if self.rate_rule_type.rate_type == 'Fixed':
    #             # Implement the logic for 'Fixed' rate type
    #             # For example, you can directly set rate_net to a fixed value.
    #             self.rate_net = 10.0  # Replace with your fixed value
    #         elif self.rate_rule_type.rate_type == 'Percentage Above':
    #             # Implement the logic for 'Percentage Above' rate type
    #             # For example, you can calculate rate_net based on a percentage of rate_gross.
    #             self.rate_net = self.rate_gross * 1.1  # 110% of rate_gross
    #         # Add more conditions for other rate types as needed
    #     else:
    #         # Handle the case where rate_rule_type is not defined
    #         self.rate_net = 0.0  # Set a default value or handle it as per your requirement

    # def save(self, *args, **kwargs):
    #     self.calculate_rate_net()
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Rate Amount")
        verbose_name_plural = _("Rate Amounts")

