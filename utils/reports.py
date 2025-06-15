# Mapping of user-friendly names to report files
IPCC_REPORTS = {
    "AR6 Synthesis Report (SPM)": "IPCC_AR6_SYR_SPM.pdf",
    "AR6 Climate Science (WGI SPM)": "IPCC_AR6_WGI_SPM.pdf",
    "AR6 Impacts & Adaptation (WGII SPM)": "IPCC_AR6_WGII_SPM.pdf",
    "AR6 Mitigation (WGIII SPM)": "IPCC_AR6_WGIII_SPM.pdf"
}

def get_report_filename(report_name):
    return IPCC_REPORTS.get(report_name, "IPCC_AR6_SYR_SPM.pdf")
