from readers import csv_reader

if __name__ == "__main__":
    df=csv_reader.extract_csv("data/dummy.csv")
    print(type(df['customer_id'][0]))