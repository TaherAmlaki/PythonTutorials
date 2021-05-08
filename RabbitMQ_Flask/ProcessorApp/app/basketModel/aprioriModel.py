from mlxtend.frequent_patterns import apriori, association_rules

from .preprocess import PreProcessShoppingLists


class AprioriModel:
    def __init__(self):
        self._preprocessor = PreProcessShoppingLists()
        self._item_sets = None
        self._frequent_item_sets = None
        self._rules = None

    def fit_model(self, user_id):
        self._preprocessor.reset()
        self._preprocessor.user_id = user_id

    @property
    def item_sets(self):
        try:
            if self._item_sets is None:
                self._item_sets = apriori(self._preprocessor.data_df,
                                          min_support=0.1,
                                          use_colnames=True)
        finally:
            return self._item_sets

    @property
    def frequent_item_sets(self):
        try:
            if self._frequent_item_sets is None:
                self._frequent_item_sets = [
                    {
                        "support": f"{int(100 * round(float(row['support']), 2))}%",
                        "itemsets": ' - '.join([s.title() for s in row['itemsets']])
                    }
                    for _, row in self.item_sets.iterrows()
                ]
                self._frequent_item_sets.sort(key=lambda itemset_: itemset_["support"], reverse=True)
        finally:
            return self._frequent_item_sets

    @property
    def rules(self):
        try:
            if self._rules is None:
                rules_ = association_rules(self.item_sets, metric="lift", min_threshold=1)
                rules_data = []
                for _, row in rules_.iterrows():
                    row = row.T.to_dict()
                    d = {
                        "antecedents": " - ".join([s.title() for s in row["antecedents"]]),
                        "consequents": " - ".join([s.title() for s in row["consequents"]]),
                        "confidence": int(100 * round(float(row['confidence']), 2)),
                        "lift": round(row["lift"], 2),
                        "leverage": round(row["leverage"], 2),
                        "conviction": round(row["conviction"], 2)
                    }
                    rules_data.append(d)
                rules_data.sort(key=lambda r: (-r["lift"], -r["confidence"]))
                self._rules = rules_data
        finally:
            return self._rules
