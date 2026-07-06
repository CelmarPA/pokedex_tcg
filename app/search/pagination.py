import math


class Pagination:

    def __init__(self, page, page_size, count, total_count):
        self.current_page = page
        self.page_size = page_size
        self.count = count
        self.total_count = total_count
        self.total_pages = math.ceil(total_count / page_size)
        self.has_previous = page > 1
        self.has_next = page < self.total_pages
        self.previous_page = page - 1 if self.has_previous else None
        self.next_page = page + 1 if self.has_next else None
        self.first_page = 1
        self.last_page = self.total_pages

    @property
    def visible_pages(self):

        pages = [1]

        start = max(2, self.current_page - 2)
        end = min(self.total_pages - 1, self.current_page + 2)

        if start > 2:
            pages.append(None)

        for page in range(start, end + 1):
            pages.append(page)

        if end < self.total_pages - 1:
            pages.append(None)

        if self.total_pages > 1:
            pages.append(self.total_pages)

        return pages