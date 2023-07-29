from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from jumping_minds.settings import PAGE_LIMIT # page_limit = 10

def get_paginated_results(data_list, page_number):
    try:
        paginator = Paginator(data_list, PAGE_LIMIT)

        try:
            page_obj = paginator.page(page_number)
            
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            
        page_context = {
            "page_number": page_number,
            "page_count": len(page_obj.object_list),
            "total_count": paginator.count,
            "total_number_of_pages": paginator.num_pages
        }
            
        return page_obj, page_context

    except Exception as e:
        raise e


def get_mail_body(elevator_number, current_floor):
    message = f'''This is an automated notification to inform you that the elevator in the Building is currently not working.

    Elevator Details:
    - Elevator Number: {elevator_number}
    - Current Floor: {current_floor}

    Please take immediate action to address the issue and resolve the elevator's functionality.

    Thank you for your attention to this matter.'''
    
    return message
