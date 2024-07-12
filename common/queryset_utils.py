from django.utils.timezone import is_naive, make_aware
from django.db.models import Count


class QuerySetDateHelper:
    def filter_between_dates(self, date_field, from_date, to_date):
        if is_naive(from_date):
            from_date = make_aware(from_date)
        if is_naive(to_date):
            to_date = make_aware(to_date)

        q = {
            f"{date_field}__range": (from_date, to_date),
        }
        return self.filter(**q)

    def base_per_date(self, date_field, day_format):
        """return count pf entries per date

        Args:
            date_field (str): date field on the model to count by
            day_format (str): format of the date in the query

        Returns:
            list: return list of dicts with date and count
        """
        return (
            self.extra(
                select={
                    "date": f"TO_CHAR({date_field}, '{day_format}')",
                }
            )
            # we can order by date normally because it will order by characters from
            # left to right
            .order_by("date").values("date")
        )

    def count_per_date(self, date_field, day_format):
        """return count pf entries per date

        Args:
            date_field (str): date field on the model to count by
            day_format (str): format of the date in the query

        Returns:
            list: return list of dicts with date and count
        """
        return self.base_per_date(date_field, day_format).annotate(
            count=Count(date_field)
        )

    def count_per_day(self, date_field):
        return self.count_per_date(date_field, day_format="YYYY-MM-DD")

    def count_per_month(self, date_field):
        return self.count_per_date(date_field, day_format="YYYY-MM")

    def count_per_year(self, date_field):
        return self.count_per_date(date_field, day_format="YYYY")
