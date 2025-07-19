# Advanced_analysis class placeholder
import pandas as pd
import matplotlib.pyplot as plt

class Advanced_analysis:
    def __init__(self, df, disp):
        self.tdf = df
        self.disp = disp

    def daily_Average_trends(self, cities, save_path=None):
        tdf = self.tdf
        disp = self.disp

        daily_avg = tdf[cities].resample('D').mean()

        plt.figure(figsize=(14, 6))
        for city in cities:
            plt.plot(daily_avg.index, daily_avg[city], label=city)

        plt.title(f'Daily Average {disp} Trends')
        plt.xlabel('Date')
        plt.ylabel(disp)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    def max_min_calculation(self, save_path=None):
        tdf = self.tdf
        disp = self.disp

        max_val = tdf.max().max()
        max_city = tdf.max().idxmax()
        max_time = tdf[tdf[max_city] == max_val].index[0]

        min_val = tdf.min().min()
        min_city = tdf.min().idxmin()
        min_time = tdf[tdf[min_city] == min_val].index[0]

        print(f"Maximum {disp}: {max_val:.2f} in {max_city} on {max_time}")
        print(f"Minimum {disp}: {min_val:.2f} in {min_city} on {min_time}")

        if save_path:
            fig, ax = plt.subplots()
            text = f"Max {disp}: {max_val:.2f} in {max_city} on {max_time}\nMin {disp}: {min_val:.2f} in {min_city} on {min_time}"
            ax.text(0.5, 0.5, text, wrap=True, ha='center', va='center')
            ax.axis('off')
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()

    def Avg_per(self, save_path=None):
        tdf = self.tdf
        disp = self.disp

        avg_vals = tdf.mean().sort_values(ascending=False)

        plt.figure(figsize=(10, 6))
        avg_vals.plot(kind='bar', color='red')
        plt.title(f'Average {disp} per City')
        plt.ylabel(disp)
        plt.xticks(rotation=90)
        plt.grid(axis='y')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

        print(f"Top 5 Highest {disp} Cities (Average):")
        print(avg_vals.head(5))

        print(f"\nTop 5 Lowest {disp} Cities (Average):")
        print(avg_vals.tail(5))

    def hist(self, save_path=None):
        tdf = self.tdf
        disp = self.disp

        monthly_avg = tdf.resample('M').mean().mean(axis=1)

        plt.figure(figsize=(10, 5))
        plt.hist(monthly_avg, bins=12, color='teal', edgecolor='black')
        plt.title(f'Histogram of Monthly Average {disp} (All Cities Combined)')
        plt.xlabel(f'Average {disp}')
        plt.ylabel('Frequency (Number of Months)')
        plt.grid(axis='y')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    def monthly_yearly_analysis_template(self, year, cities, save_path=None):
        tdf = self.tdf.copy()
        disp = self.disp

        tdf.index = pd.to_datetime(tdf.index, errors='coerce')
        tdf = tdf[tdf.index.notnull()]
        tdf = tdf.select_dtypes(include=['number'])

        valid_cities = [city for city in cities if city in tdf.columns]
        if not valid_cities:
            print(f"❌ None of the specified cities found in the dataset.")
            return []

        monthly = tdf.resample('M')
        yearly = tdf.resample('Y')

        monthly_avg = monthly.mean()
        monthly_max = monthly.max()
        monthly_min = monthly.min()

        yearly_avg = yearly.mean()
        yearly_max = yearly.max()
        yearly_min = yearly.min()

        mask = monthly_avg.index.year == int(year)
        monthly_avg_year = monthly_avg.loc[mask]
        monthly_max_year = monthly_max.loc[mask]
        monthly_min_year = monthly_min.loc[mask]

        # ✅ Collect all saved paths here
        saved_paths = []

        for city in valid_cities:
            city_safe = city.replace(" ", "_")

            # Monthly Plot
            plt.figure(figsize=(10, 5))
            plt.plot(monthly_avg_year.index.month, monthly_avg_year[city], label='Average', color='blue')
            plt.plot(monthly_max_year.index.month, monthly_max_year[city], label='Maximum', color='green')
            plt.plot(monthly_min_year.index.month, monthly_min_year[city], label='Minimum', color='red')
            plt.title(f"{disp} Monthly - {city} ({year})")
            plt.xlabel("Month")
            plt.ylabel(disp)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            if save_path:
                monthly_path = save_path.replace(".png", f"_{city_safe}_monthly.png")
                plt.savefig(monthly_path)
                saved_paths.append(monthly_path)
                plt.close()
            else:
                plt.show()

        for city in valid_cities:
            city_safe = city.replace(" ", "_")

            # Yearly Plot
            plt.figure(figsize=(10, 5))
            plt.plot(yearly_avg.index.year, yearly_avg[city], marker='o', label='Average', color='blue')
            plt.plot(yearly_max.index.year, yearly_max[city], marker='^', label='Maximum', color='green')
            plt.plot(yearly_min.index.year, yearly_min[city], marker='v', label='Minimum', color='red')
            plt.title(f"{disp} Yearly - {city}")
            plt.xlabel("Year")
            plt.ylabel(disp)
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            if save_path:
                yearly_path = save_path.replace(".png", f"_{city_safe}_yearly.png")
                plt.savefig(yearly_path)
                saved_paths.append(yearly_path)
                plt.close()
            else:
                plt.show()

        return saved_paths  # ✅ Return list of paths




    def main(self):
        tdf = self.tdf
        disp = self.disp

        print("States :")
        for i in range(len(tdf.columns)):
            print(f"{i+1}) {tdf.columns[i]}")

        inp = int(input("Enter number of Cities you want to analyze: "))
        selected_cities = [input(f"Enter City {i+1}: ").strip() for i in range(inp)]

        year = int(input("Enter year for monthly_yearly_analysis: "))

        self.monthly_yearly_analysis_template(year, selected_cities)
        self.daily_Average_trends(selected_cities)
        self.max_min_calculation()
        self.Avg_per()
        self.hist()
