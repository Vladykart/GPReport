=====
Usage
=====

To use GPReport in a project::

    from gpreport import gpreport as gp

    # To get rdn datasets:
    rdn = gp.get_rdn_dataframes(
                login = 'LOGIN',
                password = 'PASSWORD',
                station_id = ''STATION_ID,
                date_from = 'dd.mm.yyyy',
                num_days = int
                )

    # To get vdr datasets:
    vdr = gp.get_vdr_dataframes(
                login = 'LOGIN',
                password = 'PASSWORD',
                station_id = ''STATION_ID,
                date_from = 'dd.mm.yyyy',
                num_days = int
                )

This methods returns a list of dictionary::

    [{'dataframe': pandas.DataFrame,
      'date': str,
      'station_id': str}]



