# Independent_Analysis class placeholder
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

class Independent_Analysis:
    def __init__(self, df, disp):
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)
        self.pdf = df
        self.disp = disp

    def get_key(self, d, v):
        i = 0
        for k, v1 in d.items():
            i += 1
            if v == v1:
                return (k, i)
        return (None, -1) 

    def Monthly_pressure_analysis(self, *data, save_path=None):
        pdf = self.pdf
        disp = self.disp

        pdf['month'] = pdf.index.to_period('M').astype(str)
        monthly_avg = pdf.groupby('month')[data[0]].mean().round(2)

        result = {}
        for k, v in monthly_avg.items():
            result[pd.to_datetime(str(k))] = float(v)

        usr = data[1] 
        d1 = {}
        for k, v in result.items():
            if (k.year) == usr:
                d1[k.strftime("%B")] = v

        dates = d1.keys()
        pressure = d1.values()
        plt.figure(figsize=(12,6))
        plt.plot(dates, pressure, marker="o", linestyle='-', color='royalblue')
        plt.title(f"Monthly {disp} in {data[0]} in {usr}")
        plt.xlabel("Month")
        plt.ylabel(disp)
        plt.grid(True)
        plt.xticks(rotation=45)

        if save_path:
            plt.savefig(save_path)
            return save_path  
        else:
            plt.show()

        marr = np.array(list(d1.values()))
        mmax = marr.max()
        mmin = marr.min()
        mavg = marr.mean()
        print(f"Maximum {disp} is in ", self.get_key(d1, mmax)[0], " : ", mmax)
        print(f"Minimum {disp} is in ", self.get_key(d1, mmin)[0], " : ", mmin)
        print(f"Average {disp} is : ", mavg.round(2))

    def Yearly_pressure_analysis(self, state, save_path=None):
        pdf = self.pdf
        disp = self.disp

        pdf['year'] = pdf.index.to_period('Y').astype(str)
        yearly_avg = pdf.groupby('year')[state].mean().round(2)

        result = {}
        for k, v in yearly_avg.items():
            result[int(k)] = v

        years = result.keys()
        pressure = result.values()
        plt.figure(figsize=(12,6))
        plt.plot(years, pressure, marker="o", linestyle='-', color='royalblue')
        plt.title(f"Yearly {disp} analysis of {state}")
        plt.xlabel("Year")
        plt.ylabel(disp)
        plt.grid(True)
        plt.xticks(rotation=45)

        if save_path:
            plt.savefig(save_path)
            return save_path
        else:
            plt.show()

        marr = np.array(list(result.values()))
        mmax = marr.max()
        mmin = marr.min()
        mavg = marr.mean()
        print(f"Maximum {disp} is in ", self.get_key(result, mmax)[0], " : ", mmax)
        print(f"Minimum {disp} is in ", self.get_key(result, mmin)[0], " : ", mmin)
        print(f"Average {disp} is : ", mavg.round(2))
        print("\n\n\n")

    def Hourly_Analysis(self, state, disp, save_path=None):
        tdf = self.pdf
        tdf['hour'] = tdf.index.hour
        hourly_avg = tdf.groupby('hour')[state].mean()

        plt.figure(figsize=(10, 5))
        plt.plot(hourly_avg.index, hourly_avg.values, marker='o', color='purple')
        plt.title(f'Hourly Average {disp} in {state}')
        plt.xlabel('Hour of Day')
        plt.ylabel(disp)
        plt.xticks(range(0, 24))
        plt.grid(True)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            return save_path
        else:
            plt.show()

    def main(self):
        pdf = self.pdf
        disp = self.disp

        while True:
            print("States:")
            for i in range(len(pdf.columns)):
                print(f"{i+1}) {pdf.columns[i]}")

            print(f"\nSelect One Option :-")
            print("1 - Monthly Air", disp, "Analysis")
            print("2 - Yearly Air", disp, "Analysis")
            print("3 - All")
            print("4 - Exit")
            print("5 - Hourly", disp, "Analysis")
            
            pref = int(input("Enter your Preference No:- "))
            if pref == 4:
                print("Shutting Down.......")
                return
            elif pref == 1:
                state = input("Write your preference as it is:").strip()
                yr = int(input("Write Year between 2012-2017:"))
                self.Monthly_pressure_analysis(state, yr)
            elif pref == 2:
                state = input("Write your preference as it is:").strip()
                self.Yearly_pressure_analysis(state)
            elif pref == 3:
                state = input("Write your preference as it is:").strip()
                yr = int(input("Write Year between 2012-2017:"))
                self.Monthly_pressure_analysis(state, yr)
                self.Yearly_pressure_analysis(state)
                self.Hourly_Analysis(state, disp)
            elif pref == 5:
                state = input("Write your preference as it is:").strip()
                self.Hourly_Analysis(state, disp)
            else:
                print("Invalid Option")
