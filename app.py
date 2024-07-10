import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
def main():
    st.header("Convert print report PDF to CSV")
    #upload a PDF file
    pdf = st.file_uploader("Upload Print report PDF", type="pdf")

    if pdf is not None:
        reader = PdfReader(pdf)
    
        no_of_pages = len(reader.pages)
        text = ""
        for i in range (no_of_pages):
            page = reader.pages[i]
            text += page.extract_text()
        text = text.split("\n")

        #function for element extraction
        def element_extraction(element):
            element_value = []
            for i in text:
                if str(element) in i.split(": ")[0]:
                    try:
                        element_string = ""
                        for j in i.split(": ")[1:]:
                            element_string += (j + ': ') 
                        element_value.append(element_string[:len(element_string) - 2])
                    except IndexError:
                        element_value.append(0)
            return element_value

        #for column names
        columns = []
        for i in text: 
            columns.append(i.split(": ")[0])
        col = columns[2:9]
        col.append(columns[12])
        columns = col
        


        #assignment of elements to respective column CHANGE REQ
        df_col = ['Printed by', 'Filename', 'Filesize', 'Start_Time', 'End_Time', 'Duration', 'Result', 'Calculated length']
        df = pd.DataFrame(columns = df_col, index=range(no_of_pages))
        indexwise_list = []
        for k in range (no_of_pages):
            for j in range (len(df_col)):
                indexwise_list.append(element_extraction(columns[j])[k])
            df.iloc[k] = (indexwise_list)
            indexwise_list = []
        data_as_csv= df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download data as CSV", 
            data_as_csv,
            "Print Report.csv",
            
        )
if __name__ == "__main__":
    main()