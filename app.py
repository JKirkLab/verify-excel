import streamlit as st
import re

# protein_upload = st.file_uploader("Upload your protein excel file", type=["xlsx", "xls"])
st.markdown("**Paste your Protein column headers here (from Excel or CSV):**")
header_input = st.text_area("Paste headers", height=200, key = 'prot_headers')

prot_columns = [col.strip() for col in header_input.split('\t') if col.strip()]
if prot_columns:
    # prot_df = pd.read_excel(protein_upload, nrows = 0)
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
    missing_hardcoded = [col for col in hc_cols if col not in prot_columns]
    
    for col in prot_columns:
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
            st.write(f"WARNING: {name1} and {name2} have a different number of columns when they should have the same number of columns ")

    check_equal('grouped_cv', 'grouped_abundance')
    check_equal('abundances', 'normalized abundances')

    run_level_stats = [col_count[stat] for stat in ['ratio', 'pvalue', 'adjusted_pvalue']]
    if len(set(run_level_stats)) != 1:
        st.write("WARNING: ratio, pvalue, and adjusted_pvalue have different number of columns when they should have the same number of columns")


st.markdown("**Paste your Peptide column headers here (from Excel or CSV):**")
pep_header_input = st.text_area("Paste headers", height=200, key = 'pep_headers')
pep_columns = [col.strip() for col in pep_header_input.split('\t') if col.strip()]
if pep_columns: 
    hc_cols = ['Modifications', '# Protein Groups', '# Proteins', '# PSMs', 'Master Protein Accessions', 'Positions in Master Proteins', '# Missed Cleavages']
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
    missing_hardcoded = [col for col in hc_cols if col not in pep_columns]
    
    for col in pep_columns:
        for pattern, names in patterns.items(): 
            if re.match(pattern, col):
                col_count[names] += 1
    #st.write(col_count)
    if all(value != 0 for value in col_count.values()) and len(missing_hardcoded) == 0:
        st.write("✅ All columns present")

    else:
        st.write("🚫 Missing Peptide Sheet Columns")
        #print missing values
        for key, value in col_count.items():
            if value == 0:
                st.write(f'Missing {key} column')
        
        if missing_hardcoded:
            st.write(missing_hardcoded)
    
    def check_equal(name1, name2):
        if col_count[name1] != col_count[name2]:
            st.write(f"WARNING: {name1} and {name2} have a different number of columns when they should have the same number of columns")

    check_equal('grouped_cv', 'grouped_abundance')
    check_equal('abundances', 'normalized abundances')
    run_level_stats = [col_count[stat] for stat in ['ratio', 'pvalue', 'adjusted_pvalue']]
    if len(set(run_level_stats)) != 1:
        st.write("WARNING: ratio, pvalue, and adjusted_pvalue have different number of columns when they should have the same number of columns")

