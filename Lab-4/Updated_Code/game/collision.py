"""
collision: figures out whether a falling object is within the basket.
"""

def is_caught(basket_rect, obj):
    horizontal_overlap = (
        obj.x + obj.radius >= basket_rect.left
        and obj.x - obj.radius <= basket_rect.right
    )

    vertical_overlap = (
        obj.y + obj.radius >= basket_rect.top
        and obj.y - obj.radius <= basket_rect.bottom
    )

    return horizontal_overlap and vertical_overlap
