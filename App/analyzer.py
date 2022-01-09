#!/usr/bin/env python
# coding: utf-8

# -----------------------------------------------------------
# City-wide emissions project, unstructured data part.
# This file contains a class with functions to generate 
# a frequency matrix of words in a text fragment.
# -----------------------------------------------------------

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


class Text_Analyzer:

    def __init__(self, text_array):
        self.text_array = text_array

    def get_matrix(self):
        count_vec = CountVectorizer()
        count_occurs = count_vec.fit_transform(self.text_array)
        counts_matrix = count_occurs.toarray()
        words = np.array(count_vec.get_feature_names())
        df_matrix = pd.DataFrame(counts_matrix)
        df_matrix.columns = words
        df_matrix.index = ['fragment ' + str(i) for i in np.arange(1, counts_matrix.shape[0] + 1)]
        df_total = df_matrix.sum(axis=0).to_frame().T
        df_total.index = ['total']
        df_matrix = pd.concat([df_matrix, df_total], axis=0)
        return df_matrix
