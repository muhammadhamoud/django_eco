from django.contrib import admin

from .models import *

# Get all the models defined in your models.py
models_to_register = [
    # RateSegment,
    # RateSegmentGroup,
    # RateCategory,
    RateAmounts,
    RateCode,
    # RateCodeCluster,
    RateMirror,
    RateRestriction,
    RateSeason,
    # RatePool,
    # RateType,
    # RateOffer,
    RateRuleType,
    RateAvailabilityRule,
    DayOfTheWeek,

]

# Register each model with the admin site
for model in models_to_register:
    admin.site.register(model)

