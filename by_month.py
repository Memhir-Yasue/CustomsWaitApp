import pandas as pd
import os
import platform
import subprocess

script_path = os.path.dirname(os.path.realpath(__file__))

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def read_n_preprocess(dir):
    os.chdir(dir)
    file = 'by_Y_M.csv'
    df = pd.read_csv(file)
    df.drop('Unnamed: 0',axis = 1, inplace = True)
    # df.columns = ['Airport','Month','Average Wait Time (min)']
    return df

def make_airport_column(df):
    airport_column = []
    for airport in df.Airport:
        if airport not in airport_column:
            airport_column.append(airport)
        if len(airport_column) == len(set(df.Airport)):
            break
    num_months = int(df.shape[0] / len(airport_column))
    return airport_column, num_months

def make_wait_time_list(df,num_months):
    wait_time_list = []
    begin = 0
    for i in range(len(df)):
    # i + 1 so that the last set of data is included. Example if 47 is the last row, then i+1 = 48
        if ((i + 1) % num_months == 0) & (i != 0):
            to_append = list(df['Average_wait_time'][begin:i + 1])
            wait_time_list.append(to_append)
            begin = i + 1
#         print(i+1,"MOD ME")
    return wait_time_list

def make_airport_wait_time(airport_column, wait_time_list):
    airport_dict = {}
    i = 0
    for airport in airport_column:
        airport_dict[airport] = wait_time_list[i]
        i+=1
    return airport_dict

def make_airport_col_df(airport_column,airport_dict):
    airport_df = pd.DataFrame(columns=[airport for airport in airport_column])
    for airport in airport_column:
        airport_df[airport] = airport_dict[airport]
    return airport_df

def make_year_col_df(df,year):
    row_num = df.shape[0]
    some_df = pd.DataFrame({'Year':[year for i in range(row_num)]})
    return some_df

def make_month_col_df(num_months):
    month_df = pd.DataFrame({'Month':[i+1 for i in range(num_months)]})
    return month_df

def process_by_year(df):
    yearly_df_list = []
    for year in set(df.Year):
        df_year = df[df.Year == year]
        airport_col, num_months = make_airport_column(df_year)
        wait_time_list = make_wait_time_list(df_year,num_months)
        airport_dict = make_airport_wait_time(airport_col,wait_time_list)

        airport_df = make_airport_col_df(airport_col,airport_dict)
        year_df = make_year_col_df(df_year,year)
        month_df = make_month_col_df(num_months)
        time_df = concat_df_cols(year_df,month_df)
        new_df = concat_df_cols(time_df,airport_df)
        yearly_df_list.append(new_df)
    return yearly_df_list

def concat_df_cols(df1,df2):
    concatinated_df = pd.concat([df1,df2],axis = 1)
    return concatinated_df

def concat_df_rows(df1,df2):
    concatinated_df = pd.concat([df1,df2],axis = 0)
    return concatinated_df

def remove_na(df_list):
    clean_df_list = []
    for df in df_list:
        df_clean = df.dropna()
        clean_df_list.append(df_clean)
    return clean_df_list

def final_concat(clean_df_list):
    all_years_data = pd.concat(clean_df_list)
    return all_years_data

def save(new_df,cwd):
    new_df.to_excel(cwd + "/Month by Month Report.xls",index = False)
    print("**"*25)

def set_curr_dir(dir):
    path = dir
    os.chdir(path)
    return path

def main():
    # cwd = .../output
    # path = 'output/by_Y_M.csv'
    # path = set_curr_dir('output')
    # # cwd = .../output
    print(os.path.join(script_path,'output'), "&"*15)
    df = read_n_preprocess(dir = os.path.join(script_path,'output') )
    dirty_yearly_list = process_by_year(df)
    clean_yearly_list = remove_na(dirty_yearly_list)
    final_df = final_concat(clean_yearly_list)
    cwd = os.getcwd()
    save(final_df,cwd)
    os.chdir(script_path)
    open_file(path=os.path.join(script_path,'output'))
    print("--"*25)


# if __name__ == "__main__":
#     # path = 'output/by_Y_M.csv'
#     path = set_curr_dir('output')
#     # cwd = .../output
#     cwd = os.getcwd()
#     df = read_n_preprocess(file = cwd + '/by_Y_M.csv')
#     dirty_yearly_list = process_by_year(df)
#     clean_yearly_list = remove_na(dirty_yearly_list)
#     final_df = final_concat(clean_yearly_list)
#     save(final_df,cwd)
#     open_file(path=cwd)
