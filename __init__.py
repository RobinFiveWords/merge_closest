from __future__ import print_function

import numpy as np
import pandas as pd


def merge_closest(data, lookup, data_field, lookup_field,
                  include_cols=None, exclude_cols=None,
                  presorted=False):
    """Merge column(s) into DataFrame using closest-without-going-over lookup.
    
    This function mimics Excel's VLOOKUP function in approximate match
    (range lookup) mode, with added benefits of ensuring the lookup table is
    sorted and merging any subset of columns from the lookup table. It's
    similar to a left join based on the lookup_field value that is closest to
    the data_field value without going over. Only the first matching row from
    lookup is merged; if lookup_field contains duplicates, it's up to the user
    to drop duplicates in advance as appropriate. For any row in data whose
    data_field value is less than all values in lookup_field, lookup values
    in result will be missing.
    By default, all columns in lookup other than lookup_field will be merged
    with data. A specific list of columns from lookup to include or exclude
    can be passed. If both include_cols and exclude_cols are provided,
    exclude_cols is ignored. To include lookup_field in result, lookup_field
    must be passed in include_cols, perhaps as include_cols=lookup.columns.
    
    Parameters
    ----------
    data : pandas DataFrame
    lookup : pandas DataFrame
    data_field : name of column in data
    lookup_field : name of column in lookup
    include_cols : list, pandas Index, or single value; columns from lookup to
        include in result.
        If neither include_cols nor exclude_cols is provided, all columns
        from lookup except lookup_field are included in result.
    exclude_cols : list, pandas Index, or single value; columns from lookup to
        exclude from result.
        By default, lookup_field will be excluded even if not in exclude_cols.
        To include lookup_field, pass it in include_cols.
        If both include_cols and exclude_cols are provided, exclude_cols is
        ignored.
    presorted : boolean
        Unless set to True, lookup will be sorted ascending on lookup_field
        prior to merging.
    
    Returns
    -------
    result : pandas DataFrame
    """
    if (isinstance(include_cols, pd.Index)) | (isinstance(include_cols, list)):
    	pass
    elif include_cols:
        include_cols = [include_cols]
    elif isinstance(exclude_cols, pd.Index):
    	include_cols = lookup.columns.drop([lookup_field] + list(exclude_cols))
    elif isinstance(exclude_cols, list):
    	include_cols = lookup.columns.drop([lookup_field] + exclude_cols)
    elif exclude_cols:
        include_cols = lookup.columns.drop([lookup_field, exclude_cols])
    else:
        include_cols = lookup.columns.drop(lookup_field)

    if not presorted:
        lookup = lookup.sort_values(by=lookup_field).reset_index(drop=True)
    row_indices = (np.searchsorted(lookup[lookup_field],
                                   data[data_field],
                                   side='right')
                   .astype(float))
    row_indices[row_indices == 0] = np.nan
    row_indices -= 1

    result = pd.concat(
        [data, lookup.loc[row_indices, include_cols].set_index(data.index)],
        axis=1)
    
    return result


def main():
    lookup = pd.DataFrame({
        'lookup_value': np.array([1, 3, 5, 4, 2]) * 10,
        'return_value1': list('WXYZQ'),
        'return_value2': list('ABCDE'),
        'return_value3': list('FGHIJ'),
    })
    data = pd.DataFrame({
        'data_value': np.random.normal(30, 20, 30).round(0).astype(int),
        'other_value': np.arange(100, 130),
    })
    result = merge_closest(data, lookup, 'data_value', 'lookup_value',
                 include_cols=['return_value1', 'return_value3'],
                 exclude_cols='return_value2',
    )
    print(result)


if __name__ == '__main__':
    main()
