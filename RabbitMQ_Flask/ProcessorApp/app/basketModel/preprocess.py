import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

from app.models import ShoppingListModel
from app.serializers import shopping_list_serializer


class PreProcessShoppingLists:
    def __init__(self):
        self.user_id = None
        self._shopping_lists = None
        self._trx_encoder = None
        self._data_df = None
        
    def reset(self):
        self.user_id = None
        self._shopping_lists = None
        self._trx_encoder = None
        self._data_df = None

    @property
    def shopping_lists(self):
        if self.user_id is None:
            raise AttributeError("To PreProcess shopping lists we need to know user_id.")

        try:
            if self._shopping_lists is None:
                self._shopping_lists = []
                all_lists = ShoppingListModel.find_all_by_user_id(self.user_id)
                serialized_lists = shopping_list_serializer.dump(all_lists, many=True)
                for lst in serialized_lists:
                    self._shopping_lists.append([item["name"] for item in lst["items"]])
        finally:
            return self._shopping_lists

    @property
    def trx_encoder(self):
        if self._trx_encoder is None:
            self._trx_encoder = TransactionEncoder()
        return self._trx_encoder

    @property
    def data_df(self):
        try:
            if self._data_df is None:
                te_ary = self.trx_encoder.fit(self.shopping_lists).transform(self.shopping_lists, sparse=True)
                self._data_df = pd.DataFrame.sparse.from_spmatrix(te_ary, columns=self.trx_encoder.columns_)
        finally:
            return self._data_df
