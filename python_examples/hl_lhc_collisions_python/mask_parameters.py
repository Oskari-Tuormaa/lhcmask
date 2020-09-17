
mask_parameters = {
    'par_verbose'              : 1,

    # Beam parameters
    'par_beam_norm_emit'       : 2.5,   # [um]
    'par_beam_sigt'            : 0.076,        # [m]
    'par_beam_sige'            : 1.1e-4,       # [-]
    'par_beam_npart'           : 2.2e11,       # [-]
    'par_beam_energy_tot'      : 7000,         # [GeV]

    # Settings
    'par_oct_current'          : -235,         # [A]
    'par_chromaticity'         : 5,            # [-] (Q':5 for colliding bunches, Q':15 for non-colliding bunches)
    'par_vrf_total'            : 16.,          # [MV]

    # Tunes
    'par_qx0'                  : 62.31,
    'par_qy0'                  : 60.32,


    #*************************#
    # Beam-beam configuration #
    #*************************#

    'par_on_bb_switch'         : 1,
    'par_match_with_bb'        : 0,            # should be off at collision
    'par_b_t_dist'             : 25.,          # bunch separation [ns]
    'par_n_inside_D1'          : 5,            # default value for the number of additionnal parasitic encounters inside D1

    'par_nho_IR1'              : 11,           # number of slices for head-on in IR1 (between 0 and 201)
    'par_nho_IR2'              : 11,           # number of slices for head-on in IR2 (between 0 and 201)
    'par_nho_IR5'              : 11,           # number of slices for head-on in IR5 (between 0 and 201)
    'par_nho_IR8'              : 11,           # number of slices for head-on in IR8 (between 0 and 201)

    #*****************************#
    #     Luminosity parameters   #
    #*****************************#

    # This variables set the leveled luminosity in IP8 
    'par_lumi_ip8'             : 2e33,         #[Hz/cm2]

    # This variables set the leveled luminosity in IP8 
    'par_fullsep_in_sigmas_ip2': 5,

    # These variables define the number of Head-On collisions in the 4 IPs
    'par_nco_IP1'              : 2748,
    'par_nco_IP2'              : 2494,
    'par_nco_IP5'              : 2748,
    'par_nco_IP8'              : 2572,

    #*************************#
    #  Errors and corrections #
    #*************************#

    # Select seed for errors
    'par_myseed'               : 1,

    # Set this flag to correct the errors of D2 in the NLC (warning: for now only correcting b3 of D2, still in development)
    'par_correct_for_D2'       : 0,
    # Set this flag to correct the errors of MCBXF in the NLC (warning: this might be less reproducable in reality, use with care)
    'par_correct_for_MCBX'     : 0,

    'par_on_errors_LHC'        : 1,
    'par_on_errors_MBH'        : 1,
    'par_on_errors_Q5'         : 1,
    'par_on_errors_Q4'         : 1,
    'par_on_errors_D2'         : 1,
    'par_on_errors_D1'         : 1,
    'par_on_errors_IT'         : 1,
    'par_on_errors_MCBRD'      : 0,
    'par_on_errors_MCBXF'      : 0,

}
