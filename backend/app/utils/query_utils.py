from sqlalchemy.orm import Query


def apply_sorting(
    query: Query,
    allowed_columns: dict,
    sort_by: str,
    order: str,
):
    column = allowed_columns.get(sort_by)

    if column is None:
        column = next(iter(allowed_columns.values()))

    if order.lower() == "desc":
        return query.order_by(column.desc())

    return query.order_by(column.asc())


def apply_pagination(
    query: Query,
    page: int,
    limit: int,
):
    offset = (page - 1) * limit

    return query.offset(offset).limit(limit)