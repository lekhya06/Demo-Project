import pandas as pd
import numpy as np

def factorize(n):
    try:
        factors = []
        while (n & 1) == 0:
            factors.append(2)
            n >>= 1
        for d in range(3, 1 << 60, 2):
            if d * d > n:
                break
            while n % d == 0:
                factors.append(d)
                n //= d
        if n > 1:
            factors.append(n)
        return factors
    except:
        return None
 
if __name__ == '__main__':
    raw_df = pd.read_csv( "data.csv")
    print( raw_df.head() )
    grp_cols = ["State", "Year"]
    numeric_col = "Population"
    raw_df[numeric_col] = raw_df[numeric_col].astype(np.int)
    agg_df = raw_df.groupby(grp_cols)[numeric_col].sum().reset_index()
    agg_df[numeric_col] = agg_df[numeric_col].astype(np.int)
    agg_df['pct_change_yoy'] = agg_df.groupby(grp_cols[0])[numeric_col].pct_change() 
    agg_df['pct_change_yoy'] =  agg_df.groupby(grp_cols[0])[numeric_col].pct_change() 

    final_population_df = agg_df.loc[agg_df.groupby(grp_cols[0])[grp_cols[1]].idxmax()]
    print( agg_df[agg_df['State'] == 'Alabama'] )
    final_population_df['2020 factorization']  =  final_population_df[numeric_col].apply( lambda x: factorize( int(x) ))
    final_population_df['2020 factorization'] = final_population_df['2020 factorization'].\
                                                    apply( lambda x:  ";".join([ str(i) for i in x] ))
    agg_df[numeric_col+'_new'] = agg_df[numeric_col].astype(str) + ' (' + np.round(agg_df['pct_change_yoy'].astype(np.float32),5).astype(str) +'%)'
    print( final_population_df)


    table_df = agg_df.pivot_table('Population_new', ['State'], 'Year', aggfunc=lambda x: ' '.join(x))
    print( table_df)


    final_df = table_df.join(final_population_df.set_index(grp_cols[0])["2020 factorization"]).rename(
        {  'State': "State Name",
        '2020 factorization': '2020 Factors'
        },
        axis=1
    )
    final_df.to_csv("aggregated_data.csv")
    print(  "data saved to aggregated_data.csv")
