import matplotlib.pyplot as plt
import uproot
import numpy

# Monte Carlo - signal
filename_mc_PHSP_LLL_MD = '26514181_Xic0XiMuNu_MD17_PHSP_LLL_FILT_MVA_subhel.root'  
filename_mc_PHSP_LLL_MU = '26514181_Xic0XiMuNu_MU17_PHSP_LLL_FILT_MVA_subhel.root'  

# Background - real data with wrong sign
filename_data_WS_LLL_MD = 'Xic0XiMuNu_MD17_EXP_LLL_WS_FILT_MVA_subhel.root'
filename_data_WS_LLL_MU = 'Xic0XiMuNu_MU17_EXP_LLL_WS_FILT_MVA_subhel.root'

# Real data
filename_data_RS_LLL_MD = 'Xic0XiMuNu_MD17_EXP_LLL_FILT_MVA_subhel.root'
filename_data_RS_LLL_MU = 'Xic0XiMuNu_MU17_EXP_LLL_FILT_MVA_subhel.root'


# Monte Carlo - signal
filename_mc_PHSP_DDL_MD = '26514181_Xic0XiMuNu_MD17_PHSP_DDL_FILT_MVA_subhel.root'  
filename_mc_PHSP_DDL_MU = '26514181_Xic0XiMuNu_MU17_PHSP_DDL_FILT_MVA_subhel.root'  

# Background - real data with wrong sign
filename_data_WS_DDL_MD = 'Xic0XiMuNu_MD17_EXP_DDL_WS_FILT_MVA_subhel.root'
filename_data_WS_DDL_MU = 'Xic0XiMuNu_MU17_EXP_DDL_WS_FILT_MVA_subhel.root'

# Real data
filename_data_RS_DDL_MD = 'Xic0XiMuNu_MD17_EXP_DDL_FILT_MVA_subhel.root'
filename_data_RS_DDL_MU = 'Xic0XiMuNu_MU17_EXP_DDL_FILT_MVA_subhel.root'

variable_names = [ 'Xic0_M', 'Xim_M', 'L0_M', 'MLP_Response',
                   'Xic0_DIRA_OWNPV', 'Xic0_mu_TRACK_CHI2NDOF',
                   'Xic0_IPCHI2_OWNPV', 'Xic0_ENDVERTEX_CHI2',
                   'Xic0_TAUCHI2', 'Xic0_LOKI_FDS',
                   'Xic0_mu_ProbNNpi', 'Xic0_mu_ProbNNk', 'mu_ProbNNmu',
                   'eventNumber', 'runNumber'
]

def plot(f_sig, f_bck, variable, xlabel, bins=100, range=None):
    # Open files and access DecayTree
    tree_sig = uproot.open(f_sig)["DecayTree"]
    tree_bck = uproot.open(f_bck)["DecayTree"]

    # Load variable data as NumPy arrays
    data_sig = tree_sig[variable].array(library="np")
    data_bck = tree_bck[variable].array(library="np")

    # Create histograms manually
    contents_sig, edges = numpy.histogram(data_sig, bins=bins, range=range)
    contents_bck, _ = numpy.histogram(data_bck, bins=edges)
    contents_bck = contents_bck * (numpy.sum(contents_sig) / numpy.sum(contents_bck))

    # Plotting
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, height_ratios=[2/3, 1/3], figsize=(8, 6))
    x = (edges[:-1] + edges[1:]) / 2.0
    width = edges[1:] - edges[:-1]

    # Upper plot
    ax[0].step(edges[:-1], contents_sig, where='post', label='Signal', color='red')
    ax[0].step(edges[:-1], contents_bck, where='post', label='Background', color='blue')
    ax[0].set_ylabel('Entries')
    ax[0].legend()
    ax[0].grid(True)

    # Pull
    uncertainty = numpy.sqrt(contents_bck)
    with numpy.errstate(divide='ignore', invalid='ignore'):
        pull = (contents_sig - contents_bck) / uncertainty
        pull[uncertainty == 0] = 0

    ax[1].bar(x, pull, width=width, color='black', alpha=0.7)
    ax[1].axhline(0, color='gray', linestyle='--')
    ax[1].axhline(1, color='red', linestyle=':', linewidth=1)
    ax[1].axhline(-1, color='red', linestyle=':', linewidth=1)
    ax[1].set_ylabel('Pull')
    ax[1].set_xlabel(xlabel)
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()

for variable in variable_names:
    plot(filename_mc_PHSP_LLL_MD, filename_data_WS_LLL_MD, variable, variable)
    