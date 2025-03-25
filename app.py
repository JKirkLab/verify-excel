import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

protein_upload = st.file_uploader("Upload your protein excel file", type=["xlsx", "xls"])
if protein_upload:
    prot_df = pd.read_excel(protein_upload, nrows = 5)
    #st.write("Protein Columns", prot_df.columns)

    hc_cols = ['Accession', 'Description', 'Coverage [%]', '# Peptides', 
               '# PSMs', 'Gene Symbol', '# Protein Pathway Groups']
    patterns = {
        r"^Abundance Ratio:.*": 'ratio',
        r"^Abundance Ratio P-Value:.*": 'pvalue',
        r"^Abundance Ratio Adj\. P-Value:.*": 'adjusted_pvalue',
        r"^Abundance Ratio Variability.*": 'variability',
        r"^Abundances \(Grouped\):": "grouped_abundance",
        r"^Abundances \(Grouped\) CV \[%\]:": "grouped_cv",
        r"Abundance:\s*.+": 'abundances',
        r"^Abundances \(Normalized\):*": 'normalized abundances'
    }
    col_count = {label: 0 for label in patterns.values()}
    missing_hardcoded = [col for col in hc_cols if col not in prot_df.columns]
    
    for col in prot_df.columns:
        for pattern, names in patterns.items(): 
            if re.match(pattern, col):
                col_count[names] += 1
    #st.write(col_count)
    if all(value != 0 for value in col_count.values()) and len(missing_hardcoded) == 0:
        st.write("✅ All columns present")

    else:
        st.write("🚫 Missing Protein Sheet Columns")
        #print missing values
        for key, value in col_count.items():
            if value == 0:
                st.write(f'Missing {key} column')
        
        if missing_hardcoded:
            st.write(missing_hardcoded)
    
    def check_equal(name1, name2):
        if col_count[name1] != col_count[name2]:
            st.write(f"WARNING: {name1} and {name2} have a different number of columns")

    check_equal('grouped_cv', 'grouped_abundance')
    check_equal('abundances', 'normalized abundances')

    run_level_stats = [col_count[stat] for stat in ['ratio', 'pvalue', 'adjusted_pvalue']]
    if len(set(run_level_stats)) != 1:
        st.write("WARNING: ratio, pvalue, and adjusted_pvalue have different number of columns")


peptide_upload = st.file_uploader("Upload your peptide excel file", type = ["xlsx" , "xls"])

if peptide_upload:
    pep_df = pd.read_excel(peptide_upload, nrows= 5)
    st.write("Peptide Columns", pep_df.columns)

    hc_cols = ['Modifications', '# Protein Groups', '# Proteins', '# PSMs', 'Master Protein Accessions', 'Position in Master Proteins', '# Missed Cleavages']
    patterns = {
        r"^Abundance Ratio:.*": 'ratio',
        r"^Abundance Ratio P-Value:.*": 'pvalue',
        r"^Abundance Ratio Adj\. P-Value:.*": 'adjusted_pvalue',
        r"^Abundance Ratio Variability.*": 'variability',
        r"^Abundances \(Grouped\):": "grouped_abundance",
        r"^Abundances \(Grouped\) CV \[%\]:": "grouped_cv",
        r"Abundance:\s*.+": 'abundances',
        r"^Abundances \(Normalized\):*": 'normalized abundances'
    }



# if uploaded_file:
#     #read excel file in and produce protein search 
#     df = pd.read_excel(uploaded_file)
#     st.write("Preview of uploaded data:", df.head())
#     st.sidebar.header("Search For A Protein")

#     #extract abundance column names and p-value column names
#     abundance_cols = [col for col in df.columns if col.lower().startswith("abundances (grouped):")]
#     pvalue_cols = [col for col in df.columns if col.lower().startswith("abundance ratio p-value:")]

#     st.write("Detected Abundance Columns:", abundance_cols)
#     st.write("Detected P-value Columns:", pvalue_cols)
#     if not abundance_cols:
#         st.error("No 'grouped abundance' columns found in the dataset. Please check your file.")
#     else:
#         protein_col = 'Accession'
#         search_term = st.sidebar.text_input("Search:")

#         if search_term:
#             protein_data = df[df[protein_col] == search_term][abundance_cols].T
#             protein_data.index = [col.replace("Abundances (Grouped): ", "") for col in protein_data.index]
#             conditions = list(set([col.split(": ")[1] for col in abundance_cols]))

#             if protein_data.empty:
#                 st.error(f"No data found for protein: {search_term}")
#             else:
#                 protein_data.columns = ["Abundance"]
#                 protein_data.index.name = "Condition"
#                 protein_data.reset_index(inplace=True)

#                 pvalue_map = {}
#                 for col in pvalue_cols:
#                     match = re.search(r"Abundance Ratio P-Value: \(([^)]+)\) / \(([^)]+)\)", col)
#                     if match:
#                         cond_A, cond_B = match.groups()
#                         pvalue_map[(cond_A, cond_B)] = df[df[protein_col] == search_term][col].values[0]

#                 #Plot
#                 fig, ax = plt.subplots(figsize=(10, 6))
#                 ax.bar(protein_data["Condition"], protein_data["Abundance"])
#                 ax.set_xlabel("Group")
#                 ax.set_ylabel("Grouped Abundances")
#                 ax.set_title(search_term)
#                 plt.xticks(rotation=45, ha="right")

#                 max_y = protein_data["Abundance"].max()
#                 offset = max_y * 0.05  


#                 num_comparisons = 0 
#                 #iterate through dictionary and draw brackets
#                 for (cond_A, cond_B), p_val in pvalue_map.items():
#                     if cond_A in protein_data["Condition"].values and cond_B in protein_data["Condition"].values:
#                         star_label = get_pval_stars(p_val)
#                         if star_label == "n.s.":
#                             continue
                        
#                         x1 = protein_data[protein_data["Condition"] == cond_A].index[0]
#                         x2 = protein_data[protein_data["Condition"] == cond_B].index[0]

#                         # adjust bracket by offset to prevent overlap
#                         y = max_y + offset + (num_comparisons * 0.1 * max_y)

#                         num_comparisons += 1

#                         # Draw bracket
#                         ax.plot([x1, x1, x2, x2], [y, y + 0.02, y + 0.02, y], lw=1.5, color="black")

#                         # add stars based on significance level
                        
#                         ax.text((x1 + x2) / 2, y + 0.02, star_label, ha='center', va='bottom', fontsize=12, color="black")

    

#                 st.pyplot(fig)
        
        




