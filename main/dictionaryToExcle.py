data = [['1', 'EBL', '1', '1', '1', '547', '547.00', '558', '558.00'], ['2', 'NIFRA', '54', '54', '54', '213.1', '11,507.40', '217.5', '11,745.00'], ['3', 'NLIC', '3', '3', '3', '741', '2,223.00', '760', '2,280.00'], ['4', 'PRVU', '4', '4', '4', '158', '632.00', '160.9', '643.60']]
symbol = []
cdsFreeBalance = []

for d in data:
    symbol.append(d[1])
    cdsFreeBalance.append(d[3])

print(symbol)
print(cdsFreeBalance)

mainDictironary =  {
    'S.No' : 1,
    'Client Name': "AASHISH SHRESTHA",
    'BO ID': "1301060000228149",
    'Stock Symbol': symbol,
    'CDS Free Balance': cdsFreeBalance,
    'Available Trading Limit': "NPR 0.00",
}

df = pd.DataFrame(mainDictironary)
df.to_csv('output.csv')

my_index_cols = ['S.No','Client Name','Available Trading Limit','Stock Symbol'] # this can also be a list of multiple columns
df.set_index(my_index_cols).to_excel('filename.xlsx', index=True)
