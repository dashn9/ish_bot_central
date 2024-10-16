class Filter:
    def construct_filters(self, value: dict) -> dict:
        condition_map = {
            "lte": "$lte",
            "gte": "$gte",
            "lt": "$lt",
            "gt": "$gt",
            "ne": "$ne",
            "in": "$in",
            "nin": "$nin",
            "exact": None,
        }

        filters = {}
        for key, val in value.items():
            field, *condition = key.split("__", 1)
            condition = condition[0] if condition else "exact"
            operator = condition_map.get(condition)

            if operator in ["$in", "$nin"]:
                val = val.split(",")

            try:
                val = int(val)
            except (ValueError, TypeError):
                try:
                    val = float(val)
                except (ValueError, TypeError):
                    pass

            if operator:
                filters.setdefault(field, {})[operator] = val
            else:
                filters[field] = val

        return filters
