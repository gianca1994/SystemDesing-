from sqlalchemy_filters import pagination, sort, filters

class Pagination:
    def __init__(self, query, page, perpage):
        self.query = query; self.page = page; self.perpage = perpage

    def page(self, val):
        if int(val) >= 1:
            self.page = int(val)
        return self.query

    def perpage(self, val):
        if int(val) >= 1:
            self.perpage = int(val)
        return self.query

    def pagination(self):
        return pagination(self.query, page_number=self.page, page_size=self.perpage)

    def sort(self, val):
        self.query = sort(self.query, val)
        return self.query

    def filter(self, val):
        self.query = filters(self.query, val)
        return self.query

    def run(self, i, val):

        pages = {"filter": self.filter, "sort_by": self.sort, "page": self.page, "elem_per_page": self.perpage}
        if i in pages.keys():
            return pages[i](val)
        else:
            return self.query