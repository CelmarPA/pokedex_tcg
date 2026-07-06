from urllib.parse import urlencode


class SearchFilters:

    def __init__(self, args):

        self.search = args.get("search", "").strip()

        self.type = args.get("type", "").strip()

        self.rarity = args.get("rarity", "").strip()

        self.supertype = args.get("supertype", "").strip()

        self.page = args.get("page", 1, type=int)

        self.page_size = args.get("page_size", 20, type=int)

        self.order_by = args.get("order_by", "").strip()

    def to_query_params(self):

        return {
            key: value
            for key, value in {
                "search": self.search,
                "type": self.type,
                "rarity": self.rarity,
                "supertype": self.supertype,
                "page_size": self.page_size,
                "order_by": self.order_by
            }.items()
            if value not in ("", None)
        }

    def build_url(self, page):

        params = self.to_query_params()
        params["page"] = page

        return "?" + urlencode(params)
