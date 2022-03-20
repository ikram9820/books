from django.core.exceptions import ValidationError

def validate_pdf_size(pdf):
    max_size_mb = 100
    mb=1024*1024

    if pdf.size >max_size_mb * mb:
        raise ValidationError(f"pdf cann't be larger than {max_size_mb} MB!")
