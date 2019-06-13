import pandas as pd
import glob
import os
from os import listdir

class Automater:

    def __init__(self,exe_dir,entries):
        # a constant
        self.script_path = os.path.dirname(os.path.dirname(exe_dir))
        # nested because it's a
        # where_I_want_to_be_at/gui/gui.exe
        self.path = os.path.dirname(os.path.dirname(exe_dir))
        self.entries = entries
        self.raw_file_extension = None
        self.all_entry_dirty_df = []
        self.concatinated_df = None
        self.df_row_len = 0

    def return_entries(self):
        return self.entries

    def set_curr_dir(self,dir):
        path = self.path
        self.path = os.path.join(path,dir)
        os.chdir(self.path)
        print(os.listdir())

    def reset_pwd(self):
        # reset self.path, otherwise new directories will be concatinated to old ones
        self.path = self.script_path
        os.chdir(self.script_path)

    def set_extension(self,extension):
        self.raw_file_extension = extension

    def curr_dir_XType_files(self,extension):
        """
        Enter '.xls' if that's the extension name of the data file
        """
        path_to_dir = self.path
        os.chdir(path_to_dir)
        files = glob.glob('*.{}'.format(extension))
        print(files,"^"*20)
        return files

    def htm_to_df(self):
        """
        converts from an htm file type to a pandas dataframe.
        Note the xls file from the awt.cbo.gov is recognized as html by pandas
        """
        files = self.curr_dir_XType_files(self.raw_file_extension)
        df_list = []
        for file in files:
            print(file,"^"*10)
            df_Xtype = pd.read_html(file)
            df_Xtype = df_Xtype[0]
            self.df_row_len += len(df_Xtype.index)
            df_list.append(df_Xtype)
        self.all_entry_dirty_df.append(df_list)
        return df_list

    def pre_process_df(self):
        """
        renames the columns of the dataframes
        """
        nested_df = self.all_entry_dirty_df
        df_list = [df for dfs in nested_df for df in dfs]

        clean_df_list = []
        cols = [
                 'Airport','Terminal','Date','Hour','U.S Citizen Avrg Wait',
                 'U.S Citizen Max Wait', 'Non U.S Citizen Avrg Wait', 'Non U.S Citizen Max Wait',
                 'All Avrg Wait', 'All Max Wait',
                 '0-15', '16-30','31-45','46-60','61-90','91-120','120 plus',
                 'Excluded','Total','Flights','Booths'
               ]
        for df in df_list:
            # Change column name
            df.columns = cols
            clean_df_list.append(df)
        return clean_df_list

    def concatinate_df(self,clean_df_list):
        df_list = clean_df_list
        concatinated_df = pd.concat(df_list)
        row_num_orig = len (concatinated_df.index)
        if len (concatinated_df.index) != self.df_row_len:
            raise ValueError("Some data might have been lost from the input files. ORIGINAL {} Concatinated {}".format(row_num_orig, self.df_row_len))
        self.concatinated_df = concatinated_df
        return pd.concat(df_list)

    def output_csv(self):
        df = self.concatinated_df
        df.to_csv('output.csv')
        print(os.getcwd())
        print("Successfully wrote output.csv file")

    def main(exe_dir,entries):
        robo = Automater(exe_dir,entries)
        dir_entries = robo.return_entries()
        robo.set_extension('xls')
        for dir_year in dir_entries:
            robo.set_curr_dir('drop_here')
            robo.set_curr_dir(dir_year)
            dirty_df_list = robo.htm_to_df()
            robo.reset_pwd()

        clean_df_list = robo.pre_process_df()
        robo.concatinate_df(clean_df_list)
        robo.reset_pwd()
        robo.set_curr_dir('output')
        robo.output_csv()
        robo.reset_pwd()



# if __name__ == "__main__":
