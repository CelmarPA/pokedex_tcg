class SearchFilters:

    def __init__(self, args):

        self.search = args.get("search", "").strip()

        self.type = args.get("type", "").strip()

        self.rarity = args.get("rarity", "").strip()

        self.supertype = args.get("supertype", "").strip()

        self.page = args.get("page", 1, type=int)

        self.page_size = args.get("page_size", 20, type=int)

        self.order_by = args.get("order_by", "").strip()
