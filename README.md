## merge_closest
### Merge column(s) into DataFrame using closest-without-going-over lookup.

The `merge_closest` function mimics Excel's VLOOKUP function in approximate
match (range lookup) mode, with added benefits of ensuring the lookup table is
sorted and merging any subset of columns from the lookup table. It's
similar to a left join based on the `lookup_field` value that is closest to
the `data_field` value without going over. Only the first matching row from
`lookup` is merged; if `lookup_field` contains duplicates, it's up to the user
to drop duplicates in advance as appropriate. For any row in `data` whose
`data_field` value is less than all values in `lookup_field`, `lookup` values
in `result` will be missing.

By default, all columns in `lookup` other than `lookup_field` will be merged
with `data`. A specific list of columns from `lookup` to include or exclude
can be passed. If both `include_cols` and `exclude_cols` are provided,
`exclude_cols` is ignored. To include `lookup_field` in `result`, `lookup_field`
must be passed in `include_cols`, perhaps as `include_cols=lookup.columns`.

### This is my first Python package and first GitHub repo...

...and any comments or suggestions are most welcome.

### Use

    from merge_closest import merge_closest
    
    merge_closest(data, lookup, data_field, lookup_field,
                  include_cols=None, exclude_cols=None,
                  presorted=False)

### Parameters

**`data`** : pandas DataFrame

**`lookup`** : pandas DataFrame

**`data_field`** : name of column in `data`

**`lookup_field`** : name of column in `lookup`

**`include_cols`** : list, pandas Index, or single value; columns from
    `lookup` to include in `result`.
    If neither `include_cols` nor `exclude_cols` is provided, all columns
    from `lookup` except `lookup_field` are included in `result`.

**`exclude_cols`** : list, pandas Index, or single value; columns from
    `lookup` to exclude from `result`.
    By default, `lookup_field` will be excluded even if not in `exclude_cols`.
    To include `lookup_field`, pass it in `include_cols`.
    If both `include_cols` and `exclude_cols` are provided, `exclude_cols` is
    ignored.

**`presorted`** : boolean; unless set to True, `lookup` will be sorted
    ascending on `lookup_field` prior to merging.

### Returns

**`result`** : pandas DataFrame