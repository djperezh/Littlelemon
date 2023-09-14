from django.forms import ModelForm, DateInput, ChoiceField, Select, MultipleChoiceField
from .models import Booking

CHOICES = [
    ("1", "10am"),
    ("2", "11am"),
    ("3", "12pm"),
    ("4", "1pm"),
    ("5", "2pm"),
    ("6", "3pm"),
    ("7", "4pm"),
    ("8", "5pm"),
    ("9", "6pm"),
    ("10", "7pm"),
    ("11", "8pm")
]

# CHOICES = ["10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm","8pm"]

class BookingForm(ModelForm):
    # time = Select(attrs={"required": "required", "choices": ["10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm","8pm"]})
    time = ChoiceField(choices=CHOICES)
    date = DateInput(attrs={
        'type': 'date',
        'placeholder': 'yyyy-mm-dd',
        'class': 'form-control',
        'required': 'required',
        "onClick": "dateListener();"
    })
    
    # date = DateInput()
    
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            "date": DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "yyyy-mm-dd",
                    "class": "form-control",
                    "required": "required"
                }
            ),
            # "time": ChoiceField(choices=CHOICES)
            # "time": Select(
            #     attrs={
            #         "required": "required",
            #         "choices": ["10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm","8pm"]
            #     }
            # )
        }

class ReservationsForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"