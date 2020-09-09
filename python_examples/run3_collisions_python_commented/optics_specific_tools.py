import pymask as pm

# The parts marked by (*) in following need to be
# adapted according to knob definitions

def build_sequence(mad, beam):

    slicefactor = 2

    pm.make_links(force=True, links_dict={
        'optics_indep_macros.madx': 'tools/optics_indep_macros.madx',
        'macro.madx': ('/afs/cern.ch/user/s/sterbini/public/'
                         'tracking_tools/tools/macro.madx'),
        'optics_runII': '/afs/cern.ch/eng/lhc/optics/runII',
        'optics_runIII': '/afs/cern.ch/eng/lhc/optics/runIII',})


    mylhcbeam = int(beam)

    mad.input('ver_lhc_run = 3')

    mad.input(f'mylhcbeam = {beam}')
    mad.input('option, -echo,warn, -info;')

    # optics dependent macros
    mad.call('macro.madx')
    # optics independent macros
    mad.call('optics_indep_macros.madx')

    assert mylhcbeam in [1, 2, 4], "Invalid mylhcbeam (it should be in [1, 2, 4])"

    if mylhcbeam in [1, 2]:
        mad.call('optics_runII/2018/lhc_as-built.seq')
    else:
        mad.call('optics_runII/2018/lhcb4_as-built.seq')

    # New IR7 MQW layout and cabling
    mad.call('optics_runIII/RunIII_dev/IR7-Run3seqedit.madx')

    # Makethin part
    if slicefactor > 0:
        # the variable in the macro is slicefactor
        mad.input(f'slicefactor={slicefactor};')
        mad.call('optics_runII/2018/toolkit/myslice.madx')
        mad.beam()
        for my_sequence in ['lhcb1','lhcb2']:
            if my_sequence in list(mad.sequence):
                mad.input(f'use, sequence={my_sequence}; makethin, sequence={my_sequence}, style=teapot, makedipedge=false;')
    else:
        warnings.warn('The sequences are not thin!')

    # Cycling w.r.t. to IP3 (mandatory to find closed orbit in collision in the presence of errors)
    for my_sequence in ['lhcb1','lhcb2']:
        if my_sequence in list(mad.sequence):
            mad.input(f'seqedit, sequence={my_sequence}; flatten; cycle, start=IP3; flatten; endedit;')

def apply_optics(mad, optics_file):
    pm.make_links(force=True, links_dict={
        'optics.madx' : 'optics_runIII/RunIII_dev/2022_V1/PROTON/' + optics_file})
    mad.call('optics.madx')

def check_beta_at_ips_against_madvars(beam, twiss_df, variable_dicts, tol):
    twiss_value_checks=[]
    for iip, ip in enumerate([1,2,5,8]):
        for plane in ['x', 'y']:
            # (*) Adapet based on knob definitions
            twiss_value_checks.append({
                    'element_name': f'ip{ip}:1',
                    'keyword': f'bet{plane}',
                    'varname': f'bet{plane}ip{ip}b{beam}',
                    'tol': tol[iip]})

    pm.check_twiss_against_madvars(twiss_value_checks, twiss_df, variable_dicts)


def set_optics_specific_knobs(mad, mode=None):

    from knob_parameters import knob_parameters as kp

    mad.set_variables_from_dict(params=kp)

    # Set IP knobs
    mad.globals['on_x1'] = kp['par_x1']
    mad.globals['on_sep1'] = kp['par_sep1']

    mad.globals['on_x2h'] = kp['par_x2h']
    mad.globals['on_x2v'] = kp['par_x2v']
    mad.globals['on_sep2h'] = kp['par_sep2h']
    mad.globals['on_sep2v'] = kp['par_sep2v']

    mad.globals['on_x5'] = kp['par_x5']
    mad.globals['on_sep5'] = kp['par_sep5']

    mad.globals['on_x8h'] = kp['par_x8h']
    mad.globals['on_x8v'] = kp['par_x8v']
    mad.globals['on_sep8h'] = kp['par_sep8h']
    mad.globals['on_sep8v'] = kp['par_sep8v']

    mad.globals['on_disp'] = kp['par_on_disp']

    # A check
    if mad.globals.nrj < 500:
        assert kp['par_on_disp'] == 0

    # Spectrometers at experiments
    if kp['par_on_alice'] == 1:
        mad.globals.on_alice = 7000./mad.globals.nrj
    if kp['par_on_lhcb'] == 1:
        mad.globals.on_lhcb = 7000./mad.globals.nrj

    # Solenoids at experiments
    mad.globals.on_sol_atlas = kp['par_on_sol_atlas']
    mad.globals.on_sol_cms = kp['par_on_sol_cms']
    mad.globals.on_sol_alice = kp['par_on_sol_alice']

def check_separations_at_ips_against_madvars(twiss_df_b1, twiss_df_b2,
        variables_dict, tol):

    separations_to_check = []
    for iip, ip in enumerate([2,8]):
        for plane in ['x', 'y']:
            # (*) Adapet based on knob definitions
            separations_to_check.append({
                    'element_name': f'ip{ip}:1',
                    'scale_factor': -2*1e-3,
                    'plane': plane,
                    # knobs like on_sep1h, onsep8v etc
                    'varname': f'on_sep{ip}'+{'x':'h', 'y':'v'}[plane],
                    'tol': tol[iip]})
    separations_to_check.append({ # IP1
            'element_name': f'ip1:1',
                    'scale_factor': -2*1e-3,
                    'plane': 'x',
                    'varname': 'on_sep1',
                    'tol': tol[0]})
    separations_to_check.append({ # IP5
            'element_name': f'ip5:1',
                    'scale_factor': -2*1e-3,
                    'plane': 'y',
                    'varname': 'on_sep5',
                    'tol': tol[2]})
    pm.check_separations_against_madvars(separations_to_check,
            twiss_df_b1, twiss_df_b2, variables_dict)

def twiss_and_check(mad, sequences_to_check, twiss_fname,
        tol_beta=1e-3, tol_sep=1e-6, save_twiss_files=True,
        check_betas_at_ips=True, check_separations_at_ips=True):

    var_dict = mad.get_variables_dicts()
    twiss_dfs = {}
    summ_dfs = {}
    for ss in sequences_to_check:
        mad.use(ss)
        mad.twiss()
        tdf = mad.get_twiss_df('twiss')
        twiss_dfs[ss] = tdf
        sdf = mad.get_summ_df('summ')
        summ_dfs[ss] = sdf

    if save_twiss_files:
        for ss in sequences_to_check:
            tt = twiss_dfs[ss]
            if twiss_fname is not None:
                tt.to_parquet(twiss_fname + f'_seq_{ss}.parquet')

    if check_betas_at_ips:
        for ss in sequences_to_check:
            tt = twiss_dfs[ss]
            check_beta_at_ips_against_madvars(beam=ss[-1],
                    twiss_df=tt,
                    variable_dicts=var_dict,
                    tol=tol_beta)
        print('IP beta test against knobs passed!')

    if check_separations_at_ips:
        twiss_df_b1 = twiss_dfs['lhcb1']
        twiss_df_b2 = twiss_dfs['lhcb2']
        check_separations_at_ips_against_madvars(twiss_df_b1, twiss_df_b2,
                var_dict, tol=tol_sep)
        print('IP separation test against knobs passed!')

    other_data = {}
    other_data.update(var_dict)
    other_data['summ_dfs'] = summ_dfs

    return twiss_dfs, other_data
