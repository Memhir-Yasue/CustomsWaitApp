import pandas as pd
import glob
import os
from os import listdir

class Automater:

    def __init__(self):
        print(os.listdir())
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.path = None
        self.raw_file_extension = None
        self.concatinated_df = None
        self.total_entries = 0


    def set_curr_dir(self,dir):
        path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(path,dir)
        os.chdir(self.path)

    def reset_pwd(self):
        os.chdir(self.script_path)

    def curr_dir_XType_files(self,extension):
        """
        Enter '.xls' if that's the extension name of the data file
        """
        self.raw_file_extension = extension
        path_to_dir = self.path
        os.chdir(path_to_dir)
        result = glob.glob('*.{}'.format(extension))
        print(result,"^"*20)
        return result

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
            self.total_entries += len(df_Xtype.index)
            df_list.append(df_Xtype)
        return df_list

    def pre_process_df(self,raw_df_list):
        """
        renames the columns of the dataframes
        """
        df_list = raw_df_list
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
        if len (concatinated_df.index) != self.total_entries:
            raise ValueError("Some data might have been lost from the input files. ORIGINAL {} Concatinated {}".format(row_num_orig, self.total_entries))
        self.concatinated_df = concatinated_df
        return pd.concat(df_list)

    def output_csv(self):
        df = self.concatinated_df
        df.to_csv('output.csv')
        print(os.getcwd())
        print("Sucessfully wrote output file")

    def main():
        robo = Automater()
        robo.set_curr_dir('drop_here')
        htm_files = robo.curr_dir_XType_files('xls')

        dirty_df_list = robo.htm_to_df()
        clean_df_list = robo.pre_process_df(dirty_df_list)
        robo.concatinate_df(clean_df_list)
        robo.set_curr_dir('..')
        robo.set_curr_dir('output')
        robo.output_csv()
        robo.reset_pwd()



# if __name__ == "__main__":
