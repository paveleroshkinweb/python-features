from re import L
from pkg_resources import yield_lines


a = [{'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]


def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            yield item

# For unhashible type
def dedupe2(items, key=None):
    seen = set()
    for item in items:
        val = item if not key else key(item)
        if val not in seen:
            yield item
            seen.add(val)
