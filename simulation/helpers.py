import re


# https://github.com/django/django/blob/92053acbb9160862c3e743a99ed8ccff8d4f8fd6/django/utils/text.py#L417
def slugify(value):
    value = re.sub('[^\w\s-]', '', value).strip().lower().replace('-', '_')
    return re.sub('[-\s]+', '_', value)
