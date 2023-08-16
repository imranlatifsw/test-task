import pandas
import numpy as np


class CSVFormatter:
    def __init__(self, filename: str):
        self.columns = ["Revenue", "Profit", "Cost", "Expense", "Income", "Price", "Salary", "Investment"]
        self.col_revenue = "Revenue"
        self.col_profit = "Profit"
        self.col_cost = "Cost"
        self.filename = filename

    def read_csv(self) -> pandas.DataFrame:
        return pandas.read_csv(self.filename)

    def clean_data(self, df: pandas.DataFrame) -> pandas.DataFrame:
        for column in self.columns:
            df[column] = df[column].str.strip()
            df[column] = df[column].str.replace("$", "")
            df[column] = df[column].replace("", np.nan)
            df[column] = df[column].astype(float).fillna(0.0)

        df.fillna(0, inplace=True)
        return df

    def format_columns(self, df: pandas.DataFrame) -> pandas.DataFrame:
        for column in self.columns[3:]:
            filt = (df[column] == 0)
            df.loc[filt, column] = ""

        for column in self.columns:
            df[column] = df[column].astype(str)
            df[column] = df[column].apply(
                lambda x: f"${float(x.replace('$', '').replace(',', '')):,.2f}" if x.strip() else ""
            )

        return df

    def calculate_revenue(self, df: pandas.DataFrame) -> pandas.DataFrame:
        filter_revenue = (df[self.col_revenue] == 0)
        for idx in df[filter_revenue].index:
            df.loc[idx, self.col_revenue] = float(df.loc[idx, self.col_profit]) / 0.2 if float(
                df.loc[idx, self.col_profit]) != 0.00 else df.loc[idx, self.col_revenue]

        return df

    def calculate_profit(self, df: pandas.DataFrame) -> pandas.DataFrame:
        filter_profit = (df[self.col_profit] == 0)
        for idx in df[filter_profit].index:
            df.loc[idx, self.col_profit] = float(df.loc[idx, self.col_revenue]) * 0.2 if float(
                df.loc[idx, self.col_revenue]) != 0.00 else df.loc[idx, self.col_profit]

        return df

    def calculate_cost(self, df: pandas.DataFrame) -> pandas.DataFrame:
        filter_cost = (df[self.col_cost] == 0)
        for idx in df[filter_cost].index:
            df.loc[idx, self.col_cost] = float(df.loc[idx, self.col_revenue]) - float(
                df.loc[idx, self.col_profit]) if float(df.loc[idx, self.col_revenue]) != 0.00 and float(
                df.loc[idx, self.col_profit]) != 0.00 else df.loc[idx, self.col_cost]

        return df

    def calculate_missing_values(self, df: pandas.DataFrame) -> pandas.DataFrame:
        df = self.calculate_revenue(df)
        df = self.calculate_profit(df)
        df = self.calculate_cost(df)

        return df

    def group_data(self):
        df = self.read_csv()
        df = self.clean_data(df)
        df = self.calculate_missing_values(df)
        # group by Master and Id
        df = df.groupby(['Master', 'ID']).sum()
        df = self.format_columns(df)
        return df


formatter = CSVFormatter('sample.csv')
formatted_data = formatter.group_data()
print(formatted_data)
