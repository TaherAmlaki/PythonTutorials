from flask_login import current_user

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

from ShoppingListApp.shoppinglistapp.models import ShoppingListModel


class PreProcessShoppingLists:
    def __init__(self):
        self._user_id = None
        self._shopping_lists = None
        self._trx_encoder = None
        self._data_df = None
        
    def reset(self):
        self._user_id = None
        self._shopping_lists = None
        self._trx_encoder = None
        self._data_df = None

    @property
    def shopping_lists(self):
        if self._user_id is None:
            self._user_id = current_user.get_id()

        try:
            if self._shopping_lists is None:
                self._shopping_lists = {}
                for lst in ShoppingListModel.find_all_by_user_id(self._user_id):
                    self._shopping_lists[str(lst.name)] = lst.items
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
                flat_lists = self._pre_process_raw_lists()
                te_ary = self.trx_encoder.fit(flat_lists).transform(flat_lists, sparse=True)
                self._data_df = pd.DataFrame.sparse.from_spmatrix(te_ary, columns=self.trx_encoder.columns_)
        finally:
            return self._data_df

    def _pre_process_raw_lists(self):
        return [[item.name for item in items] for _, items in self.shopping_lists.items()]
