from utils.exceptions import BadRequestException

def get_pagination_params(args):
    try:
        page = int(args.get("Page", 1))
        page_size = int(args.get("PageSize", 10))
    except ValueError:
        raise BadRequestException("Page and PageSize must be numbers")

    if page < 1:
        raise BadRequestException("Page must be >= 1")

    if page_size < 1 or page_size > 100:
        raise BadRequestException("PageSize must be between 1 and 100")

    return page, page_size


def paginate_query(query, page, page_size):
    total = query.count()

    items = (
        query
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return total, items


def build_pagination_response(page, page_size, total, items):
    return {
        "page": page,
        "pageSize": page_size,
        "totalCount": total,
        "totalPages": (total + page_size - 1) // page_size,
        "items": items
    }