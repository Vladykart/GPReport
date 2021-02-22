all_station_weather_gfs = """
            SELECT *
             FROM scada_v2.allstationmeteo
              WHERE DateTimeForecast
               BETWEEN %s
                AND %s
                 ORDER BY DateTimeForecast
                 """

all_station_weather_hirlam = """
            SELECT *
             FROM scada_v2.allstationmeteoHirlam 
              WHERE DateTimeForecast
               BETWEEN %s
                AND %s
                 ORDER BY DateTimeForecast
                 """

pv_forecast_result2_db = """
            SELECT * 
             FROM pvforecast_result2
              WHERE DateTimeForecast
               BETWEEN %s
                AND %s 
                 AND StationID = %s
                  ORDER BY DateTimeForecast
            """

pv_generation = """
            SELECT
    meter917_his.id_meter,
    meter917_his.DATE,
      sum(sum_val) AS sum_of_day,
            sum(meter917_his.h1 +meter917_his.h2 ) as H00,
            sum(meter917_his.h3 +meter917_his.h4 ) as H01,
            sum(meter917_his.h5 +meter917_his.h6 ) as H02,
            sum(meter917_his.h7 +meter917_his.h8 ) as H03,
            sum(meter917_his.h9 +meter917_his.h10) as H04,
            sum(meter917_his.h11+meter917_his.h12) as H05,

            sum(meter917_his.h13+meter917_his.h14) as H06,
            sum(meter917_his.h15+meter917_his.h16) as H07,
            sum(meter917_his.h17+meter917_his.h18) as H08,
            sum(meter917_his.h19+meter917_his.h20) as H09,
            sum(meter917_his.h21+meter917_his.h22) as H10,
            sum(meter917_his.h23+meter917_his.h24) as H11,
            sum(meter917_his.h25+meter917_his.h26) as H12,
            sum(meter917_his.h27+meter917_his.h28) as H13,
            sum(meter917_his.h29+meter917_his.h30) as H14,
            sum(meter917_his.h31+meter917_his.h32) as H15,
            sum(meter917_his.h33+meter917_his.h34) as H16,
            sum(meter917_his.h35+meter917_his.h36) as H17,
            sum(meter917_his.h37+meter917_his.h38) as H18,
            sum(meter917_his.h39+meter917_his.h40) as H19,
            sum(meter917_his.h41+meter917_his.h42) as H20,
            sum(meter917_his.h43+meter917_his.h44) as H21,
            sum(meter917_his.h45+meter917_his.h46) as H22,
            sum(meter917_his.h47+meter917_his.h48) as H23
                           FROM
                                meter917_his
                                    LEFT JOIN
                                meter_desc ON meter_desc.id = meter917_his.id_meter
                                       WHERE
                                meter917_his.id_meter IN (
                                SELECT
                                        id
                                    FROM
                                        meter_desc
                                    WHERE
                                        id_st = %s
                                        AND type=2 
                                        AND DATE BETWEEN %s AND %s
                                        GROUP BY meter917_his.id_meter)
           GROUP BY DATE
           ORDER BY DATE;
           """

if __name__ == "__main__":
    all_station_weather_gfs: str = all_station_weather_gfs
